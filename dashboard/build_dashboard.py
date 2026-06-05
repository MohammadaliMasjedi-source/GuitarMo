"""Build the GuitarMo dashboard (dashboard/dashboard.html).

Bakes the project plan (from project_plan.py) and the *local* git state into a
single self-contained HTML file. The HTML additionally fetches *live* GitHub
activity client-side (auto-refreshing), so it reflects both the local and the
online repository.

    python dashboard/build_dashboard.py      # or double-click Dashboard.bat
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from project_plan import to_dict  # noqa: E402


def _git(*args, default=""):
    try:
        out = subprocess.run(["git", "-C", ROOT, *args],
                             capture_output=True, text=True, timeout=15)
        return out.stdout.strip() if out.returncode == 0 else default
    except Exception:
        return default


def git_state():
    recent = []
    log = _git("log", "-8", "--pretty=%h\x1f%s\x1f%cr")
    for line in log.splitlines():
        parts = line.split("\x1f")
        if len(parts) == 3:
            recent.append({"hash": parts[0], "subject": parts[1], "date": parts[2]})
    return {
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD", default="?"),
        "last_subject": _git("log", "-1", "--pretty=%s", default="(no commits)"),
        "last_date": _git("log", "-1", "--pretty=%cr", default="-"),
        "total_commits": _git("rev-list", "--count", "HEAD", default="0"),
        "dirty": bool(_git("status", "--porcelain")),
        "recent": recent,
    }


def build():
    data = to_dict()
    data["git"] = git_state()
    data["generated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = TEMPLATE.replace("__GUITARMO_DATA__", json.dumps(data))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"dashboard -> {out}")
    print(f"  overall {data['overall']}%  |  "
          f"branch {data['git']['branch']}  |  {data['git']['total_commits']} commits")
    return out


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GuitarMo — Project Dashboard</title>
<style>
  :root{
    --bg:#0d0b09; --bg2:#15110d; --card:#1b1611; --line:#2c241b;
    --gold:#e8b04b; --gold2:#f4cf77; --ink:#efe7da; --mut:#9a8f7e;
    --done:#5fd08a; --next:#e8b04b; --todo:#6b6253;
  }
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 600px at 75% -10%,#241a10,transparent),var(--bg);
    color:var(--ink);font:15px/1.5 "Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
  a{color:var(--gold);text-decoration:none} a:hover{text-decoration:underline}
  .wrap{max-width:1180px;margin:0 auto;padding:28px 22px 60px}
  header{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:8px}
  h1{font-size:30px;margin:0;letter-spacing:.5px}
  .tag{color:var(--mut);font-size:15px}
  .badge{display:inline-flex;align-items:center;gap:6px;background:var(--card);border:1px solid var(--line);
    border-radius:999px;padding:5px 12px;font-size:12.5px;color:var(--mut)}
  .live-dot{width:8px;height:8px;border-radius:50%;background:var(--done);box-shadow:0 0 8px var(--done);
    animation:pulse 1.8s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
  .grid{display:grid;gap:16px}
  .top{grid-template-columns:280px 1fr;align-items:stretch;margin:22px 0}
  .card{background:linear-gradient(180deg,var(--bg2),var(--card));border:1px solid var(--line);
    border-radius:16px;padding:20px}
  .ring-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}
  .ring{position:relative;width:150px;height:150px}
  .ring svg{transform:rotate(-90deg)}
  .ring .pct{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
  .ring .pct b{font-size:34px;color:var(--gold)} .ring .pct span{font-size:12px;color:var(--mut)}
  .counts{display:flex;gap:10px;flex-wrap:wrap}
  .pill{flex:1;min-width:80px;background:var(--card);border:1px solid var(--line);border-radius:12px;
    padding:12px;text-align:center}
  .pill b{display:block;font-size:24px} .pill small{color:var(--mut)}
  .gh{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}
  .stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}
  .stat .v{font-size:20px;font-weight:600;color:var(--gold2)} .stat .k{color:var(--mut);font-size:12px}
  .commits{list-style:none;margin:0;padding:0;max-height:190px;overflow:auto}
  .commits li{display:flex;gap:10px;padding:7px 0;border-bottom:1px dashed var(--line);font-size:13.5px}
  .commits code{color:var(--gold);font-size:12px} .commits .d{margin-left:auto;color:var(--mut);font-size:12px;white-space:nowrap}
  h2{font-size:14px;text-transform:uppercase;letter-spacing:1.4px;color:var(--mut);margin:30px 0 12px}
  .phase{margin-bottom:12px}
  .phase .head{display:flex;align-items:center;gap:12px;cursor:pointer}
  .phase .num{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;
    font-weight:700;background:var(--card);border:1px solid var(--line)}
  .phase .ttl{font-weight:600} .phase .goal{color:var(--mut);font-size:13px}
  .bar{height:8px;border-radius:6px;background:#241d14;overflow:hidden;margin-top:8px}
  .bar>i{display:block;height:100%;background:linear-gradient(90deg,var(--gold),var(--done));
    width:0;transition:width 1.1s cubic-bezier(.2,.8,.2,1)}
  .tasks{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px;margin-top:12px;
    max-height:0;overflow:hidden;transition:max-height .4s ease}
  .phase.open .tasks{max-height:2400px}
  .task{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--todo);border-radius:10px;padding:12px}
  .task.done{border-left-color:var(--done)} .task.next{border-left-color:var(--next)}
  .task .id{color:var(--mut);font-size:12px} .task .tt{font-weight:600;margin:2px 0 6px}
  .task .dod{margin:6px 0 0;padding-left:16px;color:var(--mut);font-size:12.5px}
  .st{font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid var(--line)}
  .st.done{color:var(--done)} .st.next{color:var(--next)} .st.todo{color:var(--mut)}
  .chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
  .chip{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 14px;cursor:pointer;font-size:13px;color:var(--mut)}
  .chip.active{color:#1a140c;background:var(--gold);border-color:var(--gold);font-weight:600}
  .board{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}
  footer{margin-top:40px;color:var(--mut);font-size:12.5px;text-align:center;border-top:1px solid var(--line);padding-top:18px}
  button.refresh{background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:10px;
    padding:8px 14px;cursor:pointer} button.refresh:hover{border-color:var(--gold)}
  @media(max-width:760px){.top{grid-template-columns:1fr}.gh{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1 id="title">🎸 GuitarMo</h1>
    <span class="tag" id="tagline"></span>
    <span class="badge"><span class="live-dot"></span> live</span>
    <span style="flex:1"></span>
    <a id="repolink" class="badge" target="_blank">GitHub ↗</a>
    <button class="refresh" onclick="location.reload()">⟳ Refresh</button>
  </header>

  <div class="grid top">
    <div class="card ring-wrap">
      <div class="ring">
        <svg width="150" height="150">
          <circle cx="75" cy="75" r="60" fill="none" stroke="#241d14" stroke-width="13"></circle>
          <circle id="ringfg" cx="75" cy="75" r="60" fill="none" stroke="url(#g)" stroke-width="13"
            stroke-linecap="round" stroke-dasharray="377" stroke-dashoffset="377"></circle>
          <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#e8b04b"></stop><stop offset="1" stop-color="#5fd08a"></stop>
          </linearGradient></defs>
        </svg>
        <div class="pct"><b id="overall">0%</b><span>overall</span></div>
      </div>
      <div class="counts" id="counts"></div>
    </div>

    <div class="card">
      <h2 style="margin-top:0">Repository — local + online</h2>
      <div class="gh" id="ghstats"></div>
      <div style="display:flex;gap:18px;flex-wrap:wrap">
        <div style="flex:1;min-width:260px">
          <div style="color:var(--mut);font-size:12px;margin-bottom:6px">RECENT COMMITS (online ↔ local)</div>
          <ul class="commits" id="commits"></ul>
        </div>
      </div>
      <div id="ghnote" style="color:var(--mut);font-size:12px;margin-top:8px"></div>
    </div>
  </div>

  <h2>Phases &amp; Definition of Done</h2>
  <div id="phases"></div>

  <h2>Task board</h2>
  <div class="chips" id="chips"></div>
  <div class="board" id="board"></div>

  <footer>
    Baked <span id="generated"></span> from <code>project_plan.py</code> + local git ·
    online activity refreshed live from the GitHub API ·
    rebuild with <code>Dashboard.bat</code> / auto via <code>Sync.bat</code>.
  </footer>
</div>

<script>
const DATA = __GUITARMO_DATA__;
const SK = {done:"done", next:"next", todo:"todo"};
const EM = {done:"✅", next:"🔜", todo:"⬜"};

function el(t,c,h){const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;}

// header / meta
document.getElementById("title").textContent = DATA.meta.emoji+" "+DATA.meta.name;
document.getElementById("tagline").textContent = DATA.meta.tagline;
document.getElementById("repolink").href = DATA.meta.repo_url;
document.getElementById("generated").textContent = DATA.generated;

// ring
(function(){
  const C=2*Math.PI*60, pct=DATA.overall;
  const fg=document.getElementById("ringfg");
  fg.setAttribute("stroke-dasharray", C.toFixed(1));
  setTimeout(()=>fg.setAttribute("stroke-dashoffset",(C*(1-pct/100)).toFixed(1)),120);
  document.getElementById("overall").textContent = Math.round(pct)+"%";
})();

// counts
const cw=document.getElementById("counts");
[["done","Done"],["next","Next"],["todo","Planned"]].forEach(([k,l])=>{
  cw.appendChild(el("div","pill",`<b style="color:var(--${k})">${DATA.counts[k]}</b><small>${l}</small>`));
});

// phases
const pc=document.getElementById("phases");
DATA.phases.forEach(ph=>{
  const wrap=el("div","phase"+(ph.status==="next"?" open":""));
  const head=el("div","head");
  head.appendChild(el("div","num",ph.num));
  const mid=el("div"); mid.style.flex="1";
  mid.appendChild(el("div","ttl",`Phase ${ph.num} — ${ph.title} `+
    `<span class="st ${ph.status}">${EM[ph.status]} ${ph.progress}%</span>`));
  mid.appendChild(el("div","goal",ph.goal));
  const bar=el("div","bar"); const fill=el("i"); bar.appendChild(fill); mid.appendChild(bar);
  head.appendChild(mid);
  wrap.appendChild(head);
  const tasks=el("div","tasks");
  ph.tasks.forEach(t=>{
    const card=el("div","task "+t.status);
    card.innerHTML=`<div class="id">${t.id} · <span class="st ${t.status}">${EM[t.status]}</span></div>`+
      `<div class="tt">${t.title}</div><div style="color:var(--mut);font-size:12.5px">${t.objective}</div>`+
      `<ul class="dod">`+t.dod.map(d=>`<li>${d}</li>`).join("")+`</ul>`;
    tasks.appendChild(card);
  });
  wrap.appendChild(tasks);
  head.onclick=()=>wrap.classList.toggle("open");
  pc.appendChild(wrap);
  setTimeout(()=>fill.style.width=ph.progress+"%",200);
});

// task board + filters
const ALLT=[]; DATA.phases.forEach(ph=>ph.tasks.forEach(t=>ALLT.push({...t,phase:ph.num})));
const chips=document.getElementById("chips"); const board=document.getElementById("board");
const filters=[["all","All"],["done","✅ Done"],["next","🔜 Next"],["todo","⬜ Planned"]];
let active="all";
function renderBoard(){
  board.innerHTML="";
  ALLT.filter(t=>active==="all"||t.status===active).forEach(t=>{
    const c=el("div","task "+t.status);
    c.innerHTML=`<div class="id">P${t.phase} · ${t.id} <span class="st ${t.status}">${EM[t.status]}</span></div>`+
      `<div class="tt">${t.title}</div><div style="color:var(--mut);font-size:12.5px">${t.objective}</div>`;
    board.appendChild(c);
  });
}
filters.forEach(([k,l])=>{
  const ch=el("div","chip"+(k==="all"?" active":""),l);
  ch.onclick=()=>{active=k;[...chips.children].forEach(x=>x.classList.remove("active"));ch.classList.add("active");renderBoard();};
  chips.appendChild(ch);
});
renderBoard();

// ---- live GitHub (online) + baked local ----
const gs=document.getElementById("ghstats"); const cl=document.getElementById("commits");
function stat(k,v){return `<div class="stat"><div class="v">${v}</div><div class="k">${k}</div></div>`;}
function paintLocal(){
  const g=DATA.git;
  gs.innerHTML = stat("Branch",g.branch)+stat("Commits (local)",g.total_commits)+
    stat("Working tree", g.dirty?"✎ dirty":"✓ clean")+stat("Last commit",g.last_date);
  cl.innerHTML = g.recent.map(c=>`<li><code>${c.hash}</code><span>${c.subject}</span><span class="d">${c.date}</span></li>`).join("");
  document.getElementById("ghnote").textContent="Showing baked local git data — online fetch unavailable.";
}
async function loadOnline(){
  const O=DATA.meta.owner, R=DATA.meta.repo;
  try{
    const repo=await (await fetch(`https://api.github.com/repos/${O}/${R}`)).json();
    if(repo && repo.full_name){
      const pushed=new Date(repo.pushed_at).toLocaleString();
      gs.innerHTML = stat("★ Stars",repo.stargazers_count)+stat("Branch",DATA.git.branch)+
        stat("Open issues",repo.open_issues_count)+stat("Last push (online)",pushed);
    }
    const commits=await (await fetch(`https://api.github.com/repos/${O}/${R}/commits?per_page=8`)).json();
    if(Array.isArray(commits)){
      cl.innerHTML=commits.map(c=>{
        const h=c.sha.slice(0,7), m=(c.commit.message.split("\n")[0]);
        const d=new Date(c.commit.author.date).toLocaleDateString();
        return `<li><code>${h}</code><span>${m}</span><span class="d">${d}</span></li>`;
      }).join("");
    }
    document.getElementById("ghnote").innerHTML="🟢 Live from GitHub · auto-refresh every 5 min · last "+new Date().toLocaleTimeString();
  }catch(e){ paintLocal(); }
}
paintLocal(); loadOnline(); setInterval(loadOnline, 5*60*1000);
</script>
</body>
</html>"""


if __name__ == "__main__":
    build()
