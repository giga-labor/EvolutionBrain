from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EvoBrain Dashboard</title>
  <style>
    :root {
      --bg: #090f1a;
      --bg-soft: #101a2a;
      --card: rgba(15, 24, 39, 0.78);
      --text: #e6edf8;
      --muted: #9fb0ca;
      --line: rgba(152, 179, 219, 0.22);
      --accent: #2f80ff;
      --accent-2: #5da4ff;
      --ok: #36d399;
      --shadow: 0 18px 42px rgba(0, 0, 0, .34);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Aptos", "Bahnschrift", "Segoe UI Variable", sans-serif;
      background:
        radial-gradient(1200px 460px at -5% -5%, #1f3f79 0%, transparent 60%),
        radial-gradient(900px 380px at 120% 0%, #174865 0%, transparent 58%),
        var(--bg);
      color: var(--text);
    }
    .wrap {
      max-width: 1280px;
      margin: 0 auto;
      padding: 88px 20px 20px;
    }
    .topnav {
      position: fixed;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      width: min(1280px, calc(100vw - 24px));
      min-height: 56px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--card);
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }
    .topnav .brand { font-weight: 700; letter-spacing: .2px; }
    .topnav .links { display:flex; gap:8px; flex-wrap:wrap; }
    .topnav .links a {
      color: var(--text);
      text-decoration: none;
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--bg-soft);
      font-size: 13px;
    }
    .topnav .links a.active {
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #fff;
      border-color: transparent;
    }
    h1 { margin: 0 0 10px; font-size: 30px; letter-spacing: .2px; }
    h2 { margin: 0 0 10px; font-size: 18px; }
    .muted { color: var(--muted); margin-bottom: 16px; }
    .muted a { color: var(--accent-2); text-decoration: none; }
    .muted a:hover { text-decoration: underline; }
    .grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 14px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 14px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }
    .kpi { grid-column: span 3; }
    .wide { grid-column: span 6; }
    .full { grid-column: span 12; }
    .label { color: var(--muted); font-size: 12px; }
    .value { font-size: 31px; font-weight: 700; }
    .ok { color: var(--ok); font-weight: 600; }
    input, textarea, select, button {
      width: 100%;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 10px;
      font: inherit;
      background: var(--bg-soft);
      color: var(--text);
    }
    textarea { min-height: 90px; resize: vertical; }
    input::placeholder, textarea::placeholder { color: #7f91ad; }
    button {
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #fff;
      border: none;
      cursor: pointer;
      font-weight: 600;
      transition: transform .12s ease, filter .12s ease;
    }
    button:hover { transform: translateY(-1px); filter: brightness(1.06); }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .row3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
    .list { max-height: 280px; overflow: auto; border: 1px solid var(--line); border-radius: 8px; }
    .item { padding: 8px; border-bottom: 1px solid var(--line); }
    .item:last-child { border-bottom: none; }
    .mini { font-size: 12px; color: var(--muted); }
    pre {
      background: #070e1a;
      color: #dce7f7;
      padding: 10px;
      border-radius: 8px;
      border: 1px solid var(--line);
      overflow: auto;
      max-height: 220px;
      margin: 0;
    }
    @media (max-width: 980px) {
      .kpi, .wide { grid-column: span 12; }
      .row, .row3 { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="topnav">
    <div class="brand">Ebby UI</div>
    <div class="links">
      <a href="/api/v1/ui/dashboard" class="active">Dashboard</a>
      <a href="/api/v1/ui/graph">Graph</a>
      <a href="/api/v1/ui/chat">Chat</a>
      <a href="/api/v1/ui/audit">Audit</a>
    </div>
  </div>
  <div class="wrap">
    <div class="muted">Gestione live del tuo cervello: dati, ricerca, chat, audit.</div>

    <div class="grid">
      <div class="card kpi"><div class="label">Documenti</div><div class="value" id="kDocs">0</div></div>
      <div class="card kpi"><div class="label">Note</div><div class="value" id="kNotes">0</div></div>
      <div class="card kpi"><div class="label">Progetti</div><div class="value" id="kProjects">0</div></div>
      <div class="card kpi"><div class="label">System</div><div id="kHealth" class="value ok" style="font-size:22px">OK</div></div>

      <div class="card wide">
        <h2>Fonti Preconfigurate</h2>
        <div class="row3">
          <input id="srcName" placeholder="Nome fonte (es. Repo Marketing)">
          <select id="srcType">
            <option value="folder">cartella</option>
            <option value="file">file</option>
            <option value="url">sito/url</option>
            <option value="manual">manuale</option>
          </select>
          <button onclick="createSource()">Salva Fonte</button>
        </div>
        <input id="srcRef" placeholder="Path o URL della fonte">
      </div>

      <div class="card wide">
        <h2>Importa Documento</h2>
        <div class="row">
          <input id="docTitle" placeholder="Titolo documento">
          <select id="docSourceProfile"></select>
        </div>
        <div class="row3">
          <button type="button" onclick="pickFile()">Scegli File (Explorer)</button>
          <button type="button" onclick="pickFolder()">Scegli Cartella (Explorer)</button>
          <button type="button" onclick="importSelectedFiles()">Importa Selezionati</button>
        </div>
        <input id="filePicker" type="file" style="display:none" accept=".txt,.md,.json,.csv,.log,.py,.js,.ts,.html,.xml,.yaml,.yml">
        <input id="folderPicker" type="file" style="display:none" webkitdirectory directory multiple>
        <textarea id="docContent" placeholder="Contenuto da importare..."></textarea>
        <button onclick="importDocument()">Importa</button>
        <div class="mini" id="selectedFileInfo">Nessun file selezionato.</div>
      </div>

      <div class="card wide">
        <h2>Crea Nota</h2>
        <div class="row">
          <input id="noteTitle" placeholder="Titolo nota">
          <input id="noteType" placeholder="note_type" value="manual">
        </div>
        <textarea id="noteBody" placeholder="Testo nota..."></textarea>
        <button onclick="createNote()">Salva Nota</button>
      </div>

      <div class="card wide">
        <h2>Crea Progetto</h2>
        <div class="row">
          <input id="projectName" placeholder="Nome progetto">
          <input id="projectType" placeholder="project_type" value="general">
        </div>
        <textarea id="projectDesc" placeholder="Descrizione progetto"></textarea>
        <button onclick="createProject()">Crea Progetto</button>
      </div>

      <div class="card wide">
        <h2>Ricerca e Chat</h2>
        <div class="row3">
          <input id="searchQ" placeholder="query...">
          <select id="searchMode"><option>hybrid</option><option>keyword</option><option>semantic</option></select>
          <button onclick="runSearch()">Cerca</button>
        </div>
        <div style="margin-top:8px" class="row">
          <input id="chatMsg" placeholder="Domanda in linguaggio naturale">
          <button onclick="runChat()">Chat Grounded</button>
        </div>
        <pre id="searchOut">Nessuna ricerca eseguita.</pre>
      </div>

      <div class="card wide">
        <h2>Audit</h2>
        <div class="row">
          <input id="auditEntityType" placeholder="entity_type (opzionale)">
          <button onclick="loadAudit()">Aggiorna Audit</button>
        </div>
        <pre id="auditOut">Caricamento...</pre>
      </div>

      <div class="card wide">
        <h2>Documenti</h2>
        <div class="list" id="documentsList"></div>
      </div>

      <div class="card wide">
        <h2>Note</h2>
        <div class="list" id="notesList"></div>
      </div>

      <div class="card wide">
        <h2>Progetti</h2>
        <div class="list" id="projectsList"></div>
      </div>

      <div class="card wide">
        <h2>System State</h2>
        <pre id="systemOut"></pre>
      </div>

      <div class="card full mini" id="statusBar">Pronto.</div>
    </div>
  </div>

  <script>
    function setStatus(msg){ document.getElementById('statusBar').textContent = msg; }
    function itemHtml(title, sub){ return `<div class="item"><div>${title}</div><div class="mini">${sub}</div></div>`; }
    let selectedFiles = [];

    async function api(url, options){
      const res = await fetch(url, options);
      const data = await res.json().catch(() => ({}));
      if(!res.ok){ throw new Error((data && data.error && data.error.message) || `HTTP ${res.status}`); }
      return data;
    }

    async function refreshAll(){
      try {
        const [health, state, docs, notes, projects, sources] = await Promise.all([
          api('/api/v1/system/health'),
          api('/api/v1/system/state'),
          api('/api/v1/documents'),
          api('/api/v1/notes'),
          api('/api/v1/projects'),
          api('/api/v1/sources'),
        ]);

        document.getElementById('kDocs').textContent = docs?.data?.total ?? 0;
        document.getElementById('kNotes').textContent = notes?.data?.total ?? 0;
        document.getElementById('kProjects').textContent = projects?.data?.total ?? 0;
        document.getElementById('kHealth').textContent = (health?.overall_status || 'unknown').toUpperCase();

        const dList = (docs?.data?.items || []).map(x => itemHtml(x.title || '(senza titolo)', `${x.id} | ${x.source_type} | ${x.source_ref || 'n/a'}`)).join('') || itemHtml('Nessun documento', '');
        const nList = (notes?.data?.items || []).map(x => itemHtml(x.title, `${x.id} | ${x.note_type} | conf ${x.confidence}`)).join('') || itemHtml('Nessuna nota', '');
        const pList = (projects?.data?.items || []).map(x => itemHtml(x.name, `${x.id} | ${x.status}`)).join('') || itemHtml('Nessun progetto', '');

        document.getElementById('documentsList').innerHTML = dList;
        document.getElementById('notesList').innerHTML = nList;
        document.getElementById('projectsList').innerHTML = pList;
        document.getElementById('systemOut').textContent = JSON.stringify(state, null, 2);
        const srcSel = document.getElementById('docSourceProfile');
        const srcItems = sources?.data?.items || [];
        srcSel.innerHTML = srcItems.map(s => `<option value="${s.id}" data-type="${s.source_type}" data-ref="${s.source_ref}">${s.name} (${s.source_type})</option>`).join('');
        if (!srcSel.innerHTML) {
          srcSel.innerHTML = '<option value="">Nessuna fonte salvata</option>';
        }

        await loadAudit();
        setStatus('Dashboard aggiornata.');
      } catch (e) {
        setStatus('Errore refresh: ' + e.message);
      }
    }

    async function createSource(){
      try {
        const payload = {
          name: document.getElementById('srcName').value,
          source_type: document.getElementById('srcType').value,
          source_ref: document.getElementById('srcRef').value
        };
        await api('/api/v1/sources', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
        setStatus('Fonte salvata.');
        document.getElementById('srcName').value = '';
        document.getElementById('srcRef').value = '';
        await refreshAll();
      } catch (e) { setStatus('Errore salvataggio fonte: ' + e.message); }
    }

    async function importDocument(){
      try {
        const srcSel = document.getElementById('docSourceProfile');
        const opt = srcSel.options[srcSel.selectedIndex];
        const sourceType = opt?.dataset?.type || 'manual';
        const sourceRef = opt?.dataset?.ref || null;
        const payload = {
          title: document.getElementById('docTitle').value || null,
          source_type: sourceType,
          source_ref: sourceRef,
          content: document.getElementById('docContent').value
        };
        await api('/api/v1/documents/import', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
        setStatus('Documento importato.');
        document.getElementById('docContent').value = '';
        await refreshAll();
      } catch (e) { setStatus('Errore import documento: ' + e.message); }
    }

    function pickFile(){
      document.getElementById('filePicker').click();
    }

    function pickFolder(){
      document.getElementById('folderPicker').click();
    }

    async function fileToText(file){
      return await file.text();
    }

    function setSelectedInfo(){
      const box = document.getElementById('selectedFileInfo');
      if(!selectedFiles.length){
        box.textContent = 'Nessun file selezionato.';
        return;
      }
      const names = selectedFiles.slice(0, 3).map(f => f.webkitRelativePath || f.name).join(', ');
      box.textContent = `${selectedFiles.length} file selezionati: ${names}${selectedFiles.length > 3 ? ' ...' : ''}`;
    }

    document.getElementById('filePicker').addEventListener('change', async (ev) => {
      const file = ev.target.files && ev.target.files[0];
      if(!file) return;
      selectedFiles = [file];
      setSelectedInfo();
      const txt = await fileToText(file);
      document.getElementById('docTitle').value = file.name;
      document.getElementById('docContent').value = txt;
      setStatus(`File caricato: ${file.name}`);
    });

    document.getElementById('folderPicker').addEventListener('change', (ev) => {
      const files = Array.from(ev.target.files || []);
      if(!files.length) return;
      selectedFiles = files;
      setSelectedInfo();
      setStatus(`Cartella selezionata: ${files.length} file pronti per import.`);
    });

    async function importSelectedFiles(){
      if(!selectedFiles.length){
        setStatus('Seleziona prima almeno un file o una cartella.');
        return;
      }
      const srcSel = document.getElementById('docSourceProfile');
      const opt = srcSel.options[srcSel.selectedIndex];
      const sourceTypeBase = opt?.dataset?.type || 'file';
      const sourceRefBase = opt?.dataset?.ref || '';
      let imported = 0;
      for(const file of selectedFiles){
        const text = await fileToText(file);
        const relative = file.webkitRelativePath || file.name;
        const payload = {
          title: relative,
          source_type: sourceTypeBase,
          source_ref: sourceRefBase ? `${sourceRefBase} :: ${relative}` : relative,
          content: text
        };
        await api('/api/v1/documents/import', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify(payload)
        });
        imported += 1;
      }
      setStatus(`Import completato: ${imported} file.`);
      document.getElementById('docContent').value = '';
      selectedFiles = [];
      setSelectedInfo();
      await refreshAll();
    }

    async function createNote(){
      try {
        const payload = {
          title: document.getElementById('noteTitle').value,
          body_markdown: document.getElementById('noteBody').value,
          note_type: document.getElementById('noteType').value || 'manual',
          source_type: 'manual'
        };
        await api('/api/v1/notes', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
        setStatus('Nota salvata.');
        document.getElementById('noteBody').value = '';
        await refreshAll();
      } catch (e) { setStatus('Errore creazione nota: ' + e.message); }
    }

    async function createProject(){
      try {
        const payload = {
          name: document.getElementById('projectName').value,
          description: document.getElementById('projectDesc').value || null,
          project_type: document.getElementById('projectType').value || 'general'
        };
        await api('/api/v1/projects', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
        setStatus('Progetto creato.');
        await refreshAll();
      } catch (e) { setStatus('Errore creazione progetto: ' + e.message); }
    }

    async function runSearch(){
      try {
        const q = encodeURIComponent(document.getElementById('searchQ').value || '');
        const mode = encodeURIComponent(document.getElementById('searchMode').value || 'hybrid');
        const data = await api(`/api/v1/search?q=${q}&mode=${mode}`);
        document.getElementById('searchOut').textContent = JSON.stringify(data, null, 2);
        setStatus('Ricerca completata.');
      } catch (e) { setStatus('Errore ricerca: ' + e.message); }
    }

    async function runChat(){
      try {
        const message = document.getElementById('chatMsg').value;
        const data = await api('/api/v1/chat/query', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message})});
        document.getElementById('searchOut').textContent = JSON.stringify(data, null, 2);
        setStatus('Risposta chat ricevuta.');
      } catch (e) { setStatus('Errore chat: ' + e.message); }
    }

    async function loadAudit(){
      try {
        const et = document.getElementById('auditEntityType').value;
        const qs = et ? `?entity_type=${encodeURIComponent(et)}` : '';
        const data = await api('/api/v1/audit/logs' + qs);
        document.getElementById('auditOut').textContent = JSON.stringify(data, null, 2);
      } catch (e) {
        document.getElementById('auditOut').textContent = 'Errore audit: ' + e.message;
      }
    }

    // Auto-refresh every 30 seconds
    refreshAll();
    setInterval(refreshAll, 30000);

    // Show next-refresh countdown
    let _nextRefresh = 30;
    setInterval(() => {
      _nextRefresh -= 1;
      if (_nextRefresh <= 0) _nextRefresh = 30;
      const bar = document.getElementById('statusBar');
      if (!bar.textContent.startsWith('Errore')) {
        bar.textContent = `Aggiornamento automatico tra ${_nextRefresh}s`;
      }
    }, 1000);
  </script>
</body>
</html>
"""


@router.get("/audit", response_class=HTMLResponse)
def audit_console():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EvoBrain Audit Console</title>
  <style>
    :root {
      --bg: #090f1a;
      --card: rgba(15, 24, 39, 0.78);
      --text: #e6edf8;
      --muted: #9fb0ca;
      --line: rgba(152, 179, 219, 0.22);
      --accent: #5da4ff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Aptos", "Bahnschrift", "Segoe UI Variable", sans-serif;
      background:
        radial-gradient(1200px 460px at -5% -5%, #1f3f79 0%, transparent 60%),
        radial-gradient(900px 380px at 120% 0%, #174865 0%, transparent 58%),
        var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 88px 20px 20px;
    }
    .card {
      width: min(760px, 100%);
      margin: 0 auto;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: var(--card);
      backdrop-filter: blur(10px);
      padding: 22px;
    }
    .topnav{
      position: fixed;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      width: min(1280px, calc(100vw - 24px));
      min-height: 56px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--card);
      backdrop-filter: blur(10px);
      padding: 10px 12px;
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:12px;
      flex-wrap:wrap;
    }
    .topnav .brand { font-weight: 700; letter-spacing: .2px; }
    .topnav .links { display:flex; gap:8px; flex-wrap:wrap; }
    .topnav .links a {
      color: var(--text);
      text-decoration: none;
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #101a2a;
      font-size: 13px;
    }
    .topnav .links a.active {
      background: linear-gradient(135deg, #2f80ff, #5da4ff);
      color: #fff;
      border-color: transparent;
    }
    .muted { color: var(--muted); }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="topnav">
    <div class="brand">Ebby UI</div>
    <div class="links">
      <a href="/api/v1/ui/dashboard">Dashboard</a>
      <a href="/api/v1/ui/graph">Graph</a>
      <a href="/api/v1/ui/chat">Chat</a>
      <a href="/api/v1/ui/audit" class="active">Audit</a>
    </div>
  </div>
  <div class="card">
    <p class="muted">Audit rapido. Usa la dashboard per operativita completa.</p>
  </div>
</body>
</html>
"""


@router.get("/graph", response_class=HTMLResponse)
def graph_view():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EvoBrain Graph</title>
  <style>
    :root {
      --bg: #090f1a;
      --bg-soft: #101a2a;
      --card: rgba(15, 24, 39, 0.78);
      --text: #e6edf8;
      --muted: #9fb0ca;
      --line: rgba(152, 179, 219, 0.22);
      --accent: #2f80ff;
      --accent-2: #5da4ff;
    }
    body {
      margin:0;
      font-family: "Aptos", "Bahnschrift", "Segoe UI Variable", sans-serif;
      background:
        radial-gradient(1200px 460px at -5% -5%, #1f3f79 0%, transparent 60%),
        radial-gradient(900px 380px at 120% 0%, #174865 0%, transparent 58%),
        var(--bg);
      color: var(--text);
      padding-top: 88px;
    }
    .top {
      padding:10px 12px;
      border-bottom:1px solid var(--line);
      background: var(--card);
      backdrop-filter: blur(10px);
      display:flex;
      gap:10px;
      align-items:center;
      flex-wrap: wrap;
    }
    .top a { color: var(--accent-2); text-decoration:none; }
    .top input, .top button, .top select {
      padding:9px 10px;
      border-radius:10px;
      border:1px solid var(--line);
      background: var(--bg-soft);
      color: var(--text);
    }
    .top button {
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      border:none;
      cursor:pointer;
      color: #fff;
      font-weight: 600;
    }
    .topnav {
      position: fixed;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      width: min(1280px, calc(100vw - 24px));
      min-height: 56px;
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--card);
      display:flex;
      justify-content: space-between;
      align-items:center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .topnav .brand { font-weight: 700; letter-spacing: .2px; }
    .topnav .links { display:flex; gap:8px; flex-wrap:wrap; }
    .topnav .links a {
      color: var(--text);
      text-decoration: none;
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--bg-soft);
      font-size: 13px;
    }
    .topnav .links a.active {
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #fff;
      border-color: transparent;
    }
    .wrap { display:grid; grid-template-columns: 1fr 320px; height: calc(100vh - 160px); }
    #viewport { width:100%; height:100%; display:block; }
    .side { border-left:1px solid var(--line); background: var(--card); padding:12px; overflow:auto; backdrop-filter: blur(10px); }
    .muted { color: var(--muted); font-size:12px; }
    .item { border:1px solid var(--line); border-radius:10px; padding:8px; margin-bottom:8px; background: var(--bg-soft); }
    .legend-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
    #hoverTag {
      position: fixed; pointer-events:none; z-index:10; padding:6px 8px; border-radius:6px;
      background: rgba(5,13,25,.96); border:1px solid var(--line); color:var(--text); font-size:12px; display:none;
    }
    @media (max-width: 980px) {
      .wrap { grid-template-columns: 1fr; height: auto; min-height: calc(100vh - 160px); }
      #viewport { min-height: 58vh; }
      .side { border-left: none; border-top: 1px solid var(--line); }
    }
  </style>
</head>
<body>
  <div class="topnav">
    <div class="brand">Ebby UI</div>
    <div class="links">
      <a href="/api/v1/ui/dashboard">Dashboard</a>
      <a href="/api/v1/ui/graph" class="active">Graph</a>
      <a href="/api/v1/ui/chat">Chat</a>
      <a href="/api/v1/ui/audit">Audit</a>
    </div>
  </div>
  <div class="top">
    <input id="q" placeholder="Filtra nodo per nome...">
    <select id="relTypeFilter">
      <option value="">tutti i link</option>
      <option value="similar_to">similar_to</option>
      <option value="belongs_to">belongs_to</option>
      <option value="supports">supports</option>
      <option value="contradicts">contradicts</option>
      <option value="depends_on">depends_on</option>
    </select>
    <button onclick="resetGraphSync(); reloadGraph()">Aggiorna</button>
    <label class="muted" style="display:flex;align-items:center;gap:6px">
      <input type="checkbox" id="liveMode" checked> live
    </label>
    <span class="muted" id="stats"></span>
    <span class="muted">Controls: W/S zoom avanti-indietro, A/D sinistra-destra, Q/E su-giu, arrows rotate, wheel zoom</span>
  </div>
  <div class="wrap">
    <canvas id="viewport"></canvas>
    <div class="side">
      <h3>Nodo selezionato</h3>
      <div id="sel" class="muted">Clicca un nodo nel grafo.</div>
      <h3>Legenda</h3>
      <div class="item">
        <div><span class="legend-dot" style="background:#60a5fa"></span> concept (cerchio, simbolo C)</div>
        <div><span class="legend-dot" style="background:#34d399"></span> project/task/goal (quadrato, simbolo W)</div>
        <div><span class="legend-dot" style="background:#fbbf24"></span> identity/meta (pentagono, simbolo I)</div>
        <div><span class="legend-dot" style="background:#f97316"></span> procedure/process (rombo, simbolo P)</div>
        <div><span class="legend-dot" style="background:#c084fc"></span> decision/strategy (triangolo, simbolo D)</div>
        <div><span class="legend-dot" style="background:#fb7185"></span> risk/contradiction (croce, simbolo !)</div>
      </div>
      <h3>Relazioni</h3>
      <div id="rels"></div>
    </div>
  </div>
  <div id="hoverTag"></div>
<script>
const canvas = document.getElementById('viewport');
const ctx = canvas.getContext('2d');
const hoverTag = document.getElementById('hoverTag');
let W=0,H=0;

let rawNodes = [], rawEdges = [], selected = null;
let viewNodes = [];
let liveTimer = null;
let knownNodeIds = new Set();
let knownEdgeIds = new Set();
let selfModelCache = null;
const DATASETS = {
  concepts: { url: '/api/v1/concepts', entity: 'concept', items: [], byId: new Map(), offset: 0, done: false },
  relations: { url: '/api/v1/relations', entity: 'relation', items: [], byId: new Map(), offset: 0, done: false },
  documents: { url: '/api/v1/documents', entity: 'document', items: [], byId: new Map(), offset: 0, done: false },
  notes: { url: '/api/v1/notes', entity: 'note', items: [], byId: new Map(), offset: 0, done: false },
  projects: { url: '/api/v1/projects', entity: 'project', items: [], byId: new Map(), offset: 0, done: false },
  goals: { url: '/api/v1/goals', entity: 'goal', items: [], byId: new Map(), offset: 0, done: false },
  tasks: { url: '/api/v1/tasks', entity: 'task', items: [], byId: new Map(), offset: 0, done: false },
  decisions: { url: '/api/v1/decisions', entity: 'decision', items: [], byId: new Map(), offset: 0, done: false },
  procedures: { url: '/api/v1/procedures', entity: 'procedure', items: [], byId: new Map(), offset: 0, done: false },
  episodes: { url: '/api/v1/episodes', entity: 'episode', items: [], byId: new Map(), offset: 0, done: false },
  jobs: { url: '/api/v1/jobs', entity: 'job', items: [], byId: new Map(), offset: 0, done: false },
  memoryItems: { url: '/api/v1/memory/items', entity: 'memory_item', items: [], byId: new Map(), offset: 0, done: false },
};
const MAX_RENDER_NODES = 5000;
const MAX_RENDER_EDGES = 12000;
let rotX = -0.35, rotY = 0.45, zoom = 1.0;
let camX = 0, camY = 0, camZ = 0;
let panX = 0, panY = 0;
let dragging = false, lastX = 0, lastY = 0;
const keyState = {};

function resize(){
  W = canvas.clientWidth || canvas.parentElement.clientWidth;
  H = canvas.clientHeight || canvas.parentElement.clientHeight;
  canvas.width = Math.max(1, Math.floor(W * devicePixelRatio));
  canvas.height = Math.max(1, Math.floor(H * devicePixelRatio));
  ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
}
window.addEventListener('resize', ()=>{resize(); draw();});
resize();

function inferNodeType(name){
  const n = (name || '').toLowerCase();
  if (n.includes('project') || n.includes('progetto') || n.includes('task') || n.includes('goal')) return 'work';
  if (n.includes('self') || n.includes('meta') || n.includes('identity') || n.includes('profilo')) return 'identity';
  if (n.includes('procedur') || n.includes('workflow') || n.includes('pipeline') || n.includes('process')) return 'procedure';
  if (n.includes('decision') || n.includes('strateg') || n.includes('piano')) return 'decision';
  if (n.includes('risk') || n.includes('rischio') || n.includes('error') || n.includes('contrad')) return 'risk';
  return 'concept';
}

function inferNodeTypeFromEntity(entity){
  const e = (entity || '').toLowerCase();
  if(['project', 'task', 'goal'].includes(e)) return 'work';
  if(['self_model', 'self-model', 'selfmodel'].includes(e)) return 'identity';
  if(['procedure', 'job'].includes(e)) return 'procedure';
  if(['decision'].includes(e)) return 'decision';
  if(['relation', 'risk'].includes(e)) return 'risk';
  if(['memory_item', 'memory'].includes(e)) return 'memory';
  if(['note', 'episode', 'document'].includes(e)) return 'knowledge';
  return 'concept';
}

function styleForType(t){
  if (t === 'work') return { color:0x34d399, shape:'box', symbol:'W', layer:1, yBand:20 };
  if (t === 'identity') return { color:0xfbbf24, shape:'pentagon', symbol:'I', layer:0, yBand:42 };
  if (t === 'procedure') return { color:0xf97316, shape:'diamond', symbol:'P', layer:2, yBand:8 };
  if (t === 'decision') return { color:0xc084fc, shape:'triangle', symbol:'D', layer:2, yBand:-10 };
  if (t === 'risk') return { color:0xfb7185, shape:'cross', symbol:'!', layer:3, yBand:-24 };
  if (t === 'knowledge') return { color:0x22d3ee, shape:'hex', symbol:'K', layer:1, yBand:-8 };
  if (t === 'memory') return { color:0xa3e635, shape:'ring', symbol:'M', layer:3, yBand:28 };
  return { color:0x60a5fa, shape:'sphere', symbol:'C', layer:1, yBand:0 };
}

function edgeColor(type){
  if(type === 'supports') return 0x22c55e;
  if(type === 'contradicts') return 0xef4444;
  if(type === 'belongs_to') return 0xf59e0b;
  if(type === 'depends_on') return 0xa78bfa;
  return 0x93c5fd;
}

function build3DLayout(nodes){
  const rings = [45, 80, 115, 150];
  const grouped = new Map();
  for(const n of nodes){
    const t = n.nodeType || 'concept';
    if(!grouped.has(t)) grouped.set(t, []);
    grouped.get(t).push(n);
  }

  const placed = [];
  for(const [type, arr] of grouped.entries()){
    const st = styleForType(type);
    const radius = rings[Math.max(0, Math.min(rings.length - 1, st.layer ?? 1))];
    const yBase = st.yBand ?? 0;
    const count = arr.length || 1;
    for(let i=0;i<count;i++){
      const theta = (Math.PI * 2 * i) / count;
      const wobble = ((i % 5) - 2) * 2.2;
      placed.push({
        ...arr[i],
        x: Math.cos(theta) * radius,
        y: yBase + wobble,
        z: Math.sin(theta) * radius,
      });
    }
  }
  return placed;
}

function rotatePoint(x,y,z){
  x -= camX;
  y -= camY;
  z -= camZ;
  const cx = Math.cos(rotX), sx = Math.sin(rotX);
  const cy = Math.cos(rotY), sy = Math.sin(rotY);
  let yy = y*cx - z*sx;
  let zz = y*sx + z*cx;
  let xx = x*cy + zz*sy;
  zz = -x*sy + zz*cy;
  return {x:xx, y:yy, z:zz};
}

function project(p){
  const fov = 340 * zoom;
  const z = p.z + 260;
  const k = fov / Math.max(40, z);
  return {x: W/2 + p.x*k + panX, y: H/2 + p.y*k + panY, k, z};
}

function renderSide(node){
  const sel=document.getElementById('sel');
  const relBox=document.getElementById('rels');
  if(!node){ sel.textContent='Clicca un nodo nel grafo.'; relBox.innerHTML=''; return; }
  sel.innerHTML = `<div class="item"><strong>${node.label}</strong><div class="muted">${node.id}</div><div class="muted">type=${node.nodeType}</div></div>`;
  const rels = rawEdges.filter(e=>e.source_id===node.id||e.target_id===node.id);
  relBox.innerHTML = rels.map(r=>`<div class="item"><div><strong>${r.relation_type}</strong></div><div class="muted">${r.source_id.slice(0,6)} -> ${r.target_id.slice(0,6)}</div><div class="muted">conf=${r.confidence}</div></div>`).join('') || '<div class="muted">Nessuna relazione.</div>';
}

function draw(){
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle = '#081120';
  ctx.fillRect(0,0,W,H);
  if(!viewNodes.length) return;

  const nodeById = new Map(viewNodes.map(n => [n.id, n]));
  const edgeBudget = Math.min(rawEdges.length, MAX_RENDER_EDGES);

  // edges
  for(let idx = 0; idx < edgeBudget; idx++){
    const e = rawEdges[idx];
    const a = nodeById.get(e.source_id);
    const b = nodeById.get(e.target_id);
    if(!a || !b) continue;
    const col = edgeColor(e.relation_type).toString(16).padStart(6,'0');
    ctx.strokeStyle = '#' + col;
    ctx.globalAlpha = 0.55;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(a.sx, a.sy);
    ctx.lineTo(b.sx, b.sy);
    ctx.stroke();
  }

  // nodes (back to front)
  const sorted = [...viewNodes].sort((a,b)=>a.sz-b.sz).slice(0, MAX_RENDER_NODES);
  for(const n of sorted){
    const st = styleForType(n.nodeType);
    const col = st.color.toString(16).padStart(6,'0');
    const r = Math.max(2.8, 2.8 + n.scale * 2.2);
    const isFresh = n.justAddedUntil && n.justAddedUntil > Date.now();
    if(isFresh){
      ctx.globalAlpha = 0.22;
      ctx.fillStyle = '#f8fafc';
      ctx.beginPath();
      ctx.arc(n.sx, n.sy, r + 8, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1.0;
    ctx.fillStyle = '#' + col;
    if(st.shape === 'box'){
      ctx.fillRect(n.sx-r, n.sy-r, r*2, r*2);
    } else if(st.shape === 'pentagon'){
      ctx.beginPath();
      for(let i=0;i<5;i++){
        const a = -Math.PI/2 + i * (Math.PI*2/5);
        const x = n.sx + Math.cos(a)*r;
        const y = n.sy + Math.sin(a)*r;
        if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      }
      ctx.closePath();
      ctx.fill();
    } else if(st.shape === 'diamond'){
      ctx.beginPath();
      ctx.moveTo(n.sx, n.sy-r);
      ctx.lineTo(n.sx+r, n.sy);
      ctx.lineTo(n.sx, n.sy+r);
      ctx.lineTo(n.sx-r, n.sy);
      ctx.closePath();
      ctx.fill();
    } else if(st.shape === 'triangle'){
      ctx.beginPath();
      ctx.moveTo(n.sx, n.sy-r);
      ctx.lineTo(n.sx+r, n.sy+r);
      ctx.lineTo(n.sx-r, n.sy+r);
      ctx.closePath();
      ctx.fill();
    } else if(st.shape === 'cross'){
      const w = Math.max(2, r * 0.6);
      const b = Math.max(1.4, r * 0.28);
      ctx.fillRect(n.sx - b, n.sy - w, b * 2, w * 2);
      ctx.fillRect(n.sx - w, n.sy - b, w * 2, b * 2);
    } else if(st.shape === 'hex'){
      ctx.beginPath();
      for(let i=0;i<6;i++){
        const a = (Math.PI/3) * i;
        const x = n.sx + Math.cos(a)*r;
        const y = n.sy + Math.sin(a)*r;
        if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      }
      ctx.closePath();
      ctx.fill();
    } else if(st.shape === 'ring'){
      ctx.beginPath();
      ctx.arc(n.sx, n.sy, r, 0, Math.PI*2);
      ctx.fill();
      ctx.globalCompositeOperation = 'destination-out';
      ctx.beginPath();
      ctx.arc(n.sx, n.sy, Math.max(1.2, r*0.5), 0, Math.PI*2);
      ctx.fill();
      ctx.globalCompositeOperation = 'source-over';
    } else {
      ctx.beginPath(); ctx.arc(n.sx, n.sy, r, 0, Math.PI*2); ctx.fill();
    }
    if(st.symbol){
      ctx.fillStyle = '#ecf3ff';
      ctx.font = `${Math.max(8, Math.floor(r*1.15))}px Segoe UI`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(st.symbol, n.sx, n.sy+0.5);
    }
    if(selected && selected.id === n.id){
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(n.sx, n.sy, r+3, 0, Math.PI*2); ctx.stroke();
    }
  }
}

function rebuildView(){
  const laid = build3DLayout(rawNodes);
  viewNodes = laid.map(n => {
    const rp = rotatePoint(n.x, n.y, n.z);
    const pp = project(rp);
    return {
      ...n,
      sx: pp.x,
      sy: pp.y,
      sz: rp.z,
      scale: pp.k/6
    };
  });
  draw();
}

function pickNode(clientX, clientY){
  const rect = canvas.getBoundingClientRect();
  const x = clientX - rect.left;
  const y = clientY - rect.top;
  let best = null, bestD = 1e9;
  for(const n of viewNodes){
    const d2 = (n.sx-x)*(n.sx-x) + (n.sy-y)*(n.sy-y);
    if(d2 < 250 && d2 < bestD){ best = n; bestD = d2; }
  }
  return best;
}

function onPointerMove(ev){
  if(dragging){
    const dx = ev.clientX - lastX;
    const dy = ev.clientY - lastY;
    rotY += dx * 0.006;
    rotX += dy * 0.006;
    lastX = ev.clientX; lastY = ev.clientY;
    rebuildView();
    hoverTag.style.display = 'none';
    return;
  }
  const hit = pickNode(ev.clientX, ev.clientY);
  if(hit){
    hoverTag.style.display = 'block';
    hoverTag.style.left = (ev.clientX + 12) + 'px';
    hoverTag.style.top = (ev.clientY + 12) + 'px';
    hoverTag.textContent = `${hit.label} (${hit.nodeType})`;
  } else {
    hoverTag.style.display = 'none';
  }
}

function onClick(ev){
  const hit = pickNode(ev.clientX, ev.clientY);
  if(!hit){
    selected = null;
    renderSide(null);
    draw();
    return;
  }
  selected = hit;
  renderSide(selected);
  draw();
}

canvas.addEventListener('mousemove', onPointerMove);
canvas.addEventListener('mousedown', (ev)=>{ dragging=true; lastX=ev.clientX; lastY=ev.clientY; });
window.addEventListener('mouseup', ()=>{ dragging=false; });
canvas.addEventListener('mouseleave', ()=>{ dragging=false; hoverTag.style.display='none'; });
canvas.addEventListener('click', onClick);
canvas.addEventListener('wheel', (ev)=>{
  ev.preventDefault();
  zoom *= (ev.deltaY > 0 ? 1.06 : 0.94);
  zoom = Math.max(0.45, Math.min(2.4, zoom));
  rebuildView();
}, { passive:false });

window.addEventListener('keydown', (ev) => {
  keyState[ev.key] = true;
  const k = ev.key.toLowerCase();
  if(['w','a','s','d','q','e','arrowup','arrowdown','arrowleft','arrowright'].includes(k)){
    ev.preventDefault();
  }
});

window.addEventListener('keyup', (ev) => {
  keyState[ev.key] = false;
});

function stepControls(){
  const panStep = 6.0;
  const zoomStep = 0.04;
  const rotStep = 0.03;
  let changed = false;

  // Controlli assoluti rispetto allo schermo (indipendenti dalla rotazione camera)
  // W/S: avanti-indietro come zoom costante
  if(keyState['w'] || keyState['W']){ zoom *= (1 + zoomStep); changed = true; }
  if(keyState['s'] || keyState['S']){ zoom *= (1 - zoomStep); changed = true; }
  zoom = Math.max(0.45, Math.min(2.4, zoom));
  // A/D: pan orizzontale
  if(keyState['a'] || keyState['A']){ panX += panStep; changed = true; }
  if(keyState['d'] || keyState['D']){ panX -= panStep; changed = true; }
  // Q/E: pan verticale
  if(keyState['q'] || keyState['Q']){ panY += panStep; changed = true; }
  if(keyState['e'] || keyState['E']){ panY -= panStep; changed = true; }

  // Arrows rotation
  if(keyState['ArrowLeft']){ rotY -= rotStep; changed = true; }
  if(keyState['ArrowRight']){ rotY += rotStep; changed = true; }
  if(keyState['ArrowUp']){ rotX -= rotStep; changed = true; }
  if(keyState['ArrowDown']){ rotX += rotStep; changed = true; }

  if(changed){
    rebuildView();
    document.getElementById('stats').textContent =
      `${rawNodes.length} nodi, ${rawEdges.length} relazioni | cam(${camX.toFixed(0)},${camY.toFixed(0)},${camZ.toFixed(0)}) | pan(${panX.toFixed(0)},${panY.toFixed(0)})`;
  }
  requestAnimationFrame(stepControls);
}

async function reloadGraph(){
  async function fetchJson(url){
    const r = await fetch(url);
    return await r.json();
  }
  async function fetchChunk(ds, limit=220, pagesPerTick=1){
    if(ds.done) return 0;
    let fetched = 0;
    for(let i=0; i<pagesPerTick; i++){
      const sep = ds.url.includes('?') ? '&' : '?';
      const data = await fetchJson(`${ds.url}${sep}limit=${limit}&offset=${ds.offset}`);
      const items = data?.data?.items || [];
      if(!items.length){
        ds.done = true;
        break;
      }
      for(const item of items){
        if(!ds.byId.has(item.id)){
          ds.byId.set(item.id, item);
          ds.items.push(item);
        } else {
          ds.byId.set(item.id, item);
        }
      }
      ds.offset += items.length;
      fetched += items.length;
      if(items.length < limit){
        ds.done = true;
        break;
      }
    }
    return fetched;
  }

  const q=(document.getElementById('q').value||'').trim().toLowerCase();
  const relFilter=(document.getElementById('relTypeFilter').value||'').trim();
  try{
    const firstLoad = knownNodeIds.size === 0;
    const pagesPerTick = firstLoad ? 3 : 1;
    const loaders = Object.values(DATASETS).map(ds => fetchChunk(ds, 220, pagesPerTick));
    if(!selfModelCache){
      loaders.push(
        fetchJson('/api/v1/self-model').then(v => { selfModelCache = v; return 1; })
      );
    }
    await Promise.allSettled(loaders);

    const concepts = DATASETS.concepts.items;
    const relations = DATASETS.relations.items;
    const documents = DATASETS.documents.items;
    const notes = DATASETS.notes.items;
    const projects = DATASETS.projects.items;
    const goals = DATASETS.goals.items;
    const tasks = DATASETS.tasks.items;
    const decisions = DATASETS.decisions.items;
    const procedures = DATASETS.procedures.items;
    const episodes = DATASETS.episodes.items;
    const jobs = DATASETS.jobs.items;
    const memoryItems = DATASETS.memoryItems.items;
    const selfModel = selfModelCache;

  const nodes = [];
  const rawToGraph = new Map();
  const addNode = (entity, id, label, description='') => {
    if(!id) return;
    const graphId = `${entity}:${id}`;
    const nodeType = inferNodeTypeFromEntity(entity);
    const node = { id: graphId, rawId: id, entity, label: label || `${entity}:${id.slice(0,6)}`, description, nodeType };
    nodes.push(node);
    if(!rawToGraph.has(id)) rawToGraph.set(id, []);
    rawToGraph.get(id).push(graphId);
  };

  for(const c of concepts){ addNode('concept', c.id, c.name, c.description || ''); }
  for(const d of documents){ addNode('document', d.id, d.title || '(documento senza titolo)', `${d.source_type || ''} ${d.source_ref || ''}`); }
  for(const n of notes){ addNode('note', n.id, n.title, n.note_type || ''); }
  for(const p of projects){ addNode('project', p.id, p.name, p.description || ''); }
  for(const g of goals){ addNode('goal', g.id, g.title, g.status || ''); }
  for(const t of tasks){ addNode('task', t.id, t.title, t.status || ''); }
  for(const d of decisions){ addNode('decision', d.id, d.title, d.status || ''); }
  for(const p of procedures){ addNode('procedure', p.id, p.title, p.status || ''); }
  for(const e of episodes){ addNode('episode', e.id, e.title, e.outcome || ''); }
  for(const j of jobs){ addNode('job', j.id, j.job_type, j.status || ''); }
  for(const m of memoryItems){ addNode('memory_item', m.id, `${m.object_type}:${m.object_id.slice(0,8)}`, m.layer || ''); }
  if(selfModel?.data?.id){
    const s = selfModel.data;
    addNode('self_model', s.id, s.self_name || 'Self Model', s.self_role || '');
  }

  let filteredNodes = nodes;
  if(q){ filteredNodes = nodes.filter(n=>(n.label||'').toLowerCase().includes(q)); }
  const visibleIds = new Set(filteredNodes.map(n=>n.id));

  const edges = [];
  const pushEdge = (srcGraphId, dstGraphId, relationType, confidence=0.7, evidence='') => {
    if(!srcGraphId || !dstGraphId || srcGraphId === dstGraphId) return;
    const edge = {
      id: `${srcGraphId}|${relationType}|${dstGraphId}`,
      source_id: srcGraphId,
      target_id: dstGraphId,
      relation_type: relationType,
      confidence,
      evidence
    };
    edges.push(edge);
  };
  const connectByRaw = (srcRawId, dstRawId, relationType, confidence=0.8, evidence='') => {
    const srcList = rawToGraph.get(srcRawId) || [];
    const dstList = rawToGraph.get(dstRawId) || [];
    for(const s of srcList){
      for(const d of dstList){
        pushEdge(s, d, relationType, confidence, evidence);
      }
    }
  };

  // Explicit relations table
  for(const r of relations){
    connectByRaw(r.source_id, r.target_id, r.relation_type || 'related_to', r.confidence ?? 0.7, r.evidence || '');
  }
  // Structural links from FK fields
  for(const n of notes){ if(n.document_id) connectByRaw(n.id, n.document_id, 'belongs_to', n.confidence ?? 0.9, 'note.document_id'); }
  for(const g of goals){ if(g.project_id) connectByRaw(g.id, g.project_id, 'belongs_to', 0.95, 'goal.project_id'); }
  for(const t of tasks){
    if(t.project_id) connectByRaw(t.id, t.project_id, 'belongs_to', 0.95, 'task.project_id');
    if(t.goal_id) connectByRaw(t.id, t.goal_id, 'depends_on', 0.95, 'task.goal_id');
  }
  for(const d of decisions){ if(d.project_id) connectByRaw(d.id, d.project_id, 'belongs_to', 0.95, 'decision.project_id'); }
  for(const m of memoryItems){
    connectByRaw(m.id, m.object_id, 'indexes', m.confidence ?? 0.7, 'memory.object_id');
  }

  // Keep only edges fully visible.
  const dedup = new Map();
  for(const e of edges){
    if(!visibleIds.has(e.source_id) || !visibleIds.has(e.target_id)) continue;
    if(relFilter && e.relation_type !== relFilter) continue;
    if(!dedup.has(e.id)) dedup.set(e.id, e);
  }

    rawNodes = filteredNodes;
    rawEdges = Array.from(dedup.values());

    const nodeIdSet = new Set(rawNodes.map(n => n.id));
    const edgeIdSet = new Set(rawEdges.map(e => e.id));
    const newNodes = Array.from(nodeIdSet).filter(id => !knownNodeIds.has(id));
    const newEdges = Array.from(edgeIdSet).filter(id => !knownEdgeIds.has(id));
    knownNodeIds = nodeIdSet;
    knownEdgeIds = edgeIdSet;

    const nowTs = Date.now();
    const newNodeSet = new Set(newNodes);
    for(const n of rawNodes){
      if(newNodeSet.has(n.id)) n.justAddedUntil = nowTs + 7000;
    }

    selected = null;
    renderSide(null);
    rebuildView();
    const nodeWarn = rawNodes.length > MAX_RENDER_NODES ? ` | render nodi ${MAX_RENDER_NODES}/${rawNodes.length}` : '';
    const edgeWarn = rawEdges.length > MAX_RENDER_EDGES ? ` | render link ${MAX_RENDER_EDGES}/${rawEdges.length}` : '';
    const ds = Object.values(DATASETS);
    const doneCount = ds.filter(x => x.done).length;
    document.getElementById('stats').textContent = `${rawNodes.length} nodi, ${rawEdges.length} relazioni${newNodes.length || newEdges.length ? ` | +${newNodes.length} nodi, +${newEdges.length} link` : ''}${nodeWarn}${edgeWarn} | sync ${doneCount}/${ds.length}`;
  } catch(err){
    console.error('reloadGraph failed', err);
    document.getElementById('stats').textContent = `Errore caricamento grafo: ${err?.message || err}`;
  }
}

function resetGraphSync(){
  selfModelCache = null;
  knownNodeIds = new Set();
  knownEdgeIds = new Set();
  for(const ds of Object.values(DATASETS)){
    ds.items = [];
    ds.byId = new Map();
    ds.offset = 0;
    ds.done = false;
  }
}

resetGraphSync();
reloadGraph();
stepControls();
document.getElementById('q').addEventListener('keydown', (e)=>{ if(e.key==='Enter') reloadGraph(); });
document.getElementById('relTypeFilter').addEventListener('change', reloadGraph);

function setLiveMode(){
  if(liveTimer) clearInterval(liveTimer);
  const live = document.getElementById('liveMode').checked;
  if(live){
    liveTimer = setInterval(reloadGraph, 5000);
  }
}
document.getElementById('liveMode').addEventListener('change', setLiveMode);
setLiveMode();

    </script>
</body>
</html>
"""


@router.get("/chat", response_class=HTMLResponse)
def chat_view():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ebby Chat</title>
  <style>
    :root{
      --bg:#090f1a;
      --bg-soft:#101a2a;
      --panel:rgba(15, 24, 39, 0.78);
      --line:rgba(152, 179, 219, 0.22);
      --text:#e6edf8;
      --muted:#9fb0ca;
      --user:#1d4ed8;
      --ebby:#0f766e;
      --accent:#2f80ff;
      --accent2:#5da4ff;
    }
    * { box-sizing:border-box; }
    body{
      margin:0;
      font-family:"Aptos","Bahnschrift","Segoe UI Variable",sans-serif;
      background:
        radial-gradient(1200px 460px at -5% -5%, #1f3f79 0%, transparent 60%),
        radial-gradient(900px 380px at 120% 0%, #174865 0%, transparent 58%),
        var(--bg);
      color:var(--text);
    }
    .wrap{
      max-width:1000px;
      margin:0 auto;
      height:calc(100vh - 88px);
      display:grid;
      grid-template-rows:auto 1fr auto;
      gap:10px;
      padding:88px 12px 12px;
    }
    .header-area{ display:flex; flex-direction:column; gap:0; }
    .topnav{
      position:fixed;
      top:12px;
      left:50%;
      transform:translateX(-50%);
      z-index:1000;
      width:min(1280px, calc(100vw - 24px));
      min-height:56px;
      background:var(--panel);
      border:1px solid var(--line);
      border-radius:14px;
      padding:10px 12px;
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:12px;
      flex-wrap:wrap;
      backdrop-filter: blur(10px);
    }
    .topnav .brand{ font-weight:700; letter-spacing:.2px; }
    .topnav .links{ display:flex; gap:8px; flex-wrap:wrap; }
    .topnav .links a{
      color:var(--text);
      text-decoration:none;
      padding:6px 10px;
      border:1px solid var(--line);
      border-radius:999px;
      background:var(--bg-soft);
      font-size:13px;
    }
    .topnav .links a.active{
      background:linear-gradient(135deg, var(--accent), var(--accent2));
      color:#fff;
      border-color:transparent;
    }
    .top{
      background:var(--panel);
      border:1px solid var(--line);
      border-radius:16px;
      padding:10px;
      display:flex;
      gap:10px;
      align-items:center;
      justify-content:space-between;
      flex-wrap:wrap;
      backdrop-filter: blur(10px);
    }
    .top a{ color:var(--accent2); text-decoration:none; }
    .opts{
      display:flex;
      gap:10px;
      align-items:center;
      color:var(--muted);
      font-size:13px;
    }
    .chat{
      background:var(--panel);
      border:1px solid var(--line);
      border-radius:16px;
      padding:12px;
      overflow:auto;
      display:flex;
      flex-direction:column;
      gap:10px;
      backdrop-filter: blur(10px);
    }
    .msg{
      max-width:88%;
      padding:10px 12px;
      border-radius:10px;
      border:1px solid #284166;
      white-space:pre-wrap;
      line-height:1.35;
    }
    .user{ align-self:flex-end; background:color-mix(in srgb,var(--user) 35%, transparent); }
    .ebby{ align-self:flex-start; background:color-mix(in srgb,var(--ebby) 30%, transparent); }
    .meta{ font-size:12px; color:var(--muted); margin-top:6px; }
    .composer{
      display:grid;
      grid-template-columns:1fr auto;
      gap:8px;
    }
    textarea{
      width:100%;
      min-height:62px;
      max-height:180px;
      resize:vertical;
      padding:10px;
      border-radius:10px;
      border:1px solid var(--line);
      background:var(--bg-soft);
      color:var(--text);
      font:inherit;
    }
    button{
      padding:0 16px;
      border:none;
      border-radius:10px;
      background:linear-gradient(135deg, var(--accent), var(--accent2));
      color:#fff;
      font-weight:600;
      cursor:pointer;
    }
    button:hover{ filter:brightness(1.06); }
    button:disabled{ opacity:.55; cursor:not-allowed; }
    .status{
      color:var(--muted);
      font-size:12px;
      text-align:right;
      padding-right:4px;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <!-- header + comandi: un solo elemento nella griglia -->
    <div class="header-area">
      <div class="topnav">
        <div class="brand">Ebby UI</div>
        <div class="links">
          <a href="/api/v1/ui/dashboard">Dashboard</a>
          <a href="/api/v1/ui/graph">Graph</a>
          <a href="/api/v1/ui/chat" class="active">Chat</a>
          <a href="/api/v1/ui/audit">Audit</a>
        </div>
      </div>
      <div class="top">
        <div><span style="color:var(--muted)">domande, risposte e comandi diretti</span></div>
        <div class="opts">
          <label><input type="checkbox" id="autoSave" checked> auto-salva su Ebby</label>
          <button style="padding:4px 10px;font-size:12px" onclick="toggleCmds()">Comandi</button>
        </div>
      </div>
      <div id="cmdHelp" style="display:none;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px;margin-top:8px;font-size:12px;color:var(--muted);line-height:1.8">
        <strong style="color:var(--text)">Comandi disponibili:</strong><br>
        <code>importa https://...</code> — importa il contenuto di un sito web<br>
        <code>importa testo: [testo]</code> — importa testo come documento<br>
        <code>crea nota: [testo]</code> — crea una nota nella knowledge base<br>
        <code>crea task: [titolo]</code> — crea un task<br>
        <code>cerca: [query]</code> — cerca nella knowledge base<br>
        <code>conoscenze pendenti</code> — elenca documenti/note non ancora compresi<br>
        <code>elabora tutto</code> — processa, indicizza ed estrae concetti da tutto il contenuto<br>
        <code>backup</code> — esegui un backup del database<br>
        <code>memoria auto</code> — aggiorna i livelli di memoria<br>
        <code>stato</code> — visualizza lo stato del sistema<br>
        <em>Oppure scrivi normalmente: Ebby risponde e impara da ogni messaggio. Per iterazioni tecniche profonde (multi-file, test, refactor), usa preferibilmente un ambiente agentico in IDE.</em>
      </div>
    </div>

    <div id="chatLog" class="chat"></div>

    <div>
      <div class="composer">
        <textarea id="message" placeholder="Scrivi una domanda oppure: importa https://... | crea nota: ... | cerca: ... | backup | stato"></textarea>
        <button id="sendBtn" onclick="sendMessage()">Invia</button>
      </div>
      <div id="status" class="status">Pronto.</div>
    </div>
  </div>

<script>
const log = document.getElementById('chatLog');
const input = document.getElementById('message');
const statusEl = document.getElementById('status');
const sendBtn = document.getElementById('sendBtn');
const autoSave = document.getElementById('autoSave');

function toggleCmds(){
  const el = document.getElementById('cmdHelp');
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

function stamp(){
  const d = new Date();
  return d.toLocaleString('it-IT');
}

function setStatus(msg){ statusEl.textContent = msg; }

function appendMessage(role, text, meta){
  const box = document.createElement('div');
  box.className = `msg ${role}`;
  box.textContent = text;
  if(meta){
    const m = document.createElement('div');
    m.className = 'meta';
    m.textContent = meta;
    box.appendChild(m);
  }
  log.appendChild(box);
  log.scrollTop = log.scrollHeight;
}

async function api(url, options){
  const res = await fetch(url, options);
  const data = await res.json().catch(()=> ({}));
  if(!res.ok){
    throw new Error((data && data.error && data.error.message) || `HTTP ${res.status}`);
  }
  return data;
}

async function saveTurn(question, answer, confidence){
  const title = `Chat Ebby ${new Date().toISOString()}`;
  const body = `## Domanda\\n${question}\\n\\n## Risposta\\n${answer}`;
  const payload = {
    note_type: 'chat_turn',
    title: title,
    body_markdown: body,
    source_type: 'chat',
    epistemic_type: 'fact',
    confidence: Math.max(0, Math.min(1, Number(confidence || 0.7)))
  };
  const data = await api('/api/v1/notes', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  return data?.data?.id || null;
}

async function sendMessage(){
  const message = (input.value || '').trim();
  if(!message){ return; }
  sendBtn.disabled = true;
  appendMessage('user', message, `Tu • ${stamp()}`);
  input.value = '';
  setStatus('Ebby sta rispondendo...');
  try{
    const resp = await api('/api/v1/chat/query', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ message })
    });
    const answer = resp?.answer || '(nessuna risposta)';
    const ru = resp?.token_usage || {};
    const rr = resp?.response_report || {};
    const certainty = rr?.certainty || 'n/a';
    const source = rr?.source || 'n/a';
    const action = rr?.action || 'nessuna';
    const totalTokens = (ru?.total_tokens ?? 'n/a');
    const tokenSource = ru?.source || 'n/a';
    const meta = `Ebby ? conf ${resp?.confidence ?? 'n/a'} ? certezza ${certainty} ? fonte ${source} ? azione ${action} ? token ${totalTokens} (${tokenSource}) ? ${stamp()}`;
    appendMessage('ebby', answer, meta);
    setStatus('Risposta ricevuta.');
    if(autoSave.checked){
      try{
        await saveTurn(message, answer, resp?.confidence);
      }catch(_){}
    }
  }catch(e){
    appendMessage('ebby', 'Errore: ' + e.message, `Ebby • ${stamp()}`);
    setStatus('Errore durante la richiesta.');
  }finally{
    sendBtn.disabled = false;
    input.focus();
  }
}

input.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter' && !e.shiftKey){
    e.preventDefault();
    sendMessage();
  }
});

appendMessage(
  'ebby',
  `Chat Ebby attiva.

Comandi: importa https://URL | importa testo: ... | crea nota: ... | crea task: ... | cerca: ... | backup | memoria auto | stato

Oppure scrivi normalmente: rispondo e imparo.

Nota: per sviluppo esteso e iterazione LLM avanzata, usa un'interfaccia agentica in IDE (questa chat ha limiti operativi naturali).`,
  `Ebby ? ${stamp()}`
);
</script>
</body>
</html>
"""


