$pyFolder = "C:\Users\$env:UserName\AppData\Local\Programs\Python\Python311"
$pyExec = "$pyFolder\python.exe"

if (Test-Path -Path $pyFolder ) {
    Write-Host "Python 3.11 found"
} else {
    Write-Host "Python 3.11 directory not found"
}

if (Test-Path -Path $pyExec ) {
    Write-Host "Python executable found at $pyExec"
} else {
    Write-Host "Python executable not found"
}

Write-Host "Verifying Python version..."
$pyVersion = &$pyExec --version
if ($pyVersion -match "Python 3.11.2") {
    Write-Host "Python 3.11.2 found"
} else {
    Write-Host "Python 3.11.2 not found"
}


# Run git --version and store the output
$gitVersion = git.exe --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Git not found"
} else {
    Write-Host "Git found"
}
Write-Host "Git version: $gitVersion"

Write-Host "Cloning the project repository..."

# clone the repository
git clone https://github.com/desmondharris/CARL.git

# Verify the repository was cloned
if (Test-Path -Path "CARL" ) {
    Write-Host "Repository cloned"
} else {
    Write-Host "Repository not cloned"
}

cd CARL

# create venv
Write-Host "Creating virtual environment..."
&$pyExec -m venv CARLvenv

# deactivate old venv, suppress errors
deactivate 2>$null

if (Test-Path -Path "CARLvenv" ) {
    Write-Host "Virtual environment created"
} else {
    Write-Host "Virtual environment not created"
}

CARLvenv\Scripts\Activate


# Install the project dependencies  
Write-Host "Installing project dependencies..."
&$pyFolder\Scripts\pip.exe install -r requirements.txt
 
if ($LASTEXITCODE -eq 0) {
    Write-Host "Project dependencies installed"
} else {
    Write-Host "Error installing project dependencies"
}

Write-Host "Project setup complete"
