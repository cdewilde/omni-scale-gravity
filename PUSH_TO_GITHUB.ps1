param(
    [Parameter(Mandatory=$false)]
    [string]$RepoUrl
)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed or not on PATH. Install 'Git for Windows' first."
    exit 1
}

if (-not $RepoUrl) {
    $RepoUrl = Read-Host "Enter your GitHub repo URL (e.g. https://github.com/cdewilde/omni-scale-gravity.git)"
}

Write-Host "Using repo URL: $RepoUrl"
git init
git add .
git commit -m "OSG v1c: PN seeding, GPU demos, CI"
git branch -M main
git remote remove origin 2>$null
git remote add origin $RepoUrl
git push -u origin main
git tag v1c
git push origin v1c
Write-Host "Done. Pushed 'main' and tag 'v1c'."
