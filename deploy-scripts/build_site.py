#!/usr/bin/env python3
import os
import json
import re

# Go to parent directory (recepten root) since this script is in deploy-scripts/
RECEPTEN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(RECEPTEN_DIR, 'input')
OUTPUT = os.path.join(RECEPTEN_DIR, 'index.html')

def parse_frontmatter(content):
    if not content.startswith('---'):
        return {}, content
    end = content.find('---', 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end+3:].strip()
    fm = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            fm[key.strip()] = value.strip()
    return fm, body

def parse_recipe(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fm, body = parse_frontmatter(content)

    title_match = re.search(r'^# (.+)$', body, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(filepath)

    sections = {}
    current_section = None
    current_lines = []
    for line in body.split('\n'):
        if line.startswith('## '):
            if current_section is not None:
                sections[current_section] = '\n'.join(current_lines).strip()
            current_section = line[3:].strip()
            current_lines = []
        elif not line.startswith('# ') and line.strip() != '---':
            current_lines.append(line)
    if current_section is not None:
        sections[current_section] = '\n'.join(current_lines).strip()

    ingredienten = []
    for line in sections.get('Ingrediënten', '').split('\n'):
        line = line.strip()
        if line.startswith('**') and line.endswith('**'):
            ingredienten.append({'group': line.strip('*')})
        elif line.startswith('- '):
            ingredienten.append(line[2:])

    instructies = []
    for line in sections.get('Instructies', '').split('\n'):
        m = re.match(r'^\d+\.\s+(.+)$', line.strip())
        if m:
            instructies.append(m.group(1))

    return {
        'title': title,
        'porties': fm.get('porties', ''),
        'tijd': fm.get('totale bereidingstijd', ''),
        'bron': fm.get('bron', ''),
        'cover': fm.get('cover-image', ''),
        'ingredienten': ingredienten,
        'instructies': instructies,
        'tip': sections.get('Tip', '').strip(),
    }

recipes = []
for filename in sorted(os.listdir(INPUT_DIR)):
    if filename.endswith('.md') and filename != 'recept template.md':
        try:
            recipes.append(parse_recipe(os.path.join(INPUT_DIR, filename)))
        except Exception as e:
            print(f'Fout bij {filename}: {e}')

recipes_json = json.dumps(recipes, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Recepten</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f5f5f0;
    color: #222;
    min-height: 100vh;
  }}

  header {{
    background: #fff;
    border-bottom: 1px solid #e5e5e0;
    padding: 24px 32px;
    display: flex;
    align-items: center;
    gap: 16px;
    position: sticky;
    top: 0;
    z-index: 10;
  }}
  header h1 {{ font-size: 1.4rem; font-weight: 700; }}
  #search {{
    margin-left: auto;
    padding: 8px 14px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 0.95rem;
    width: 220px;
    outline: none;
    background: #f5f5f0;
  }}
  #search:focus {{ border-color: #888; background: #fff; }}

  #grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
    padding: 32px;
    max-width: 1400px;
    margin: 0 auto;
  }}

  .card {{
    background: #fff;
    border-radius: 14px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    display: flex;
    flex-direction: column;
  }}
  .card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }}

  .card-img {{
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
    background: #e8e8e0;
  }}
  .card-img-placeholder {{
    width: 100%;
    height: 180px;
    background: linear-gradient(135deg, #e8e8e0, #d5d5cc);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
  }}
  .card-body {{
    padding: 16px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .card-title {{ font-size: 1rem; font-weight: 600; line-height: 1.3; }}
  .card-meta {{
    display: flex;
    gap: 12px;
    font-size: 0.8rem;
    color: #777;
    margin-top: auto;
    padding-top: 8px;
  }}
  .card-meta span {{ display: flex; align-items: center; gap: 4px; }}

  /* Modal */
  #overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.45);
    z-index: 100;
    overflow-y: auto;
    padding: 40px 16px;
  }}
  #overlay.open {{ display: flex; justify-content: center; align-items: flex-start; }}

  #modal {{
    background: #fff;
    border-radius: 18px;
    max-width: 720px;
    width: 100%;
    overflow: hidden;
    position: relative;
    animation: slideUp 0.2s ease;
  }}
  @keyframes slideUp {{
    from {{ transform: translateY(20px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
  }}

  #modal-close {{
    position: absolute;
    top: 14px; right: 14px;
    background: rgba(0,0,0,0.35);
    color: #fff;
    border: none;
    border-radius: 50%;
    width: 34px; height: 34px;
    font-size: 1.1rem;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    z-index: 10;
  }}
  #modal-close:hover {{ background: rgba(0,0,0,0.6); }}

  #modal-img {{
    width: 100%;
    height: 280px;
    object-fit: cover;
    display: block;
    background: #e8e8e0;
  }}
  #modal-img-placeholder {{
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #e8e8e0, #d5d5cc);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
  }}

  #modal-content {{ padding: 28px 32px 36px; }}
  #modal-title {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 10px; line-height: 1.2; }}
  #modal-meta {{
    display: flex;
    gap: 20px;
    font-size: 0.875rem;
    color: #666;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
  }}
  #modal-meta span {{ display: flex; align-items: center; gap: 5px; }}

  .section-title {{
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #444;
    margin-bottom: 12px;
  }}

  #modal-ingredienten {{ margin-bottom: 28px; }}
  .ingredient-group {{
    font-weight: 600;
    font-size: 0.875rem;
    color: #555;
    margin: 12px 0 6px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .ingredient-list {{ list-style: none; display: flex; flex-direction: column; gap: 7px; }}
  .ingredient-list li {{
    font-size: 0.95rem;
    padding-left: 16px;
    position: relative;
  }}
  .ingredient-list li::before {{
    content: '';
    position: absolute;
    left: 0; top: 9px;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #aaa;
  }}

  #modal-instructies {{ margin-bottom: 28px; }}
  .step-list {{ list-style: none; display: flex; flex-direction: column; gap: 14px; }}
  .step-list li {{
    display: flex;
    gap: 14px;
    font-size: 0.95rem;
    line-height: 1.5;
  }}
  .step-num {{
    flex-shrink: 0;
    width: 26px; height: 26px;
    background: #222;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    margin-top: 1px;
  }}

  #modal-tip {{
    background: #f9f7f0;
    border-left: 3px solid #c8a84b;
    border-radius: 0 8px 8px 0;
    padding: 14px 16px;
    font-size: 0.9rem;
    line-height: 1.5;
    color: #555;
  }}
  #modal-tip strong {{ display: block; margin-bottom: 4px; color: #333; }}

  #modal-bron {{
    margin-top: 20px;
    font-size: 0.8rem;
    color: #aaa;
    text-align: right;
  }}

  .hidden {{ display: none !important; }}
