#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error
import webbrowser
import time
import urllib.parse

def get_oauth_token():
    """Get OAuth token using device flow"""
    client_id = "e8acb11b4b2c7c0fd1ea"  # GitHub OAuth App ID for CLI tools
    
    # Step 1: Request device and user codes
    auth_url = "https://github.com/login/device/code"
    params = {
        "client_id": client_id,
        "scope": "repo,user"
    }
    
    data = urllib.parse.urlencode(params).encode('utf-8')
    
    try:
        req = urllib.request.Request(auth_url, data=data, method="POST")
        req.add_header("Accept", "application/json")
        
        with urllib.request.urlopen(req) as response:
            auth_data = json.loads(response.read().decode())
            
        device_code = auth_data['device_code']
        user_code = auth_data['user_code']
        verification_uri = auth_data['verification_uri']
        interval = auth_data.get('interval', 5)
        expires_in = auth_data.get('expires_in', 900)
        
        print(f"Visit: {verification_uri}")
        print(f"Code: {user_code}")
        
        # Open browser automatically
        webbrowser.open(verification_uri)
        
        # Step 2: Poll for token
        token_url = "https://github.com/login/oauth/access_token"
        start_time = time.time()
        
        while time.time() - start_time < expires_in:
            poll_params = {
                "client_id": client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
            
            poll_data = urllib.parse.urlencode(poll_params).encode('utf-8')
            
            try:
                req = urllib.request.Request(token_url, data=poll_data, method="POST")
                req.add_header("Accept", "application/json")
                
                with urllib.request.urlopen(req) as response:
                    token_data = json.loads(response.read().decode())
                
                if 'access_token' in token_data:
                    return token_data['access_token']
                elif token_data.get('error') == 'authorization_pending':
                    time.sleep(interval)
                    continue
                else:
                    print(f"Error: {token_data}")
                    return None
                    
            except urllib.error.HTTPError as e:
                if e.code == 400:
                    time.sleep(interval)
                    continue
                else:
                    print(f"HTTP Error: {e}")
                    return None
        
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_repo(token):
    """Create repository using GitHub API"""
    url = "https://api.github.com/user/repos"
    
    repo_data = {
        "name": "dashboard",
        "description": "Dashboard application",
        "public": True,
        "auto_init": False
    }
    
    data = json.dumps(repo_data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✓ Repository created: {result['html_url']}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print("✓ Repository already exists")
            return True
        else:
            error_msg = e.read().decode()
            print(f"Error: {error_msg}")
            return False

if __name__ == "__main__":
    print("GitHub Repository Setup")
    print("Opening browser for authentication...")
    
    token = get_oauth_token()
    
    if token:
        print("✓ Authenticated!")
        if create_repo(token):
            print("\nRepository ready. Pushing code...")
            import subprocess
            result = subprocess.run(
                "cd C:\\Users\\maxim\\ClaudeOS\\Content\\deploy && git push -u origin master",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✓ Code pushed successfully!")
            else:
                print(f"Push error: {result.stderr}")
    else:
        print("✗ Authentication failed")
