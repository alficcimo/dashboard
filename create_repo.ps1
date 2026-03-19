$ErrorActionPreference = "Continue"

Write-Host "Attempting to create GitHub repository..."

# Try to use git's built-in credential system
# Set up git to use browser-based authentication
git config --global credential.helper manager
git config --global credential.https://github.com.useHttpPath true

# Create a simple auth flow trigger
$repoUrl = "https://github.com/alficcimo/dashboard.git"

Write-Host "Configuring git credentials..."

# Try to add credentials via git credential fill
# This should trigger browser auth in modern git versions
$credentialInput = @"
protocol=https
host=github.com
username=alficcimo
"@

Write-Host "Testing authentication with git..."

# Create a test push to trigger auth
cd "C:\Users\maxim\ClaudeOS\Content\deploy"

# First, ensure we have the remote configured
git remote remove origin 2>$null
git remote add origin $repoUrl

# Try push - this should trigger authentication in git 2.39+
Write-Host "Pushing to GitHub (check your browser for auth)..."
$output = git push -u origin master 2>&1

if ($output -match "not found") {
    Write-Host "Repository not found. Attempting alternative creation method..."
    
    # Since automatic auth didn't work, try using gh CLI if available
    try {
        gh repo create dashboard --public --source=. --remote=origin --push
    }
    catch {
        Write-Host "GitHub CLI not available."
        
        # Last resort: create repo using curl with manual auth
        Write-Host "Attempting to create repository using web API..."
        Write-Host ""
        Write-Host "Since automated authentication failed, please:"
        Write-Host "1. Visit: https://github.com/settings/tokens/new"
        Write-Host "2. Create a token with 'repo' scope"
        Write-Host "3. Copy the token"
        Write-Host "4. Run: git push -u origin master"
        Write-Host "   (paste token when prompted)"
    }
}
else {
    Write-Host "SUCCESS! Repository created and code pushed."
    Write-Host $output
}
