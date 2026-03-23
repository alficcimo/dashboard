const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const deployDir = 'C:\\Users\\maxim\\ClaudeOS\\Content\\deploy';
process.chdir(deployDir);

let output = '=== COMPREHENSIVE DIAGNOSTIC & PUSH REPORT ===\n\n';
const timestamp = new Date().toISOString();
output += `Generated: ${timestamp}\n`;
output += `Directory: ${deployDir}\n\n`;

// Helper function to run commands
function runCmd(cmd, label) {
  output += `\n--- ${label} ---\n`;
  try {
    const result = execSync(cmd, { encoding: 'utf8', stdio: 'pipe' });
    output += result || '(no output)';
  } catch (e) {
    output += `Error: ${e.message}\n`;
    output += `Code: ${e.code}\n`;
    if (e.stderr) output += `Stderr: ${e.stderr}\n`;
  }
}

// Diagnostics
runCmd('git remote -v', 'Git Remote Configuration');
runCmd('git status', 'Git Status');
runCmd('git branch -a', 'Git Branches');
runCmd('git log --oneline -5', 'Git Log (last 5 commits)');
runCmd('git config --list | findstr remote', 'Git Config (remotes only)');

// List files
output += '\n--- Local HTML/MD Files ---\n';
const files = fs.readdirSync(deployDir)
  .filter(f => f.endsWith('.html') || f.endsWith('.md') || f.endsWith('.txt'))
  .sort();
files.forEach(f => {
  const stat = fs.statSync(path.join(deployDir, f));
  const date = new Date(stat.mtime).toISOString();
  output += `${f.padEnd(30)} ${stat.size.toString().padStart(8)} bytes  ${date}\n`;
});

// Try pushing with verbose output
output += '\n--- Attempting Git Push ---\n';
try {
  const result = execSync('git push -v 2>&1', { encoding: 'utf8', stdio: 'pipe', shell: 'powershell.exe' });
  output += result || 'Push completed (no output)';
} catch (e) {
  output += `Push attempt failed:\n`;
  output += `Error: ${e.message}\n`;
  output += `Code: ${e.code}\n`;
  if (e.stdout) output += `Stdout: ${e.stdout}\n`;
  if (e.stderr) output += `Stderr: ${e.stderr}\n`;
}

// Check for GitHub CLI
output += '\n--- GitHub CLI Status ---\n';
try {
  const ghVersion = execSync('.\\gh_cli\\bin\\gh.exe --version', { encoding: 'utf8' });
  output += `GitHub CLI: ${ghVersion}`;
  
  const ghAuth = execSync('.\\gh_cli\\bin\\gh.exe auth status', { encoding: 'utf8' });
  output += `Auth Status: ${ghAuth}`;
  
  // Try gh push
  output += '\n--- Attempting GitHub CLI Push ---\n';
  try {
    const ghPush = execSync('.\\gh_cli\\bin\\gh.exe repo sync', { encoding: 'utf8' });
    output += `GitHub CLI sync: ${ghPush}`;
  } catch (e) {
    output += `GH sync failed: ${e.message}\n`;
  }
} catch (e) {
  output += `GitHub CLI not working: ${e.message}\n`;
}

// Write report
const reportPath = path.join(deployDir, 'COMPLETE_DIAGNOSTIC.txt');
fs.writeFileSync(reportPath, output);
console.log('Diagnostic report saved to COMPLETE_DIAGNOSTIC.txt');
console.log(`Total output: ${output.length} characters`);
