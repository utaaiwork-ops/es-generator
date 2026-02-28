import type { Profile } from "./app-context"

/**
 * DB field_name ↔ TS Profile key の双方向マッピング
 *
 * DB側は既存テーブルの field_name をそのまま維持し、
 * フロントエンド側では使いやすいキー名を使う。
 */

/** DB field_name → TS Profile key */
const dbToTs: Record<string, keyof Profile> = {
  name: "name",
  university: "university",
  target_industry: "industry",
  hobbies: "hobby",
  research: "seminar",
  gakuchika: "gakuchika",
  self_pr: "selfPR",
  work_experience: "partTimeJob",
  strength: "strength",
  weakness: "weakness",
  values: "values",
  vision: "vision",
  other: "other",
}

/** TS Profile key → DB field_name */
const tsToDb: Record<keyof Profile, string> = {
  name: "name",
  university: "university",
  industry: "target_industry",
  hobby: "hobbies",
  seminar: "research",
  gakuchika: "gakuchika",
  selfPR: "self_pr",
  partTimeJob: "work_experience",
  strength: "strength",
  weakness: "weakness",
  values: "values",
  vision: "vision",
  other: "other",
}

/** DBから取得した { field_name: field_value } を Profile に変換 */
export function dbRowsToProfile(rows: Record<string, string>): Partial<Profile> {
  const profile: Partial<Profile> = {}
  for (const [dbField, value] of Object.entries(rows)) {
    const tsKey = dbToTs[dbField]
    if (tsKey) {
      profile[tsKey] = value
    }
  }
  return profile
}

/** Profile のキーを DB field_name に変換 */
export function profileKeyToDbField(key: keyof Profile): string {
  return tsToDb[key]
}

/** Profile 全体を DB 形式の { field_name: field_value } ペア配列に変換 */
export function profileToDbEntries(profile: Profile): { field_name: string; field_value: string }[] {
  return (Object.keys(profile) as (keyof Profile)[]).map((key) => ({
    field_name: tsToDb[key],
    field_value: profile[key],
  }))
}
