import markdown
import os
import re
import urllib.request
import base64
import json
from xhtml2pdf import pisa
from pygments.formatters import HtmlFormatter

def process_mermaid_blocks(md_text, output_dir="cloud-escape/graphs"):
    os.makedirs(output_dir, exist_ok=True)
    pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
    
    def replacer(match):
        code = match.group(1).strip()
        payload = {'code': code, 'mermaid': {'theme': 'default'}}
        b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
        url = 'https://mermaid.ink/img/' + b64
        
        filename = f"graph_visual_{abs(hash(code)) % 1000000}.jpg"
        filepath = os.path.abspath(os.path.join(output_dir, filename))
        
        if not os.path.exists(filepath):
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                # If rendering fails, just keep the raw block
                return f"```mermaid\n{code}\n```"
                
        # Use absolute path directly so xhtml2pdf can read it with link_callback
        img_url = filepath.replace('\\', '/')
        return f"![Mermaid Diagram Visualization]({img_url})"

    return pattern.sub(replacer, md_text)

with open('cloud-escape/Stage_1_Comprehensive_Writeup.md', encoding='utf-8') as f1:
    stage1 = f1.read()
    
with open('cloud-escape/Stage_2_Comprehensive_Writeup.md', encoding='utf-8') as f2:
    stage2 = f2.read()

combined_md = f"{stage1}\n\n<pdf:nextpage />\n\n{stage2}"

# Filter out shields.io badges and typing SVG headers (PDF ONLY)
combined_md = re.sub(r'!\[.*?\]\(https://img\.shields\.io/.*?\)', '', combined_md)
combined_md = re.sub(r'<img[^>]*src="https://img\.shields\.io/[^"]*"[^>]*/>?', '', combined_md, flags=re.IGNORECASE)
combined_md = re.sub(r'<img[^>]*src="https://readme-typing-svg\.demolab\.com[^"]*"[^>]*/>?', '', combined_md, flags=re.IGNORECASE)

combined_md = process_mermaid_blocks(combined_md)

md = markdown.Markdown(extensions=['fenced_code', 'tables', 'codehilite', 'toc'])
html_body = md.convert(combined_md)

# FIX FOR xhtml2pdf CODE BLOCKS NEWLINES AND SPACING
def fix_pre_block(match):
    pre_attrs = match.group(1)
    content = match.group(2)
    # Replace newlines with <br/> and double spaces with &nbsp; to preserve formatting
    content = content.replace('\n', '<br/>').replace('  ', '&nbsp;&nbsp;')
    return f"<pre{pre_attrs}>{content}</pre>"

html_body = re.sub(r'<pre(.*?)>(.*?)</pre>', fix_pre_block, html_body, flags=re.DOTALL)

pygments_css = HtmlFormatter(style='friendly').get_style_defs('.codehilite')

html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MAFAT 2026 Writeups</title>
    <style>
        @page {{
            size: A4;
            margin: 0;
            background-image: url('cloud-escape/assets/full_cover.jpg');
        }}
        @page regular {{
            size: A4;
            margin: 1.5cm;
            background-image: url('cloud-escape/assets/pattern_bg_stretched.jpg');
            @frame header_frame {{
                -pdf-frame-content: header_content;
                left: 1.5cm; width: 18cm; top: 1cm; height: 1cm;
            }}
            @frame footer_frame {{
                -pdf-frame-content: footer_content;
                left: 1.5cm; width: 18cm; bottom: 1cm; height: 1cm;
            }}
        }}
        
        body {{
            font-family: Helvetica, Arial, sans-serif;
            font-size: 11pt;
            color: #2c3e50;
            line-height: 1.6;
            word-wrap: break-word;
        }}
        
        h1 {{ color: #2c3e50; font-size: 22pt; text-align: left; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 20pt; }}
        h2 {{ color: #2980b9; font-size: 16pt; margin-top: 15pt; }}
        h3 {{ color: #34495e; font-size: 13pt; margin-top: 10pt; }}
        
        a {{ color: #3498db; text-decoration: none; word-wrap: break-word; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-top: 10pt; margin-bottom: 10pt; table-layout: fixed; word-wrap: break-word; }}
        th {{ background-color: #ecf0f1; border: 1px solid #bdc3c7; padding: 6px; font-weight: bold; text-align: left; word-wrap: break-word; }}
        td {{ border: 1px solid #bdc3c7; padding: 6px; word-wrap: break-word; }}
        
        pre {{ background-color: #f8f9f9; border: 1px solid #d5d8dc; padding: 10px; font-size: 9pt; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; }}
        code {{ font-family: "Courier New", Courier, monospace; background-color: #f2f3f4; padding: 2px 4px; font-size: 9.5pt; color: #e74c3c; border-radius: 3px; word-wrap: break-word; }}
        pre code {{ background-color: transparent; padding: 0; color: inherit; font-size: 9pt; white-space: pre-wrap; word-wrap: break-word; }}
        
        blockquote {{ border-left: 4px solid #3498db; margin-left: 0; padding-left: 15px; color: #7f8c8d; font-style: italic; background-color: #f4f6f7; padding-top: 5px; padding-bottom: 5px; }}
        
        img {{ max-width: 100%; display: block; margin: 10px auto; zoom: 70%; }}
        
        {pygments_css}
        
    </style>
</head>
<body>
    <div style="font-size: 1pt; color: transparent;">Cover</div>
    
    <pdf:nextpage name="regular" />

    <div id="header_content" style="text-align: right; font-size: 8pt; color: #95a5a6; border-bottom: 1px solid #ecf0f1; padding-bottom: 3px;">
        MAFAT 2026 CTF | Operation CloudEscape
    </div>
    <div id="footer_content" style="text-align: center; font-size: 9pt; color: #95a5a6; border-top: 1px solid #ecf0f1; padding-top: 5px;">
        Page <pdf:pagenumber> of <pdf:pagecount>
    </div>
    
    <h1>Table of Contents</h1>
    {md.toc}
    
    <pdf:nextpage />
    
    {html_body}
</body>
</html>
"""

# Must pass link_callback to resolve paths perfectly in Windows
def fetch_resources(uri, rel):
    path = uri
    if uri.startswith('file:///'):
        path = uri.replace('file:///', '')
    if os.path.exists(path):
        return path
    return uri

with open('MAFAT_2026_Writeups_Professional.pdf', 'w+b') as result_file:
    pisa.CreatePDF(html_template, dest=result_file, path=".", link_callback=fetch_resources)
