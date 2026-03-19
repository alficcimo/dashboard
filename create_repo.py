#!/usr/bin/env python3
import subprocess
import sys
import json
import urllib.request
import urllib.error

# First, try to get a personal access token via GitHub device flow
def get_device_code():
    """Initiate GitHub device flow authentication"""
    url = "https://github.com/login/device/code"
    data = urllib.parse.urlencode({"client_id": "Iv1.b507a08c87ecee34", "scope": "repo"}).encode()
    
    try:
        response = urllib.request.urlopen(url, data)
        result = json.loads(response.read().decode())
        return result
    except Exception as e:
        print(f"Error initiating device flow: {e}")
        return None

def poll_for_token(device_code, interval):
    """Poll GitHub to exchange device code for access token"""
    import time
    url = "https://github.com/login/oauth/access_token"
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Dashboard-Deploy"
    }
    
    while True:
        data = urllib.parse.urlencode({
            "client_id": "Iv1.b507a08c87ecee34",
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }).encode()
        
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            
            if "access_token" in result:
                return result["access_token"]
            elif result.get("error") == "authorization_pending":
                time.sleep(interval)
                continue
            else:
                print(f"Error: {result}")
                return None
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(interval)
            continue

def create_repository(token, repo_name="dashboard"):
    """Create a public repository on GitHub"""
    url = "https://api.github.com/user/repos"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Dashboard-Deploy"
    }
    
    data = json.dumps({
        "name": repo_name,
        "description": "Dashboard",
        "public": True,
        "auto_init": False
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        print(f"Repository created: {result.get('html_url')}")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print("Repository already exists")
            return True
        else:
            print(f"Error creating repository: {e.read().decode()}")
            return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Attempting to create GitHub repository...")
    print("\nInitiating device flow authentication...")
    
    device_result = get_device_code()
    if not device_result:
        print("Failed to initiate device flow. Trying alternative method...")
        sys.exit(1)
    
    device_code = device_result.get("device_code")
    user_code = device_result.get("user_code")
    interval = device_result.get("interval", 5)
    verification_uri = device_result.get("verification_uri")
    
    print(f"\n1. Visit: {verification_uri}")
    print(f"2. Enter code: {user_code}")
    print(f"\nWaiting for authentication...")
    
    token = poll_for_token(device_code, interval)
    
    if token:
        print(f"✓ Authenticated successfully")
        if create_repository(token):
            print("✓ Repository ready for push")
        else:
            sys.exit(1)
    else:
        print("Authentication failed")
        sys.exit(1)
