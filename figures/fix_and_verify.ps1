$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName
if (-not (Test-Path (Join-Path $baseDir "manuscript"))) {
    $baseDir = (Get-Location).Path
}

$ch3Files = Get-ChildItem -Path (Join-Path $baseDir "manuscript\03*.md")
if ($ch3Files.Count -gt 0) {
    $ch3 = $ch3Files[0].FullName
    $bytes = [System.IO.File]::ReadAllBytes($ch3)
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    
    $bt = [string][char]96
    $bad1 = $bt + $bt + "!["
    $good1 = "!["
    
    $bad2 = $bt + "mermaid"
    $good2 = $bt + $bt + $bt + "mermaid"
    
    $modified = $false
    if ($text.Contains($bad1)) {
        $text = $text.Replace($bad1, $good1)
        $modified = $true
        Write-Host "Fixed bad tag in Chapter 3"
    }
    if ($text.Contains($bad2)) {
        $text = $text.Replace($bad2, $good2)
        $modified = $true
        Write-Host "Fixed bad mermaid fence in Chapter 3"
    }
    
    if ($modified) {
        $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
        [System.IO.File]::WriteAllBytes($ch3, $utf8Bytes)
        Write-Host "Chapter 3 successfully updated and saved."
    } else {
        Write-Host "Chapter 3 had no bad patterns."
    }
}

Write-Host "=== VERIFYING ALL CHAPTERS ==="
$files = Get-ChildItem -Path (Join-Path $baseDir "manuscript\*.md") | Sort-Object Name
$fence = [string]::new([char]96, 3)

foreach ($f in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    $chars = $text.Length
    
    $hasBase64 = $text.Contains("data:image/")
    
    # Count occurrences of triple backtick
    $count = 0
    $idx = $text.IndexOf($fence)
    while ($idx -ge 0) {
        $count++
        $idx = $text.IndexOf($fence, $idx + 3)
    }
    
    $fenceBalanced = ($count % 2 -eq 0)
    
    # Check for any malformed markdown image syntax
    $hasMalformedImg = $text.Contains($bt + "![") -or $text.Contains($bt + $bt + "![")
    
    Write-Host ("[{0}] Length: {1} chars | Base64 Img: {2} | Fences Balanced: {3} (count={4}) | Malformed: {5}" -f `
        $f.Name, $chars, $hasBase64, $fenceBalanced, $count, $hasMalformedImg)
}
