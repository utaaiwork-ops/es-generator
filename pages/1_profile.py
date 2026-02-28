import streamlit as st
from lib.auth import check_password
from lib.database import get_profile, upsert_profile
from lib.styles import inject_css, page_header

st.set_page_config(page_title="プロフィール設定", page_icon="📝", layout="wide")
inject_css()

if not check_password():
    st.stop()

page_header("プロフィール設定", "ESの生成に使うあなたの情報を登録してください")

# プロフィールフィールド定義
FIELDS = [
    ("氏名", "name", "text", "例: 山田太郎"),
    ("大学・学部・学科", "university", "text", "例: 〇〇大学 経済学部 経済学科"),
    ("ゼミ・研究内容", "research", "area", "ゼミの研究テーマや内容を記入"),
    ("ガクチカ（学生時代に力を入れたこと）", "gakuchika", "area", "具体的なエピソードを記入"),
    ("強み", "strength", "text", "例: 粘り強さ、リーダーシップ"),
    ("弱み", "weakness", "text", "例: 心配性、完璧主義"),
    ("自己PR", "self_pr", "area", "具体的な成果やエピソードを交えて記入"),
    ("価値観・大切にしていること", "values", "text", "例: チームワーク、挑戦する姿勢"),
    ("将来のビジョン", "vision", "text", "例: グローバルに活躍するビジネスパーソン"),
    ("趣味・特技", "hobbies", "text", "例: プログラミング、英語（TOEIC 800点）"),
    ("アルバイト・インターン経験", "work_experience", "area", "経験した内容と学んだことを記入"),
    ("志望業界・職種", "target_industry", "text", "例: IT業界・エンジニア職"),
    ("その他自由記入", "other", "area", "上記に当てはまらない情報があれば記入"),
]

# 現在の値を読み込み
try:
    current = get_profile()
except Exception as e:
    st.error(f"データベース接続エラー: {e}")
    st.info("Supabaseの接続設定を確認してください。")
    st.stop()

# 登録率の計算
filled = sum(1 for _, key, _, _ in FIELDS if current.get(key, "").strip())
total = len(FIELDS)

st.markdown(
    f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">{filled}/{total}</div>
            <div class="metric-label">入力済み項目</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{int(filled / total * 100)}%</div>
            <div class="metric-label">完成度</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("profile_form"):
    values: dict[str, str] = {}

    # 基本情報と詳細を2カラムで
    st.markdown("### 基本情報")
    col_l, col_r = st.columns(2)

    for i, (label, key, input_type, placeholder) in enumerate(FIELDS):
        # 前半は2カラム、後半（textarea系）はフル幅
        if input_type == "text":
            target = col_l if i % 2 == 0 else col_r
            with target:
                values[key] = st.text_input(
                    label,
                    value=current.get(key, ""),
                    placeholder=placeholder,
                )
        else:
            if key == "gakuchika":
                st.markdown("### 詳細情報")
            values[key] = st.text_area(
                label,
                value=current.get(key, ""),
                height=120,
                placeholder=placeholder,
            )

    st.markdown("")
    submitted = st.form_submit_button("保存する", type="primary", use_container_width=True)

if submitted:
    try:
        for key, val in values.items():
            upsert_profile(key, val)
        st.success("プロフィールを保存しました")
    except Exception as e:
        st.error(f"保存に失敗しました: {e}")
