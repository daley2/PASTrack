@echo off
setlocal enabledelayedexpansion

cd /d c:\Users\gideo\Desktop\Django\Capstone

echo [1/3] Adding changes to git...
git add legaltrack/settings.py
if errorlevel 1 (
    echo ERROR: git add failed
    pause
    exit /b 1
)

echo [2/3] Committing...
git commit -m "Fix: Add Render platform detection for IPv4 DNS resolution and CSRF origins"
if errorlevel 1 (
    echo ERROR: git commit failed
    pause
    exit /b 1
)

echo [3/3] Pushing to master...
git push origin master
if errorlevel 1 (
    echo ERROR: git push failed
    pause
    exit /b 1
)

echo.
echo ===== SUCCESS =====
echo Changes pushed to GitHub!
echo Render will auto-redeploy when it detects the push.
echo Check: https://dashboard.render.com/
echo.
pause
