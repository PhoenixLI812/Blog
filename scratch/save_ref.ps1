$raw = Get-Content "C:\Users\Administrator\.gemini\antigravity\brain\672983e9-b752-46b0-94ac-5b38a52016eb\.system_generated\logs\transcript_full.jsonl" -Encoding UTF8
foreach ($l in $raw) {
    if ($l.Contains('"step_index":1200,')) {
        $obj = $l | ConvertFrom-Json
        $text = $obj.content
        if ($text.StartsWith("<USER_REQUEST>")) {
            $text = $text.Substring(14).TrimStart()
        }
        if ($text.EndsWith("</USER_REQUEST>")) {
            $text = $text.Substring(0, $text.Length - 15).TrimEnd()
        }
        $text | Out-File -FilePath ".\scratch\article_from_user.txt" -Encoding utf8
        Write-Host "SAVED_OK: scratch\article_from_user.txt, size: $((Get-Item .\scratch\article_from_user.txt).Length) bytes"
        break
    }
}
