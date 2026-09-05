#!/usr/bin/env python3
"""REPORT.md → docs/index.html(中文),REPORT.en.md → docs/en/index.html(英文);自包含页面,含自动目录与语言切换。
用法:python3 tools/build_site.py"""
import re, sys, html as H, datetime
from pathlib import Path
import markdown
ROOT = Path(__file__).resolve().parent.parent
DATA_AS_OF = '2026-09-04 22:30 UTC'   # 数据截至(每周刷新时改这里)

LANG = {
    'zh': dict(
        src='REPORT.md', out='docs/index.html', html_lang='zh-CN', url='https://ronfi.github.io/cex-reserves/',
        title='头部交易所储备核查 · CEX Reserves(链上直读 + 官方 PoR 对照)', og_title='头部交易所储备核查 · CEX Reserves', og_image='https://ronfi.github.io/cex-reserves/og.png', keywords='交易所储备核查, 储备证明, Proof of Reserves, PoR, 链上直读, 交易所储备, Binance, OKX, HTX, Bitfinex, DefiLlama, 加密货币交易所, 储备率',
        desc='头部加密交易所储备的链上核查:公布地址的 BTC/ETH/Tron 直读、官方 PoR 页面对照、聚合器口径规则;各所异常按同一读法标出并附核验方法。全部数字可用仓库脚本复现。',
        og='读链,不读公告。前 20 名交易所的链上储备核查,每个数字可复现。',
        update='每周一 00:00 UTC(北京时间 08:00)更新', asof='数据截至', repro='复现', source='源码与数据',
        switch='<span class="on" lang="zh-CN">中文</span><a href="en/" hreflang="en" lang="en">English</a>', toc='目录',
        legend=[('<span class="ok">绿</span>', '与聚合器对上(规则见各表标题)'), ('<mark class="r">红</mark>', '超过各表标题声明的阈值'), ('<mark class="n">黄 *</mark>', '口径差,表下有注')],
        kv_head='项', support='打赏 / Support',
        support_note='这个项目会长期免费、公开地维护下去。如果这些核对帮您省下了自己动手核一遍的时间,那就是它存在的意义。您的支持是本项目持续维护的动力,无论金额大小,都衷心感谢。请只使用 <a href="https://github.com/ronfi/cex-reserves/blob/main/DONATE.md">DONATE.md(main 分支)</a>中的地址;在其他任何地方看到的地址,无论看起来多像,都不要使用。',
        copy='点击复制', qr='展开二维码', built='页面生成', license='内容 CC BY-NC-ND 4.0 · 脚本 MIT', archive='历次版本存档', archive_href='archive/', pv='本页访问 <span id="busuanzi_value_page_pv"></span> 次(计数由第三方脚本 busuanzi 提供)', archnote='这是 {d} 的存档版本,数据与文字停留在当时;最新版见',
        donate_desc={'evm': 'ETH / L2 / BSC · ETH/USDC/USDT', 'tron': 'USDT-TRC20', 'sol': 'SOL / SPL', 'btc-segwit': 'Native SegWit(推荐)', 'btc-legacy': '兼容旧钱包'},
    ),
    'en': dict(
        src='REPORT.en.md', out='docs/en/index.html', html_lang='en', url='https://ronfi.github.io/cex-reserves/en/',
        title='Top Exchange Reserves Check · CEX Reserves (on-chain reads + official PoR)', og_title='Top Exchange Reserves Check · CEX Reserves', og_image='https://ronfi.github.io/cex-reserves/og-en.png', keywords='exchange reserves, proof of reserves, PoR, on-chain verification, crypto exchange reserves, Binance, OKX, HTX, Bitfinex, DefiLlama, reserve ratio',
        desc='On-chain verification of top crypto exchange reserves: direct BTC/ETH/Tron reads of published addresses, official PoR pages side by side, aggregator caliber rules; anomalies flagged by one uniform reading with verification methods. Every number reproducible with the repository scripts.',
        og='Read the chain, not the announcement. On-chain reserve check of the top 20 exchanges, every number reproducible.',
        update='Updated every Monday 00:00 UTC', asof='Data as of', repro='Reproduce', source='Source and data',
        switch='<a href="../" hreflang="zh-CN" lang="zh-CN">中文</a><span class="on" lang="en">English</span>', toc='Contents',
        legend=[('<span class="ok">green</span>', 'reconciles with the aggregator (rule in each table heading)'), ('<mark class="r">red</mark>', 'above the threshold stated in the table heading'), ('<mark class="n">yellow *</mark>', 'caliber difference, note under the table')],
        kv_head='Item', support='Support',
        support_note='This project will stay free and public for the long run. If these checks ever saved you the work of verifying it yourself, that is what it is for. Your support keeps it maintained; any amount is sincerely appreciated. Use only the addresses in <a href="https://github.com/ronfi/cex-reserves/blob/main/DONATE.md">DONATE.md on the main branch</a>; do not use any address you see anywhere else, however similar it looks.',
        copy='click to copy', qr='show QR code', built='Page built', license='Content CC BY-NC-ND 4.0 · scripts MIT', archive='Version archive', archive_href='../archive/', pv='<span id="busuanzi_value_page_pv"></span> page views (counted by the third-party busuanzi script)', archnote='This is the archived {d} edition; data and text are as of then. Latest:',
        donate_desc={'evm': 'ETH / L2 / BSC · ETH/USDC/USDT', 'tron': 'USDT-TRC20', 'sol': 'SOL / SPL', 'btc-segwit': 'Native SegWit (recommended)', 'btc-legacy': 'legacy wallets'},
    ),
}

