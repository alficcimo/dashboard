const fs = require('fs');
const path = require('path');

const deployDir = 'C:\\Users\\maxim\\ClaudeOS\\Content\\deploy';
const reportPath = path.join(deployDir, 'COMPLETE_DIAGNOSTIC.txt');

let summary = '=== DIAGNOSTIC ANALYSIS SUMMARY ===\n\n';

if (fs.existsSync(reportPath)) {
  const content = fs.readFileSync(reportPath, 'utf8');
  const lines = content.split('\n');
  
  // Extract git remote info
  let inRemoteSection = false;
  let remoteInfo = '';
  for (const line of lines) {
    if (line.includes('Git Remote Configuration')) {
      inRemoteSection = true;
      continue;
    }
    if (inRemoteSection) {
      if (line.startsWith('---')) break;
      remoteInfo += line + '\n';
    }
  }
  
  summary += 'GIT REMOTE:\n';
  summary += remoteInfo || '(NOT FOUND)\n';
  
  // Check for common errors
  summary += '\n=== ERROR CHECK ===\n';
  let hasErrors = false;
  for (const line of lines) {
    if (line.includes('Error') || line.includes('fatal') || line.includes('failed')) {
      summary += line + '\n';
      hasErrors = true;
    }
  }
  if (!hasErrors) {
    summary += 'No fatal errors detected\n';
  }
  
  // Check auth status
  summary += '\n=== AUTHENTICATION STATUS ===\n';
  let authFound = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('Auth Status')) {
      authFound = true;
      summary += lines[i] + '\n';
      if (i + 1 < lines.length && !lines[i + 1].startsWith('---')) {
        summary += lines[i + 1] + '\n';
      }
    }
  }
  if (!authFound) {
    summary += 'Auth status section not found\n';
  }
  
  // Check push attempt result
  summary += '\n=== PUSH ATTEMPT RESULT ===\n';
  let pushFound = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('Attempting Git Push')) {
      pushFound = true;
      // Get next few lines
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        if (lines[j].startsWith('---')) break;
        summary += lines[j] + '\n';
      }
    }
  }
  if (!pushFound) {
    summary += 'No push attempt section found\n';
  }
  
  // List HTML files found
  summary += '\n=== LOCAL FILES ===\n';
  let filesFound = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('Local HTML')) {
      filesFound = true;
      for (let j = i + 1; j < lines.length; j++) {
        if (lines[j].startsWith('---')) break;
        if (lines[j].includes('.html') || lines[j].includes('.md')) {
          summary += lines[j] + '\n';
        }
      }
    }
  }
  if (!filesFound) {
    summary += 'No file listing found\n';
  }
  
  // Overall assessment
  summary += '\n=== ASSESSMENT ===\n';
  if (content.includes('fatal') || content.includes('Permission denied')) {
    summary += 'STATUS: AUTHENTICATION FAILURE - Cannot push without credentials\n';
    summary += 'ACTION: Need to set up git credentials (SSH key or personal access token)\n';
  } else if (content.includes('pushed')) {
    summary += 'STATUS: PUSH SUCCESSFUL\n';
  } else if (content.includes('Everything up-to-date')) {
    summary += 'STATUS: Repository up to date (already pushed)\n';
  } else {
    summary += 'STATUS: UNCLEAR - Check full diagnostic report\n';
  }
  
} else {
  summary += 'ERROR: Diagnostic file not found\n';
}

// Write summary
const summaryPath = path.join(deployDir, 'DIAGNOSTIC_SUMMARY.txt');
fs.writeFileSync(summaryPath, summary);
console.log('Summary written to DIAGNOSTIC_SUMMARY.txt');
console.log('\nSummary content:\n');
console.log(summary);
