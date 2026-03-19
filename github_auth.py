#!/usr/bin/env python3
import subprocess
import json
import sys

# Try to get GitHub username from environment or git config
try:
    # First try to read from git config
    user_name = subprocess.check_output(['git', 'config', 'user.name'], text=True).strip()
    print(f"Git user name: {user_name}")
except:
    print("Could not read git config")

# Try to authenticate with GitHub using device flow
print("\nAttempting GitHub authentication...")
print("Please visit: https://github.com/login/device")
print("And enter the code that will be provided by the GitHub CLI when running 'gh auth login'")
print("\nSince gh CLI is not installed, you'll need to either:")
print("1. Provide your GitHub username and create a Personal Access Token at:")
print("   https://github.com/settings/tokens")
print("2. Or use SSH keys if already set up")
