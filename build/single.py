"""Builds ONE self-contained index.html (CSS, JS, all pages and all images embedded).
Run from the site folder:  python3 build/single.py
"""
import os, re, io, json, base64, tempfile, subprocess, sys
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
tmp = tempfile.mkdtemp()
subprocess.check_call([sys.executable, os.path.join(ROOT, "build", "pages.py"), tmp])
css = open(os.path.join(ROOT, "style.css")).read()
PAGES = {"index":"home","club":"club","fixtures":"fixtures","team":"team","season":"season","misty-game":"misty-game","medics-match":"medics-match","rhino-cup":"rhino-cup","gallery":"gallery","join":"join"}
titles = {}
views, header = [], ""
imgs = {}
def enc(path):
    full = os.path.join(ROOT, path)
    im = Image.open(full).convert("RGB")
    w = 640 if path.endswith("logo.png") else 1400
    if im.width > w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=72, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
for fn, vid in PAGES.items():
    h = open(os.path.join(tmp, fn + ".html")).read()
    titles[vid] = re.search(r"<title>(.*?)</title>", h).group(1)
    if fn == "index": header = re.search(r"<header>.*?</header>", h, re.S).group(0)
    body = h.split("</header>", 1)[1].split('<script src="site.js">')[0]
    body = re.sub(r"<footer>.*?</footer>", "", body, flags=re.S)
    body = body.replace(' loading="lazy"', "")
    body = re.sub(r'href="([a-z-]+)\.html"', lambda m: 'href="#%s"' % PAGES.get(m.group(1), m.group(1)), body)
    for p in re.findall(r'src="(assets/[^"]+)"', body): imgs[p] = None
    body = re.sub(r'src="(assets/[^"]+)"', r'data-src="\1"', body)
    views.append('<main class="view" id="v-%s" hidden>%s</main>' % (vid, body))
header = re.sub(r'href="([a-z-]+)\.html"', lambda m: 'href="#%s"' % PAGES.get(m.group(1), m.group(1)), header)
header = header.replace('class=cur', '').replace('src="assets/logo.png"', 'data-src="assets/logo.png"')
header = header.replace('href="#home"', 'href="#home"')
imgs["assets/logo.png"] = None
_b = json.load(open(os.path.join(ROOT, "build", "bios.json"), encoding="utf-8"))
for _x in _b:
    if _x.get("photo") and os.path.exists(os.path.join(ROOT, _x["photo"])): imgs[_x["photo"]] = None
    else: _x["photo"] = None
