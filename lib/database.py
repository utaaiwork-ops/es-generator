import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Streamlit Cloud: secretsから環境変数に転送
for key in ("SUPABASE_URL", "SUPABASE_KEY", "ANTHROPIC_API_KEY"):
    if key not in os.environ and key in st.secrets:
        os.environ[key] = st.secrets[key]

_client: Client | None = None


def get_client() -> Client:
    """Supabaseクライアントのシングルトンを返す。"""
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
        if not url or not key:
            raise ValueError("SUPABASE_URLとSUPABASE_KEYを.envに設定してください")
        _client = create_client(url, key)
    return _client


# --- Profile ---

def get_profile() -> dict[str, str]:
    """プロフィール全件をdict形式で返す。"""
    res = get_client().table("profile").select("field_name, field_value").execute()
    return {row["field_name"]: (row["field_value"] or "") for row in res.data}


def upsert_profile(field_name: str, field_value: str) -> None:
    """プロフィールの1フィールドを登録・更新する。"""
    client = get_client()
    existing = (
        client.table("profile")
        .select("id")
        .eq("field_name", field_name)
        .execute()
    )
    if existing.data:
        client.table("profile").update(
            {"field_value": field_value, "updated_at": "now()"}
        ).eq("field_name", field_name).execute()
    else:
        client.table("profile").insert(
            {"field_name": field_name, "field_value": field_value}
        ).execute()


# --- Companies ---

def create_company(name: str, url: str | None, scraped_info: str | None, notes: str | None) -> int:
    """会社情報を作成し、IDを返す。"""
    res = get_client().table("companies").insert({
        "name": name,
        "url": url,
        "scraped_info": scraped_info,
        "notes": notes,
    }).execute()
    return res.data[0]["id"]


def get_company(company_id: int) -> dict | None:
    """会社情報を1件取得する。"""
    res = get_client().table("companies").select("*").eq("id", company_id).execute()
    return res.data[0] if res.data else None


def list_companies() -> list[dict]:
    """会社情報を全件取得する。"""
    res = (
        get_client()
        .table("companies")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return res.data


# --- Generated ES ---

def save_es(company_id: int, es_type: str, question: str | None, char_limit: int, content: str) -> int:
    """生成ESを保存し、IDを返す。"""
    res = get_client().table("generated_es").insert({
        "company_id": company_id,
        "es_type": es_type,
        "question": question,
        "char_limit": char_limit,
        "content": content,
    }).execute()
    return res.data[0]["id"]


def update_es(es_id: int, content: str) -> None:
    """生成ESの内容を更新する。"""
    get_client().table("generated_es").update({
        "content": content,
        "is_edited": True,
        "updated_at": "now()",
    }).eq("id", es_id).execute()


def list_es(company_id: int | None = None) -> list[dict]:
    """生成ES一覧を取得する。company_id指定でフィルタ可能。"""
    query = (
        get_client()
        .table("generated_es")
        .select("*, companies(name)")
        .order("created_at", desc=True)
    )
    if company_id is not None:
        query = query.eq("company_id", company_id)
    return query.execute().data


def delete_es(es_id: int) -> None:
    """生成ESを削除する。"""
    get_client().table("generated_es").delete().eq("id", es_id).execute()
