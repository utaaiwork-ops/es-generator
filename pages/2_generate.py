import streamlit as st
from lib.auth import check_password
from lib.database import get_profile, create_company, save_es
from lib.scraper import scrape_company_page
from lib.generator import generate_es
from lib.styles import inject_css, page_header, step_badge
from prompts.templates import ES_TYPES

st.set_page_config(page_title="ES生成", page_icon="📝", layout="wide")
inject_css()

if not check_password():
    st.stop()

page_header("ES生成", "企業情報を入力して、あなたに合ったESを自動生成します")

# --- Step 1 ---
step_badge(1, "会社情報を入力")

company_name = st.text_input("会社名", placeholder="例: 株式会社〇〇")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '<div class="card-header">URLからスクレイピング</div>',
        unsafe_allow_html=True,
    )
    company_url = st.text_input(
        "会社HPのURL",
        placeholder="https://example.co.jp",
        label_visibility="collapsed",
    )
    if company_url and st.button("ページを取得", use_container_width=True):
        with st.spinner("ページを取得中..."):
            try:
                scraped_text = scrape_company_page(company_url)
                st.session_state["scraped_text"] = scraped_text
                st.success(f"取得完了 ({len(scraped_text):,}文字)")
            except Exception as e:
                st.error(f"取得失敗: {e}")

    if st.session_state.get("scraped_text"):
        with st.expander(f"スクレイピング結果 ({len(st.session_state['scraped_text']):,}文字)"):
            st.text(st.session_state["scraped_text"][:2000])

with col2:
    st.markdown(
        '<div class="card-header">手動入力</div>',
        unsafe_allow_html=True,
    )
    manual_info = st.text_area(
        "会社情報",
        height=180,
        placeholder="企業理念、事業内容、求める人物像など...",
        label_visibility="collapsed",
    )

st.divider()

# --- Step 2 ---
step_badge(2, "ES項目を選択")

col_a, col_b = st.columns([1, 1])

with col_a:
    es_type = st.selectbox("ES項目", list(ES_TYPES.keys()) + ["その他（自由入力）"])

with col_b:
    custom_question = None
    if es_type == "その他（自由入力）":
        custom_question = st.text_input("質問文", placeholder="例: 当社でどのような貢献ができますか？")
    else:
        st.markdown(
            f'<div style="padding-top: 1.75rem; color: #64748B; font-size: 0.9rem;">'
            f'{ES_TYPES[es_type]}を生成します</div>',
            unsafe_allow_html=True,
        )

st.divider()

# --- Step 3 ---
step_badge(3, "文字数を指定")

char_limit = st.slider("文字数上限", min_value=100, max_value=800, value=400, step=50)
st.caption(f"生成されるES文章は {char_limit}字以内 に収まります")

st.divider()

# --- Step 4 ---
step_badge(4, "生成")

if st.button("ESを生成する", type="primary", use_container_width=True):
    # バリデーション
    errors = []
    if not company_name:
        errors.append("会社名を入力してください")

    company_info_parts = []
    if st.session_state.get("scraped_text"):
        company_info_parts.append(st.session_state["scraped_text"])
    if manual_info:
        company_info_parts.append(manual_info)
    if not company_info_parts:
        errors.append("会社情報（URLまたは手動入力）を入力してください")

    if es_type == "その他（自由入力）" and not custom_question:
        errors.append("質問文を入力してください")

    if errors:
        for err in errors:
            st.error(err)
        st.stop()

    company_info = "\n\n".join(company_info_parts)

    # プロフィール取得
    try:
        profile = get_profile()
    except Exception as e:
        st.error(f"プロフィール取得失敗: {e}")
        st.stop()

    if not profile:
        st.warning("プロフィールが未登録です。先にプロフィール設定画面で登録してください。")
        st.stop()

    # 生成実行
    with st.spinner("AIがES文章を作成しています..."):
        try:
            result = generate_es(
                profile=profile,
                company_info=company_info,
                es_type=es_type,
                char_limit=char_limit,
                custom_question=custom_question,
            )
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")
            st.stop()

    st.session_state["generated_result"] = result
    st.session_state["generation_meta"] = {
        "company_name": company_name,
        "company_url": company_url,
        "company_info": company_info,
        "manual_info": manual_info,
        "es_type": es_type,
        "custom_question": custom_question,
        "char_limit": char_limit,
    }

# --- 結果表示 ---
if "generated_result" in st.session_state:
    st.divider()
    st.markdown(
        """
        <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px;
                    padding: 1rem 1.25rem; margin-bottom: 1rem;">
            <span style="font-weight: 600; color: #166534;">生成完了</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state["generated_result"]
    meta = st.session_state["generation_meta"]

    edited = st.text_area("生成結果（編集可能）", value=result, height=300)

    # 文字数表示
    current_len = len(edited)
    limit = meta["char_limit"]
    color = "#22C55E" if current_len <= limit else "#EF4444"
    st.markdown(
        f'<p style="text-align: right; font-size: 0.85rem;">'
        f'文字数: <span style="color: {color}; font-weight: 600;">{current_len}</span>'
        f' / {limit}字</p>',
        unsafe_allow_html=True,
    )

    col_save, col_copy = st.columns(2)

    with col_save:
        if st.button("データベースに保存", type="primary", use_container_width=True):
            try:
                company_id = create_company(
                    name=meta["company_name"],
                    url=meta["company_url"] or None,
                    scraped_info=st.session_state.get("scraped_text") or None,
                    notes=meta["manual_info"] or None,
                )
                save_es(
                    company_id=company_id,
                    es_type=meta["es_type"],
                    question=meta["custom_question"],
                    char_limit=meta["char_limit"],
                    content=edited,
                )
                st.success("保存しました")
            except Exception as e:
                st.error(f"保存に失敗しました: {e}")

    with col_copy:
        if st.button("コピー用に表示", use_container_width=True):
            st.code(edited, language=None)
