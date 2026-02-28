import streamlit as st
from lib.auth import check_auth, logout_button
from lib.styles import inject_css, hero_header

st.set_page_config(
    page_title="ES Generator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

if not check_auth():
    st.stop()

logout_button()

# --- Hero ---
hero_header(
    "プロフィールを1回登録。<br/>あとは企業URLを変えるだけ。",
    "何十社分のES作成を、圧倒的にラクにする。",
)

# --- Feature Cards ---
col1, col2, col3 = st.columns(3)

ICON_USER = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06B6A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
ICON_SPARKLES = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06B6A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.5 4.5H18l-3.5 2.5L16 14.5 12 12l-4 2.5 1.5-4.5L6 7.5h4.5z"/></svg>'
ICON_FILE = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06B6A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'

with col1:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon-box">{ICON_USER}</div>
            <div class="feature-title">プロフィール設定</div>
            <div class="feature-desc">一度だけ登録すれば、何十社分でもOK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("プロフィール設定へ", use_container_width=True, type="primary"):
        st.switch_page("pages/1_profile.py")

with col2:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon-box">{ICON_SPARKLES}</div>
            <div class="feature-title">ES生成</div>
            <div class="feature-desc">企業URLを貼って、ワンクリックで生成</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("ES生成へ", use_container_width=True, type="primary"):
        st.switch_page("pages/2_generate.py")

with col3:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon-box">{ICON_FILE}</div>
            <div class="feature-title">履歴一覧</div>
            <div class="feature-desc">生成したESを企業別に管理・編集</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("履歴一覧へ", use_container_width=True, type="primary"):
        st.switch_page("pages/3_history.py")

# --- Step Guide ---
st.markdown("")
st.markdown(
    """
    <div class="step-guide">
        <div class="step-guide-title">使い方</div>
        <div class="step-flow">
            <div class="step-flow-item">
                <span class="step-flow-num">1</span>
                <span class="step-flow-text">プロフィール登録（初回のみ）</span>
            </div>
            <span class="step-flow-arrow">→</span>
            <div class="step-flow-item">
                <span class="step-flow-num">2</span>
                <span class="step-flow-text">企業URLを入力</span>
            </div>
            <span class="step-flow-arrow">→</span>
            <div class="step-flow-item">
                <span class="step-flow-num">3</span>
                <span class="step-flow-text">ES自動生成</span>
            </div>
            <span class="step-flow-arrow">→</span>
            <div class="step-flow-item">
                <span class="step-flow-num" style="font-size: 0.55rem;">完了</span>
                <span class="step-flow-text">コピペして提出</span>
            </div>
        </div>
        <p style="margin-top: 0.75rem; font-size: 0.78rem; color: #6B7280;">
            まずはプロフィールから始めてみましょう。完璧でなくてもOKです。
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
