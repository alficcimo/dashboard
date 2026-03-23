@echo off
cd /d "C:\Users\maxim\ClaudeOS\Content\deploy"

REM Try standard git push
echo === Attempting git push === >> push_results.log
git push 2>&1 >> push_results.log
echo Exit code: %ERRORLEVEL% >> push_results.log

REM Try git push with verbose
echo === Attempting git push -v === >> push_results.log
git push -v 2>&1 >> push_results.log
echo Exit code: %ERRORLEVEL% >> push_results.log

REM Try git push with specific branch
echo === Attempting git push origin master === >> push_results.log
git push origin master 2>&1 >> push_results.log
echo Exit code: %ERRORLEVEL% >> push_results.log

REM Check remote
echo === Git remote -v === >> push_results.log
git remote -v >> push_results.log

REM Check status
echo === Git status === >> push_results.log
git status >> push_results.log

REM Check log
echo === Git log (last 3 commits) === >> push_results.log
git log --oneline -3 >> push_results.log

echo Push attempts completed. Results saved to push_results.log
