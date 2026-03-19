const fs = require('fs');
const path = require('path');

// Read all JSON files
const tabs = [
  { id: 'ideas', file: 'content-ideas.json' },
  { id: 'analyzed', file: 'content-analyzed.json' },
  { id: 'titles', file: 'content-titles.json' },
  { id: 'title_analyzer', file: 'content-title-analyzer.json' },
  { id: 'captions', file: 'content-captions.json' },
  { id: 'carousels', file: 'content-carousels.json' },
  { id: 'feed', file: 'content-feed.json' },
  { id: 'improver', file: 'content-improver.json' },
];

const dataMap = {};
tabs.forEach(tab => {
  try {
    const data = JSON.parse(fs.readFileSync(tab.file, 'utf-8'));
    dataMap[tab.id] = data;
  } catch (e) {
    dataMap[tab.id] = [];
  }
});

// Read the original HTML
const html = fs.readFileSync('index.html', 'utf-8');

// Find where to inject the data
const injectionPoint = "const TABS = [";
const updatedHtml = html.replace(
  injectionPoint,
  `const EMBEDDED_DATA = ${JSON.stringify(dataMap)};\n\n    ${injectionPoint}`
);

// Modify fetchAllData to use embedded data with fallback to live fetch
const newFetchFunction = `
    async function fetchAllData() {
      const results = {};
      await Promise.all(
        TABS.map(async tab => {
          try {
            // Try live fetch first
            const res = await fetch(tab.file + '?_=' + Date.now());
            if (res.ok) {
              results[tab.id] = await res.json();
              return;
            }
          } catch {}
          // Fallback to embedded data
          results[tab.id] = EMBEDDED_DATA[tab.id] || [];
        })
      );
      return results;
    }
`;

const finalHtml = updatedHtml.replace(
  /async function fetchAllData\(\) \{[\s\S]*?return results;\s*\}/,
  newFetchFunction
);

fs.writeFileSync('standalone.html', finalHtml);
console.log('✅ Created standalone.html with embedded data!');
