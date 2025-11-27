# Load .env.local into the current PowerShell session
# Usage: .\scripts\load-env.ps1
param(
  [string]$Path = '.env.local'
)
if (-not (Test-Path $Path)) {
  Write-Error "File $Path not found. Copy .env.example to .env.local and fill secrets before running."
  return
}
Get-Content $Path | ForEach-Object {
  if ($_ -and -not $_.TrimStart().StartsWith('#')) {
    $parts = $_ -split '=', 2
    if ($parts.Count -eq 2) {
      $name = $parts[0].Trim()
      $value = $parts[1].Trim()
      # Remove surrounding quotes if present
      if ($value.StartsWith('"') -and $value.EndsWith('"')) { $value = $value.Substring(1,$value.Length-2) }
      ${env:$name} = $value
    }
  }
}
Write-Output "Loaded environment from $Path"
