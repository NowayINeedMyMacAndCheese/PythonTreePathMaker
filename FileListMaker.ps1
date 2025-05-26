Write-Host "=== File List Generator (PowerShell) ==="

$choice = Read-Host "Do you want to generate the file list in the current directory? (y/n)"

if ($choice -eq "y") {
    $target = Get-Location
} else {
    $target = Read-Host "Enter full path of the target directory"
    if (-not (Test-Path $target)) {
        Write-Host "`n❌ The directory does not exist."
        Pause
        exit
    }
    $target = Get-Item $target
}

$fileList = Join-Path $target "filelist.txt"
$inaccessible = @()
$allPaths = @()

try {
    # Add root directory
    $allPaths += $target.FullName

    # Get subdirectories
    $directories = Get-ChildItem -Path $target -Directory -Recurse -Force -ErrorAction SilentlyContinue
    $directories = $directories.FullName

    foreach ($dir in $directories) {
        $allPaths += $dir
        try {
            $files = Get-ChildItem -Path $dir -File -Force -ErrorAction Stop
            $allPaths += $files.FullName
        } catch {
            $inaccessible += $dir
        }
    }

    # Get files in root folder
    try {
        $rootFiles = Get-ChildItem -Path $target -File -Force -ErrorAction Stop
        $allPaths += $rootFiles.FullName
    } catch {
        $inaccessible += $target.FullName
    }

    $allPaths | Sort-Object | Set-Content -Path $fileList -Encoding UTF8
    Write-Host "`n✅ File list saved to $fileList"

    if ($inaccessible.Count -gt 0) {
        Write-Host "`n⚠️ Warning: Some folders could not be accessed:"
        $inaccessible | Sort-Object | ForEach-Object { Write-Host " - $_" }
    }

} catch {
    Write-Host "`n❌ An unexpected error occurred: $_"
}

Pause
