import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# ES作成に有用なページを見つけるためのキーワード
_RELEVANT_KEYWORDS = [
    # 事業・サービス
    "事業", "サービス", "service", "business", "product", "solution",
    # 企業情報
    "会社概要", "企業情報", "about", "company", "corporate", "理念", "ミッション",
    "ビジョン", "mission", "vision", "philosophy", "value",
    # 採用
    "採用", "recruit", "career", "新卒", "キャリア", "働く", "仕事",
    "job", "entry", "intern",
    # 社員
    "社員", "メンバー", "member", "people", "interview", "インタビュー",
    "voice", "先輩", "座談会", "team",
    # 文化・環境
    "文化", "culture", "環境", "welfare", "制度",
]


def _is_relevant_link(href: str, text: str) -> bool:
    """リンクがES作成に関連するページかどうかを判定する。"""
    target = (href + " " + text).lower()
    return any(kw.lower() in target for kw in _RELEVANT_KEYWORDS)


def _extract_text(soup: BeautifulSoup, max_chars: int = 4000) -> str:
    """BeautifulSoupオブジェクトから本文テキストを抽出する。"""
    for tag in soup(["script", "style", "nav", "footer", "header", "iframe", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    result = "\n".join(lines)

    if len(result) > max_chars:
        result = result[:max_chars]

    return result


def _fetch_page(url: str, timeout: int = 15) -> BeautifulSoup | None:
    """URLからページを取得してBeautifulSoupを返す。失敗時はNone。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return BeautifulSoup(resp.text, "html.parser")
    except Exception:
        return None


def _find_relevant_links(soup: BeautifulSoup, base_url: str, max_links: int = 8) -> list[tuple[str, str]]:
    """ページ内からES作成に関連するリンクを抽出する。"""
    base_domain = urlparse(base_url).netloc
    found: dict[str, str] = {}

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        text = a_tag.get_text(strip=True)

        # 相対URLを絶対URLに変換
        full_url = urljoin(base_url, href)

        # 同一ドメインのみ
        if urlparse(full_url).netloc != base_domain:
            continue

        # ファイルリンク除外
        if re.search(r"\.(pdf|jpg|png|gif|zip|doc|xlsx)$", full_url, re.IGNORECASE):
            continue

        # 関連性チェック
        if _is_relevant_link(href, text) and full_url not in found:
            label = text[:50] if text else href
            found[full_url] = label

        if len(found) >= max_links:
            break

    return list(found.items())


def scrape_company_page(url: str, timeout: int = 15) -> str:
    """URLから会社情報をスクレイピングし、テキストを返す。
    トップページに加え、事業内容・採用・社員の声などの関連ページも自動で取得する。
    """
    # 1. トップページを取得
    soup = _fetch_page(url, timeout)
    if soup is None:
        raise ConnectionError(f"ページの取得に失敗しました: {url}")

    sections: list[str] = []
    top_text = _extract_text(soup, max_chars=3000)
    sections.append(f"【トップページ】\n{top_text}")

    # 2. 関連ページのリンクを発見
    links = _find_relevant_links(soup, url)

    # 3. 関連ページを巡回して情報取得
    for link_url, label in links:
        sub_soup = _fetch_page(link_url, timeout)
        if sub_soup is None:
            continue

        sub_text = _extract_text(sub_soup, max_chars=2000)
        if len(sub_text) > 100:  # 中身が薄いページはスキップ
            sections.append(f"【{label}】\n{sub_text}")

    result = "\n\n".join(sections)

    # 全体の上限（Claude APIのコンテキスト節約）
    max_total = 12000
    if len(result) > max_total:
        result = result[:max_total] + "\n...(以下省略)"

    return result
