# Build the frontend and copy the dist output into static/frontend
Set-StrictMode -Version Latest

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$frontend = Join-Path $root '..\frontend'
$out = Join-Path $root '..\static\frontend'

Write-Host "Building frontend in $frontend"
Push-Location $frontend
npm install
npm run build
Pop-Location

if (Test-Path $out) { Remove-Item $out -Recurse -Force }
New-Item -ItemType Directory -Path $out | Out-Null

Write-Host "Copying build to $out"
Copy-Item -Path (Join-Path $frontend 'dist\*') -Destination $out -Recurse

Write-Host "Frontend build complete. Serve from /static/frontend/index.html"
