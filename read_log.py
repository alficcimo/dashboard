#!/usr/bin/env python3
import os

os.chdir(r'C:\Users\maxim\ClaudeOS\Content\deploy')

# Read and print all log files
for logfile in ['gh_test.log', 'push_results.log']:
    if os.path.exists(logfile):
        print(f"\n=== {logfile} ===")
        with open(logfile, 'r') as f:
            print(f.read())
    else:
        print(f"\n{logfile} not found")

# Also try git commands and save output
print("\n=== Running git commands ===")
import subprocess

try:
    result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
    print("GIT REMOTE:")
    print(result.stdout)
    print(result.stderr)
except Exception as e:
    print(f"Error: {e}")

try:
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    print("\nGIT STATUS:")
    print(result.stdout)
    print(result.stderr)
except Exception as e:
    print(f"Error: {e}")

print("\n=== Done ===")
