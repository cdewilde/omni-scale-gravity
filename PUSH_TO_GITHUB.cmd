@echo off
setlocal
if "%~1"=="" (
  echo Usage: PUSH_TO_GITHUB.cmd ^<GITHUB_REPO_URL^>
  echo   Example: PUSH_TO_GITHUB.cmd https://github.com/cdewilde/omni-scale-gravity.git
  exit /b 1
)
where git >nul 2>&1
if errorlevel 1 (
  echo Git is not installed or not on PATH. Install "Git for Windows" first.
  exit /b 1
)
set REPO=%~1
echo Using repo URL: %REPO%
git init
git add .
git commit -m "OSG v1d: PN seeding, GPU demos, CI"
git branch -M main
git remote remove origin 2>nul
git remote add origin %REPO%
git push -u origin main
git tag v1d
git push origin v1d
echo Done. Pushed 'main' and tag 'v1d'.
endlocal
