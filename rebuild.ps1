
# Read the EMBEDDED_DATA line from original file
$lines = Get-Content 'C:\Users\maxim\ClaudeOS\Content\deploy\index.html'
$embeddedLine = $lines[55].Trim()  # line 56 (0-indexed=55): const EMBEDDED_DATA = {...}

$part1 = @'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Content Farm Dashboard</title>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
  <div id="root"></div>
  <script>
    const COLUMN_DEFS = {
      ideas:          ['date','source','idea'],
      analyzed:       ['idea','psychology','energy','king','magic_pill','summary'],
      titles:         ['date','title'],
      title_analyzer: ['date','original_title','improved_title','issues_found','virality_after','changes_made'],
      captions:       ['date','title','caption'],
      carousels:      ['title','carousel','caption_under'],
      feed:           ['date','social_url','title','views'],
      improver:       ['social_url','original_title','improved_title','issues_found','virality_before','virality_after','changes_made','status']
    };
    const MULTILINE_COLS = new Set([
      'caption','carousel','caption_under','caption_preview',
      'reels_structure','carousel_slides','stories_hook','stories_cta',
      'adapted_hook','core_angle','reels_hook','carousel_hook','issues_found','changes_made'
    ]);
'@

$part2 = @'

    const TABS = [
      { id: 'ideas',          label: 'Ideas',          file: 'content-ideas.json' },
      { id: 'analyzed',       label: 'Analyzed',       file: 'content-analyzed.json' },
      { id: 'titles',         label: 'Titles',         file: 'content-titles.json' },
      { id: 'title_analyzer', label: 'Title Analyzer', file: 'content-title-analyzer.json' },
      { id: 'captions',       label: 'Captions',       file: 'content-captions.json' },
      { id: 'carousels',      label: 'Carousels',      file: 'content-carousels.json' },
      { id: 'feed',           label: 'Feed Analyzer',  file: 'content-feed.json' },
      { id: 'improver',       label: 'Improver',       file: 'content-improver.json' }
    ];
    const POLL_INTERVAL_MS = 30000;

    async function fetchAllData() {
      const results = {};
      await Promise.all(TABS.map(async tab => {
        try {
          const res = await fetch(tab.file + '?_=' + Date.now());
          if (res.ok) { results[tab.id] = await res.json(); return; }
        } catch {}
        results[tab.id] = EMBEDDED_DATA[tab.id] || [];
      }));
      return results;
    }

    const e = React.createElement;

    function SyncIndicator({ lastSync, polling }) {
      const [elapsed, setElapsed] = React.useState(0);
      React.useEffect(() => {
        if (!lastSync) return;
        const iv = setInterval(() => setElapsed(Math.floor((Date.now() - lastSync) / 1000)), 1000);
        return () => clearInterval(iv);
      }, [lastSync]);
      if (!lastSync) return e('span', {className: 'text-xs text-gray-400'}, polling ? 'Loading...' : 'No connection');
      const color = elapsed < 35 ? 'text-green-600' : elapsed < 70 ? 'text-yellow-600' : 'text-red-500';
      return e('span', {className: 'text-xs font-medium flex items-center gap-1 ' + color},
        e('span', {className: 'inline-block w-2 h-2 rounded-full bg-current'}),
        elapsed < 5 ? 'Just updated' : 'Updated ' + elapsed + 's ago',
        ' \u00b7 ',
        e('span', {className: 'text-gray-400 font-normal'}, 'auto-refresh every 30s')
      );
    }

    function TabBar({ activeTab, rowCounts, onTabChange }) {
      return e('div', {className: 'flex border-b border-gray-300 bg-white overflow-x-auto sticky top-0 z-10 shadow-sm'},
        TABS.map(function(tab) {
          const count = rowCounts[tab.id] != null ? rowCounts[tab.id] : 0;
          const isActive = activeTab === tab.id;
          return e('button', {
            key: tab.id,
            onClick: function() { onTabChange(tab.id); },
            className: 'px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ' +
              (isActive ? 'border-blue-500 text-blue-600 bg-blue-50' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50')
          },
            tab.label,
            count > 0 ? e('span', {
              className: 'ml-2 px-2 py-0.5 rounded-full text-xs font-semibold ' +
                (isActive ? 'bg-blue-100 text-blue-700' : 'bg-gray-200 text-gray-600')
            }, count) : null
          );
        })
      );
    }

    function DropZone({ onLoad, error, setError }) {
      const inputRef = React.useRef(null);
      const [dragging, setDragging] = React.useState(false);
      function processFile(file) {
        if (!file) return;
        if (file.size > 5*1024*1024) { setError('File too large (max 5MB)'); return; }
        if (!file.name.toLowerCase().endsWith('.json')) { setError('Must be a .json file'); return; }
        const reader = new FileReader();
        reader.onload = ev => {
          try {
            const parsed = JSON.parse(ev.target.result);
            if (!Array.isArray(parsed)) throw new Error('must be array');
            setError(null); onLoad(parsed);
          } catch { setError('Invalid JSON file'); }
        };
        reader.readAsText(file);
      }
      return e('div', {className: 'px-4 pt-3 pb-1'},
        e('div', {
          onClick: () => inputRef.current && inputRef.current.click(),
          onDragOver: ev => { ev.preventDefault(); setDragging(true); },
          onDragLeave: () => setDragging(false),
          onDrop: ev => { ev.preventDefault(); setDragging(false); processFile(ev.dataTransfer.files[0]); },
          className: 'border-2 border-dashed rounded-lg p-3 text-center cursor-pointer transition-colors ' +
            (dragging ? 'border-blue-400 bg-blue-50' : error ? 'border-red-400 bg-red-50' : 'border-gray-200 bg-white hover:border-blue-300 hover:bg-blue-50')
        },
          error ? e('p', {className: 'text-red-600 text-xs font-medium'}, error)
                : e('p', {className: 'text-gray-400 text-xs'}, dragging ? 'Drop it!' : 'Drop JSON to merge or click to upload'),
          e('input', {ref: inputRef, type: 'file', accept: '.json,.JSON', className: 'hidden',
            onChange: ev => processFile(ev.target.files[0])})
        )
      );
    }

    function DataTable({ tabId, rows, isManual, onClearManual }) {
      const columns = COLUMN_DEFS[tabId] || [];
      const headerCells = [
        e('th', {key:'#', className:'px-3 py-2 text-left font-semibold text-gray-600 border border-gray-300 bg-gray-100 whitespace-nowrap text-xs'}, '#')
      ].concat(columns.map(col =>
        e('th', {key:col, className:'px-3 py-2 text-left font-semibold text-gray-600 border border-gray-300 bg-gray-100 whitespace-nowrap text-xs'}, col)
      ));
      const bodyRows = rows.length === 0
        ? [e('tr', {key:'empty'}, e('td', {colSpan: columns.length+1, className:'px-3 py-8 text-center text-gray-400 text-sm'}, 'No data yet. Run the skill to populate this tab.'))]
        : rows.map((row, i) => {
            const cells = [
              e('td', {key:'#', className:'px-3 py-2 border border-gray-200 text-gray-400 text-xs select-none'}, i+1)
            ].concat(columns.map(col =>
              e('td', {key:col, className:'px-3 py-2 border border-gray-200 text-gray-800 align-top max-w-xs ' +
                (MULTILINE_COLS.has(col) ? 'whitespace-pre-wrap' : 'whitespace-normal')},
                row[col] != null ? row[col] : '')
            ));
            return e('tr', {key:i, className: i%2===0 ? 'bg-white' : 'bg-gray-50'}, cells);
          });
      return e('div', null,
        isManual ? e('div', {className:'px-4 py-1.5 bg-amber-50 border-b border-amber-200 flex items-center justify-between'},
          e('span', {className:'text-xs text-amber-700 font-medium'}, 'Merged: uploaded + live \u2014 ' + rows.length + ' rows'),
          e('button', {onClick: onClearManual, className:'text-xs text-amber-600 hover:text-amber-800 underline'}, 'Remove upload')
        ) : null,
        e('div', {className:'overflow-x-auto'},
          e('table', {className:'min-w-full text-sm border-collapse'},
            e('thead', null, e('tr', null, headerCells)),
            e('tbody', null, bodyRows)
          )
        )
      );
    }

    function mergeRows(uploaded, live) {
      const seen = new Set(live.map(r => JSON.stringify(r)));
      return uploaded.filter(r => !seen.has(JSON.stringify(r))).concat(live);
    }

    function TabPanel({ tabId, liveRows }) {
      const [merged, setMerged] = React.useState(null);
      const [error,  setError]  = React.useState(null);
      const manualRef           = React.useRef(null);
      React.useEffect(() => {
        if (manualRef.current) setMerged(mergeRows(manualRef.current, liveRows));
      }, [liveRows]);
      function handleUpload(up) { manualRef.current = up; setMerged(mergeRows(up, liveRows)); setError(null); }
      function handleClear()    { manualRef.current = null; setMerged(null); setError(null); }
      const rows     = merged != null ? merged : liveRows;
      const isManual = merged != null;
      return e('div', null,
        e(DropZone,  {onLoad: handleUpload, error, setError}),
        e(DataTable, {tabId, rows, isManual, onClearManual: handleClear})
      );
    }

    function App() {
      const [activeTab, setActiveTab] = React.useState('ideas');
      const [data,      setData]      = React.useState(() => { const d={}; TABS.forEach(t=>d[t.id]=[]); return d; });
      const [lastSync,  setLastSync]  = React.useState(null);
      const [polling,   setPolling]   = React.useState(false);
      const [isLocal,   setIsLocal]   = React.useState(false);

      React.useEffect(() => { if (window.location.protocol === 'file:') setIsLocal(true); }, []);

      React.useEffect(() => {
        if (isLocal) return;
        function load() {
          setPolling(true);
          fetchAllData()
            .then(r => { setData(r); setLastSync(Date.now()); })
            .catch(() => {})
            .finally(() => setPolling(false));
        }
        load();
        const timer = setInterval(load, POLL_INTERVAL_MS);
        return () => clearInterval(timer);
      }, [isLocal]);

      const rowCounts = React.useMemo(() => {
        const c = {}; TABS.forEach(t => c[t.id] = (data[t.id]||[]).length); return c;
      }, [data]);

      if (isLocal) {
        return e('div', {className:'min-h-screen bg-gray-50 flex items-center justify-center'},
          e('div', {className:'bg-white rounded-xl shadow p-10 max-w-md text-center'},
            e('h2', {className:'text-xl font-bold text-gray-800 mb-2'}, 'Open Online'),
            e('p',  {className:'text-gray-500 text-sm mb-4'}, 'Open it via GitHub Pages for live data.'),
            e('a',  {href:'https://alficcimo.github.io/dashboard/', className:'inline-block bg-blue-600 text-white px-5 py-2 rounded-lg text-sm font-medium'}, 'Open Dashboard')
          )
        );
      }

      return e('div', {className:'min-h-screen bg-gray-50'},
        e('div', {className:'bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between'},
          e('div', null,
            e('h1', {className:'text-lg font-bold text-gray-800'}, 'Content Farm Dashboard'),
            e('p',  {className:'text-xs text-gray-500'}, '@novaya_energia \u2014 Max Kibrik')
          ),
          e(SyncIndicator, {lastSync, polling})
        ),
        e(TabBar, {activeTab, rowCounts, onTabChange: setActiveTab}),
        TABS.map(tab => activeTab === tab.id
          ? e(TabPanel, {key: tab.id, tabId: tab.id, liveRows: data[tab.id]||[]})
          : null
        )
      );
    }

    const rootEl = ReactDOM.createRoot(document.getElementById('root'));
    rootEl.render(e(App, null));
  </script>
</body>
</html>
'@

$newHtml = $part1 + "`n    " + $embeddedLine + "`n" + $part2
[System.IO.File]::WriteAllText('C:\Users\maxim\ClaudeOS\Content\deploy\index.html', $newHtml, [System.Text.Encoding]::UTF8)

$info = Get-Item 'C:\Users\maxim\ClaudeOS\Content\deploy\index.html'
$lineCount = (Get-Content 'C:\Users\maxim\ClaudeOS\Content\deploy\index.html').Count
Write-Output "Done. Size: $($info.Length) bytes, Lines: $lineCount"
