$files = Get-ChildItem -Path ".\manuscript\*.md" | Sort-Object Name
foreach ($f in $files) {
    [Console]::WriteLine($f.Name)
}
