$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName

$extremeTerms = @(
    "万劫不复", "必死无疑", "彻底毁灭", "彻头彻尾的骗局", "绝对深渊", "自毁倾向",
    "死局", "灭顶之灾", "血腥味", "血流成河", "暴毙", "死刑判决", "万丈深渊",
    "宏观大坍塌", "彻底的解体", "自恋防线", "令人脊背发凉", "两眼一抹黑的远古原始人"
)

$files = Get-ChildItem -LiteralPath (Join-Path $baseDir "manuscript") -Filter "*.md" | Sort-Object Name

$report = @()

foreach ($f in $files) {
    $lines = [System.IO.File]::ReadAllLines($f.FullName, [System.Text.Encoding]::UTF8)
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        foreach ($term in $extremeTerms) {
            if ($line.Contains($term)) {
                $report += [PSCustomObject]@{
                    File = $f.Name
                    Line = $i + 1
                    Term = $term
                    Snippet = $line.Trim()
                }
            }
        }
    }
}

$json = $report | ConvertTo-Json -Depth 3
[System.IO.File]::WriteAllText((Join-Path $baseDir "figures\extreme_terms_report.json"), $json, [System.Text.Encoding]::UTF8)
Write-Host ("Found {0} occurrences of extreme terms across manuscript." -f $report.Count)
