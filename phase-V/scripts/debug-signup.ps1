$ErrorActionPreference = "Stop"

Write-Host "Debugging Signup endpoint..." -ForegroundColor Cyan

$url = "http://localhost:3000/api/auth/sign-up"
$body = @{
    email = "debug-test@example.com"
    password = "password123"
    name = "Debug User"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json"
    Write-Host "Signup Successful!" -ForegroundColor Green
    $jsonResponse = $response | ConvertTo-Json -Depth 5
    Write-Host "Response: $jsonResponse"
} catch {
    Write-Host "Signup Failed!" -ForegroundColor Red
    
    # Check if we have a response object
    if ($_.Exception.Response) {
        $img = $_.Exception.Response.StatusCode
        Write-Host "Status Code: $img"
        
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $errorBody = $reader.ReadToEnd()
        Write-Host "Error Body: $errorBody"
    } else {
        $msg = $_.Exception.Message
        Write-Host "Exception: $msg"
    }
}
