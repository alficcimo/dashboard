print('Python is working')
print('Testing Selenium import...')
try:
    from selenium import webdriver
    print('Selenium imported successfully')
except Exception as e:
    print(f'Selenium import failed: {e}')
