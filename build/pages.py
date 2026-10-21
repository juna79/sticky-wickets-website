import os, sys
OUT = sys.argv[1]
NAV = [("club.html","The Club"),("fixtures.html","Fixtures"),("season.html","Season 2026"),("team.html","The Team"),("gallery.html","Gallery"),("join.html","Join")]
import json
BIOS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"bios.json"),encoding="utf-8"))
_o = {"Felix Rigg","Tony Clegg Butt","Annick Deridder"}
_first = ["Jezza Cordingley","Angus Miller"]
_ord = [x for n in _first for x in BIOS if x["name"]==n] + [x for x in BIOS if x["name"] not in _first and x["name"] not in _o]
SQUAD = [(x["name"],x["role"],1 if x["name"] in _first else 0) for x in _ord]
OFFICIALS = [(x["name"],x["role"]) for x in BIOS if x["name"] in _o]

def head(title, cur=""):
    items = "".join(f'<li><a href="{h}"{" class=cur" if h==cur else ""}>{n}</a></li>' for h,n in NAV)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — The Sticky Wickets Cricket Club</title>
<meta name="description" content="Cricket, friendship and tradition in the Kenyan highlands. The Sticky Wickets Cricket Club, Tigoni.">
<link rel="icon" href="assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head><body>
<header><div class="wrap nav"><a class="brand" href="index.html"><img src="assets/logo.png" alt="Sticky Wickets crest"><span>Sticky Wickets</span></a>
<nav><ul id="menu">{items}<li><a href="fixtures.html" class="btn solid" style="padding:9px 20px;color:#fff">Next match</a></li></ul></nav>
<button class="burger" aria-label="Menu" onclick="document.getElementById('menu').classList.toggle('open')">☰</button></div></header>
'''
FOOT = '''<section class="join" style="padding:80px 0"><div class="wrap"><img src="assets/logo.png" alt="" style="border-radius:50%;width:110px"><h2 style="font-size:2.4rem">Fancy a game?</h2><p>Whether you bat, bowl, or just bring excellent snacks — there's a place at the Tigoni pavilion.</p><a class="btn solid" href="join.html">Join the Stickies</a></div></section>
<footer><div class="wrap"><span><b style="color:var(--cream)">The Sticky Wickets Cricket Club</b> · Tigoni, Kenya</span><span>Adhaerere Maneat</span></div></footer>
<script src="site.js"></script></body></html>'''
FOOT_NOJOIN = FOOT

def hero(eyebrow, title, sub, img=None, crumbs=""):
    c = f'<div class="crumbs">{crumbs}</div>' if crumbs else ''
    i = f'<img src="{img}" alt="">' if img else ''
    return f'<div class="page-hero{" img" if img else ""}">{i}<div class="wrap">{c}<span class="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{sub}</p></div></div>'

def write(name, html):
    open(os.path.join(OUT,name),"w").write(html)

def player_card(n,r,cap=0):
    ini="".join(w[0] for w in n.split()[:2])
    return f'<button type="button" class="player{" cap" if cap else ""}" data-bio="{n}" aria-label="Read the bio of {n}"><div class="photo"><span class="ini">{ini}</span></div><div class="info"><h3>{n}</h3><div class="role">{r}</div><span class="rd">Read bio →</span></div></button>'

NEXT = '<div class="date"><b>31</b><span>Oct</span></div><div><div class="vs">Sticky Wickets v Mutaiga Country Club</div><div class="sub">Saturday 31 October 2026 · Limuru Grounds · Start time TBC</div></div><span class="tag">Upcoming</span>'
PAST = '''<a class="match" href="medics-match.html"><div class="date"><b>2026</b><span>Season</span></div><div><div class="vs">Sticky Wickets v The Medics</div><div class="sub">Tigoni · A clinical performance in glorious sunshine</div></div><span class="tag win">Match report →</span></a>
<a class="match" href="misty-game.html"><div class="date"><b>11</b><span>Jul</span></div><div><div class="vs">Sticky Wickets in the Mist</div><div class="sub">Tigoni · Visibility optional, appeals compulsory</div></div><span class="tag win">Match report →</span></a>
<a class="match" href="rhino-cup.html"><div class="date"><b>Jun</b><span>2026</span></div><div><div class="vs">The Rhino Cup</div><div class="sub">Club tour · Nanyuki</div></div><span class="tag win">Tour story →</span></a>'''

def story(href,img,eb,t,p,more):
    return f'<a class="story" href="{href}"><img src="{img}" alt="" loading="lazy"><div><span class="eyebrow">{eb}</span><h3>{t}</h3><p>{p}</p><span class="more">{more}</span></div></a>'
S_MIST = story("misty-game.html","assets/misty/hero.jpg","Match report · 11 July 2026","Sticky Wickets in the Mist","Visibility became optional, appeals remained compulsory and the pavilion stove emerged as the day's most consistent performer.","Read the match report →")
S_MED = story("medics-match.html","assets/medics/photo-15.jpg","Match report · Season 2026","The Medics Match","A clinical performance, glorious sunshine and excellent company. The Medics brought the precision; the Stickies brought the optimism.","Read the match report →")
S_RHINO = story("rhino-cup.html","assets/rhino/scoreboard-mountain.jpg","First club tour · June 2026","Our First Rhino Cup","Sticky Wickets headed north to Nanyuki for tournament cricket, enormous skies and the beginning of a new tradition.","See the tour story →")

def sec_head(eb,t,right=""):
    return f'<div class="sec-head reveal"><div><span class="eyebrow">{eb}</span><h2>{t}</h2></div>{right}</div>'

# ---------- index
idx = head("Home") + f'''
<div class="hero"><img src="assets/misty/hero.jpg" alt="Morning mist over the Tigoni cricket ground"><img class="logo" src="assets/logo.png" alt="The Sticky Wickets coat of arms">
<div class="wrap"><span class="eyebrow">Our home in Tigoni · Kenya</span><h1>Sticky Wickets <em>Cricket Club</em></h1><p>Cricket, friendship and tradition in the Kenyan highlands.</p>
<div class="cta"><a class="btn solid" href="fixtures.html">Fixtures &amp; results</a><a class="btn ghost" href="club.html">Discover our club →</a></div></div></div>
<div class="strip"><div class="wrap"><div><span class="pill">Next match</span></div><div><b>Sticky Wickets v Mutaiga Country Club</b><div class="meta">Saturday 31 October 2026 · Limuru Grounds</div></div><a class="btn ghost" href="fixtures.html">All fixtures →</a></div></div>
<section><div class="wrap"><div class="about"><div class="reveal"><span class="eyebrow">The club</span><h2>More than a cricket club.</h2>
<p>Sticky Wickets is built around good company, adventurous fixtures and the firm belief that every match deserves a proper story afterwards.</p>
<p>From our home in Tigoni to club tours beneath Mount Kenya, we play for the cricket, the camaraderie and everything that happens between the overs.</p><a class="btn ghost" href="club.html">About the club →</a></div>
<div class="reveal"><img src="assets/rhino/team-spirit.jpg" alt="The Stickies on tour" style="border-radius:var(--r);border:1px solid var(--line)"></div></div></div></section>
<section class="band"><div class="wrap">{sec_head("Season 2026","Latest stories",'<a class="btn ghost" href="season.html">All stories →</a>')}
<div class="stories reveal">{S_MIST}{S_MED}{S_RHINO}</div></div></section>
<section><div class="wrap"><div class="cards3 reveal">
<a class="card" href="fixtures.html"><span class="eyebrow">Fixtures</span><h3>Fixtures &amp; results</h3><p>See the next match and catch up on past reports.</p></a>
<a class="card" href="team.html"><span class="eyebrow">The squad</span><h3>Meet the team</h3><p>The Stickies on and off the field.</p></a>
<a class="card" href="gallery.html"><span class="eyebrow">Club archive</span><h3>Three shades of Sticky</h3><p>Sunny beginnings, the deep mist of Tigoni and the dry gold of Nanyuki.</p></a></div></div></section>
<section style="padding:20px 0 90px"><div class="wrap reveal"><blockquote>“Proper cricket. Questionable judgement. Excellent company.”</blockquote></div></section>
''' + FOOT
write("index.html", idx)

# ---------- club
write("club.html", head("The Club","club.html") + hero("The club","More than a cricket club.","Good company, adventurous fixtures, and the belief that every match deserves a proper story afterwards.","assets/rhino/wide-match.jpg") + f'''
<section><div class="wrap"><div class="about"><div class="reveal"><span class="eyebrow">Who we are</span><h2>Cricket, friendship and tradition.</h2>
<p>Sticky Wickets is built around good company, adventurous fixtures and the firm belief that every match deserves a proper story afterwards.</p>
<p>From our home in Tigoni to club tours beneath Mount Kenya, we play for the cricket, the camaraderie and everything that happens between the overs.</p>
<p style="font-family:'Barlow Condensed','Arial Narrow',sans-serif;font-style:italic;color:var(--gold)">Adhaerere Maneat</p></div>
<div class="stats reveal"><div class="stat"><strong>Tigoni</strong><span>Our home ground</span></div><div class="stat"><strong>1st</strong><span>Rhino Cup tour, Nanyuki</span></div><div class="stat"><strong>3</strong><span>Stories from Season 2026</span></div><div class="stat"><strong>∞</strong><span>Cups of tea at the pavilion</span></div></div></div></div></section>
<section class="band"><div class="wrap">{sec_head("Where we play","From the mist to the mountain")}
<div class="cards3 reveal"><a class="card" href="misty-game.html"><span class="eyebrow">Home · Tigoni</span><h3>The mist of Tigoni</h3><p>Our home ground, high in the Kenyan highlands, with a pavilion stove that has never let us down.</p></a>
<a class="card" href="rhino-cup.html"><span class="eyebrow">Away · Nanyuki</span><h3>Rhino Cup</h3><p>Our first club tour, beneath Mount Kenya.</p></a>
<a class="card" href="fixtures.html"><span class="eyebrow">Next · Limuru</span><h3>Mutaiga Country Club</h3><p>Saturday 31 October 2026 at Limuru Grounds.</p></a></div></div></section>
<section style="padding:20px 0 90px"><div class="wrap reveal"><blockquote>“Proper cricket. Questionable judgement. Excellent company.”</blockquote></div></section>
''' + FOOT)

# ---------- fixtures
write("fixtures.html", head("Fixtures","fixtures.html") + hero("Season 2026","Fixtures &amp; results","The next match, and everything we have played so far.") + f'''
<section><div class="wrap"><div class="sec-head reveal"><div><span class="eyebrow">Next match</span><h2>Coming up</h2></div></div>
<div class="nextcard reveal"><div class="big">31<small>OCTOBER</small></div><div><span class="pill">Upcoming</span><h3 style="margin-top:10px">Sticky Wickets v Mutaiga Country Club</h3><div class="sub">Saturday 31 October 2026 · Limuru Grounds · Start time TBC</div></div></div></div></section>
<section class="band"><div class="wrap"><div class="sec-head reveal"><div><span class="eyebrow">Season 2026</span><h2>Results &amp; reports</h2></div></div>
<div class="matches panel on reveal" style="display:grid">{PAST}</div>
<p class="note">Full scorecards will be added as they come in.</p></div></section>
''' + FOOT)

# ---------- team
write("team.html", head("The Team","team.html") + hero("The squad","Meet the team","Click a name to read the bio. Photos coming soon.") + f'''
<section><div class="wrap"><div class="group-title">Players</div><div class="team tight reveal">{"".join(player_card(*p) for p in SQUAD)}</div>
<div class="group-title">Officials</div><div class="team tight reveal">{"".join(player_card(n,r) for n,r in OFFICIALS)}</div></div></section>
''' + FOOT)

# ---------- season
write("season.html", head("Season 2026","season.html") + hero("Match reports","Season 2026","From the mist of Tigoni to highland cricket on tour — and a clinical encounter with the Medics.") + f'''
<section><div class="wrap"><div class="grid-news reveal">{S_MIST}{S_MED}{S_RHINO}</div></div></section>''' + FOOT)

# ---------- reports
def fig(src,cap): return f'<figure><img src="{src}" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>'
def report(fn,cur,eb,title,sub,hero_img,facts,body):
    f = "".join(f"<div><b>{k}</b>{v}</div>" for k,v in facts)
    write(fn, head(title) + hero(eb,title,sub,hero_img,'<a href="season.html">Season 2026</a> / '+title) + f'<section><div class="wrap"><div class="facts article" style="max-width:1000px;margin-left:auto;margin-right:auto">{f}</div><div class="article">{body}</div></div></section>' + FOOT)

report("misty-game.html","","Match report · 11 July 2026","Sticky Wickets in the Mist","Visibility became optional, appeals remained compulsory and the pavilion stove emerged as the day's most consistent performer.","assets/misty/hero.jpg",
 [("Date","11 July 2026"),("Venue","Tigoni"),("Start","2:00 pm"),("Altitude","About 2,300 m")],
 "<p>Cold, damp and wrapped in heavy mist, Tigoni gave us conditions in which fielders were often heard before they were seen.</p>"+fig("assets/misty/fog-action.jpg","Players barely visible in the mist")+
 "<h2>The format</h2><p>Twelve balls per player, bonus points for fielding, a ten-point deduction for wickets, and extra scoring for wides and run-outs. A maiden over was later agreed to earn the bowler ten points.</p>"+fig("assets/misty/pitch.jpg","The marked pitch leading into the mist")+
 "<h2>The result</h2><p>Anshul took first place with a consistent all-round display. Rory finished second with 24 points after a strong recovery. The key moment: Dominic running out Paris, a 20-point swing.</p>"+fig("assets/misty/action.jpg","The mist begins to lift")+
 "<h2>Off the field</h2><p>The pavilion stove, the sandwiches and the tea were the real stars, and the match earned a five-star tea rating.</p>"+fig("assets/misty/fireplace.jpg","The most productive players of the afternoon")+fig("assets/misty/lunch.jpg","Tea, lunch and tactical observation")+fig("assets/misty/players.jpg","The Stickies after the match")+fig("assets/misty/whitecap.jpg","A White Cap overlooking the misty field")+
 "<p><em>The complete scorecard is still to come.</em></p>")

report("medics-match.html","","Match report · Season 2026","The Medics Match","A clinical performance, glorious sunshine and excellent company. The Medics brought the precision; the Stickies brought the optimism.","assets/medics/photo-15.jpg",
 [("Opponent","The Medics"),("Venue","Tigoni"),("Conditions","Glorious sunshine")],
 "<p>The Medics came to Tigoni on a sunny afternoon and were far more precise than the Stickies, winning convincingly. Our spirited but outmatched performance was met with the usual self-deprecating humour.</p>"+fig("assets/medics/photo-15.jpg","A glorious afternoon for cricket")+
 "<p>Hats off to the opposition for their play and for their company.</p>"+fig("assets/medics/photo-4.jpg","Gathered by the pavilion in the sunshine")+fig("assets/medics/photo-16.jpg","A bowler in full delivery stride")+fig("assets/medics/photo-22.jpg","A batter taking guard")+fig("assets/medics/photo-24.jpg","Playing a shot on the sunny pitch")+
 "<h2>The view from the sidelines</h2><p>Afterwards the Medics played an extra match among themselves while the Stickies watched from the sidelines, chairs and all.</p>"+fig("assets/medics/photo-6.jpg","The view from the sidelines")+fig("assets/medics/photo-9.jpg","Players gathered on the outfield")+fig("assets/medics/photo-12.jpg","Conferring between deliveries")+fig("assets/medics/photo-20.jpg","Two batters preparing beside the pavilion"))

report("rhino-cup.html","","First club tour · June 2026","Our First Rhino Cup","Sticky Wickets headed north to Nanyuki for tournament cricket, enormous skies and the beginning of a new tradition.","assets/rhino/scoreboard-mountain.jpg",
 [("Tour","First club tour"),("When","June 2026"),("Where","Nanyuki")],
 "<p>Sticky Wickets' first club tour took us to Nanyuki for our first appearance at the Rhino Cup. The matches were played on highland grass with Mount Kenya in the background.</p>"+fig("assets/rhino/wide-match.jpg","Tournament cricket on the high plains outside Nanyuki")+fig("assets/rhino/nutty-mountain.jpg","Mount Kenya in the background")+fig("assets/rhino/running.jpg","Returning from the field in good spirits")+
 "<p><em>The full match report, results and opponent details are still to be written and will be added as they arrive.</em></p>"+
 "<h2>Tour gallery</h2>"+"".join(fig(f"assets/rhino/{x}.jpg",c) for x,c in [("action-wide","Rhino Cup action"),("team-spirit","Celebrating beside the tent"),("bowling","Bowling"),("batting","Batting"),("waiting-to-bat","Waiting to bat"),("pads","Padded up"),("tour-humour","Tour humour"),("candid","Candid"),("portrait","Portrait under a vivid blue sky")]))

# ---------- gallery
G = [("misty/fog-action","Misty Match"),("rhino/team-spirit","Tour Spirit"),("rhino/wide-match","Highland Cricket"),("misty/lunch","Tea & Tactics"),("rhino/scoreboard-wide","Mount Kenya Watching"),("misty/fireplace","Fireside"),("medics/photo-15","Sunshine v the Medics"),("rhino/bowling","Bowling"),("rhino/batting","Batting"),("misty/players","After the Mist"),("rhino/nutty-mountain","Mount Kenya"),("medics/photo-4","Pavilion"),("rhino/pads","Padded up"),("medics/photo-16","Delivery stride"),("rhino/portrait","Blue sky"),("misty/pitch","Into the mist")]
write("gallery.html", head("Gallery","gallery.html") + hero("Club archive","Three shades of Sticky","Sunny beginnings, the deep mist of Tigoni and the dry gold of Nanyuki.") + '<section><div class="wrap"><div class="gallery reveal">' + "".join(f'<a href="javascript:void 0"><img src="assets/{p}.jpg" alt="{c}" loading="lazy"><span>{c}</span></a>' for p,c in G) + '</div></div></section><div class="lb" id="lb"><img alt=""></div>' + FOOT)

# ---------- join
write("join.html", head("Join","join.html") + hero("Join us","Fancy a game?","Whether you bat, bowl, or just bring excellent snacks — there's a place at the Tigoni pavilion.") + '''
<section><div class="wrap"><div class="cards3 reveal"><div class="card"><span class="eyebrow">Come and watch</span><h3>Next match</h3><p>Sticky Wickets v Mutaiga Country Club, Saturday 31 October 2026, Limuru Grounds.</p></div>
<div class="card"><span class="eyebrow">Play for us</span><h3>New Stickies welcome</h3><p>Contact details are being added to this page.</p></div>
<div class="card"><span class="eyebrow">Home ground</span><h3>Tigoni, Kenya</h3><p>Adhaerere Maneat.</p></div></div></div></section>
''' + FOOT)

open(os.path.join(OUT,"site.js"),"w").write('''const h=document.querySelector('header');
const sc=()=>h.classList.toggle('scrolled',scrollY>40);addEventListener('scroll',sc);sc();
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
const lb=document.getElementById('lb');
if(lb){document.querySelectorAll('.gallery a').forEach(a=>a.onclick=e=>{e.preventDefault();lb.querySelector('img').src=a.querySelector('img').src;lb.classList.add('on')});lb.onclick=()=>lb.classList.remove('on');addEventListener('keydown',e=>e.key==='Escape'&&lb.classList.remove('on'))}
''')