CSS = """
:root{--paper:#F5F7F4;--paper2:#EDF1EC;--ink:#14201B;--ink2:#5E6B66;--rule:#D6DDD8;--stamp:#1D4E89;--red:#B42318;--redbg:#FBE9E7;--green:#1E7F4F;--greenbg:#E6F4EC;--code:#E9EEE9;--mark:#FFF3C4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#121715;--paper2:#181F1C;--ink:#E7ECE8;--ink2:#9FAAA4;--rule:#2B3531;--stamp:#8DB4E2;--red:#FF8E85;--redbg:#3D1A17;--green:#7BD3A3;--greenbg:#173324;--code:#1E2623;--mark:#4A3F12}}
:root[data-theme="dark"]{--paper:#121715;--paper2:#181F1C;--ink:#E7ECE8;--ink2:#9FAAA4;--rule:#2B3531;--stamp:#8DB4E2;--red:#FF8E85;--redbg:#3D1A17;--green:#7BD3A3;--greenbg:#173324;--code:#1E2623;--mark:#4A3F12}
*{box-sizing:border-box}html{scroll-behavior:smooth}@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);font:15.5px/1.72 "Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;font-variant-numeric:tabular-nums}
html[lang=en] body{font-family:"Noto Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--stamp);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--stamp) 35%,transparent)}a:hover{border-bottom-color:var(--stamp)}a:focus-visible{outline:2px solid var(--stamp);outline-offset:2px}
.mast{border-bottom:1px solid var(--rule);background:var(--paper2)}
.mast-in{max-width:1180px;margin:0 auto;padding:22px 24px;display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center}.mast .meta{flex-basis:100%}
.mast h1{font:600 26px/1.25 "Noto Serif SC","Songti SC","SimSun",serif;margin:0;letter-spacing:.2px;text-wrap:balance}
html[lang=en] .mast h1,html[lang=en] h2{font-family:"Noto Serif",Georgia,"Times New Roman",serif}
.mast .meta{color:var(--ink2);font-size:13px;display:flex;gap:18px;flex-wrap:wrap;align-items:baseline}
.mast .lang{margin-left:auto;display:inline-flex;border:1px solid var(--rule);border-radius:6px;overflow:hidden;background:var(--paper);font-size:13px;line-height:1}.mast .lang a,.mast .lang span{padding:7px 12px;border:0;font-weight:600;color:var(--ink2)}.mast .lang a:hover{color:var(--stamp);background:var(--paper2)}.mast .lang .on{background:var(--stamp);color:#fff}
.mast code{font:12.5px/1.4 "JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;background:var(--code);padding:2px 7px;border-radius:4px}
.wrap{max-width:1180px;margin:0 auto;padding:26px 24px 70px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:40px}
nav.toc{position:sticky;top:18px;align-self:start;font-size:13px;line-height:1.5}
nav.toc .lbl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);margin-bottom:8px}
nav.toc ol{list-style:none;margin:0;padding:0;border-left:1px solid var(--rule)}nav.toc li a{display:block;padding:4px 0 4px 12px;color:var(--ink2);border:0;margin-left:-1px;border-left:2px solid transparent}nav.toc li a:hover{color:var(--ink);border-left-color:var(--stamp)}
.legend{margin-top:22px;padding-top:14px;border-top:1px solid var(--rule);color:var(--ink2);font-size:12.5px;display:grid;gap:6px}
.legend span{display:inline-block;padding:0 6px;border-radius:3px;margin-right:6px}
main{min-width:0}
main>blockquote:first-child{margin:0 0 26px;padding:14px 18px;border-left:3px solid var(--stamp);background:var(--paper2);color:var(--ink2);font-size:14px}
main>blockquote:first-child p{margin:.35em 0}
h2{font:600 21px/1.35 "Noto Serif SC","Songti SC","SimSun",serif;margin:2.2em 0 .7em;padding-top:.6em;border-top:1px solid var(--rule);text-wrap:balance;scroll-margin-top:16px}
h2:first-of-type{border-top:0;padding-top:0;margin-top:.2em}
h3{font:600 16px/1.4 "Noto Sans SC",sans-serif;margin:1.6em 0 .5em;color:var(--ink)}html[lang=en] h3{font-family:inherit}
p,li{max-width:none}main p{margin:.6em 0}ol,ul{padding-left:1.4em}li{margin:.28em 0}li::marker{color:var(--ink2)}
blockquote{margin:1em 0;padding:10px 16px;border-left:3px solid var(--rule);background:var(--paper2);color:var(--ink)}blockquote p{margin:.35em 0}
.tbl{overflow-x:auto;margin:.8em 0 1.4em;border:1px solid var(--rule);border-radius:4px;background:var(--paper2)}
table{border-collapse:collapse;width:100%;font-size:13.5px;line-height:1.5}table.kv th:first-child,table.kv td:first-child{white-space:nowrap;width:1%}
th{font-weight:600;color:var(--ink2);font-size:12.5px;letter-spacing:.02em;text-align:left;background:var(--paper2);border-bottom:1px solid var(--rule);padding:9px 10px;white-space:nowrap}
html[lang=en] th{white-space:normal;line-height:1.3;font-size:12px}html[lang=en] table{font-size:13px}html[lang=en] td{padding:7px 8px}html[lang=en] th{padding:8px 8px}
td{padding:8px 10px;border-top:1px solid var(--rule);vertical-align:top;background:var(--paper)}
mark.r{background:var(--redbg);color:var(--red);padding:1px 5px;border-radius:3px;font-weight:600}mark.n{background:var(--mark);color:inherit;padding:1px 5px;border-radius:3px;font-weight:600}
mark{background:var(--mark);color:inherit}
details.fold{border:1px solid var(--rule);border-radius:6px;background:var(--paper2);margin:40px 0 0}
details.fold>summary{padding:12px 16px;cursor:pointer;color:var(--stamp);font-weight:600;list-style:none}
details.fold>summary::before{content:"▸ ";color:var(--ink2)}details.fold[open]>summary::before{content:"▾ "}
.foldbody{padding:4px 16px 16px}.foldbody p.note{color:var(--ink2);font-size:13px;line-height:1.7;margin:6px 0 12px}
.donate{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.dcard{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:12px;min-width:0}
.dcard b{font-size:13.5px}.dcard span{color:var(--ink2);font-size:12px;margin-left:8px}
.dcard code{display:block;margin-top:6px;font-size:11.5px;word-break:break-all;color:var(--stamp);cursor:pointer;background:none;padding:0}
.dqr summary{color:var(--ink2);font-size:12px;cursor:pointer;margin-top:8px;list-style:none}.dqr summary::before{content:"▸ "}.dqr[open] summary::before{content:"▾ "}
.dqr svg{display:block;margin-top:8px;width:148px;height:148px}
.ok{color:var(--green);background:var(--greenbg);padding:0 5px;border-radius:3px;font-weight:600}
code{font:12.5px/1.5 "JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;background:var(--code);padding:1px 5px;border-radius:3px}
pre{background:var(--code);padding:12px 14px;border-radius:5px;overflow-x:auto;font-size:12.5px;line-height:1.6}pre code{background:none;padding:0}
hr{border:0;border-top:1px solid var(--rule);margin:2em 0}
footer{grid-column:1/-1;margin-top:34px;padding-top:14px;border-top:1px solid var(--rule);color:var(--ink2);font-size:12.5px;display:flex;flex-wrap:wrap;gap:8px 22px}
@media (max-width:900px){.wrap{grid-template-columns:1fr;gap:18px}nav.toc{position:static}nav.toc ol{display:flex;flex-wrap:wrap;gap:4px 14px;border:0}nav.toc li a{padding:2px 0;border:0}.legend{display:none}}
"""

