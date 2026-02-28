"""ES種類ごとのプロンプトテンプレート。"""

SYSTEM_PROMPT = """\
あなたは就活生のES（エントリーシート）を作成するプロのキャリアアドバイザーです。
以下のルールを厳守してください：
- 具体的なエピソードを盛り込む
- 企業の事業内容・理念と学生の経験を結びつける
- 自然な日本語で、就活ESにふさわしい文体にする
- 抽象的な表現を避け、数字や固有名詞を使う
- 指定された文字数以内で収める
- 結論ファースト（PREP法）で書く
"""

ES_TYPES = {
    "志望動機": "この企業への志望動機",
    "ガクチカ": "学生時代に力を入れたこと（ガクチカ）",
    "自己PR": "自己PR",
    "強み・弱み": "自分の強み・弱み",
    "将来やりたいこと": "入社後・将来やりたいこと",
}


def build_user_prompt(
    profile: dict[str, str],
    company_info: str,
    es_type: str,
    char_limit: int,
    custom_question: str | None = None,
) -> str:
    """プロフィール・企業情報からユーザープロンプトを組み立てる。"""

    # プロフィール整形
    profile_text = "\n".join(
        f"- {key}: {value}" for key, value in profile.items() if value
    )

    # ES項目名の決定
    if custom_question:
        es_label = custom_question
    else:
        es_label = ES_TYPES.get(es_type, es_type)

    return f"""\
【学生のプロフィール】
{profile_text}

【企業情報】
{company_info}

【指示】
上記の学生のプロフィールと企業情報を踏まえ、この企業に刺さる「{es_label}」を{char_limit}字以内で作成してください。

【出力形式】
- ES本文のみを出力してください（前置きや説明は不要）
- {char_limit}字以内に厳密に収めてください
"""
