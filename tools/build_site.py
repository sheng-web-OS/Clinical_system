import json, html, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
units=json.loads((ROOT/'knowledge/catalog.json').read_text())['units']
out=ROOT/'dist';out.mkdir(exist_ok=True)
css='body{font:18px/1.75 system-ui;max-width:850px;margin:auto;padding:24px;color:#192b35;background:#fafcfd}nav a{margin-right:1rem}article{margin-top:3rem}h1,h2{line-height:1.3}a{color:#086d83}p{margin:1em 0}header{border-bottom:1px solid #ccd}footer{margin-top:4rem;color:#687}'
(out/'style.css').write_text(css)
def render(md):
    chunks=[]
    for line in md.splitlines():
        if line.startswith('# '): chunks.append('<h1>'+html.escape(line[2:])+'</h1>')
        elif line.startswith('## '): chunks.append('<h2>'+html.escape(line[3:])+'</h2>')
        elif line.strip():
            s=html.escape(line)
            s=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
            s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
            chunks.append('<p>'+s+'</p>')
    return '\n'.join(chunks)
nav=' '.join(f'<a href="{u["id"]}.html">{html.escape(u["title"])}</a>' for u in units if u['status']=='published')
for u in units:
    if u['status']!='published':continue
    content=(ROOT/u['file']).read_text()
    page=f'<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(u["title"])}</title><link rel="stylesheet" href="style.css"><header><nav>{nav}</nav></header><article>{render(content)}</article><footer>Clinical Knowledge OS · versioned source, not clinical advice</footer></html>'
    (out/f'{u["id"]}.html').write_text(page)
(out/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=overview.html"><a href="overview.html">Enter site</a>')
print('Built',len(list(out.glob('*.html'))),'HTML pages')
