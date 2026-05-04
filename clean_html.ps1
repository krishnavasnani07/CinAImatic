$htmlFiles = Get-ChildItem -Path "screens" -Filter "*.html"

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Remove Tailwind CDN
    $content = $content -replace '<script src="https://cdn\.tailwindcss\.com\?plugins=forms,container-queries"></script>', ''
    
    # Remove tailwind-config block
    $content = $content -replace '(?s)<script id="tailwind-config">.*?</script>', ''
    
    # Add link to style.css before </head> if not already present
    if ($content -notmatch 'href="/src/style.css"') {
        $content = $content -replace '</head>', '<link rel="stylesheet" href="/src/style.css"></head>'
    }
    
    # Remove the embedded <style> blocks (because they are now in style.css)
    $content = $content -replace '(?s)<style>.*?</style>', ''
    
    Set-Content -Path $file.FullName -Value $content
}
