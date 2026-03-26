const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'index.html');
const content = fs.readFileSync(filePath, 'utf8');

// Print first 100 lines to understand structure
const lines = content.split('\n');
lines.forEach((line, idx) => {
  if (idx < 100) {
    console.log(`${idx + 1}: ${line}`);
  }
});
