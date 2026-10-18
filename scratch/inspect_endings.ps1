$files = Get-ChildItem -Path ".\manuscript\*.md" | Sort-Object Name
foreach ($f in $files) {
    $lines = [System.IO.File]::ReadAllLines($f.FullName, [System.Text.Encoding]::UTF8)
    $hasMatch = $false
    $matchIdx = -1
    for ($i = 0; $i -lt $lines.Length; $i++) {
        if ($lines[$i] -match "承上启下" -or $lines[$i] -match "衔接第") {
            $hasMatch = $true
            $matchIdx = $i
            break
        }
    }
    if ($hasMatch) {
        [System.Console]::WriteLine("=== " + $f.Name + " ===")
        $start = [System.Math]::Max(0, $matchIdx - 6)
        for ($i = $start; $i -lt $lines.Length; $i++) {
            [System.Console]::WriteLine(($i + 1).ToString("D3") + ": " + $lines[$i])
        }
        [System.Console]::WriteLine("`n----------------------------------------`n")
    }
}
