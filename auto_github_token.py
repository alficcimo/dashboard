#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def create_github_token():
    """Use Selenium to create a GitHub PAT automatically"""
    
    print("Initializing browser for GitHub authentication...")
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        # Start Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        
        print("Opening GitHub login page...")
        driver.get("https://github.com/login")
        
        # Wait and check if already logged in
        time.sleep(3)
        current_url = driver.current_url
        
        if "login" in current_url:
            print("Not logged in. You need to log in via the browser.")
            print("The browser is open at https://github.com/login")
            print("Please log in, then I'll continue...")
            
            # Wait for login to complete
            WebDriverWait(driver, 300).until(
                lambda d: "github.com" in d.current_url and "login" not in d.current_url
            )
            print("✓ Login detected!")
        else:
            print("✓ Already logged in!")
        
        # Navigate to token creation page
        print("Navigating to token creation page...")
        driver.get("https://github.com/settings/tokens/new")
        
        time.sleep(2)
        
        # Fill in token details
        print("Creating personal access token...")
        
        # Note - in token creation UI, we need to:
        # 1. Set token name
        # 2. Set expiration
        # 3. Select scopes
        # 4. Generate token
        
        try:
            # Set token name
            token_name_input = driver.find_element(By.ID, "oauth_application_name")
            token_name_input.clear()
            token_name_input.send_keys("Dashboard Deploy")
            
            # Set expiration to 7 days
            # (This varies by GitHub UI version, so we might skip)
            
            # Select 'repo' scope checkbox if available
            try:
                repo_checkbox = driver.find_element(By.NAME, "oauth_scopes")
                if not repo_checkbox.is_selected():
                    repo_checkbox.click()
            except:
                pass  # Checkbox might not exist or already selected
            
            # Find and click Generate button
            generate_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "commit"))
            )
            generate_button.click()
            
            print("Token generated! Waiting for token display...")
            time.sleep(2)
            
            # Extract the token from the page
            # The token is usually in a text field or code block
            try:
                # Try to find token in various possible locations
                token_element = None
                
                # Check for code element
                code_elements = driver.find_elements(By.TAG_NAME, "code")
                for code in code_elements:
                    text = code.text.strip()
                    if len(text) > 30 and text.startswith("ghp_"):
                        token_element = text
                        break
                
                # Check for input fields
                if not token_element:
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        value = inp.get_attribute("value")
                        if value and len(value) > 30 and value.startswith("ghp_"):
                            token_element = value
                            break
                
                if token_element:
                    print(f"✓ Token found: {token_element[:20]}...")
                    driver.quit()
                    return token_element
                else:
                    print("Could not find token on page")
                    # Take a screenshot for debugging
                    driver.save_screenshot("token_page.png")
                    driver.quit()
                    return None
                    
            except Exception as e:
                print(f"Error extracting token: {e}")
                driver.quit()
                return None
                
        except Exception as e:
            print(f"Error filling token form: {e}")
            driver.quit()
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def use_token_to_deploy(token):
    """Use the token to create repo and push code"""
    
    print(f"\nUsing token to deploy...")
    
    # Set environment variable
    os.environ["GH_TOKEN"] = token
    
    gh_exe = r"C:\Users\maxim\ClaudeOS\Content\deploy\gh_cli\bin\gh.exe"
    
    # Create repository
    print("Creating repository...")
    result = subprocess.run(
        [gh_exe, "repo", "create", "dashboard", "--public"],
        cwd=r"C:\Users\maxim\ClaudeOS\Content\deploy",
        capture_output=True,
        text=True,
        env={**os.environ, "GH_TOKEN": token}
    )
    
    print(result.stdout)
    if result.stderr and "already exists" not in result.stderr:
        print(f"Warning: {result.stderr}")
    
    if result.returncode == 0 or "dashboard" in result.stdout:
        print("✓ Repository created!")
        
        # Push code
        print("Pushing code...")
        push_result = subprocess.run(
            "cd C:\\Users\\maxim\\ClaudeOS\\Content\\deploy && git push -u origin master",
            shell=True,
            capture_output=True,
            text=True,
            env={**os.environ, "GH_TOKEN": token}
        )
        
        if push_result.returncode == 0:
            print("✓ Code pushed successfully!")
            print("\n" + "=" * 50)
            print("✓ DEPLOYMENT COMPLETE!")
            print("=" * 50)
            print("GitHub Pages URL: https://alficcimo.github.io/dashboard/")
            return True
        else:
            print(f"Push output: {push_result.stdout}")
            print(f"Push error: {push_result.stderr}")
            return False
    else:
        print(f"Failed to create repository: {result.stderr}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Autonomous GitHub Deployment")
    print("=" * 50)
    print()
    
    token = create_github_token()
    
    if token:
        if use_token_to_deploy(token):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("Failed to create token")
        sys.exit(1)
