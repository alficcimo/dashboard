import re

with open('current_index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find script tag
script_start = content.find('<script type="text/babel">')
if script_start < 0:
    print("ERROR: No React script tag found!")
else:
    script_end = content.find('</script>', script_start)
    script_content = content[script_start:script_end]
    
    # Check for syntax issues
    issues = []
    
    # Check for unmatched brackets
    open_braces = script_content.count('{')
    close_braces = script_content.count('}')
    if open_braces != close_braces:
        issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")
    
    # Check for unmatched parentheses
    open_parens = script_content.count('(')
    close_parens = script_content.count(')')
    if open_parens != close_parens:
        issues.append(f"Unmatched parens: {open_parens} open, {close_parens} close")
    
    # Check for incomplete strings
    single_quotes = script_content.count("'")
    if single_quotes % 2 != 0:
        issues.append(f"Odd number of single quotes: {single_quotes}")
    
    double_quotes = script_content.count('"')
    if double_quotes % 2 != 0:
        issues.append(f"Odd number of double quotes: {double_quotes}")
    
    if issues:
        print("SYNTAX ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("JavaScript syntax looks OK")
        print(f"Script section: {len(script_content)} characters")
        
        # Check if React component is being rendered
        if 'ReactDOM.render' in script_content or 'ReactDOM.createRoot' in script_content:
            print("React render call found")
        else:
            print("WARNING: No React render call found!")
