#!/usr/bin/env python3
import subprocess
import os
import sys
from datetime import datetime
import io

# Set UTF-8 output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.chdir('C:\\Users\\maxim\\ClaudeOS\\Content\\deploy')

try:
    print("Adding files to git...")
    subprocess.run(['git', 'add', '.'], check=True)
    print("✓ Files added")
    
    print("Checking git status...")
    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
    print("Current status:")
    print(result.stdout)
    
    print("Creating commit...")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subprocess.run(['git', 'commit', '-m', f'Auto-deploy: Update content files [{timestamp}]'], check=True)
    print("✓ Commit created")
    
    print("Pushing to GitHub...")
    subprocess.run(['git', 'push', 'origin', 'master'], check=True)
    print("✓ Pushed successfully!")
    
    print("\n✅ All done!")
    print("Dashboard URLs:")
    print("  - Main: https://alficcimo.github.io/dashboard/")
    print("  - Captions only: https://alficcimo.github.io/dashboard/captions-only.html")
    print("  - React test: https://alficcimo.github.io/dashboard/test-react.html")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
