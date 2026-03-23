import urllib.request
import re

try:
    url = 'https://alficcimo.github.io/dashboard/'
    with urllib.request.urlopen(url, timeout=10) as response:
        content = response.read().decode('utf-8')
    
    print(f"Page loaded: {len(content)} bytes")
    
    # Check for errors
    if 'error' in content.lower():
        print("\nERROR found in page:")
        errors = re.findall(r'.{0,100}error.{0,100}', content.lower())
        for e in errors[:3]:
            print(f"  - {e}")
    
    # Check for React
    if 'React' in content:
        print("React is loaded")
    
    # Check for root element
    if 'id="root"' in content:
        print("Root element found")
    
    # Check for console errors by looking for script issues
    if 'Uncaught' in content or 'SyntaxError' in content:
        print("JavaScript errors detected!")
    
    # Show first 2000 chars of body
    body_start = content.find('<body')
    if body_start > 0:
        print(f"\nBody content (first 1000 chars):")
        print(content[body_start:body_start+1000])
        
except Exception as e:
    print(f"Error: {e}")
