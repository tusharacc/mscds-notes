"""Generate HTML index for Computer Systems course notes."""

import re
from pathlib import Path


def markdown_to_html(markdown_text):
    """Convert markdown to HTML with basic formatting."""
    html = markdown_text

    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)

    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'\_\_(.*?)\_\_', r'<strong>\1</strong>', html)
    html = re.sub(r'\_(.*?)\_', r'<em>\1</em>', html)

    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Lists (unordered)
    lines = html.split('\n')
    in_list = False
    result = []
    for line in lines:
        if re.match(r'^\s*[\-\*\+]\s+', line):
            if not in_list:
                result.append('<ul>')
                in_list = True
            item = re.sub(r'^\s*[\-\*\+]\s+', '', line)
            result.append(f'<li>{item}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    html = '\n'.join(result)

    # Lists (ordered)
    lines = html.split('\n')
    in_list = False
    result = []
    for line in lines:
        if re.match(r'^\s*\d+\.\s+', line):
            if not in_list:
                result.append('<ol>')
                in_list = True
            item = re.sub(r'^\s*\d+\.\s+', '', line)
            result.append(f'<li>{item}</li>')
        else:
            if in_list:
                result.append('</ol>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ol>')
    html = '\n'.join(result)

    # Paragraphs
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = f'<p>{html}</p>'
    html = html.replace('<p><h', '<h').replace('</h1></p>', '</h1>')
    html = html.replace('</h2></p>', '</h2>').replace('</h3></p>', '</h3>')
    html = html.replace('<p><ul>', '<ul>').replace('</ul></p>', '</ul>')
    html = html.replace('<p><ol>', '<ol>').replace('</ol></p>', '</ol>')
    html = html.replace('<p><pre>', '<pre>').replace('</pre></p>', '</pre>')
    html = html.replace('<p></p>', '')

    return html


def generate_index():
    """Generate the main index.html for computer systems."""
    base_dir = Path(__file__).parent
    weeks = []

    # Read each week's README
    for i in range(1, 11):
        week_dir = base_dir / f"Week{i}"
        readme_path = week_dir / "README.md"

        if readme_path.exists():
            content = readme_path.read_text(encoding='utf-8')
            # Extract title from first heading
            title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else f"Week {i}"

            # Convert markdown to HTML
            html_content = markdown_to_html(content)

            weeks.append({
                'number': i,
                'title': title,
                'content': html_content
            })

    # Generate HTML
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Computer Systems course notes — MScDS IIIT Hyderabad. Weeks 1–10: MIPS, Pipelining, Memory, Networking.">
<title>Computer Systems — Course Notes</title>

<!-- Scholarly fonts: Playfair Display (headings) + Lora (body) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,600&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --page-bg: #faf6ef;
  --surface:  #fffdf9;
  --border:   #e5d9c8;
  --text:     #1c1410;
  --text-muted: #6b5f54;
  --gold:     #92400e;
  --accent:   #c05e2e;
  --toc-w: 270px;
  --radius: 10px;
  --shadow-sm: 0 1px 3px rgba(28,20,16,.06), 0 1px 2px rgba(28,20,16,.04);
  --shadow-md: 0 4px 14px rgba(28,20,16,.10), 0 2px 4px rgba(28,20,16,.06);
}}

html {{ scroll-behavior: smooth; font-size: 16px; }}
body {{
  font-family: 'Lora', Georgia, serif;
  background: var(--page-bg);
  color: var(--text);
  line-height: 1.8;
}}

/* ── Layout ── */
.layout {{ display: flex; min-height: 100vh; }}

/* ── TOC Rail ── */
.toc-rail {{
  width: var(--toc-w); flex-shrink: 0;
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 1.8rem 1rem 2.5rem;
}}
.toc-rail > .toc-title {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: .68rem; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 1.4rem; padding: 0 .4rem;
}}

.toc-week {{ margin-bottom: .8rem; }}
.toc-week a {{
  display: block;
  font-family: 'Lora', Georgia, serif;
  font-size: .82rem; color: var(--text-muted); text-decoration: none;
  padding: .5rem .8rem; border-radius: 6px; line-height: 1.4;
  transition: all .2s;
  border-left: 3px solid transparent;
}}
.toc-week a:hover {{
  color: var(--gold);
  background: rgba(146, 64, 14, 0.05);
  border-left-color: var(--accent);
}}

