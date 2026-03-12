@echo off
setlocal enabledelayedexpansion

cd /d c:\Users\gideo\Desktop\Django\Capstone

echo [1/4] Adding changes...
git add legaltrack/settings.py render.yaml

echo [2/4] Checking status...
git status --short

echo [3/4] Committing...
git commit -m "Fix: Improve serverless detection (Render, production without .env) and IPv4 DNS resolution"

echo [4/4] Pushing to master (this triggers Render auto-deploy)...
git push -v origin master

echo.
echo ===== SUCCESS =====
echo Push complete! Render will auto-redeploy in a few moments.
echo Check Render Dashboard: https://dashboard.render.com/
echo.
echo Look for debug output [INFO] in Render logs showing DNS resolution.
echo.
pause
