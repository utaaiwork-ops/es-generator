import os
import streamlit as st
from dotenv import load_dotenv
from lib.styles import inject_css

load_dotenv()


def check_password() -> bool:
    """簡易パスワード認証。認証済みならTrueを返す。"""
    if st.session_state.get("authenticated"):
        return True

    inject_css()

    st.markdown(
        """
        <div class="login-container">
            <div class="login-logo">ES Generator</div>
            <div class="login-subtitle">就活ES志望動機ジェネレーター</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        password = st.text_input("パスワード", type="password", label_visibility="collapsed", placeholder="パスワードを入力")
        if st.button("ログイン", type="primary", use_container_width=True):
            app_password = os.getenv("APP_PASSWORD", "")
            if not app_password:
                st.error("APP_PASSWORDが未設定です。.envファイルを確認してください。")
                return False
            if password == app_password:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("パスワードが正しくありません")
    return False
