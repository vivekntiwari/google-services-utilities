# Git Setup and GitHub Upload Guide

Follow these steps to upload your Google Services Utilities to GitHub.

## Step 1: Initialize Git Repository

```bash
# Navigate to your project directory (if not already there)
cd /Users/vivektiwari/Documents/code/Utilities

# Initialize git repository
git init
```

## Step 2: Configure Git (if not already done)

```bash
# Set your name and email (use your GitHub email)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Add Files to Git

```bash
# Check what files will be added (verify .gitignore is working)
git status

# Add all files (respecting .gitignore)
git add .

# Verify what's staged
git status
```

## Step 4: Create Initial Commit

```bash
# Commit the files
git commit -m "Initial commit: Google Drive and Photos manager utilities"
```

## Step 5: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the **+** icon in the top right
3. Select **New repository**
4. Fill in:
   - **Repository name**: `google-services-utilities` (or your preferred name)
   - **Description**: "Python CLI tools to manage and analyze Google Drive and Google Photos"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

## Step 6: Connect Local Repo to GitHub

```bash
# Add GitHub as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Verify remote was added
git remote -v
```

## Step 7: Push to GitHub

```bash
# Push to GitHub (first time)
git push -u origin main

# If it says 'master' instead of 'main', use:
# git branch -M main
# git push -u origin main
```

## Step 8: Verify Upload

1. Go to your GitHub repository URL
2. Verify that files are uploaded
3. **IMPORTANT**: Check that these files are **NOT** visible:
   - ❌ `credentials.json`
   - ❌ `token.json`
   - ❌ `drive_cache.json`
   - ❌ Any `.csv` or `.json` export files
   - ❌ `test_*.py` files
   - ❌ `hello.py`

## What Should Be Visible ✅

- ✅ `README.md`
- ✅ `.gitignore`
- ✅ `drive_manager/` folder with Python source files
- ✅ `photos_manager/` folder with Python source files
- ✅ `requirements.txt` files

## Future Updates

After making changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with a message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Troubleshooting

### If you get authentication errors:
- GitHub now requires Personal Access Tokens instead of passwords
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate a new token with 'repo' permissions
- Use the token as your password when pushing

### If you accidentally committed sensitive files:
```bash
# Remove from git but keep locally
git rm --cached path/to/sensitive/file

# Commit the removal
git commit -m "Remove sensitive file"

# Push
git push
```

## Security Checklist ✅

Before pushing, verify:
- [ ] `.gitignore` is properly configured
- [ ] No credentials files are staged (`git status` shows no credentials.json, token.json)
- [ ] No cache files are staged (no drive_cache.json, photos_cache.json)
- [ ] No export files with personal data are staged (no .csv/.json exports)
- [ ] Test files are excluded
