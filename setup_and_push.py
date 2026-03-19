#!/usr/bin/env python3
import subprocess
import time
import sys

def run_git_command(cmd):
    """Run a git command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timeout"

def main():
    print("Dashboard GitHub Pages Deployment")
    print("=" * 50)
    
    # Step 1: Try to push (this will trigger auth if needed)
    print("\n1. Attempting to push to GitHub...")
    print("   (Your browser may open for authentication)")
    
    code, stdout, stderr = run_git_command("cd C:\\Users\\maxim\\ClaudeOS\\Content\\deploy && git push -u origin master")
    
    if code == 0:
        print("✓ Push successful!")
        print(stdout)
    else:
        if "not found" in stderr.lower() or "repository not found" in stderr.lower():
            print("✗ Repository doesn't exist on GitHub yet")
            print("\nTo create it, visit:")
            print("https://github.com/new")
            print("\nThen fill in:")
            print("  Repository name: dashboard")
            print("  Visibility: Public")
            print("\nAfter creating, run: git push -u origin master")
            return False
        elif "authentication" in stderr.lower() or "auth" in stderr.lower():
            print("✗ Authentication needed")
            print("Please check your browser for the authentication prompt")
            return False
        else:
            print(f"✗ Error: {stderr}")
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
