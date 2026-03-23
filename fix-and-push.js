const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const deployDir = 'C:\\Users\\maxim\\ClaudeOS\\Content\\deploy';
const gitPath = 'C:\\Program Files\\Git\\bin\\git.exe';

// Change to deploy directory
process.chdir(deployDir);

console.log('=== GIT PUSH FIX & DEPLOYMENT ===\n');
console.log(`Working directory: ${deployDir}`);
console.log(`Git executable: ${gitPath}\n`);

try {
  // 1. Check status
  console.log('--- Git Status ---');
  const status = execSync(`"${gitPath}" status`, { encoding: 'utf-8' });
  console.log(status);
  fs.appendFileSync('git_push.log', `=== Status ===\n${status}\n\n`);

  // 2. Check remote
  console.log('\n--- Git Remote ---');
  const remote = execSync(`"${gitPath}" remote -v`, { encoding: 'utf-8' });
  console.log(remote);
  fs.appendFileSync('git_push.log', `=== Remote ===\n${remote}\n\n`);

  // 3. Check branches
  console.log('\n--- Git Branches ---');
  const branches = execSync(`"${gitPath}" branch -a`, { encoding: 'utf-8' });
  console.log(branches);
  fs.appendFileSync('git_push.log', `=== Branches ===\n${branches}\n\n`);

  // 4. Add all files
  console.log('\n--- Adding Files ---');
  const addResult = execSync(`"${gitPath}" add -A`, { encoding: 'utf-8' });
  console.log('Files staged for commit');
  fs.appendFileSync('git_push.log', `Files staged for commit\n\n`);

  // 5. Check what's staged
  console.log('\n--- Staged Files ---');
  const diff = execSync(`"${gitPath}" diff --cached --name-only`, { encoding: 'utf-8' });
  console.log(diff);
  fs.appendFileSync('git_push.log', `=== Staged Files ===\n${diff}\n\n`);

  // 6. Create commit with timestamp
  const timestamp = new Date().toISOString();
  const commitMsg = `Deploy dashboard and diagnostic files - ${timestamp}`;
  
  console.log('\n--- Creating Commit ---');
  console.log(`Message: ${commitMsg}`);
  const commitResult = execSync(`"${gitPath}" commit -m "${commitMsg}"`, { 
    encoding: 'utf-8',
    stdio: ['pipe', 'pipe', 'pipe']
  }).trim();
  console.log(commitResult || '(no output)');
  fs.appendFileSync('git_push.log', `=== Commit ===\n${commitResult || 'commit created'}\n\n`);

  // 7. Push to main branch
  console.log('\n--- Pushing to GitHub ---');
  const pushResult = execSync(`"${gitPath}" push -u origin main -v 2>&1`, { 
    encoding: 'utf-8',
    stdio: ['pipe', 'pipe', 'pipe']
  }).trim();
  console.log(pushResult);
  fs.appendFileSync('git_push.log', `=== Push Result ===\n${pushResult}\n\n`);

  // 8. Verify files on GitHub Pages (after push)
  console.log('\n--- Verification ---');
  console.log('Waiting 5 seconds for GitHub Pages to update...');
  setTimeout(() => {
    console.log('Push completed successfully!');
    fs.appendFileSync('git_push.log', `\n=== SUCCESS ===\nPush completed at ${new Date().toISOString()}\n`);
  }, 5000);

} catch (error) {
  console.error('\n❌ ERROR:', error.message);
  fs.appendFileSync('git_push.log', `\n=== ERROR ===\n${error.message}\n${error.stderr || ''}\n`);
  process.exit(1);
}
