@echo off
cd /d c:\Users\gideo\Desktop\Django\Capstone

echo ===== FINAL FIX: Add gunicorn to requirements =====
echo.

echo [1/3] Adding requirements.txt...
git add requirements.txt

echo [2/3] Committing...
git commit -m "Add gunicorn to requirements.txt for Render deployment"

echo [3/3] Pushing to trigger Render rebuild...
git push origin master

echo.
echo ✅ Done! Render will rebuild with gunicorn.
echo.
echo Check Render logs in ~1 minute for successful deployment.
echo Then test: https://your-render-url.onrender.com/
echo.
pause
