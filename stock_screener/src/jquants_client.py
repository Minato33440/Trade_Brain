"""
J-Quants API V2 クライアント

認証: x-api-key ヘッダー
Base URL: https://api.jquants.com/v2
プラン: Free（12週遅延、2年ヒストリカル）

キャッシュ:
  同日の同一リクエストは JSON キャッシュから返し、API クォータを節約する。
  master データ: cache/master_YYYYMMDD.json（当日有効）
  price データ : cache/prices_YYYYMMDD.json（永続有効・変わらない過去データ）
"""
import json
import os
import time
import logging
from datetime import date, timedelta
from typing import Optional
from pathlib import Path

import requests
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).parent.parent.parent / ".env"
load_dotenv(_ENV_PATH)

logger = logging.getLogger(__name__)

BASE_URL = "https://api.jquants.com/v2"
FREE_PLAN_DELAY_WEEKS = 12

# デフォルトキャッシュディレクトリ: stock_screener/data/.cache/
_DEFAULT_CACHE_DIR = Path(__file__).parent.parent / "data" / ".cache"


# ── APIキー解決 ───────────────────────────────────────────────────────────────

def _read_env_key_raw(env_path: Path, key: str) -> Optional[str]:
    """python-dotenv がパースできないキー（スペース入り等）を直接読む。"""
    try:
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(key + "="):
                    return line[len(key) + 1:].strip()
    except OSError:
        pass
    return None


def _resolve_api_key(api_key: Optional[str]) -> str:
    if api_key:
        return api_key
    for name in (
        "JQUANTS_API_KEY",
        "J-Quants_V2_API_Key",
        "J-Quants V2 API Key",
        "JQUANTS_V2_API_KEY",
    ):
        val = os.environ.get(name)
        if val:
            return val
    val = _read_env_key_raw(_ENV_PATH, "J-Quants V2 API Key")
    if val:
        return val
    raise ValueError(
        "J-Quants API キーが見つかりません。"
        ".env に 'JQUANTS_API_KEY' または 'J-Quants_V2_API_Key' を設定してください"
    )


# ── キャッシュ ────────────────────────────────────────────────────────────────

def _cache_path(cache_dir: Path, key: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{key}.json"


def _load_cache(cache_dir: Path, key: str) -> Optional[list]:
    p = _cache_path(cache_dir, key)
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            logger.info("キャッシュ読込: %s (%d 件)", p.name, len(data))
            return data
        except Exception as e:
            logger.warning("キャッシュ読込失敗（無視）: %s → %s", p.name, e)
    return None


def _save_cache(cache_dir: Path, key: str, data: list) -> None:
    p = _cache_path(cache_dir, key)
    try:
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        logger.debug("キャッシュ保存: %s (%d 件)", p.name, len(data))
    except Exception as e:
        logger.warning("キャッシュ保存失敗（無視）: %s → %s", p.name, e)


# ── クライアント本体 ──────────────────────────────────────────────────────────

class JQuantsClient:
    """J-Quants API V2 クライアント（APIキー認証方式）。"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        cache_dir: Optional[Path] = None,
    ):
        key = _resolve_api_key(api_key)
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": key})
        self.cache_dir = cache_dir or _DEFAULT_CACHE_DIR

    # ── 低レベル ─────────────────────────────────────────────────────────────

    def _get(self, path: str, params: Optional[dict] = None, retries: int = 5) -> dict:
        url = f"{BASE_URL}{path}"
        for attempt in range(retries):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                if resp.status_code == 429:
                    # 指数バックオフ: 4s, 8s, 16s, 32s, 64s
                    wait = 4 * (2 ** attempt)
                    logger.warning(
                        "429 Rate Limit: %s → %ds 待機 (試行 %d/%d)",
                        path, wait, attempt + 1, retries,
                    )
                    time.sleep(wait)
                    continue
                if resp.status_code in (401, 403):
                    raise RuntimeError(
                        f"認証エラー ({resp.status_code}): APIキーを確認してください"
                    )
                resp.raise_for_status()
                return resp.json()
            except requests.Timeout:
                logger.warning("タイムアウト: %s (試行 %d/%d)", path, attempt + 1, retries)
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
            except requests.ConnectionError as e:
                logger.warning("接続エラー: %s → %s", path, e)
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    raise
        raise RuntimeError(
            f"レート制限超過 or 接続失敗 ({retries} 回リトライ済み): {url}\n"
            "→ API クォータが上限に達した可能性があります。時間をおいて再実行してください。"
        )

    @staticmethod
    def _extract_list(data: dict, *hint_keys: str) -> list:
        """レスポンス dict からデータリストを抽出する。"""
        for key in hint_keys:
            if key in data and isinstance(data[key], list):
                return data[key]
        skip = {"pagination_key", "total_pages", "total_count", "message"}
        for k, v in data.items():
            if k not in skip and isinstance(v, list):
                logger.debug("データキー自動検出: '%s'", k)
                return v
        return []

    def _paginate(self, path: str, params: dict, *hint_keys: str) -> list:
        """ページネーション付きで全件取得する。"""
        params = dict(params)
        results = []
        page = 0
        while True:
            data = self._get(path, params)
            page_data = self._extract_list(data, *hint_keys)
            results.extend(page_data)
            next_key = data.get("pagination_key")
            if not next_key:
                break
            params["pagination_key"] = next_key
            page += 1
            logger.debug("%s ページ %d 取得済み（累計 %d 件）", path, page, len(results))
            time.sleep(1)
        return results

    # ── 公開 API（キャッシュ付き） ────────────────────────────────────────────

    def get_listed_master(self, date: Optional[str] = None) -> list[dict]:
        """GET /equities/master — 上場銘柄マスタ。当日キャッシュ有効。"""
        today = _today_str()
        cache_key = f"master_{today}"
        cached = _load_cache(self.cache_dir, cache_key)
        if cached is not None:
            return cached

        params = {}
        if date:
            params["date"] = date
        logger.debug("GET /equities/master date=%s", date or "latest")
        records = self._paginate(
            "/equities/master", params, "equities_master", "info", "listed_info"
        )
        if records:
            _save_cache(self.cache_dir, cache_key, records)
        return records

    def get_daily_quotes_by_date(self, date_str: str) -> list[dict]:
        """GET /equities/bars/daily?date=YYYYMMDD — 指定日の全銘柄株価。永続キャッシュ。"""
        cache_key = f"prices_{date_str}"
        cached = _load_cache(self.cache_dir, cache_key)
        if cached is not None:
            return cached

        logger.debug("GET /equities/bars/daily date=%s", date_str)
        records = self._paginate(
            "/equities/bars/daily",
            {"date": date_str},
            "data",
            "daily_quotes",
            "bars",
            "prices",
        )
        if records:
            _save_cache(self.cache_dir, cache_key, records)
        return records

    def get_fins_summary(self, code: str) -> list[dict]:
        """GET /fins/summary?code=XXXX — 財務サマリ（発行済株数用）。"""
        time.sleep(1)
        data = self._get("/fins/summary", {"code": code})
        return self._extract_list(data, "fins_summary", "summary")

    # ── ユーティリティ ────────────────────────────────────────────────────────

    @staticmethod
    def latest_available_date(delay_weeks: int = FREE_PLAN_DELAY_WEEKS) -> str:
        """Free プランで取得可能な最新営業日（YYYYMMDD）を返す。"""
        d = date.today() - timedelta(weeks=delay_weeks)
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        return d.strftime("%Y%m%d")


def _today_str() -> str:
    return date.today().strftime("%Y%m%d")
