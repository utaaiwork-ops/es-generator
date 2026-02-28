"""共通CSSスタイル定義。UI/UX Pro Max デザインシステム準拠。"""

# カラーパレット（Job Board/Recruitment ベース）
COLORS = {
    "primary": "#0369A1",
    "primary_light": "#0EA5E9",
    "primary_dark": "#075985",
    "cta": "#22C55E",
    "cta_hover": "#16A34A",
    "bg": "#F0F9FF",
    "bg_white": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "text": "#0C4A6E",
    "text_muted": "#64748B",
    "text_light": "#94A3B8",
    "border": "#E2E8F0",
    "border_focus": "#0EA5E9",
    "success": "#22C55E",
    "success_bg": "#F0FDF4",
    "error": "#EF4444",
    "error_bg": "#FEF2F2",
    "warning_bg": "#FFFBEB",
}

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* === Global === */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #F0F9FF;
    }

    /* === Hide Streamlit defaults === */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* === Typography === */
    h1 {
        color: #0C4A6E !important;
        font-weight: 700 !important;
        font-size: 1.875rem !important;
        letter-spacing: -0.025em;
        padding-bottom: 0.25rem !important;
    }

    h2 {
        color: #075985 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        color: #0369A1 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    p, li, label, .stMarkdown {
        color: #0C4A6E;
        line-height: 1.6;
    }

    /* === Cards === */
    .card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .card-header {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 0.5rem;
    }

    /* === Metric Cards === */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        flex: 1;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0369A1;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 0.25rem;
    }

    /* === Step indicator === */
    .step-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #0369A1;
        color: #FFFFFF;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
    }

    /* === Status badges === */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .badge-blue {
        background: #DBEAFE;
        color: #1E40AF;
    }

    .badge-green {
        background: #DCFCE7;
        color: #166534;
    }

    .badge-gray {
        background: #F1F5F9;
        color: #475569;
    }

    /* === Primary Buttons === */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {
        background-color: #0369A1 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 1.5rem !important;
        transition: background-color 200ms ease !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        background-color: #075985 !important;
    }

    /* === Secondary Buttons === */
    .stButton > button:not([kind="primary"]) {
        background-color: #FFFFFF !important;
        color: #0369A1 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 200ms ease !important;
    }

    .stButton > button:not([kind="primary"]):hover {
        border-color: #0369A1 !important;
        background-color: #F0F9FF !important;
    }

    /* === Inputs === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border-color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 200ms ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0EA5E9 !important;
        box-shadow: 0 0 0 1px #0EA5E9 !important;
    }

    /* === Slider === */
    .stSlider > div > div > div > div {
        background-color: #0369A1 !important;
    }

    /* === Expander === */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        color: #0C4A6E !important;
    }

    /* === Divider === */
    hr {
        border-color: #E2E8F0 !important;
    }

    /* === Success/Error/Info messages === */
    .stSuccess {
        background-color: #F0FDF4 !important;
        color: #166534 !important;
        border-left: 4px solid #22C55E !important;
    }

    .stError {
        background-color: #FEF2F2 !important;
        color: #991B1B !important;
        border-left: 4px solid #EF4444 !important;
    }

    /* === Sidebar === */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #0C4A6E;
    }

    /* === Tabs === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        color: #64748B;
        font-weight: 500;
        padding: 0.75rem 1.25rem;
    }

    .stTabs [aria-selected="true"] {
        color: #0369A1 !important;
        border-bottom: 2px solid #0369A1;
    }

    /* === Page header helper === */
    .page-header {
        background: linear-gradient(135deg, #0369A1 0%, #0EA5E9 100%);
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    .page-header h1 {
        color: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .page-header p {
        color: rgba(255, 255, 255, 0.85) !important;
        margin: 0.5rem 0 0 0;
    }

    /* === Empty state === */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #64748B;
    }

    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.4;
    }

    /* === Login page === */
    .login-container {
        max-width: 400px;
        margin: 10vh auto;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
    }

    .login-logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0369A1;
        margin-bottom: 0.25rem;
    }

    .login-subtitle {
        color: #64748B;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
</style>
"""


def inject_css():
    """StreamlitページにカスタムCSSを注入する。"""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def page_header(title: str, description: str = ""):
    """グラデーション付きページヘッダーを表示する。"""
    import streamlit as st
    desc_html = f"<p>{description}</p>" if description else ""
    st.markdown(
        f'<div class="page-header"><h1>{title}</h1>{desc_html}</div>',
        unsafe_allow_html=True,
    )


def step_badge(number: int, label: str):
    """ステップバッジを表示する。"""
    import streamlit as st
    st.markdown(
        f'<div class="step-badge">STEP {number}　{label}</div>',
        unsafe_allow_html=True,
    )


def metric_cards(metrics: list[tuple[str, str]]):
    """メトリクスカードを横並びに表示する。[(value, label), ...]"""
    import streamlit as st
    cards_html = ""
    for value, label in metrics:
        cards_html += f'''
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>'''
    st.markdown(f'<div class="metric-row">{cards_html}</div>', unsafe_allow_html=True)


def badge(text: str, variant: str = "blue"):
    """バッジHTMLを返す。variant: blue, green, gray"""
    return f'<span class="badge badge-{variant}">{text}</span>'
