$raw = Get-Content ".\scratch\article_from_user.txt" -Encoding UTF8

$filtered = @()
$recording = $false

foreach ($line in $raw) {
    if ($line.Contains('生命与智能的演化阶梯')) {
        $recording = $true
        # Extract title if line has preceding text
        $idx = $line.IndexOf('生命与智能的演化阶梯')
        $line = $line.Substring($idx)
    }
    if ($recording) {
        if ($line.Contains('</USER_REQUEST>') -or $line.Contains('<ADDITIONAL_METADATA>')) {
            break
        }
        $filtered += $line
    }
}

$filtered | Out-File -FilePath ".\生命与智能的演化阶梯_从化学编码到全球脑的抽象层级跃迁.md" -Encoding UTF8
Write-Host "SAVED_SUCCESSFULLY: lines=$($filtered.Length)"
