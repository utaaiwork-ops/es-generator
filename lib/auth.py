import streamlit as st
from lib.styles import inject_css


def check_auth() -> bool:
    """Google OIDC認証（st.login ベース）。"""
    if st.user.is_logged_in:
        return True

    inject_css()

    # フルスクリーンのポップなグラデーション背景
    st.markdown(
        """
        <style>
            .stApp { background: linear-gradient(135deg, #14B8A6, #06B6D4, #6366F1) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="login-card">
            <div class="login-logo">ES Generator</div>
            <div class="login-subtitle">何十社分のES、もう1から書かなくていい。</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.markdown('<div class="login-area">', unsafe_allow_html=True)
        if st.button("Googleでログイン", type="primary", use_container_width=True):
            st.login("google")
        st.markdown('</div>', unsafe_allow_html=True)

    return False


def logout_button():
    """サイドバーにログアウトボタンを表示する。"""
    if st.user.is_logged_in:
        with st.sidebar:
            st.divider()
            st.markdown(
                f'<span style="font-size: 0.78rem; color: #6B7280;">'
                f'{st.user.email}</span>',
                unsafe_allow_html=True,
            )
            if st.button("ログアウト", use_container_width=True):
                st.logout()
