"""共通CSSスタイル定義。Genspark デザイン準拠。Notion/Linear風ミニマルUI。"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* === Global === */
    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #FAFAFA;
    }

    /* === Hide Streamlit defaults === */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* === Typography === */
    h1 {
        color: #1A1A2E !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        letter-spacing: -0.02em;
        line-height: 1.4 !important;
    }

    h2 {
        color: #1A1A2E !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    h3 {
        color: #1A1A2E !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    p, li, label, .stMarkdown {
        color: #1A1A2E;
        line-height: 1.65;
    }

    /* === Sidebar === */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E5E7EB;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #6B7280;
        font-size: 0.85rem;
    }

    /* === Primary Buttons === */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {
        background-color: #06B6A0 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Noto Sans JP', sans-serif !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.9rem !important;
        transition: all 200ms ease !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        background-color: #0F766E !important;
    }

    /* === Secondary Buttons === */
    .stButton > button:not([kind="primary"]) {
        background-color: #FFFFFF !important;
        color: #1A1A2E !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        font-family: 'Noto Sans JP', sans-serif !important;
        font-size: 0.82rem !important;
        transition: all 200ms ease !important;
    }

    .stButton > button:not([kind="primary"]):hover {
        border-color: #06B6A0 !important;
        background-color: #F0FDFA !important;
        color: #06B6A0 !important;
    }

    /* === Inputs === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 1.5px solid #E5E7EB !important;
        font-family: 'Noto Sans JP', sans-serif !important;
        font-size: 0.88rem !important;
        background: #FAFBFC !important;
        transition: all 200ms ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #06B6A0 !important;
        box-shadow: 0 0 0 2px rgba(6, 182, 160, 0.1) !important;
        background: #FFFFFF !important;
    }

    /* === Slider === */
    .stSlider > div > div > div > div {
        background-color: #06B6A0 !important;
    }

    /* === Expander === */
    .streamlit-expanderHeader {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        color: #1A1A2E !important;
    }

    /* === Divider === */
    hr {
        border-color: #E5E7EB !important;
        margin: 1rem 0 !important;
    }

    /* === Tabs === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #E5E7EB;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        color: #6B7280;
        font-weight: 500;
        padding: 0.75rem 1.25rem;
    }

    .stTabs [aria-selected="true"] {
        color: #06B6A0 !important;
        border-bottom: 2px solid #06B6A0;
    }

    /* ===================== Custom Components ===================== */

    /* --- Hero header (gradient) --- */
    .hero-header {
        background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
        color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -15%;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-header h1 {
        color: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 1.35rem !important;
        line-height: 1.6 !important;
        position: relative;
    }

    .hero-header p {
        color: rgba(255, 255, 255, 0.7) !important;
        margin: 0.5rem 0 0 0;
        font-size: 0.85rem;
        position: relative;
    }

    /* --- Minimal page header (Notion/Linear style) --- */
    .page-header-minimal {
        padding-bottom: 0.25rem;
        margin-bottom: 1rem;
    }

    .page-header-minimal h1 {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #1A1A2E !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .page-header-minimal p {
        font-size: 0.78rem;
        color: #6B7280 !important;
        margin: 0.1rem 0 0 0;
    }

    /* --- Soft header (teal tinted background) --- */
    .soft-header {
        background: linear-gradient(135deg, rgba(13,148,136,0.08) 0%, rgba(20,184,166,0.08) 100%);
        padding: 1.75rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.25rem;
    }

    .soft-header h1 {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #1A1A2E !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .soft-header p {
        font-size: 0.82rem;
        color: #6B7280 !important;
        margin: 0.3rem 0 0 0;
    }

    /* --- Section Card --- */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    .section-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1A1A2E;
        margin-bottom: 0.75rem;
    }

    /* --- Compact Step Card (for Generate page) --- */
    .step-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
    }

    .step-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }

    .step-num {
        width: 20px;
        height: 20px;
        background-color: #06B6A0;
        color: #FFFFFF;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.65rem;
        font-weight: 700;
    }

    .step-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #1A1A2E;
    }

    /* --- Metric Cards --- */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.25rem;
    }

    .metric-card {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 1rem;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }

    .metric-icon-box {
        width: 40px;
        height: 40px;
        background: #F0FDFA;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1A1A2E;
        font-family: 'Inter', sans-serif;
        line-height: 1;
    }

    .metric-label {
        font-size: 0.7rem;
        color: #6B7280;
        margin-top: 0.15rem;
    }

    /* --- Progress Bar --- */
    .progress-container {
        background: #E5E7EB;
        border-radius: 100px;
        height: 10px;
        overflow: hidden;
        margin: 0.75rem 0 0.5rem 0;
    }

    .progress-fill {
        height: 100%;
        border-radius: 100px;
        background-color: #06B6A0;
        transition: width 500ms ease;
    }

    .progress-fill-low {
        background-color: #F97316;
    }

    .progress-fill-complete {
        background-color: #059669;
    }

    /* --- Feature Card (Home) --- */
    .feature-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.75rem 1.5rem;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: all 250ms ease;
        cursor: pointer;
    }

    .feature-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }

    .feature-icon-box {
        width: 40px;
        height: 40px;
        background: #F0FDFA;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1A1A2E;
        margin-bottom: 0.35rem;
    }

    .feature-desc {
        font-size: 0.78rem;
        color: #6B7280;
        line-height: 1.6;
    }

    /* --- Hint box --- */
    .hint-box {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        background: #F0FDFA;
        border: 1px solid rgba(13,148,136,0.12);
        border-radius: 16px;
        padding: 0.85rem 1.25rem;
        margin: 0.5rem 0;
        font-size: 0.75rem;
        color: rgba(26,26,46,0.6);
        line-height: 1.6;
    }

    /* --- Compact hint (inside step card) --- */
    .hint-compact {
        display: flex;
        align-items: flex-start;
        gap: 0.4rem;
        background: #F0FDFA;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        font-size: 0.7rem;
        color: rgba(26,26,46,0.55);
        line-height: 1.5;
    }

    /* --- Badge --- */
    .badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
        font-size: 0.68rem;
        font-weight: 500;
    }

    .badge-teal {
        background: #F0FDFA;
        color: #0F766E;
    }

    .badge-gray {
        background: #F3F4F6;
        color: #6B7280;
    }

    .badge-green {
        background: #ECFDF5;
        color: #059669;
    }

    /* --- Char counter pill --- */
    .char-pill {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }

    .char-ok { background: rgba(5,150,105,0.08); color: #059669; }
    .char-warn { background: rgba(245,158,11,0.08); color: #D97706; }
    .char-over { background: rgba(220,38,38,0.08); color: #DC2626; }

    /* --- Success indicator (minimal) --- */
    .success-inline {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 0.5rem;
    }

    .success-inline-text {
        font-size: 0.78rem;
        font-weight: 500;
        color: #059669;
    }

    .success-inline-sub {
        font-size: 0.72rem;
        color: #6B7280;
    }

    /* --- Step guide (Home) --- */
    .step-guide {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    .step-guide-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1A1A2E;
        margin-bottom: 1rem;
    }

    .step-flow {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.75rem;
    }

    .step-flow-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .step-flow-num {
        width: 28px;
        height: 28px;
        background-color: #06B6A0;
        color: #FFFFFF;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }

    .step-flow-text {
        font-size: 0.85rem;
        color: #1A1A2E;
    }

    .step-flow-arrow {
        color: rgba(107,114,128,0.4);
        font-size: 0.85rem;
    }

    /* --- Login Screen --- */
    .login-card {
        max-width: 400px;
        margin: 8vh auto 1.5rem;
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .login-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFFFFF;
    }

    .login-subtitle {
        color: rgba(255,255,255,0.75);
        font-size: 0.85rem;
        margin-top: 0.75rem;
        line-height: 1.5;
    }

    /* Login page input overrides */
    .login-area .stTextInput > div > div {
        border: none !important;
        background: transparent !important;
    }

    .login-area .stTextInput > div > div > input {
        background: rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        font-size: 0.9rem !important;
        padding: 0.7rem 1rem !important;
    }

    .login-area .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.5) !important;
    }

    .login-area .stTextInput > div > div > input:focus {
        border-color: rgba(255,255,255,0.5) !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.15) !important;
        background: rgba(255,255,255,0.25) !important;
    }

    .login-area .stTextInput label,
    .login-area .stTextInput .st-emotion-cache-ue6h4q {
        display: none !important;
    }

    .login-area .stButton > button[kind="primary"] {
        background: rgba(255,255,255,0.95) !important;
        color: #0D9488 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
    }

    .login-area .stButton > button[kind="primary"]:hover {
        background: #FFFFFF !important;
        color: #0F766E !important;
    }

    /* --- Empty State --- */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        border: 1px dashed #E5E7EB;
        border-radius: 10px;
        background: #FFFFFF;
    }

    /* --- Filter bar --- */
    .filter-bar {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
    }

    /* --- Card header (small caps label) --- */
    .card-header {
        font-size: 0.72rem;
        font-weight: 500;
        color: #6B7280;
        display: flex;
        align-items: center;
        gap: 0.35rem;
        margin-bottom: 0.35rem;
    }

    /* --- Encourage text (subtle) --- */
    .encourage-text {
        font-size: 0.75rem;
        color: #6B7280;
        text-align: center;
        padding: 0.5rem 0;
    }
</style>
"""


