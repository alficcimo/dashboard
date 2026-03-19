#!/usr/bin/env python3
import subprocess
import os
import sys
import urllib.request
import json
import shutil
import zipfile

def download_gh_cli():
    """Download GitHub CLI from releases"""
    print("Downloading GitHub CLI...")
    
    # Get latest release info
    api_url = "https://api.github.com/repos/cli/cli/releases/latest"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            release_data = json.loads(response.read().decode())
        
        # Find Windows x64 asset
        for asset in release_data['assets']:
            if 'windows_amd64' in asset['name'] and asset['name'].endswith('.zip'):
                download_url = asset['browser_download_url']
                filename = asset['name']
                break
        else:
            print("Could not find Windows binary")
            return None
        
        # Download the file
        filepath = f"C:\\Users\\maxim\\ClaudeOS\\Content\\deploy\\{filename}"
        print(f"Downloading from {download_url}...")
        urllib.request.urlretrieve(download_url, filepath)
        
        return filepath
        
    except Exception as e:
        print(f"Error downloading: {e}")
        return None

def extract_and_run(zip_path):
    """Extract CLI and authenticate"""
    try:
        extract_dir = "C:\\Users\\maxim\\ClaudeOS\\Content\\deploy\\gh_cli"
        os.makedirs(extract_dir, exist_ok=True)
        
        print(f"Extracting to {extract_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find gh.exe
        gh_exe = None
        for root, dirs, files in os.walk(extract_dir):
            if 'gh.exe' in files:
                gh_exe = os.path.join(root, 'gh.exe')
                break
        
        if not gh_exe:
            print("Could not find gh.exe")
            return False
        
        print(f"Found gh.exe: {gh_exe}")
        
        # Run gh auth login
        print("\nRunning GitHub CLI authentication...")
        print("(Browser will open for authentication)")
        
        result = subprocess.run([gh_exe, "auth", "login"], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print("✓ Authenticated!")
            
            # Create repository
            print("Creating repository...")
            result = subprocess.run(
                [gh_exe, "repo", "create", "dashboard", "--public"],
                cwd="C:\\Users\\maxim\\ClaudeOS\\Content\\deploy",
                capture_output=True,
                text=True
            )
            print(result.stdout)
            
            if "dashboard" in result.stdout or result.returncode == 0:
                print("✓ Repository created!")
                
                # Push code
                print("Pushing code...")
                result = subprocess.run(
                    "cd C:\\Users\\maxim\\ClaudeOS\\Content\\deploy && git push -u origin master",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print("✓ Code pushed successfully!")
                    return True
                else:
                    print(f"Push failed: {result.stderr}")
                    return False
            else:
                print(f"Repository creation failed: {result.stderr}")
                return False
        else:
            print(f"Authentication failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("GitHub Pages Deployment - Full Automation")
    print("=" * 50)
    
    zip_file = download_gh_cli()
    if zip_file:
        if extract_and_run(zip_file):
            print("\n✓ DEPLOYMENT COMPLETE!")
            print("GitHub Pages URL: https://alficcimo.github.io/dashboard/")
        else:
            print("\n✗ Deployment failed")
            sys.exit(1)
    else:
        print("\n✗ Could not download GitHub CLI")
        sys.exit(1)
