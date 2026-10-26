"""Editorial-first homepage for the published Clinical System reading library.

Only published entries from site/pages.json may appear. Editorial status and
clinical-review records remain separate from the public reading surface.
"""
from html import escape


def _card(page, collection, label, cue, featured=False):
    title = escape(page["title"])
    subtitle = escape(page["subtitle"])
    url = escape(page["output"], quote=True)
    return f'''<a class="library-card{' library-card-feature' if featured else ''}" href="{url}" data-collection="{collection}">
      <span class="library-card-kind">{label}</span>
      <span class="library-card-middle"><strong>{title}</strong><span>{subtitle}</span></span>
      <span class="library-card-bottom"><span>{cue}</span><span aria-hidden="true">↗</span></span>
    </a>'''


def render_home(pages):
    """Build the discovery view using the same explicit publication whitelist."""
    originals = [p for p in pages if p.get("kind") == "historical_original"]
    lessons = [p for p in pages if p.get("collection") == "xiaoma-internal-medicine" and p.get("date") and not p.get("exam")]
    integrations = [p for p in pages if p.get("kind") == "ai_integrated"]
    cards = []
    # Current integrated publications lead; preserved historical originals are a
    # separate, explicitly archived reading path rather than the default version.
    # Preserve the explicitly featured current DCM version before newer companion readings.
    ordered_integrations = sorted(integrations, key=lambda row: row["date"], reverse=True)
    featured_dcm = next((p for p in ordered_integrations if p["output"] == "xiaoma-reading-dcm-integrated.html"), None)
    if featured_dcm:
        ordered_integrations.remove(featured_dcm)
        ordered_integrations.insert(0, featured_dcm)
    for p in ordered_integrations:
        cards.append(_card(p, "integrated", "小麻閱讀 · 最新整合", "閱讀完整教材"))
    for p in sorted(originals, key=lambda row: row["date"], reverse=True):
        cards.append(_card(p, "original", "小麻閱讀 · 歷史原稿", "查閱原稿存檔"))
    for p in sorted(lessons, key=lambda row: row["date"], reverse=True):
        cards.append(_card(p, "medicine", "內科國考 · 持續更新", "從臨床問題開始"))
    if not cards:
        return '''<!doctype html><html lang="zh-Hant"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>小麻閱讀｜編輯預覽</title>
<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="home.css">
</head><body class="reader-page library-page"><main class="library-wrap" id="main">
<section class="library-hero"><p class="library-kicker">小麻閱讀</p>
<h1>醫學知識，<em>從理解出發。</em></h1>
<p class="library-intro">目前教材仍在核對原稿、圖表與臨床證據。這是未發布的編輯預覽頁，尚無作品通過正式上架驗收。</p>
</section></main></body></html>'''
    listing = "\n".join(cards)

    return f'''<!doctype html><html lang="zh-Hant"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="小麻閱讀與 Clinical System：把醫學知識連成能用的臨床判斷。">
<title>小麻閱讀 · Clinical System</title>
<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="home.css">
</head><body class="reader-page library-page">
<a class="skip-link" href="#main">跳到主要內容</a>
<header class="library-header">
  <a class="library-logo" href="index.html" aria-label="小麻閱讀首頁"><span class="library-logo-mark" aria-hidden="true">小</span><span>小麻閱讀<small>MEDICAL READING</small></span></a>
  <nav aria-label="主要導覽"><a href="index.html" aria-current="page">首頁</a><a href="knowledge-atlas.html">知識地圖</a><a href="xiaoma-reading.html">小麻閱讀</a><a href="xiaoma-internal-medicine.html">內科國考</a></nav>
  <button class="library-theme" id="theme" aria-label="切換明暗主題" title="切換主題">◐</button>
</header>
<main class="library-wrap" id="main">
  <section class="library-hero" aria-labelledby="library-title">
    <p class="library-kicker"><span aria-hidden="true" class="library-kicker-mark"></span> 小麻閱讀 <span>／</span> 醫學知識圖書館</p>
    <h1 id="library-title">把醫學，讀成<br><em>能用的判斷。</em></h1>
    <p class="library-intro">從一個值得追問的問題開始，連接生理機轉、臨床證據與決策。保留完整論述，也讓每一次閱讀更有方向。</p>
    <div class="library-search-wrap">
      <label for="search">找一個想弄懂的問題</label>
      <div class="library-search-field"><span aria-hidden="true">⌕</span><input id="search" type="search" class="searchbox" placeholder="搜尋疾病、概念或臨床問題…" autocomplete="off" aria-describedby="library-search-help"><kbd>/</kbd></div>
      <p id="library-search-help">可搜尋已公開文章全文；搜尋結果會顯示在下方。</p>
      <div class="results library-search-results" id="results" aria-live="polite"></div>
    </div>
    <a class="library-resume" href="xiaoma-reading.html" id="resume-reading" hidden><span><small>繼續上次閱讀</small><strong id="resume-title"></strong></span><span aria-hidden="true">→</span></a>
  </section>
  <section class="library-atlas" aria-labelledby="atlas-heading">
    <div class="library-atlas-copy"><p class="library-overline">CONNECT THE REASONING</p>
      <h2 id="atlas-heading">看見文章之間，<br>真正相連的問題。</h2>
      <p>例如，呼吸困難可能涉及肺泡換氣、心臟充盈、前向血流或組織供氧。先從症狀選擇一條生理分支，再依先備知識、病例推理與國考驗證找到下一篇；不用在兩份閱讀清單間來回。</p>
      <a class="library-atlas-cta" href="knowledge-atlas.html">探索臨床知識脈絡 <span aria-hidden="true">↗</span></a>
    </div>
    <div class="library-atlas-steps" aria-label="知識建構路徑">
      <div><span>01 / OBSERVE</span><strong>現在看到了什麼？</strong><small>症狀、檢驗與影像各自提供哪些證據</small></div>
      <div><span>02 / EXPLAIN</span><strong>背後的機轉是什麼？</strong><small>從共同生理前提區分不同疾病</small></div>
      <div><span>03 / DECIDE</span><strong>何時必須改變處置？</strong><small>讓臨床風險與證據決定下一步</small></div>
    </div>
  </section>
  <section class="library-section" id="articles" aria-labelledby="articles-heading">
    <div class="library-section-heading"><div><p class="library-overline">READ THE IDEAS</p><h2 id="articles-heading">開始閱讀</h2></div><p>已公開的完整教材與文章</p></div>
    <div class="library-filters" role="group" aria-label="篩選文章">
       <button class="is-active" data-library-filter="all" aria-pressed="true">全部文章</button>
       <button data-library-filter="original" aria-pressed="false">歷史原稿</button>
       <button data-library-filter="integrated" aria-pressed="false">整合教材</button>
       <button data-library-filter="medicine" aria-pressed="false">內科國考</button>
    </div>
    <div class="library-grid" id="library-grid">{listing}</div>
    <p class="library-filter-empty" id="library-filter-empty" hidden>此分類目前沒有公開文章。</p>
  </section>
  <section class="library-section library-paths" aria-labelledby="paths-heading">
    <div class="library-section-heading"><div><p class="library-overline">EXPLORE THE COLLECTIONS</p><h2 id="paths-heading">沿著一條脈絡讀</h2></div></div>
    <div class="library-path-grid">
      <a class="library-path" href="knowledge-atlas.html"><span class="library-path-number">01 / CLINICAL QUESTIONS</span><h3>知識地圖</h3><p>以臨床問題為起點，同時查看機轉分支、閱讀順序及對應驗證題。</p><span>進入脈絡 <span aria-hidden="true">↗</span></span></a>
      <a class="library-path" href="xiaoma-reading.html"><span class="library-path-number">02 / ESSAYS</span><h3>小麻閱讀</h3><p>從 Pocket Medicine 的定義與圖表出發，展開背後的機轉與臨床判斷。</p><span>探索系列 <span aria-hidden="true">↗</span></span></a>
      <a class="library-path" href="xiaoma-internal-medicine.html"><span class="library-path-number">03 / INTERNAL MEDICINE</span><h3>小麻內科國考</h3><p>以臨床問題串連內科主題、先備知識與國考題目。</p><span>進入課程 <span aria-hidden="true">↗</span></span></a>
    </div>
  </section>
  <footer class="library-footer"><div><strong>小麻閱讀</strong><span>從生理機轉，走到有依據的臨床判斷。</span></div><nav aria-label="補充資訊"><a href="xiaoma-reading.html">原創閱讀</a><a href="knowledge-atlas.html">臨床問題地圖</a></nav></footer>
</main>
<script src="site-index.js"></script><script src="app.js" defer></script>
</body></html>'''
