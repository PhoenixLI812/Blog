$path = "C:\Users\Administrator\.gemini\antigravity\brain\672983e9-b752-46b0-94ac-5b38a52016eb\.system_generated\logs\transcript_full.jsonl"
$lines = [System.IO.File]::ReadAllLines($path, [System.Text.Encoding]::UTF8)

foreach ($l in $lines) {
    if ($l.Contains('"step_index":1200,')) {
        $obj = $l | ConvertFrom-Json
        $content = $obj.content
        if ($content.StartsWith("<USER_REQUEST>")) {
            $content = $content.Substring(14).Trim()
        }
        if ($content.EndsWith("</USER_REQUEST>")) {
            $content = $content.Substring(0, $content.Length - 15).Trim()
        }
        Set-Content -Path ".\生命与智能的演化阶梯_参考原文.md" -Value $content -Encoding UTF8
        Write-Host "Successfully saved article! Length: $($content.Length)"
        break
    }
}
