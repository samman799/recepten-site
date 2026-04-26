---
name: build-and-deploy-recipes
description: Build and deploy your recipes website to GitHub. Runs your build_site.py script to generate the website from Markdown files, then commits and pushes all changes to GitHub with an auto-generated timestamp. Use this whenever you've added or modified recipes and want to update your live website. This is your one-command workflow to go from local changes to live deployment.
---

# Build and Deploy Recipes Website

You're automating the recipe website deployment workflow. This skill handles the entire pipeline: regenerating the website from your Markdown recipe files, committing the changes with a timestamped message, and pushing to GitHub so the site goes live.

## What this skill does

1. **Builds the website** — Runs your `build_site.py` script to convert Markdown recipe files into a static website
2. **Commits changes** — Stages all changes and creates a Git commit with an auto-generated timestamp message
3. **Pushes to GitHub** — Syncs everything to your remote repository so the website updates live

The script runs in your recipe directory and the commit message is automatically formatted as "Update recipes - [date/time]" so you don't have to think about it.

## Prerequisites

Before using this skill, make sure:
- You're in your recipe website directory (`/Users/samtenvoorde/Documents/recepten`)
- Your Git repository is set up and you have a remote called `origin` pointing to GitHub
- Your `build_site.py` script works and creates your website files
- You have the ability to push to GitHub (SSH key or git credentials configured)

## How to use this skill

### From Cowork (easiest) 🎯
Just ask Claude to deploy your site:
- "Deploy mijn recepten website"
- "Bouw en push de website naar GitHub"
- "Run het build script en commit alles"

Claude executes the entire workflow automatically.

### From your terminal
```bash
# Using Python script
cd /Users/samtenvoorde/Documents/recepten
python3 build-and-deploy-recipes/scripts/deploy.py

# Or using the bash script
bash build-and-deploy-recipes/scripts/deploy.sh
```

## The workflow

**Step 1: Run the build**
Execute the build_site.py script in your repository directory. This regenerates the website from all your Markdown recipe files. The script will output how many recipes were processed and confirm the site was generated.

**Step 2: Check what changed**
Look at what files the build script modified or created. Typically this is your `index.html` and any HTML files generated from recipes.

**Step 3: Create a Git commit**
Stage all changes with `git add .`, then create a commit with an auto-generated message. The message format is `"Update recipes - [YYYY-MM-DD HH:MM]"` using the current date and time. This gives you a clean, timestamped history of when each deployment happened.

**Step 4: Push to GitHub**
Push your commit to the `origin/main` branch (or whatever your primary branch is called). This syncs the generated website to your GitHub repository, and if you have a deployment pipeline set up, it will go live automatically.

## Error handling

- **Build script fails**: If `build_site.py` returns an error, stop and debug the script (check that your MD files are valid, etc.) before trying again
- **Git config missing**: If Git doesn't know who you are, you'll get an error about `user.name` and `user.email`. Configure them with:
  ```
  git config user.name "Your Name"
  git config user.email "your.email@example.com"
  ```
- **Can't push**: Make sure you have push access to the GitHub repository and your credentials are set up (SSH keys or personal access token)

## Example

You've just added three new recipes to your `recipes/` folder as Markdown files. You want to:
1. Generate the updated website
2. Deploy it live

Run this skill, and it will handle the entire workflow automatically — no manual Git commands needed.

## Notes

- The commit message always includes the current timestamp, so you don't have to think about describing the change
- All changes in your working directory are included in the commit (the script uses `git add .`)
- The workflow assumes you're pushing to `origin` on the `main` branch — if your setup differs, let me know and we can adjust
