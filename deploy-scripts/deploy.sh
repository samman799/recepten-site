#!/bin/bash
# Build and deploy recipes website to GitHub
# This script runs build_site.py and commits+pushes to GitHub
# Usage: bash deploy.sh (run from recepten folder) or ./deploy.sh

set -e  # Exit on any error

# Get the directory of this script and go to parent (recepten root)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$( dirname "$SCRIPT_DIR" )"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "📦 Building recipes website in: $REPO_DIR"
cd "$REPO_DIR"

# Verify we have the build script
if [ ! -f "deploy-scripts/build_site.py" ]; then
    echo "❌ Error: build_site.py not found in deploy-scripts/"
    exit 1
fi

# Run the build script
python3 deploy-scripts/build_site.py

echo ""
echo "✅ Website built successfully"
echo ""
echo "📝 Checking Git status..."
git status

echo ""
echo "🔄 Staging changes..."
git add .

echo "💾 Creating commit with timestamp: $TIMESTAMP"
git commit -m "Update recipes - $TIMESTAMP" || echo "ℹ️  No changes to commit"

echo ""
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✨ Done! Your website is now live on GitHub."
echo "📅 Commit message: Update recipes - $TIMESTAMP"
