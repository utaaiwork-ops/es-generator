import { supabase } from "./supabase"
import type { Profile } from "./app-context"
import { dbRowsToProfile, profileKeyToDbField } from "./field-map"

// --- Profile ---

/** プロフィール全件を Profile 型で返す */
export async function getProfile(): Promise<Partial<Profile>> {
  const { data, error } = await supabase
    .from("profile")
    .select("field_name, field_value")

  if (error) throw error

  const rows: Record<string, string> = {}
  for (const row of data ?? []) {
    rows[row.field_name] = row.field_value ?? ""
  }
  return dbRowsToProfile(rows)
}

/** プロフィールの1フィールドを登録・更新する */
export async function upsertProfile(key: keyof Profile, value: string): Promise<void> {
  const fieldName = profileKeyToDbField(key)

  const { data: existing } = await supabase
    .from("profile")
    .select("id")
    .eq("field_name", fieldName)

  if (existing && existing.length > 0) {
    const { error } = await supabase
      .from("profile")
      .update({ field_value: value, updated_at: new Date().toISOString() })
      .eq("field_name", fieldName)
    if (error) throw error
  } else {
    const { error } = await supabase
      .from("profile")
      .insert({ field_name: fieldName, field_value: value })
    if (error) throw error
  }
}

// --- Companies ---

/** 会社情報を作成し、IDを返す */
export async function createCompany(
  name: string,
  url: string | null,
  scrapedInfo: string | null,
  notes: string | null,
): Promise<number> {
  const { data, error } = await supabase
    .from("companies")
    .insert({ name, url, scraped_info: scrapedInfo, notes })
    .select("id")
    .single()

  if (error) throw error
  return data.id
}

/** 会社情報を1件取得する */
export async function getCompany(companyId: number) {
  const { data, error } = await supabase
    .from("companies")
    .select("*")
    .eq("id", companyId)
    .single()

  if (error) throw error
  return data
}

/** 会社情報を全件取得する */
export async function listCompanies() {
  const { data, error } = await supabase
    .from("companies")
    .select("*")
    .order("created_at", { ascending: false })

  if (error) throw error
  return data ?? []
}

// --- Generated ES ---

/** 生成ESを保存し、IDを返す */
export async function saveEs(
  companyId: number,
  esType: string,
  question: string | null,
  charLimit: number,
  content: string,
): Promise<number> {
  const { data, error } = await supabase
    .from("generated_es")
    .insert({
      company_id: companyId,
      es_type: esType,
      question,
      char_limit: charLimit,
      content,
    })
    .select("id")
    .single()

  if (error) throw error
  return data.id
}

/** 生成ESの内容を更新する */
export async function updateEs(esId: number, content: string): Promise<void> {
  const { error } = await supabase
    .from("generated_es")
    .update({
      content,
      is_edited: true,
      updated_at: new Date().toISOString(),
    })
    .eq("id", esId)

  if (error) throw error
}

/** 生成ES一覧を取得する。companyId指定でフィルタ可能 */
export async function listEs(companyId?: number) {
  let query = supabase
    .from("generated_es")
    .select("*, companies(name)")
    .order("created_at", { ascending: false })

  if (companyId !== undefined) {
    query = query.eq("company_id", companyId)
  }

  const { data, error } = await query
  if (error) throw error
  return data ?? []
}

/** 生成ESを削除する */
export async function deleteEs(esId: number): Promise<void> {
  const { error } = await supabase
    .from("generated_es")
    .delete()
    .eq("id", esId)

  if (error) throw error
}
