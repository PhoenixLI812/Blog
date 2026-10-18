$files = Get-ChildItem -Path ".\manuscript\*.md" | Sort-Object Name
$errorsFound = $false

foreach ($f in $files) {
    $text = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    
    $p1 = [char]0x627F + [char]0x4E0A + [char]0x542F + [char]0x4E0B
    if ($text.IndexOf($p1) -ge 0) {
        Write-Host "ERROR: Found ChengShangQiXia in $($f.Name)"
        $errorsFound = $true
    }
    
    $p2 = [char]0x8854 + [char]0x63A5 + [char]0x7B2C
    if ($text.IndexOf($p2) -ge 0) {
        Write-Host "ERROR: Found XianJieDi in $($f.Name)"
        $errorsFound = $true
    }
    
    $lines = [System.IO.File]::ReadAllLines($f.FullName, [System.Text.Encoding]::UTF8)
    $fenceCount = 0
    foreach ($line in $lines) {
        if ($line.TrimStart().StartsWith('```')) {
            $fenceCount++
        }
    }
    if ($fenceCount % 2 -ne 0) {
        Write-Host "ERROR: Unbalanced code fences ($fenceCount) in $($f.Name)"
        $errorsFound = $true
    } else {
        Write-Host "OK: $($f.Name) (lines: $($lines.Length), fences: $fenceCount)"
    }
}

if (-not $errorsFound) {
    Write-Host "ALL CHECKS PASSED: Zero forbidden markers, all fences balanced."
} else {
    Write-Host "CHECKS FAILED!"
}
