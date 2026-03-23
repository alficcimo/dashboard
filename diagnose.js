const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const deployDir = 'C:\\Users\\maxim\\ClaudeOS\\Content\\deploy';
process.chdir(deployDir);

console.log('=== DIAGNOSTIC REPORT ===\n');

// Read log files
const logFiles = ['gh_test.log', 'push_results.log'];
for (const logFile of logFiles) {
  const filePath = path.join(deployDir, logFile);
  if (fs.existsSync(filePath)) {
    console.log(`\n--- ${logFile} ---`);
    const content = fs.readFileSync(filePath, 'utf8');
    console.log(content);
  } else {
    console.log(`\n${logFile} not found`);
  }
}

// Try git commands
console.log('\n--- Git Commands ---');
try {
  const remote = execSync('git remote -v', { encoding: 'utf8' });
  console.log('GIT REMOTE:\n', remote);
} catch (e) {
  console.log('Error getting remote:', e.message);
}

try {
  const status = execSync('git status', { encoding: 'utf8' });
  console.log('GIT STATUS:\n', status);
} catch (e) {
  console.log('Error getting status:', e.message);
}

try {
  const log = execSync('git log --oneline -5', { encoding: 'utf8' });
  console.log('GIT LOG (last 5):\n', log);
} catch (e) {
  console.log('Error getting log:', e.message);
}

// List HTML files
console.log('\n--- HTML Files in Directory ---');
const files = fs.readdirSync(deployDir).filter(f => f.endsWith('.html') || f.endsWith('.md'));
files.forEach(f => {
  const stat = fs.statSync(path.join(deployDir, f));
  console.log(`${f}: ${stat.size} bytes`);
});

console.log('\n=== END DIAGNOSTIC ===');

// Save to file for verification
fs.writeFileSync('diagnostic_output.txt', '\n--- Diagnostic completed successfully ---');
