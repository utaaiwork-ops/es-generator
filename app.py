import streamlit as st
from lib.auth import check_password
from lib.styles import inject_css

st.set_page_config(
    page_title="ES志望動機ジェネレーター",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

if not check_password():
    st.stop()

# --- トップページ ---
st.markdown(
    """
    <div class="page-header" style="text-align: center; padding: 3rem 2rem;">
        <h1 style="font-size: 2rem !important;">ES志望動機ジェネレーター</h1>
        <p style="font-size: 1.05rem;">プロフィールを登録して、企業ごとに刺さるESを自動生成</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #0369A1;">&#x1F464;</div>
            <h3 style="margin: 0 0 0.5rem 0 !important;">プロフィール設定</h3>
            <p style="font-size: 0.9rem; color: #64748B;">
                自分の情報を登録・編集<br/>
                ガクチカ・強み・経験など
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #0EA5E9;">&#x2728;</div>
            <h3 style="margin: 0 0 0.5rem 0 !important;">ES生成</h3>
            <p style="font-size: 0.9rem; color: #64748B;">
                企業HPを入力してAIが生成<br/>
                志望動機・ガクチカ・自己PR
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #22C55E;">&#x1F4DA;</div>
            <h3 style="margin: 0 0 0.5rem 0 !important;">履歴一覧</h3>
            <p style="font-size: 0.9rem; color: #64748B;">
                過去に生成したESを管理<br/>
                検索・編集・再生成
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="text-align: center; margin-top: 1.5rem; color: #64748B; font-size: 0.85rem;">
        左のサイドバーからページを選択してください
    </div>
    """,
    unsafe_allow_html=True,
)
