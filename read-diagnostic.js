const fs = require('fs');
const path = require('path');

const deployDir = 'C:\\Users\\maxim\\ClaudeOS\\Content\\deploy';
const reportPath = path.join(deployDir, 'COMPLETE_DIAGNOSTIC.txt');

if (fs.existsSync(reportPath)) {
  const content = fs.readFileSync(reportPath, 'utf8');
  console.log(content);
  
  // Also analyze and create summary
  const lines = content.split('\n');
  const summary = [];
  
  // Look for key information
  for (const line of lines) {
    if (line.includes('remote') || 
        line.includes('branch') || 
        line.includes('Error') ||
        line.includes('fatal') ||
        line.includes('Auth') ||
        line.includes('push')) {
      summary.push(line);
    }
  }
  
  if (summary.length > 0) {
    console.log('\n\n=== KEY FINDINGS ===');
    summary.forEach(line => {
      if (line.trim()) console.log(line);
    });
  }
} else {
  console.log('COMPLETE_DIAGNOSTIC.txt not found');
}