</style>
</head>
<body>

<header>
  <h1>🍽 Recepten</h1>
  <input type="text" id="search" placeholder="Zoeken..." oninput="filterRecipes()">
</header>

<div id="grid"></div>

<div id="overlay" onclick="closeIfOutside(event)">
  <div id="modal">
    <button id="modal-close" onclick="closeModal()">✕</button>
    <div id="modal-header"></div>
    <div id="modal-content">
      <h2 id="modal-title"></h2>
      <div id="modal-meta"></div>
      <div id="modal-ingredienten"></div>
      <div id="modal-instructies"></div>
      <div id="modal-tip-wrap"></div>
      <div id="modal-bron"></div>
    </div>
  </div>
</div>

<script>
const recipes = {recipes_json};

function emoji(recipe) {{
  const t = recipe.title.toLowerCase();
  if (t.includes('pasta') || t.includes('linguine') || t.includes('penne') || t.includes('orzo') || t.includes('rigatoni')) return '🍝';
  if (t.includes('taco') || t.includes('fajita') || t.includes('wrap') || t.includes('quesadilla')) return '🌮';
  if (t.includes('salade') || t.includes('panzanella')) return '🥗';
  if (t.includes('soep')) return '🍜';
  if (t.includes('noedel') || t.includes('ramen') || t.includes('gyoza')) return '🍜';
  if (t.includes('pizza')) return '🍕';
  if (t.includes('bowl') || t.includes('falafel')) return '🥙';
  if (t.includes('kip') || t.includes('kipschnitzel')) return '🍗';
  if (t.includes('biefstuk')) return '🥩';
  if (t.includes('flatbread')) return '🫓';
  if (t.includes('curry') || t.includes('linzen')) return '🍛';
  return '🍴';
}}

