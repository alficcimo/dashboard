#!/usr/bin/env python3
import subprocess
import os

os.chdir(r'C:\Users\maxim\ClaudeOS\Content\deploy')

output = []

# Check git status
try:
    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, timeout=10)
    output.append("=== GIT STATUS ===")
    output.append(result.stdout)
    if result.stderr:
        output.append("STDERR: " + result.stderr)
except Exception as e:
    output.append(f"Error checking status: {e}")

# List HTML files
try:
    result = subprocess.run(['git', 'ls-files', '*.html'], capture_output=True, text=True, timeout=10)
    output.append("\n=== GIT TRACKED HTML FILES ===")
    output.append(result.stdout)
except Exception as e:
    output.append(f"Error listing files: {e}")

# Check for untracked files
try:
    result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True, timeout=10)
    output.append("\n=== UNTRACKED FILES ===")
    output.append(result.stdout)
except Exception as e:
    output.append(f"Error: {e}")

# Try to add all changes
try:
    output.append("\n=== ADDING FILES ===")
    result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True, timeout=10)
    output.append(f"Return code: {result.returncode}")
    if result.stdout:
        output.append("STDOUT: " + result.stdout)
    if result.stderr:
        output.append("STDERR: " + result.stderr)
except Exception as e:
    output.append(f"Error adding: {e}")

# Check status again
try:
    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, timeout=10)
    output.append("\n=== STATUS AFTER ADD ===")
    output.append(result.stdout)
except Exception as e:
    output.append(f"Error: {e}")

# Write output to file
with open('push_log.txt', 'w') as f:
    f.write('\n'.join(output))

print("Log written to push_log.txt")
