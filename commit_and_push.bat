@echo off
cd /D C:\Users\maxim\ClaudeOS\Content\deploy
git add content-ideas.json content-analyzed.json content-titles.json
git commit -m "Update dashboard data"
git push origin master
