import streamlit as st
from lib.auth import check_auth, logout_button
from lib.database import get_profile, create_company, save_es
from lib.scraper import scrape_company_page
from lib.generator import generate_es
from lib.styles import inject_css, page_header_minimal, step_badge, hint_box, char_pill
from prompts.templates import ES_TYPES

st.set_page_config(page_title="ES生成", page_icon="", layout="wide")
inject_css()

if not check_auth():
    st.stop()

logout_button()

# --- Minimal header (Notion/Linear style) ---
page_header_minimal("ES生成", "企業情報を入力して、AIが自動生成")

# --- Step 1: 会社情報 ---
st.markdown('<div class="step-card">', unsafe_allow_html=True)
step_badge(1, "会社情報")

company_name = st.text_input("会社名", placeholder="株式会社〇〇")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '<div class="card-header">'
        '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
        'URLから自動取得</div>',
        unsafe_allow_html=True,
    )
    company_url = st.text_input(
        "URL", placeholder="https://example.com", label_visibility="collapsed",
    )
    if company_url and st.button("取得", use_container_width=True):
        with st.spinner("トップ + 関連ページを取得中..."):
            try:
                scraped_text = scrape_company_page(company_url)
                st.session_state["scraped_text"] = scraped_text
                section_count = scraped_text.count("【")
                st.success(f"取得完了（{section_count}ページ, {len(scraped_text):,}文字）")
            except Exception as e:
                st.error(f"取得失敗: {e}")

    if st.session_state.get("scraped_text"):
        with st.expander(f"取得結果（{len(st.session_state['scraped_text']):,}文字）"):
            st.text(st.session_state["scraped_text"][:3000])

with col2:
    st.markdown(
        '<div class="card-header">'
        '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>'
        '手動入力</div>',
        unsafe_allow_html=True,
    )
    manual_info = st.text_area(
        "会社情報", height=150, placeholder="企業理念、事業内容など",
        label_visibility="collapsed",
    )

st.markdown(
    '<div class="hint-compact">URLと手動入力は併用可。説明会で聞いた情報を追加すると精度UP</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Step 2: ES項目 ---
st.markdown('<div class="step-card">', unsafe_allow_html=True)
step_badge(2, "ES項目")

col_a, col_b = st.columns([1, 1])

with col_a:
    es_type = st.selectbox("ES項目", list(ES_TYPES.keys()) + ["その他（自由入力）"],
                           label_visibility="collapsed")

with col_b:
    custom_question = None
    if es_type == "その他（自由入力）":
        custom_question = st.text_input("質問文", placeholder="質問文を入力")
    else:
        st.markdown(
            f'<span style="font-size: 0.82rem; color: #6B7280;">'
            f'{ES_TYPES[es_type]}を生成</span>',
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)

# --- Step 3: 文字数 ---
st.markdown('<div class="step-card">', unsafe_allow_html=True)
step_badge(3, "文字数")

char_limit = st.slider("文字数上限", min_value=100, max_value=800, value=400, step=50,
                        label_visibility="collapsed")

st.markdown(
    f'<div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #6B7280;">'
    f'<span>100字</span>'
    f'<span style="background: rgba(6,182,160,0.08); color: #06B6A0; padding: 0.1rem 0.6rem; '
    f'border-radius: 6px; font-weight: 600; font-family: Inter, sans-serif;">{char_limit}字</span>'
    f'<span>800字</span></div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Step 4: 生成 ---
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

    try:
        profile = get_profile()
    except Exception as e:
        st.error(f"プロフィール取得失敗: {e}")
        st.stop()

    if not profile:
        st.warning("プロフィールが未登録です。先にプロフィール設定画面で登録してください。")
        st.stop()

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

    # Minimal success indicator
    st.markdown(
        '<div class="success-inline">'
        '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
        '<span class="success-inline-text">生成完了</span>'
        '<span class="success-inline-sub">- このまま提出できるレベルです</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    result = st.session_state["generated_result"]
    meta = st.session_state["generation_meta"]

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    edited = st.text_area("生成結果（編集可能）", value=result, height=280,
                          label_visibility="collapsed")

    # 文字数カウント（空白除く）
    clean_text = (
        edited.replace("\n", "").replace("\r", "")
        .replace(" ", "").replace("\u3000", "")
    )
    current_len = len(clean_text)
    limit = meta["char_limit"]
    char_pill(current_len, limit)

    # コピーボタン（★最大・オレンジ）
    st.markdown(
        '<style>'
        '.copy-btn .stButton > button[kind="primary"] {'
        '  background-color: #F97316 !important;'
        '  font-size: 1rem !important;'
        '  font-weight: 700 !important;'
        '  padding: 0.75rem !important;'
        '}'
        '.copy-btn .stButton > button[kind="primary"]:hover {'
        '  background-color: #EA580C !important;'
        '}'
        '</style>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="copy-btn">', unsafe_allow_html=True)
        if st.button("コピー", type="primary", use_container_width=True):
            st.code(edited, language=None)
            st.success("上のテキストをコピーしてください")
        st.markdown('</div>', unsafe_allow_html=True)

    col_save, col_next = st.columns(2)

    with col_save:
        if st.button("保存する", use_container_width=True):
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
                st.error(f"保存失敗: {e}")

    with col_next:
        if st.button("次の企業のESを作る", use_container_width=True):
            for key in ["generated_result", "generation_meta", "scraped_text"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
