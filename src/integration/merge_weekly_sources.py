#!/usr/bin/env python3
r"""
週末市況統合スクリプト (merge_weekly_sources.py)

Boss市況テキスト + python main.py --news + hermes x_search ヘッドライン
を統合して、charts/Market conditions -YYYY-M-D~.txt を生成

使用例:
  python src/integration/merge_weekly_sources.py \
    --boss-text "Boss market commentary (YYYY-MM-DD to YYYY-MM-DD)" \
    --news-output logs/weekly/news_output.txt \
    --x-headlines logs/weekly/x_headlines_raw.txt \
    --output logs/weekly/2026/2026-5-24_wk21/charts/Market conditions -2026-5-24~.txt
"""

import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def parse_x_headlines(raw_output: str) -> List[Dict[str, str]]:
    """
    hermes -z -t x_search の出力をパース

    想定フォーマット:
    1. JSON形式（Grok API native）
    2. Markdown形式（ポスト列挙）
    3. 混合形式（自然言語 + メタデータ）
    """
    tweets = []

    # Try JSON parsing first
    try:
        data = json.loads(raw_output)
        if isinstance(data, list):
            tweets = data[:3]  # Top 3
        elif isinstance(data, dict) and "posts" in data:
            tweets = data["posts"][:3]
        elif isinstance(data, dict) and "tweets" in data:
            tweets = data["tweets"][:3]
    except json.JSONDecodeError:
        pass

    if tweets:
        return tweets

    # Fallback: Regex-based markdown parsing
    # Pattern: "Post by @user (date) | engagement metrics"
    # or "Tweet: ... | by @user | 123 likes, 45 retweets"

    lines = raw_output.split('\n')
    current_tweet = {"text": "", "author": "", "engagement": 0}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect author line
        author_match = re.search(r'(?:by|from|@)\s*(@?\w+)', line, re.IGNORECASE)
        if author_match:
            current_tweet["author"] = author_match.group(1)

        # Detect engagement metrics (likes, retweets, replies)
        engagement = 0
        for metric in re.findall(r'(\d+)\s*(like|retweet|reply|engagement)', line, re.IGNORECASE):
            engagement += int(metric[0])
        if engagement > 0:
            current_tweet["engagement"] = engagement
            if len(current_tweet["text"]) > 10:  # Only save if has content
                tweets.append(current_tweet.copy())
                current_tweet = {"text": "", "author": "", "engagement": 0}

        # Accumulate text
        if line and not any(kw in line for kw in ["like", "retweet", "reply", "by @", "from "]):
            if current_tweet["text"]:
                current_tweet["text"] += " " + line
            else:
                current_tweet["text"] = line

    # Sort by engagement descending
    tweets.sort(key=lambda x: x.get("engagement", 0), reverse=True)

    return tweets[:3]


def summarize_tweet(tweet: Dict[str, str]) -> str:
    """
    ツイートを 2-3 行で日本語要約

    フォーマット:
    - **[著者]**: ツイートの要点（1-2行）
    """
    if isinstance(tweet, str):
        # If tweet is already a string, return as-is
        return f"- {tweet[:150]}..."

    author = tweet.get("author", "Unknown")
    text = tweet.get("text", "")
    engagement = tweet.get("engagement", 0)

    # Truncate text to ~150 chars (適応的な要約)
    if len(text) > 150:
        text = text[:147] + "..."

    summary = f"- **@{author.lstrip('@')}**: {text}\n  (engagement: ~{engagement})"

    return summary


def merge_sources(
    boss_text: Optional[str],
    news_output_path: Optional[Path],
    x_headlines_path: Optional[Path],
) -> str:
    """
    3つのソースを統合して markdown を生成
    """
    sections = []

    # Section 1: Boss市況テキスト
    if boss_text:
        sections.append("## 📊 市況（Minato）\n")
        sections.append(boss_text)
        sections.append("\n")

    # Section 2: GMニュース（--news 出力）
    if news_output_path and news_output_path.exists():
        sections.append("\n## 📰 GMニュース（RSS + API）\n")
        try:
            with open(news_output_path, 'r', encoding='utf-8') as f:
                news_content = f.read().strip()
                sections.append(news_content)
                sections.append("\n")
        except Exception as e:
            sections.append(f"⚠️ ニュース読み込みエラー: {e}\n")

    # Section 3: X市況ヘッドライン（新規・2026-05-24）
    if x_headlines_path and x_headlines_path.exists():
        sections.append("\n## 𝕏 市況ヘッドライン（注目度TOP3）\n")
        try:
            with open(x_headlines_path, 'r', encoding='utf-8') as f:
                raw_x = f.read()

            tweets = parse_x_headlines(raw_x)

            if tweets:
                sections.append("**最新の注目ツイート**:\n")
                for tweet in tweets:
                    summary = summarize_tweet(tweet)
                    sections.append(summary + "\n")
            else:
                sections.append("（取得ツイートなし）\n")

        except Exception as e:
            sections.append(f"⚠️ X ヘッドライン読み込みエラー: {e}\n")

    # Footer
    sections.append(f"\n---\n*統合生成時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    return "".join(sections)


def main():
    parser = argparse.ArgumentParser(
        description="週末市況テキストを統合生成"
    )
    parser.add_argument("--boss-text", type=str, default=None,
                        help="Boss が提供する市況テキスト（直接渡し）")
    parser.add_argument("--boss-file", type=Path, default=None,
                        help="Boss市況テキストのファイルパス")
    parser.add_argument("--news-output", type=Path, default=None,
                        help="python main.py --news の出力ファイル")
    parser.add_argument("--x-headlines", type=Path, default=None,
                        help="hermes -z -t x_search の出力ファイル")
    parser.add_argument("--output", type=Path, required=True,
                        help="出力ファイルパス (charts/Market conditions -YYYY-M-D~.txt)")
    parser.add_argument("--dry-run", action="store_true",
                        help="出力ファイルを作成せず stdout に出力")

    args = parser.parse_args()

    # Boss市況テキスト の取得
    boss_text = args.boss_text
    if args.boss_file:
        boss_file_path = Path(args.boss_file)
        if not boss_file_path.is_absolute():
            # 相対パスの場合、カレントディレクトリを基準にする
            boss_file_path = Path.cwd() / boss_file_path

        if boss_file_path.exists():
            with open(boss_file_path, 'r', encoding='utf-8') as f:
                boss_text = f.read()
        else:
            print(f"⚠️ Boss市況ファイルが見つかりません: {boss_file_path}", file=sys.stderr)

    # 統合
    merged = merge_sources(boss_text, args.news_output, args.x_headlines)

    # 出力
    if args.dry_run:
        print(merged)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(merged)
        print(f"✅ 統合ファイル生成: {args.output}")


if __name__ == "__main__":
    main()
