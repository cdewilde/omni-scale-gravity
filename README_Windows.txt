Windows Publish Kit — OmniScale Gravity (OSG)
Date: 2025-08-10

This folder contains two helpers to push your local repo to GitHub on Windows:
- PUSH_TO_GITHUB.ps1   (PowerShell)
- PUSH_TO_GITHUB.cmd   (classic CMD)

Usage (PowerShell, recommended):
1) Open Windows Terminal or PowerShell.
2) cd into your local repo folder (e.g., osg_repo_v1c).
3) Option A: Provide the URL as a parameter:
   .\PUSH_TO_GITHUB.ps1 -RepoUrl "https://github.com/cdewilde/omni-scale-gravity.git"
   Option B: Run without params and paste the URL when prompted:
   .\PUSH_TO_GITHUB.ps1

If you see a script-execution warning:
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
…then re-run the script.

Usage (CMD):
  PUSH_TO_GITHUB.cmd https://github.com/cdewilde/omni-scale-gravity.git

Notes:
- You need Git for Windows installed (adds 'git' to PATH).
- If using HTTPS, GitHub may prompt for a Personal Access Token (PAT) instead of a password.
- The script initializes a repo, pushes 'main', and tags/releases v1c.
