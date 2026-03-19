# Blue App Works — Corporate Website

**URL**: https://www.blueappworks.com
**開業日**: 2026年1月29日  
**事業者**: 喜田紘介 / Blue App Works

---

## プロジェクト概要

Blue App Worksの静的コーポレートサイトです。  
Snowflake Nativeのアプリ実行・管理プラットフォーム「Blue App Gallery」のランディングページおよびコーポレート情報ページで構成されています。

---

## ファイル構成

```
index.html        # トップページ（Hero / 課題 / サービス / How it works / Tech / 料金 / About）
privacy.html      # プライバシーポリシー（日英バイリンガル・言語切り替え機能付き）
contact.html      # お問い合わせページ（フォーム + mailto fallback）
css/
  style.css       # メインスタイルシート（レスポンシブ対応）
README.md         # このファイル
```

---

## ページ一覧 / URI

| ページ | パス | 説明 |
|--------|------|------|
| トップ | `/` または `/index.html` | サービス全体説明 |
| プライバシーポリシー | `/privacy.html` | 日英バイリンガル、言語切り替えボタン付き |
| お問い合わせ | `/contact.html` | 問い合わせフォーム（mailto方式） |
| | `/contact.html?type=demo` | デモ申し込み（種別プリセット） |
| | `/contact.html?type=saas` | SaaS詳細問い合わせ（プリセット） |
| | `/contact.html?type=selfhost` | セルフホスト見積もり（プリセット） |
| | `/contact.html?type=consulting` | 伴走支援相談（プリセット） |
| | `/contact.html?type=snowflake` | Snowflake環境相談（プリセット） |

---

## 主な機能

- ✅ レスポンシブデザイン（モバイル対応・ハンバーガーメニュー）
- ✅ スクロール連動ヘッダー（固定ナビ）
- ✅ スクロールアニメーション（カード・ステップ等）
- ✅ Hero フローティングカード（CSS アニメーション）
- ✅ プライバシーポリシーの言語切り替え（日本語 / English / 両言語）
- ✅ お問い合わせフォーム（mailto fallback、URLパラメータで種別プリセット）
- ✅ Snowflake Marketplace 連携案内

---

## カラーパレット

| 変数 | 値 | 用途 |
|------|----|------|
| `--blue-dark` | `#0a2540` | ヘッダー・フッター・Hero背景 |
| `--blue-mid` | `#1a4a8a` | セカンダリ |
| `--blue-accent` | `#2d7dd2` | CTA・リンク |
| `--blue-light` | `#e8f1fb` | バッジ・背景 |

---

## お問い合わせ先

| 用途 | メールアドレス |
|------|---------------|
| 一般問い合わせ | contact@blueappworks.com |
| 技術サポート | support@blueappworks.com |

---

## 今後の実装候補

- [ ] Snowflake Marketplace出品後のリンク追加
- [ ] Blue App Gallery サービスサイト (blueappgallery.com)
- [ ] お問い合わせフォームのバックエンド連携（Formspree / Netlify Forms等）
- [ ] ブログ / ナレッジベースページ
- [ ] 日英切り替え（ページ全体のi18n）
- [ ] GitHub Pages / Cloudflare Pages へのデプロイ設定

---

## デプロイ方法（GitHub Pages）

```bash
# 1. GitHubリポジトリにプッシュ
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/[username]/blueappworks-site.git
git push -u origin main

# 2. Settings → Pages → Source: main branch / root
# 3. Custom domain: blueappworks.com
# 4. お名前.comでCNAMEレコード追加:
#    ホスト: @ / www
#    参照先: [username].github.io
```

---

*Last updated: 2026-03-18*
