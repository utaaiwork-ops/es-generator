# ES志望動機ジェネレーター - タスク表

> **目標**: 5人に使ってもらえる状態まで完成させる
> **コアバリュー**: ES生成の精度（ここがLTV直結）
> **方針**: 最小限の機能 → 完成 → フィードバックで改善

---

## Phase 1: 動く状態にする（ブロッカー解消）

コードは書き終わっている。あとは外部サービスの接続だけ。

### 1-1. Supabase接続 ← 手動作業
- [ ] https://supabase.com でプロジェクト作成
- [ ] SQL Editor で以下を実行（テーブル3つ作成）

```sql
CREATE TABLE profile (
  id SERIAL PRIMARY KEY,
  field_name TEXT NOT NULL,
  field_value TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE companies (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  url TEXT,
  scraped_info TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE generated_es (
  id SERIAL PRIMARY KEY,
  company_id INTEGER REFERENCES companies(id),
  es_type TEXT NOT NULL,
  question TEXT,
  char_limit INTEGER,
  content TEXT NOT NULL,
  is_edited BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

- [ ] .envに設定を記入
  - `SUPABASE_URL` → Settings > API > Project URL
  - `SUPABASE_KEY` → Settings > API > anon public

### 1-2. Claude API接続 ← 手動作業
- [ ] https://console.anthropic.com でAPIキー取得
- [ ] .env に `ANTHROPIC_API_KEY` を設定

### 1-3. ログインパスワード
- [ ] .env の `APP_PASSWORD` を本番用に変更

### 1-4. 動作確認（Claude Codeで実行）
- [ ] `streamlit run app.py` で起動
- [ ] ログインできる
- [ ] プロフィール保存できる
- [ ] ES生成できる（ここが最重要）
- [ ] 履歴に保存・表示できる

---

## Phase 2: ES生成の精度を上げる（LTVの源泉）

5人が「また使いたい」と思うかは、ここで決まる。

- [ ] プロンプトのチューニング（prompts/templates.py）
  - [ ] 実際の企業HP（3社以上）でテスト生成
  - [ ] 生成結果を読んで、具体性・説得力を評価
  - [ ] 「嘘っぽい」「抽象的すぎる」部分をプロンプトで改善
- [ ] ES種類ごとの出力品質チェック
  - [ ] 志望動機
  - [ ] ガクチカ
  - [ ] 自己PR
  - [ ] 強み・弱み
  - [ ] 将来やりたいこと

---

## Phase 3: デプロイ（5人に配る）

- [ ] GitHubリポジトリ作成・push
- [ ] Streamlit Cloud で公開
  - Secrets に .env の4つの値を設定
- [ ] 5人にURL共有

---

## 完了済み

- [x] プロジェクト構築（ディレクトリ、パッケージ、設定ファイル）
- [x] 全画面のコード実装（ログイン・プロフィール・ES生成・履歴）
- [x] UI/UXデザイン適用
- [x] スクレイピング機能
- [x] Claude API連携コード
- [x] Supabase CRUD コード

---

## 拡張候補（Phase 3以降、フィードバック次第）

- 生成結果の「再生成」ボタン（パラメータ変えて複数パターン出す）
- プロンプトに「トーン」選択を追加（堅め/カジュアル/熱量高め）
- 複数ユーザー対応（認証をSupabase Authに切り替え）
- ES添削モード（既存の文章をブラッシュアップ）
- 企業ごとの「刺さるポイント」分析表示