def inject_css():
    """StreamlitページにカスタムCSSを注入する。"""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def hero_header(title: str, subtitle: str = ""):
    """ティールグラデーションのヒーローヘッダー。"""
    import streamlit as st
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="hero-header"><h1>{title}</h1>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def page_header_minimal(title: str, subtitle: str = ""):
    """Notion/Linear風のミニマルヘッダー。"""
    import streamlit as st
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="page-header-minimal"><h1>{title}</h1>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def soft_header(title: str, subtitle: str = ""):
    """ティール色の薄い背景ヘッダー。"""
    import streamlit as st
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="soft-header"><h1>{title}</h1>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def step_badge(number: int, label: str):
    """コンパクトなステップバッジ。"""
    import streamlit as st
    st.markdown(
        f'<div class="step-header">'
        f'<span class="step-num">{number}</span>'
        f'<span class="step-label">{label}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def metric_cards(metrics: list[tuple[str, str, str]]):
    """メトリクスカード。[(value, label, svg_icon), ...]"""
    import streamlit as st
    cards_html = ""
    for value, label, icon_svg in metrics:
        cards_html += f'''
        <div class="metric-card">
            <div class="metric-icon-box">{icon_svg}</div>
            <div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
        </div>'''
    st.markdown(f'<div class="metric-row">{cards_html}</div>', unsafe_allow_html=True)


def badge(text: str, variant: str = "teal"):
    """バッジHTMLを返す。"""
    return f'<span class="badge badge-{variant}">{text}</span>'


def progress_bar(percent: int, label: str = ""):
    """プログレスバー。"""
    import streamlit as st
    fill_class = "progress-fill"
    if percent < 30:
        fill_class = "progress-fill progress-fill-low"
    elif percent >= 100:
        fill_class = "progress-fill progress-fill-complete"

    label_html = ""
    if label:
        label_html = (
            f'<div style="display: flex; justify-content: space-between; '
            f'font-size: 0.82rem; color: #1A1A2E;">'
            f'<span style="font-weight: 500;">{label}</span>'
            f'<span style="font-weight: 700; color: #06B6A0; '
            f'font-family: Inter, sans-serif;">{percent}%</span></div>'
        )

    st.markdown(
        f'{label_html}'
        f'<div class="progress-container">'
        f'<div class="{fill_class}" style="width: {percent}%"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def hint_box(text: str):
    """ヒントボックス。"""
    import streamlit as st
    st.markdown(f'<div class="hint-box">{text}</div>', unsafe_allow_html=True)


def char_pill(current: int, limit: int):
    """文字数カウンターpill。"""
    import streamlit as st
    if current <= limit * 0.9:
        cls = "char-ok"
        msg = "文字数制限内です"
    elif current <= limit:
        cls = "char-warn"
        msg = f"あと{limit - current}字"
    else:
        cls = "char-over"
        msg = f"{current - limit}字オーバー"

    st.markdown(
        f'<div style="display: flex; justify-content: space-between; '
        f'align-items: center; margin-top: -0.25rem; padding: 0.25rem 0;">'
        f'<span style="font-size: 0.72rem; color: #6B7280;">{msg}</span>'
        f'<span class="char-pill {cls}">{current} / {limit}字</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
