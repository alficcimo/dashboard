const fs = require('fs');
const path = require('path');

// Read the index.html file
const htmlPath = path.join(__dirname, 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

// Find the MULTILINE_COLS definition
const multilineCOlsMatch = htmlContent.match(/MULTILINE_COLS\s*=\s*new\s+Set\s*\(\s*\[\s*([^\]]+)\s*\]\s*\)/);

if (multilineCOlsMatch) {
  const columnsStr = multilineCOlsMatch[1];
  console.log('✅ MULTILINE_COLS found!');
  console.log('Columns: [' + columnsStr + ']');
  
  // Check if 'caption' is in the set
  if (columnsStr.includes("'caption'") || columnsStr.includes('"caption"')) {
    console.log('\n✅ SUCCESS! "caption" is in MULTILINE_COLS');
    console.log('   Caption cells will now preserve whitespace and line breaks!');
  } else {
    console.log('\n❌ ERROR: "caption" is NOT in MULTILINE_COLS');
    console.log('   Fix was not applied correctly.');
  }
} else {
  console.log('❌ MULTILINE_COLS definition not found in index.html');
}

// Also verify the whitespace-pre-wrap CSS is applied
const whitespaceCSSMatch = htmlContent.match(/whitespace-pre-wrap/g);
if (whitespaceCSSMatch) {
  console.log(`\n✅ Found ${whitespaceCSSMatch.length} references to 'whitespace-pre-wrap' CSS class`);
  console.log('   This CSS preserves paragraph structure and line breaks.');
}
