param(
  [string]$MapPath = 'secrets/secret-map.json',
  [string]$OutPath = '.env.local'
)
if (-not (Test-Path $MapPath)) {
  Write-Error "Secret map $MapPath not found. Create and map your Bitwarden items there."
  exit 1
}
if (-not (Get-Command bw -ErrorAction SilentlyContinue)) {
  Write-Error "Bitwarden CLI 'bw' not found. Install it first."; exit 1
}

$map = Get-Content $MapPath -Raw | ConvertFrom-Json

if (-not $env:BW_SESSION) {
  if ($env:BW_CLIENTID -and $env:BW_CLIENTSECRET) {
    Write-Output "Logging into Bitwarden using client credentials..."
    $session = bw login --client $env:BW_CLIENTID --secret $env:BW_CLIENTSECRET --raw
    if ($LASTEXITCODE -ne 0) { Write-Error "bw login failed"; exit 1 }
    $env:BW_SESSION = $session
  } else {
    Write-Error "BW_SESSION not set and BW_CLIENTID/BW_CLIENTSECRET not provided. Please login interactively or set BW_SESSION."; exit 1
  }
}

$outLines = @()
$outLines += "# Generated .env.local (from Bitwarden)"
foreach ($m in $map.mappings) {
  $envname = $m.env
  $item = $m.bw_item
  $field = $m.field
  Write-Output "Fetching $envname from Bitwarden item '$item' field '$field'..."
  $itemJson = bw get item $item --session $env:BW_SESSION 2>$null
  if (-not $itemJson) { Write-Warning "Item $item not found or inaccessible. Skipping $envname"; continue }
  $obj = $itemJson | ConvertFrom-Json
  $value = $null
  if ($obj.fields) {
    foreach ($f in $obj.fields) { if ($f.name -eq $field) { $value = $f.value; break } }
  }
  if (-not $value -and $obj.login) { $value = $obj.login.password }
  if (-not $value) { Write-Warning "No value found for $envname in item $item. Skipping"; continue }
  $outLines += "${envname}=${value}"
}

$outLines | Out-File -FilePath $OutPath -Encoding utf8
icacls $OutPath /inheritance:r | Out-Null
Write-Output "Written $OutPath with fetched secrets. Set secure permissions as needed."
