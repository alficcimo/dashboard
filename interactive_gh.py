#!/usr/bin/env python3
import subprocess
import time
import sys
import os

def run_gh_with_interaction():
    """Run gh CLI with interactive handling"""
    gh_exe = r"C:\Users\maxim\ClaudeOS\Content\deploy\gh_cli\bin\gh.exe"
    
    print("Starting GitHub CLI authentication...")
    print("(A browser window should open for authentication)")
    print()
    
    # Start the auth login process
    try:
        # Use Popen to maintain the process and allow interaction
        process = subprocess.Popen(
            [gh_exe, "auth", "login", "--web"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            cwd=r"C:\Users\maxim\ClaudeOS\Content\deploy"
        )
        
        # Give it time to open the browser
        time.sleep(3)
        
        # Check if browser opened by looking for windows
        print("Waiting for authentication...")
        
        # Try to read output with a timeout
        try:
            stdout_data, stderr_data = process.communicate(timeout=120)
            
            if process.returncode == 0:
                print("✓ Authentication successful!")
                print(stdout_data)
                
                # Now try to create the repository
                print("\nCreating repository...")
                result = subprocess.run(
                    [gh_exe, "repo", "create", "dashboard", "--public"],
                    cwd=r"C:\Users\maxim\ClaudeOS\Content\deploy",
                    capture_output=True,
                    text=True
                )
                
                print(result.stdout)
                if result.stderr:
                    print("Error:", result.stderr)
                
                if result.returncode == 0 or "dashboard" in result.stdout:
                    print("✓ Repository created!")
                    
                    # Push code
                    print("\nPushing code...")
                    push_result = subprocess.run(
                        "cd C:\\Users\\maxim\\ClaudeOS\\Content\\deploy && git push -u origin master",
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    
                    if push_result.returncode == 0:
                        print("✓ Code pushed successfully!")
                        print("\n" + "=" * 50)
                        print("DEPLOYMENT COMPLETE!")
                        print("=" * 50)
                        print("GitHub Pages URL: https://alficcimo.github.io/dashboard/")
                        return True
                    else:
                        print(f"Push failed: {push_result.stderr}")
                        return False
            else:
                print(f"Authentication failed. Return code: {process.returncode}")
                print(f"Error: {stderr_data}")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            print("Process timed out. The browser authentication may still be pending.")
            print("Check if a browser window is open and complete the authentication.")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = run_gh_with_interaction()
    sys.exit(0 if success else 1)
