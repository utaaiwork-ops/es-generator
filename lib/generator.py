import os
import anthropic
from dotenv import load_dotenv
from prompts.templates import SYSTEM_PROMPT, build_user_prompt

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

    user_prompt = build_user_prompt(
        profile=profile,
        company_info=company_info,
        es_type=es_type,
        char_limit=char_limit,
        custom_question=custom_question,
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return message.content[0].text