function renderGrid(list) {{
  const grid = document.getElementById('grid');
  grid.innerHTML = list.map((r, i) => `
    <div class="card" onclick="openModal(${{i}})">
      ${{r.cover
        ? `<img class="card-img" src="${{r.cover}}" alt="${{r.title}}" onerror="this.outerHTML='<div class=card-img-placeholder>${{emoji(r)}}</div>'">`
        : `<div class="card-img-placeholder">${{emoji(r)}}</div>`
      }}
      <div class="card-body">
        <div class="card-title">${{r.title}}</div>
        <div class="card-meta">
          ${{r.tijd ? `<span>⏱ ${{r.tijd}}</span>` : ''}}
          ${{r.porties ? `<span>👤 ${{r.porties}}</span>` : ''}}
        </div>
      </div>
    </div>
  `).join('');
}}

let filteredRecipes = [...recipes];

function filterRecipes() {{
  const q = document.getElementById('search').value.toLowerCase();
  filteredRecipes = recipes.filter(r =>
    r.title.toLowerCase().includes(q) ||
    r.ingredienten.some(i => typeof i === 'string' && i.toLowerCase().includes(q))
  );
  renderGrid(filteredRecipes);
}}

function openModal(idx) {{
  const r = filteredRecipes[idx];

  // Header image
  const header = document.getElementById('modal-header');
  if (r.cover) {{
    header.innerHTML = `<img id="modal-img" src="${{r.cover}}" alt="${{r.title}}" onerror="this.outerHTML='<div id=modal-img-placeholder>${{emoji(r)}}</div>'">`;
  }} else {{
    header.innerHTML = `<div id="modal-img-placeholder">${{emoji(r)}}</div>`;
  }}

  document.getElementById('modal-title').textContent = r.title;

  document.getElementById('modal-meta').innerHTML = `
    ${{r.tijd ? `<span>⏱ ${{r.tijd}}</span>` : ''}}
    ${{r.porties ? `<span>👤 ${{r.porties}} personen</span>` : ''}}
    ${{r.bron ? `<span>📖 ${{r.bron}}</span>` : ''}}
  `;

  // Ingredienten
  let ingHtml = '<div class="section-title">Ingrediënten</div><ul class="ingredient-list">';
  r.ingredienten.forEach(item => {{
    if (typeof item === 'object' && item.group) {{
      ingHtml += `</ul><div class="ingredient-group">${{item.group}}</div><ul class="ingredient-list">`;
    }} else {{
      ingHtml += `<li>${{item}}</li>`;
    }}
  }});
  ingHtml += '</ul>';
  document.getElementById('modal-ingredienten').innerHTML = ingHtml;

  // Instructies
  const stepsHtml = '<div class="section-title">Instructies</div><ol class="step-list">' +
    r.instructies.map((s, i) => `<li><span class="step-num">${{i+1}}</span><span>${{s}}</span></li>`).join('') +
    '</ol>';
  document.getElementById('modal-instructies').innerHTML = stepsHtml;

  // Tip
  const tipWrap = document.getElementById('modal-tip-wrap');
  tipWrap.innerHTML = r.tip
    ? `<div id="modal-tip"><strong>Tip</strong>${{r.tip}}</div>`
    : '';

  document.getElementById('modal-bron').innerHTML = r.bron
    ? `Bron: ${{r.bron}}`
    : '';

  document.getElementById('overlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}}

function closeModal() {{
  document.getElementById('overlay').classList.remove('open');
  document.body.style.overflow = '';
}}

function closeIfOutside(e) {{
  if (e.target === document.getElementById('overlay')) closeModal();
}}

document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});

renderGrid(recipes);
</script>
</body>
</html>
'''


with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Site gegenereerd: {OUTPUT}')
print(f'{len(recipes)} recepten verwerkt.')