for p in imgs: imgs[p] = enc(p)
bios = _b
modal = '<div class="bio-bg" id="bioBg" hidden><div class="bio" id="bioDlg" role="dialog" aria-modal="true" aria-labelledby="bioName" aria-describedby="bioBody" tabindex="-1"><div class="bio-head"><div class="bio-ph" id="bioPh"></div><div class="bio-id"><h2 id="bioName"></h2><div class="sub" id="bioSub"></div></div><button type="button" class="bio-x" id="bioX" aria-label="Close biography">\u00d7</button></div><div class="bio-body" id="bioBody"></div><div class="bio-nav"><button type="button" id="bioPrev"></button><button type="button" id="bioNext"></button></div></div></div>'
footer = '<footer><div class="wrap"><span><b style="color:var(--cream)">The Sticky Wickets Cricket Club</b> · Tigoni, Kenya</span><span>Adhaerere Maneat</span></div></footer>'
js = r'''
const IMG=%s, TITLES=%s, BIOS=%s;
document.querySelectorAll('[data-src]').forEach(i=>i.src=IMG[i.dataset.src]);
const fav=document.createElement('link');fav.rel='icon';fav.href=IMG['assets/logo.png'];document.head.appendChild(fav);
const hd=document.querySelector('header');
const sc=()=>hd.classList.toggle('scrolled',scrollY>40);addEventListener('scroll',sc);
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
function route(){
  let id=(location.hash||'#home').slice(1); if(!TITLES[id]) id='home';
  document.querySelectorAll('.view').forEach(v=>v.hidden=v.id!=='v-'+id);
  document.title=TITLES[id];
  const cur=({'misty-game':'season','medics-match':'season','rhino-cup':'season'})[id]||id;
  document.querySelectorAll('#menu a').forEach(a=>a.classList.toggle('cur',a.getAttribute('href')==='#'+cur));
  document.getElementById('menu').classList.remove('open');
  scrollTo(0,0);sc();
  setTimeout(()=>document.querySelectorAll('#v-'+id+' .reveal').forEach(e=>e.classList.add('in')),250);
}
addEventListener('hashchange',route);route();
const lb=document.getElementById('lb');
document.querySelectorAll('.gallery a').forEach(a=>a.onclick=e=>{e.preventDefault();lb.querySelector('img').src=a.querySelector('img').src;lb.classList.add('on')});
lb.onclick=()=>lb.classList.remove('on');
lb.onclick=()=>lb.classList.remove('on');
const bg=document.getElementById('bioBg'),dlg=document.getElementById('bioDlg');
let bi=0,lastBtn=null;const IDS=BIOS.map(b=>b.id);
const FOC='button:not([disabled]),[href],[tabindex]:not([tabindex="-1"])';
function fillBio(i){bi=(i+BIOS.length)%%BIOS.length;const b=BIOS[bi];
  document.getElementById('bioName').textContent=b.name+(b.tag?' ('+b.tag+')':'');document.getElementById('bioSub').textContent=b.subtitle;
  const ph=document.getElementById('bioPh');ph.innerHTML='';const sp=document.createElement('span');sp.textContent=b.initials;ph.appendChild(sp);
  if(b.photo&&IMG[b.photo]){const im=new Image();im.alt=b.name;im.onerror=()=>im.remove();im.src=IMG[b.photo];ph.appendChild(im)}
  const body=document.getElementById('bioBody');body.innerHTML='';b.paras.forEach(t=>{const p=document.createElement('p');p.textContent=t;body.appendChild(p)});
  const pv=BIOS[(bi-1+BIOS.length)%%BIOS.length],nx=BIOS[(bi+1)%%BIOS.length];
  document.getElementById('bioPrev').textContent='\u2190 '+pv.name;document.getElementById('bioNext').textContent=nx.name+' \u2192';
  body.scrollTop=0}
function showBio(i,btn){if(btn)lastBtn=btn;fillBio(i);if(bg.hidden){bg.hidden=false;document.body.style.overflow='hidden'}document.getElementById('bioX').focus()}
function hideBio(){if(bg.hidden)return;bg.hidden=true;document.body.style.overflow='';if(lastBtn&&document.contains(lastBtn))lastBtn.focus()}
document.querySelectorAll('[data-bio]').forEach(el=>el.addEventListener('click',()=>showBio(IDS.indexOf(el.dataset.bio),el)));
document.getElementById('bioX').onclick=hideBio;
let downOnBg=false;bg.addEventListener('mousedown',e=>{downOnBg=e.target===bg});bg.addEventListener('click',e=>{if(e.target===bg&&downOnBg)hideBio();downOnBg=false});
document.getElementById('bioPrev').onclick=()=>showBio(bi-1);document.getElementById('bioNext').onclick=()=>showBio(bi+1);
addEventListener('keydown',e=>{if(bg.hidden)return;
  if(e.key==='Escape'){e.preventDefault();hideBio();return}
  if(e.key==='ArrowLeft'&&!e.target.closest('input,textarea')){showBio(bi-1);return}
  if(e.key==='ArrowRight'&&!e.target.closest('input,textarea')){showBio(bi+1);return}
  if(e.key==='Tab'){const f=[...dlg.querySelectorAll(FOC)].filter(x=>x.offsetParent!==null);if(!f.length)return;
    const first=f[0],last=f[f.length-1];
    if(e.shiftKey&&(document.activeElement===first||document.activeElement===dlg)){e.preventDefault();last.focus()}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}
    else if(!dlg.contains(document.activeElement)){e.preventDefault();first.focus()}}});
addEventListener('keydown',e=>e.key==='Escape'&&lb.classList.remove('on'));
''' % (json.dumps(imgs), json.dumps(titles), json.dumps(bios, ensure_ascii=False))
html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Sticky Wickets Cricket Club</title>
<meta name="description" content="Cricket, friendship and tradition in the Kenyan highlands. The Sticky Wickets Cricket Club, Tigoni.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>%s
.view[hidden]{display:none}</style></head><body>
%s
%s
%s
%s<div class="lb" id="lb"><img alt=""></div>
<script>%s</script></body></html>''' % (css, header, "\n".join(views), footer, modal, js)
html = html.replace('<div class="lb" id="lb"><img alt=""></div>', '', html.count('<div class="lb" id="lb"><img alt=""></div>') - 1) if html.count('id="lb"') > 1 else html
open(os.path.join(ROOT, "index.html"), "w").write(html)
print("index.html", round(len(html)/1e6, 2), "MB")
