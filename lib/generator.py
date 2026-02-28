import os
import anthropic
from dotenv import load_dotenv
from prompts.templates import get_system_prompt, build_user_prompt

load_dotenv()


def generate_es(
    profile: dict[str, str],
    company_info: str,
    es_type: str,
    char_limit: int,
    custom_question: str | None = None,
) -> str:
    """Claude APIを呼び出してES文章を生成する。"""
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEYを.envに設定してください")

    client = anthropic.Anthropic(api_key=api_key)

    # LLMは日本語の文字数カウントが不正確なので、内部的に25%少ない上限を渡す
    internal_limit = int(char_limit * 0.75)

    user_prompt = build_user_prompt(
        profile=profile,
        company_info=company_info,
        es_type=es_type,
        char_limit=internal_limit,
        custom_question=custom_question,
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=get_system_prompt(es_type),
        messages=[{"role": "user", "content": user_prompt}],
    )

    return message.content[0].text
