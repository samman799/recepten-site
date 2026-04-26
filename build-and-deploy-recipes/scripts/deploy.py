#!/usr/bin/env python3
"""
Build and deploy recipes website to GitHub.
Runs build_site.py, commits changes, and pushes to GitHub with auto-generated timestamp.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_command(cmd, description="", cwd=None):
    """Run a shell command and handle errors."""
    print(f"\n{'🔄' if not description else '📝'} {description}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def main():
    # Default to current directory or use argument
    if len(sys.argv) > 1:
        repo_dir = Path(sys.argv[1])
    else:
        # If run from scripts folder, go to parent folder
        current = Path.cwd()
        if current.name == "scripts" and (current.parent / "build_site.py").exists():
            repo_dir = current.parent
        else:
            repo_dir = current

    # Verify directory exists and has build script
    if not repo_dir.exists():
        print(f"❌ Directory not found: {repo_dir}")
        sys.exit(1)

    build_script = repo_dir / "build_site.py"
    if not build_script.exists():
        print(f"❌ build_site.py not found in {repo_dir}")
        print(f"   Looked in: {repo_dir}")
        print(f"   Files found: {list(repo_dir.glob('*.py'))[:5]}")
        sys.exit(1)

    print(f"📦 Building recipes website in: {repo_dir}")
    print("=" * 60)

    # Step 1: Run build script
    if not run_command(f"python3 build_site.py", "🏗️  Building website", cwd=repo_dir):
        sys.exit(1)

    print("\n✅ Website built successfully")

    # Step 2: Check git status
    run_command("git status", "📊 Git status", cwd=repo_dir)

    # Step 3: Commit changes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"Update recipes - {timestamp}"

    print(f"\n🔄 Staging all changes...")
    if not run_command("git add .", "", cwd=repo_dir):
        print("⚠️  Warning: git add failed")

    print(f"💾 Creating commit: '{commit_msg}'")
    result = subprocess.run(
        f'git commit -m "{commit_msg}"',
        shell=True,
        cwd=repo_dir,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)
    elif "nothing to commit" in result.stderr:
        print("ℹ️  No changes to commit")
    else:
        print(f"❌ Commit failed: {result.stderr}")
        sys.exit(1)

    # Step 4: Push to GitHub
    print(f"\n🚀 Pushing to GitHub...")
    if not run_command("git push origin main", "", cwd=repo_dir):
        print("❌ Push failed - check your GitHub credentials and internet connection")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✨ Done! Your website is now live on GitHub.")
    print(f"📅 Commit: Update recipes - {timestamp}")
    print("=" * 60)

if __name__ == "__main__":
    main()