DONATE = [  # 与 DONATE.md(main 分支,唯一权威源)逐字一致
    ('EVM', '0xcd98738afada22ace19830f2e7bcd1dee89f6869', 'evm'),
    ('TRON', 'TSjurosohn1psMKg5xV4L2ELCiLJTzcPMD', 'tron'),
    ('Solana', '6LWiGPToGAjgYVwsYgqv5QAKfGm38jnhyDALbZYK3weC', 'sol'),
    ('Bitcoin', 'bc1qtpxutlz9ttve7z7mnvt87w95njeejmeallvwyg', 'btc-segwit'),
    ('Bitcoin · Legacy', '132v6ZpuZEFVCrkoRbUfKGCBayy31gWZnj', 'btc-legacy'),
]
donate_md = (ROOT / 'DONATE.md').read_text(encoding='utf8')
for _, addr, _q in DONATE:
    assert addr in donate_md, f'地址不在 DONATE.md:{addr}'

def _qr(name):
    f = ROOT / 'assets' / 'qr' / f'{name}.svg'
    return f.read_text(encoding='utf8') if f.exists() else ''

FONTS = {'zh': 'family=Noto+Serif+SC:wght@600&family=Noto+Sans+SC:wght@400;600', 'en': 'family=Noto+Serif:wght@600&family=Noto+Sans:wght@400;600'}

