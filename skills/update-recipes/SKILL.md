---
name: update-recepten-website
description: Update your recipes website by building and/or deploying. This skill runs build_site.py to regenerate index.html from your Markdown recipes, and deploy.py to commit and push to GitHub. Use whenever you've added or modified recipes and want to update your live website. Trigger this when you say things like "update recepten website", "build and deploy recipes", "push recipe updates", or "generate and deploy website".
---

# Update Recepten Website

Automate your full recipes website workflow. This skill lets you:
- **Build**: Regenerate `index.html` from your Markdown recipe files
- **Deploy**: Commit changes and push to GitHub with a timestamped message
- **Both**: Build + deploy in one go

## What the skill does

When you ask to update your recipes website, this skill:

1. Asks if you want to **build** (regenerate the website), **deploy** (commit+push to GitHub), or **both**
2. Runs `build_site.py` in your `deploy-scripts/` folder to create the latest `index.html`
3. Runs `deploy.py` to handle Git workflow:
   - Stages all changes
   - Creates a commit with timestamp: `"Update recipes - [date/time]"`
   - Pushes to GitHub `main` branch

## Prerequisites

Your recepten folder structure should be:
```
/Users/samtenvoorde/Documents/recepten/
├── deploy-scripts/
│   ├── build_site.py
│   ├── deploy.py
│   └── deploy.sh
├── input/           (your recipe .md files)
├── index.html       (generated output)
└── .git/            (GitHub repo)
```

## How it works

**Step 1: Choose your action**
The skill asks: "Do you want to build, deploy, or both?"

**Step 2: Build (optional)**
If you chose build or both:
- Runs `python3 deploy-scripts/build_site.py` from your recepten folder
- Regenerates `index.html` from all `.md` files in `input/`
- Shows how many recipes were processed

**Step 3: Deploy (optional)**
If you chose deploy or both:
- Stages all changes: `git add .`
- Creates commit with auto-generated timestamp
- Pushes to GitHub: `git push origin main`

**Step 4: Done!**
Your website is updated and live on GitHub.

## Example uses

**Just built new recipes, deploy them:**
> "Update recepten website"
→ Skill asks what you want, you choose "deploy" → commits and pushes

**Added recipes, need to rebuild and redeploy:**
> "Update mijn recepten website"
→ Skill asks, you choose "both" → builds fresh index.html, then deploys

**Only rebuild the website (no GitHub push):**
> "Update recepten website"
→ Choose "build" → regenerates index.html only

## Notes

- The commit message is always auto-generated with timestamp — no need to type it
- All changes in your recepten folder are included in the commit
- Git credentials must be configured for push to work
- If you just added recipes to `input/`, you probably want to choose "both"
- If you only changed styling or settings, "deploy" alone might be enough

## Troubleshooting

**Build fails**: Check that your Markdown files in `input/` follow the template format
**Deploy fails**: Make sure you have Git configured and credentials set up
**Nothing to commit**: The skill will skip the commit if there are no changes

---

## When to use this skill

Use this skill whenever you want to update your recipes website. It's perfect for:
- Adding new recipes
- Updating existing recipe content
- Making style or layout changes
- Keeping your website in sync with GitHub

Simply say something like:
- "Update recepten website"
- "Build and deploy my recipes"
- "Push recipe changes live"
- "Generate new website and deploy"
