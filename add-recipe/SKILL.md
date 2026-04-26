---
name: add-recipe
description: Add a new recipe to your collection from a URL or file. This skill lets you quickly import recipes from the web or from local files (PDF, Word, images, text) and converts them to Markdown using your recipe template. Use when you want to add recipes - say things like "add recipe", "voeg recept toe", "import recipe from URL", or just share a link and Claude will handle the rest.
---

# Add Recipe

Easily add new recipes to your collection. This skill handles the entire process:
1. You provide a recipe source (URL or file)
2. Claude extracts the recipe content
3. Converts to Markdown using your template
4. Saves to `input/` folder ready for building

## How it works

When you say something like **"Add recipe"** or **"Voeg recept toe"**, this skill:

### Step 1: Ask for input
- **URL**: Paste a link to a recipe website
- **File**: Upload a PDF, Word doc, image, or text file with recipe content

### Step 2: Extract recipe
- If URL: Visit the link, extract recipe (title, ingredients, instructions, etc.)
- If file: Read and parse the file content

### Step 3: Convert to template
Using your existing recipe template format:
```markdown
---
porties: [number]
totale bereidingstijd: [time]
bron: [source]
cover-image: [optional image URL]
---

# [Recipe name]

---
## Ingrediënten
- ingredient 1
- ingredient 2

---
## Instructies
1. Step 1
2. Step 2

---
## Tip
[Optional tip]
```

### Step 4: Save to folder
Saves the recipe as a `.md` file in your `input/` folder with a descriptive name.

## What you provide

- **Recipe source**: 
  - URL to a recipe website (allrecipes.com, budget-bytes, etc.)
  - File: PDF, Word document, screenshot of recipe, text file
  - Or describe a recipe idea and Claude will create it

- **Recipe name** (if not obvious from source)

## Output

A new Markdown file in `/Users/samtenvoorde/Documents/recepten/input/` ready to be built into your website.

Example: `Tiramisu.md`, `Pasta Carbonara.md`, etc.

## Next steps

After adding the recipe:
1. Review the generated Markdown file
2. Make any edits if needed
3. Use **"Update recepten website"** skill to build and deploy

## Template requirements

Your recipes MUST follow this structure:
- **Frontmatter**: porties, totale bereidingstijd, bron, cover-image
- **Title**: # Recipe Name
- **Ingrediënten**: ## Ingrediënten section with bullet points
- **Instructies**: ## Instructies section with numbered steps
- **Tip**: Optional ## Tip section

## Supported sources

- Recipe websites (allrecipes.com, budget-bytes, etc.)
- PDF files with recipes
- Word documents (.docx)
- Images/screenshots of recipes
- Text files with recipe content
- Direct recipe descriptions from you

## Notes

- The skill will ask clarifying questions if recipe data is unclear
- Cooking times should be in Dutch format (e.g., "30 minuten")
- Portions should be simple (e.g., "4 personen")
- If a source image is available, it will be included in the frontmatter
- Files are saved with descriptive names (recipe name + .md)

---

**When to use this skill:**

Use "add recipe" whenever you want to add a new recipe to your collection:
- Found a recipe online you want to save
- Have a PDF or document with a recipe
- Want to add your own recipe idea
- Got a screenshot of a recipe you like
