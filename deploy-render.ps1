#!/usr/bin/env pwsh
# Deploy fixes to Render

Set-Location "c:\Users\gideo\Desktop\Django\Capstone"

Write-Host "📝 Staging changes..." -ForegroundColor Green
git add legaltrack/settings.py

Write-Host "💾 Committing..." -ForegroundColor Green
git commit -m "Fix: Add Render platform detection for IPv4 DNS resolution and CSRF origins"

Write-Host "🚀 Pushing to master..." -ForegroundColor Green
git push origin master

Write-Host "`n✅ Done! Render will auto-redeploy when it sees the push." -ForegroundColor Green
Write-Host "Check your Render dashboard: https://dashboard.render.com" -ForegroundColor Cyan
