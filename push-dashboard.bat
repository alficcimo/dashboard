@echo off
cd /d "C:\Users\maxim\ClaudeOS\Content\deploy"

echo Adding files to git...
git add index.html standalone.html captions-only.html test-react.html

echo Creating commit...
git commit -m "Fix: Update dashboard with working React rendering and simplified captions view"

echo Pushing to GitHub...
git push origin master

echo Done! Check the dashboard at: https://alficcimo.github.io/dashboard/
echo Or try the captions-only version: https://alficcimo.github.io/dashboard/captions-only.html
pause