import requests
from bs4 import BeautifulSoup


def scrape_company_page(url: str, timeout: int = 15) -> str:
    """URLから会社情報をスクレイピングし、テキストを返す。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, "html.parser")

    # 不要なタグを除去
    for tag in soup(["script", "style", "nav", "footer", "header", "iframe", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # 空行の連続を圧縮
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    result = "\n".join(lines)

    # 長すぎる場合は先頭を切り出す（Claude APIのコンテキスト節約）
    max_chars = 8000
    if len(result) > max_chars:
        result = result[:max_chars] + "\n...(以下省略)"

    return result