def build(lang):
    T = LANG[lang]
    md = (ROOT / T['src']).read_text(encoding='utf8')
    lines = md.split('\n'); title = lines[0].lstrip('# ').strip()
    body = markdown.markdown('\n'.join(lines[1:]), extensions=['tables', 'fenced_code', 'toc'],
                             extension_configs={'toc': {'toc_depth': '2', 'slugify': lambda v, s: re.sub(r'[^\w一-鿿]+', '-', v).strip('-').lower()}})
    body = re.sub(r'<table>(\s*<thead>\s*<tr>\s*<th>' + re.escape(T['kv_head']) + r'</th>)', r'<table class="kv">\1', body)  # 键值表首列不换行
    toc = [f'<li><a href="#{m.group(1)}">{re.sub(r"<[^>]+>", "", m.group(2))}</a></li>' for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body)]
    # 不按交易所名染色;红/绿只由正文里按统一规则写下的 <mark class="r"> / <span class="ok"> 决定;表格包一层可横滚容器
    body = re.sub(r'<table( class="kv")?>', r'<div class="tbl"><table\1>', body).replace('</table>', '</table></div>')
    donate_html = ''.join(
        f'<div class="dcard"><b>{net}</b><span>{T["donate_desc"][q]}</span>'
        f'<code onclick="navigator.clipboard&&navigator.clipboard.writeText(this.textContent)" title="{T["copy"]}">{addr}</code>'
        f'<details class="dqr"><summary>{T["qr"]}</summary>{_qr(q)}</details></div>' for net, addr, q in DONATE)
    support_html = (f'<details class="fold"><summary>{T["support"]}</summary><div class="foldbody">'
                    f'<p class="note">{T["support_note"]}</p><div class="donate">{donate_html}</div></div></details>')
    legend = ''.join(f'<div>{k}{v}</div>' for k, v in T['legend'])
    built = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    other = LANG['en' if lang == 'zh' else 'zh']; archived = False
    import json as _json
    jsonld = _json.dumps({'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', 'name': 'CEX Reserves', 'url': LANG['zh']['url'], 'inLanguage': ['zh-CN', 'en']},
        {'@type': 'Dataset', 'name': T['og_title'], 'description': T['desc'], 'url': T['url'], 'inLanguage': T['html_lang'], 'license': 'https://creativecommons.org/licenses/by-nc-nd/4.0/', 'isAccessibleForFree': True,
         'dateModified': DATA_AS_OF[:10], 'keywords': [k.strip() for k in T['keywords'].split(',')], 'creator': {'@type': 'Organization', 'name': 'CEX Reserves', 'url': 'https://github.com/ronfi/cex-reserves'},
         'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'application/json', 'contentUrl': 'https://github.com/ronfi/cex-reserves/tree/main/data'}],
         'sameAs': 'https://github.com/ronfi/cex-reserves'}]}, ensure_ascii=False)
    html = f"""<!DOCTYPE html><html lang="{T['html_lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(T['title'])}</title>
<meta name="description" content="{H.escape(T['desc'])}">
<meta name="robots" content="{'noindex,follow' if archived else 'index,follow,max-image-preview:large'}"><meta name="keywords" content="{H.escape(T['keywords'])}">
<link rel="canonical" href="{T['url']}"><link rel="alternate" hreflang="{T['html_lang']}" href="{T['url']}"><link rel="alternate" hreflang="{other['html_lang']}" href="{other['url']}"><link rel="alternate" hreflang="x-default" href="{LANG['zh']['url']}"><link rel="alternate" type="application/rss+xml" title="CEX Reserves versions" href="https://ronfi.github.io/cex-reserves/feed.xml">
<meta property="og:type" content="article"><meta property="og:site_name" content="CEX Reserves"><meta property="og:locale" content="{'zh_CN' if lang == 'zh' else 'en_US'}"><meta property="og:title" content="{H.escape(T['og_title'])}"><meta property="og:description" content="{H.escape(T['og'])}"><meta property="og:url" content="{T['url']}"><meta property="og:image" content="{T['og_image']}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="article:modified_time" content="{DATA_AS_OF[:10]}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{H.escape(T['og_title'])}"><meta name="twitter:description" content="{H.escape(T['og'])}"><meta name="twitter:image" content="{T['og_image']}">
<script type="application/ld+json">{jsonld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[lang]}&family=JetBrains+Mono:wght@400;500&display=swap">
<style>{CSS}</style></head><body>
<header class="mast"><div class="mast-in"><h1>{H.escape(title)}</h1><nav class="lang" aria-label="language">{T['switch']}</nav><div class="meta"><span>{T['asof']} {DATA_AS_OF}</span><span>{T['update']}</span><span>{T['repro']} <code>python3 tools/cex_reserves_verify.py --chain all</code></span><span><a href="https://github.com/ronfi/cex-reserves">{T['source']}</a></span></div></div></header>
<div class="wrap">
<nav class="toc" aria-label="{T['toc']}"><div class="lbl">{T['toc']}</div><ol>{''.join(toc)}</ol>
<div class="legend">{legend}</div></nav>
<main>
{body}
{support_html}
</main>
<footer><span>{T['source']}: <a href="https://github.com/ronfi/cex-reserves">github.com/ronfi/cex-reserves</a></span><span><a href="{T['archive_href']}">{T['archive']}</a></span><span>{T['built']} {built}</span><span>{T['license']}</span><span id="busuanzi_container_page_pv" style="display:none">{T['pv']}</span></footer>
</div><script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script></body></html>"""
    out = ROOT / T['out']; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html, encoding='utf8')
    if '--archive' in sys.argv:
        d = DATA_AS_OF[:10]; arch = ROOT / 'docs' / 'archive'; arch.mkdir(exist_ok=True)
        note = f'<div class="archnote">{T["archnote"].format(d=d)} <a href="{LANG["zh"]["url"] if lang == "zh" else LANG["en"]["url"]}">{LANG["zh"]["url"] if lang == "zh" else LANG["en"]["url"]}</a> · <a href="./">{T["archive"]}</a></div>'
        a = html.replace('href="en/"', f'href="{LANG["en"]["url"]}"').replace('href="../"', f'href="{LANG["zh"]["url"]}"').replace(f'href="{T["archive_href"]}"', 'href="./"')
        a = a.replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex,follow">', 1)
        a = a.replace('<body>', '<body>' + note, 1).replace('</style>', '.archnote{background:var(--mark);color:var(--ink);padding:10px 24px;font-size:13px}</style>', 1)
        (arch / (f'{d}.html' if lang == 'zh' else f'{d}.en.html')).write_text(a, encoding='utf8')
    print(lang, 'built', len(html), 'bytes; toc', len(toc), '; tables', html.count('<table'), '; wrapped', html.count('<div class="tbl"><table'), '; ok', html.count('class="ok"'), '; red', html.count('mark class="r"'))

