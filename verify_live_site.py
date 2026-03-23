import urllib.request
import urllib.error

try:
    url = 'https://alficcimo.github.io/dashboard/'
    req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode('utf-8')
        
    if 'Открою вам ужас' in content:
        print("SUCCESS: Live dashboard HAS updated captions!")
        print("The dashboard at https://alficcimo.github.io/dashboard/ is serving the updated content.")
    else:
        print("Site loaded but captions not found yet")
        print("GitHub Pages may still be refreshing (can take up to 5 minutes)")
        if 'caption' in content:
            print("Note: 'caption' references found in page")
except Exception as e:
    print(f"Error fetching site: {e}")
    print("This might be a network issue or GitHub Pages is updating")
