-- ============================================
-- Supabase RLS (Row Level Security) ポリシー設定
-- Supabase Dashboard > SQL Editor で実行してください
-- ============================================

-- 1. 各テーブルにuser_idカラムがなければ追加（既にある場合はスキップされます）
ALTER TABLE profile ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES auth.users(id);
ALTER TABLE companies ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES auth.users(id);
ALTER TABLE generated_es ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES auth.users(id);

-- 2. RLSを有効化
ALTER TABLE profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_es ENABLE ROW LEVEL SECURITY;

-- 3. profile テーブルのポリシー
CREATE POLICY "Users can view own profile" ON profile
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON profile
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON profile
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own profile" ON profile
  FOR DELETE USING (auth.uid() = user_id);

-- 4. companies テーブルのポリシー
CREATE POLICY "Users can view own companies" ON companies
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own companies" ON companies
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own companies" ON companies
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own companies" ON companies
  FOR DELETE USING (auth.uid() = user_id);

-- 5. generated_es テーブルのポリシー
CREATE POLICY "Users can view own es" ON generated_es
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own es" ON generated_es
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own es" ON generated_es
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own es" ON generated_es
  FOR DELETE USING (auth.uid() = user_id);
