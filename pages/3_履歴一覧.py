import streamlit as st
from lib.auth import check_auth, logout_button
from lib.database import list_companies, list_es, update_es, delete_es
from lib.styles import inject_css, page_header_minimal, metric_cards, badge, char_pill
from prompts.templates import ES_TYPES

st.set_page_config(page_title="履歴一覧", page_icon="", layout="wide")
inject_css()

if not check_auth():
    st.stop()

logout_button()

# --- Minimal header ---
page_header_minimal("履歴一覧", "生成したESを企業ごとに管理")

# データ取得
try:
    companies = list_companies()
except Exception as e:
    st.error(f"データベース接続エラー: {e}")
    st.stop()

if not companies:
    st.markdown("")
    st.markdown(
        """
        <div class="empty-state">
            <div style="width: 48px; height: 48px; margin: 0 auto 0.75rem; background: #F3F4F6;
                        border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                     stroke="#6B7280" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
            </div>
            <p style="font-size: 0.92rem; font-weight: 500; color: #1A1A2E; margin-bottom: 0.25rem;">
                まだ保存されたESはありません
            </p>
            <p style="font-size: 0.78rem; color: #6B7280;">
                ES生成画面で作成して保存するとここに表示されます
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# サマリー
try:
    all_es = list_es()
except Exception as e:
    st.error(f"データ取得エラー: {e}")
    st.stop()

ICON_BUILDING = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06B6A0" stroke-width="2"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>'
ICON_FILE = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06B6A0" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'

metric_cards([
    (str(len(companies)), "登録企業数", ICON_BUILDING),
    (str(len(all_es)), "生成ES数", ICON_FILE),
])

# --- フィルタ ---
col_filter, col_search = st.columns([1, 2])

with col_filter:
    company_options = {"すべての企業": None}
    company_options.update({c["name"]: c["id"] for c in companies})
    selected_company = st.selectbox("企業フィルタ", list(company_options.keys()),
                                    label_visibility="collapsed")
    company_id_filter = company_options[selected_company]

with col_search:
    search_query = st.text_input("キーワード検索", placeholder="キーワード検索",
                                 label_visibility="collapsed")

# --- 一覧取得 ---
es_list = list_es(company_id=company_id_filter) if company_id_filter is not None else all_es

if search_query:
    q = search_query.lower()
    es_list = [
        es for es in es_list
        if q in (es.get("content", "") or "").lower()
        or q in (es.get("es_type", "") or "").lower()
        or q in (es.get("question", "") or "").lower()
    ]

if not es_list:
    st.info("該当するESが見つかりません。")
    st.stop()

st.caption(f"{len(es_list)}件のES")

# --- ES一覧 ---
for es in es_list:
    company_name = (
        es.get("companies", {}).get("name", "不明")
        if es.get("companies")
        else "不明"
    )
    es_type = es.get("es_type", "")
    question = es.get("question", "")
    created = es.get("created_at", "")[:10]
    char_limit = es.get("char_limit", 999)
    content = es.get("content", "")

    label_parts = [company_name, es_type]
    if question:
        label_parts.append(question)
    label = " / ".join(label_parts)

    with st.expander(label):
        st.markdown(
            f'{badge(es_type, "teal")}  {badge(created, "gray")}  '
            f'<span style="color: #6B7280; font-size: 0.72rem;">上限 {char_limit}字</span>',
            unsafe_allow_html=True,
        )

        edited_content = st.text_area(
            "内容", value=content, height=200,
            key=f"edit_{es['id']}", label_visibility="collapsed",
        )

        clean = (
            edited_content.replace("\n", "").replace("\r", "")
            .replace(" ", "").replace("\u3000", "")
        )
        char_pill(len(clean), char_limit or 999)

        st.markdown(
            '<span style="font-size: 0.72rem; color: #6B7280;">編集して内容を調整できます</span>',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("更新", key=f"update_{es['id']}", use_container_width=True,
                         type="primary"):
                try:
                    update_es(es["id"], edited_content)
                    st.success("更新しました")
                except Exception as e:
                    st.error(f"更新失敗: {e}")

        with col2:
            if st.button("コピー", key=f"copy_{es['id']}", use_container_width=True):
                st.code(edited_content, language=None)

        with col3:
            st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
            if st.button("削除", key=f"delete_{es['id']}", use_container_width=True):
                try:
                    delete_es(es["id"])
                    st.success("削除しました")
                    st.rerun()
                except Exception as e:
                    st.error(f"削除失敗: {e}")
            st.markdown('</div>', unsafe_allow_html=True)
