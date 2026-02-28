import streamlit as st
from lib.auth import check_auth, logout_button
from lib.database import get_profile, upsert_profile
from lib.styles import inject_css, soft_header, progress_bar, hint_box

st.set_page_config(page_title="プロフィール設定", page_icon="", layout="wide")
inject_css()

if not check_auth():
    st.stop()

logout_button()

# --- Soft header ---
soft_header("プロフィール設定", "ここで登録した情報をもとに、全企業のESを生成します")

# --- フィールド定義（セクション分け） ---
SECTIONS = {
    "基本情報": [
        ("氏名", "name", "text", "山田 太郎"),
        ("大学・学部・学科", "university", "text", "東京大学 工学部"),
        ("志望業界・職種", "target_industry", "text", "IT、コンサル、メーカーなど"),
        ("趣味・特技", "hobbies", "text", "読書、サッカーなど"),
    ],
    "あなたのエピソード": [
        ("ゼミ・研究内容", "research", "area", "ゼミや研究の内容を具体的に書いてください"),
        ("ガクチカ（学生時代に力を入れたこと）", "gakuchika", "area",
         "取り組んだこと、工夫した点、結果を書いてください"),
        ("自己PR", "self_pr", "area",
         "自分の強みが発揮されたエピソードを書いてください"),
        ("アルバイト・インターン経験", "work_experience", "area",
         "バイト先、役割、学んだことなど"),
    ],
    "あなたの軸": [
        ("強み", "strength", "text", "リーダーシップ、分析力など"),
        ("弱み", "weakness", "text", "心配性、こだわりが強いなど"),
        ("価値観・大切にしていること", "values", "area", "仕事で大切にしたいこと"),
        ("将来のビジョン", "vision", "area", "5〜10年後にどうなっていたいか"),
        ("その他自由記入", "other", "area", "補足情報があれば記入してください"),
    ],
}

ALL_FIELDS = []
for fields in SECTIONS.values():
    ALL_FIELDS.extend(fields)

# --- 現在のプロフィール読み込み ---
try:
    current = get_profile()
except Exception as e:
    st.error(f"データベース接続エラー: {e}")
    st.info("Supabaseの接続設定を確認してください。")
    st.stop()

# --- プログレスバー ---
filled = sum(1 for _, key, _, _ in ALL_FIELDS if current.get(key, "").strip())
total = len(ALL_FIELDS)
percent = int(filled / total * 100)

# プログレスカード
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown(
    '<div style="display: flex; justify-content: space-between; align-items: center;">'
    '<span style="font-size: 0.85rem; font-weight: 500; color: #1A1A2E;">'
    '一度登録すれば、何社分でもESが作れます</span>'
    f'<span style="font-size: 0.85rem; font-weight: 700; color: #06B6A0; '
    f'font-family: Inter, sans-serif;">{percent}%</span></div>',
    unsafe_allow_html=True,
)
progress_bar(percent)

# 段階メッセージ
if percent == 0:
    msg = "まずは名前と大学だけでもOK"
elif percent < 30:
    msg = "少しずつ埋めていきましょう"
elif percent < 80:
    msg = "エピソード欄を埋めるとES生成の質がグッと上がります"
elif percent < 100:
    msg = "あと少しで完成！"
else:
    msg = "全項目入力済み！ESを生成してみましょう"

st.markdown(
    f'<p style="font-size: 0.78rem; color: #6B7280; margin-top: 0.25rem;">{msg}</p>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# --- フォーム ---
with st.form("profile_form"):
    values: dict[str, str] = {}

    for section_name, fields in SECTIONS.items():
        st.markdown(
            f'<div class="section-card"><div class="section-title">{section_name}</div>',
            unsafe_allow_html=True,
        )

        text_fields = [(l, k, t, p) for l, k, t, p in fields if t == "text"]
        area_fields = [(l, k, t, p) for l, k, t, p in fields if t == "area"]

        if text_fields:
            cols = st.columns(2)
            for i, (label, key, _, placeholder) in enumerate(text_fields):
                with cols[i % 2]:
                    values[key] = st.text_input(
                        label,
                        value=current.get(key, ""),
                        placeholder=placeholder,
                    )

        for label, key, _, placeholder in area_fields:
            values[key] = st.text_area(
                label,
                value=current.get(key, ""),
                height=110,
                placeholder=placeholder,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ヒント
    hint_box(
        "数字や固有名詞を入れると、AIがより具体的なESを生成できます。"
        "完璧でなくても大丈夫、あとから編集できます。"
    )

    submitted = st.form_submit_button("保存する", type="primary", use_container_width=True)

if submitted:
    try:
        for key, val in values.items():
            upsert_profile(key, val)
        st.success("プロフィールを保存しました")
        st.rerun()
    except Exception as e:
        st.error(f"保存に失敗しました: {e}")

# 完成したらES生成への導線
if percent == 100:
    if st.button("ES生成画面へ進む", use_container_width=True):
        st.switch_page("pages/2_generate.py")
