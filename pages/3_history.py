import streamlit as st
from lib.auth import check_password
from lib.database import list_companies, list_es, update_es, delete_es
from lib.styles import inject_css, page_header, metric_cards, badge
from prompts.templates import ES_TYPES

st.set_page_config(page_title="履歴一覧", page_icon="📝", layout="wide")
inject_css()

if not check_password():
    st.stop()

page_header("履歴一覧", "過去に生成したESを確認・編集できます")

# データ取得
try:
    companies = list_companies()
except Exception as e:
    st.error(f"データベース接続エラー: {e}")
    st.stop()

if not companies:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">&#x1F4C4;</div>
            <p style="font-size: 1.1rem; font-weight: 500;">まだ保存されたESはありません</p>
            <p style="font-size: 0.9rem;">ES生成画面で作成してみましょう</p>
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

metric_cards([
    (str(len(companies)), "登録企業数"),
    (str(len(all_es)), "生成ES数"),
])

# フィルタ行
col_filter, col_search = st.columns([1, 2])

with col_filter:
    company_options = {"すべて": None}
    company_options.update({c["name"]: c["id"] for c in companies})
    selected_company = st.selectbox("会社でフィルタ", list(company_options.keys()))
    company_id_filter = company_options[selected_company]

with col_search:
    search_query = st.text_input("キーワード検索", placeholder="検索したいキーワード...")

# 一覧取得
es_list = list_es(company_id=company_id_filter) if company_id_filter is not None else all_es

# キーワードフィルタ
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

# ES一覧
for es in es_list:
    company_name = (
        es.get("companies", {}).get("name", "不明")
        if es.get("companies")
        else "不明"
    )
    es_type = es.get("es_type", "")
    question = es.get("question", "")
    created = es.get("created_at", "")[:10]
    char_limit = es.get("char_limit", "?")

    # ヘッダー
    label_parts = [company_name, es_type]
    if question:
        label_parts.append(question)
    label = " / ".join(label_parts)

    type_badge = badge(es_type, "blue")
    date_badge = badge(created, "gray")

    with st.expander(label):
        st.markdown(
            f"{type_badge}　{date_badge}　"
            f'<span style="color: #64748B; font-size: 0.8rem;">文字数上限: {char_limit}字</span>',
            unsafe_allow_html=True,
        )

        edited_content = st.text_area(
            "内容",
            value=es.get("content", ""),
            height=220,
            key=f"edit_{es['id']}",
            label_visibility="collapsed",
        )

        current_len = len(edited_content)
        color = "#22C55E" if current_len <= (char_limit or 999) else "#EF4444"
        st.markdown(
            f'<p style="text-align: right; font-size: 0.85rem; margin-top: -0.5rem;">'
            f'文字数: <span style="color: {color}; font-weight: 600;">{current_len}</span>'
            f' / {char_limit}字</p>',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("更新", key=f"update_{es['id']}", use_container_width=True):
                try:
                    update_es(es["id"], edited_content)
                    st.success("更新しました")
                except Exception as e:
                    st.error(f"更新失敗: {e}")

        with col2:
            if st.button("コピー用表示", key=f"copy_{es['id']}", use_container_width=True):
                st.code(edited_content, language=None)

        with col3:
            if st.button("削除", key=f"delete_{es['id']}", use_container_width=True):
                try:
                    delete_es(es["id"])
                    st.success("削除しました")
                    st.rerun()
                except Exception as e:
                    st.error(f"削除失敗: {e}")
