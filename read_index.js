const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');
const lines = content.split('\n');
console.log('=== Lines 30-50 ===');
lines.slice(30, 50).forEach((l, i) => {
  console.log((31+i) + ': ' + l);
});
console.log('\n=== Lines 60-80 ===');
lines.slice(60, 80).forEach((l, i) => {
  console.log((61+i) + ': ' + l);
});