/* ── Main content ── */
main {{ flex: 1; max-width: 900px; padding: 3rem 2.5rem 6rem; }}

/* ── Page Header ── */
.page-header {{
  margin-bottom: 3.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border);
  position: relative;
}}
.page-header::after {{
  content: '';
  position: absolute; bottom: -3px; left: 0;
  width: 4rem; height: 3px;
  background: var(--gold); border-radius: 2px;
}}
.page-header h1 {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.8rem; font-weight: 800; color: var(--text);
  line-height: 1.15; letter-spacing: -.02em;
}}
.page-header .subtitle {{
  color: var(--text-muted); margin-top: .5rem;
  font-size: .88rem; font-style: italic;
}}

/* ── Week Section ── */
.week-section {{ margin-bottom: 5rem; scroll-margin-top: 2rem; }}
.week-banner {{
  padding: 1.5rem 1.8rem;
  border-radius: 12px; margin-bottom: 2rem;
  background: linear-gradient(135deg, #e0e7ff 0%, #f5f3ff 70%);
  border-left: 5px solid #4338ca;
}}
.week-banner .week-tag {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: .65rem; font-weight: 700; letter-spacing: .16em;
  text-transform: uppercase; opacity: .7;
}}
.week-banner h2 {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.6rem; font-weight: 700; line-height: 1.2; margin-top: .15rem;
}}

/* ── Typography ── */
.content h1, .content h2, .content h3 {{
  font-family: 'Playfair Display', Georgia, serif;
  margin-top: 2rem; margin-bottom: 1rem;
  color: var(--text);
}}
.content h1 {{ font-size: 2rem; font-weight: 700; }}
.content h2 {{ font-size: 1.5rem; font-weight: 700; }}
.content h3 {{ font-size: 1.2rem; font-weight: 600; }}

.content p {{ margin-bottom: 1.2rem; }}
.content ul, .content ol {{ margin-left: 1.5rem; margin-bottom: 1.2rem; }}
.content li {{ margin-bottom: .5rem; }}

.content code {{
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: .88em;
  background: rgba(146, 64, 14, 0.08);
  padding: .15rem .4rem;
  border-radius: 4px;
  color: #92400e;
}}

.content pre {{
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 1.2rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1.5rem;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: .88rem;
  line-height: 1.6;
}}
.content pre code {{
  background: none;
  color: inherit;
  padding: 0;
}}

.content strong {{ font-weight: 600; color: var(--text); }}
.content em {{ font-style: italic; }}

.content table {{
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}}
.content th, .content td {{
  border: 1px solid var(--border);
  padding: .75rem;
  text-align: left;
}}
.content th {{
  background: rgba(146, 64, 14, 0.08);
  font-weight: 600;
}}

/* ── Responsive ── */
@media (max-width: 900px) {{
  .layout {{ flex-direction: column; }}
  .toc-rail {{
    width: 100%; height: auto; position: static;
    border-right: none; border-bottom: 1px solid var(--border);
  }}
  main {{ padding: 2rem 1.5rem; }}
  .page-header h1 {{ font-size: 2rem; }}
}}
</style>
</head>
<body>

<div class="layout">
  <nav class="toc-rail">
    <div class="toc-title">Contents</div>
    {toc}
  </nav>

  <main>
    <div class="page-header">
      <h1>Computer Systems</h1>
      <p class="subtitle">Architecture, Pipelining, and Networking — MScDS IIIT Hyderabad</p>
    </div>

    {weeks}
  </main>
</div>

</body>
</html>
'''

    # Generate TOC
    toc_html = ''
    for week in weeks:
        toc_html += f'''    <div class="toc-week">
      <a href="#week{week['number']}">{week['title']}</a>
    </div>
'''

    # Generate week sections
    weeks_html = ''
    for week in weeks:
        weeks_html += f'''    <section id="week{week['number']}" class="week-section">
      <div class="week-banner">
        <div class="week-tag">Week {week['number']}</div>
        <h2>{week['title']}</h2>
      </div>
      <div class="content">
        {week['content']}
      </div>
    </section>

'''

    # Write output
    output_html = html_template.format(toc=toc_html, weeks=weeks_html)
    output_path = base_dir / "index.html"
    output_path.write_text(output_html, encoding='utf-8')
    print(f"Generated: {output_path}")
    print(f"Total weeks: {len(weeks)}")


if __name__ == '__main__':
    generate_index()