for lang in LANG:
    build(lang)
if '--archive' in sys.argv:  # 存档目录页(中英同页)
    arch = ROOT / 'docs' / 'archive'
    dates = sorted({f.name[:10] for f in arch.glob('????-??-??*.html')}, reverse=True)
    items = ''.join(f'<li><span class="d">{d}</span> <a href="{d}.html">中文</a> · <a href="{d}.en.html">English</a></li>' for d in dates)
    (arch / 'index.html').write_text(f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CEX Reserves · 历次版本存档 / Version archive</title>
<style>{CSS}.arch{{max-width:760px;margin:0 auto;padding:30px 24px}}.arch li{{margin:.5em 0}}.arch .d{{font-family:"JetBrains Mono",ui-monospace,monospace;margin-right:10px}}</style></head><body>
<div class="arch"><h2>历次版本存档 / Version archive</h2><p>不回改的可信度 = 旧版本的可访问性。每周更新时存一份当时的页面,数据与文字停留在当时。<br>Credibility without retroactive edits = old versions stay reachable. A copy of the page is archived at each weekly update, with the data and text as of then.</p><ul>{items}</ul><p><a href="{LANG['zh']['url']}">← 最新版 / Latest</a></p></div></body></html>""", encoding='utf8')
    print('archive', dates)
(ROOT / 'docs' / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://ronfi.github.io/cex-reserves/sitemap.xml\n')
_lm = DATA_AS_OF[:10]
(ROOT / 'docs' / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
    + ''.join(f'<url><loc>{LANG[l]["url"]}</loc><lastmod>{_lm}</lastmod><changefreq>weekly</changefreq><priority>{"1.0" if l == "zh" else "0.9"}</priority>'
              + ''.join(f'<xhtml:link rel="alternate" hreflang="{LANG[m]["html_lang"]}" href="{LANG[m]["url"]}"/>' for m in LANG) + '</url>' for l in LANG)
    + '<url><loc>https://ronfi.github.io/cex-reserves/archive/</loc><changefreq>weekly</changefreq><priority>0.3</priority></url></urlset>')
# RSS:每期存档一条
_arch = sorted({f.name[:10] for f in (ROOT / 'docs' / 'archive').glob('????-??-??.html')}, reverse=True) if (ROOT / 'docs' / 'archive').exists() else []
_items = ''.join(f'<item><title>CEX Reserves · 数据截至 {d}</title><link>https://ronfi.github.io/cex-reserves/archive/{d}.html</link><guid>https://ronfi.github.io/cex-reserves/archive/{d}.html</guid><pubDate>{datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate><description>头部交易所储备核查,数据截至 {d};最新版 https://ronfi.github.io/cex-reserves/</description></item>' for d in _arch)
(ROOT / 'docs' / 'feed.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>CEX Reserves · 头部交易所储备核查</title><link>https://ronfi.github.io/cex-reserves/</link><description>每周更新的头部交易所储备链上核查;每期存档一条。</description><language>zh-CN</language>{_items}</channel></rss>', encoding='utf8')
