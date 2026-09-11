import os
import glob
import subprocess
from pypdf import PdfReader

# High-speed CDN mirror for GitHub repository that serves Content-Type: application/pdf
# enabling on-the-fly inline viewing in iOS Safari, Files app, and desktop browsers
CDN_BASE = "https://cdn.jsdelivr.net/gh/vtrandal/WordofGod@main/books"

def get_book_metadata():
    files = sorted(glob.glob("books/[0-9][0-9]_*.pdf"))
    books = []
    front_matter = None
    
    for f in files:
        basename = os.path.basename(f)
        if basename == "00_Front_Matter.pdf":
            r = PdfReader(f)
            front_matter = {
                "file": f,
                "filename": basename,
                "pages": len(r.pages),
                "title": "Front Matter (Title, Preface, Table of Contents)"
            }
            continue
            
        r = PdfReader(f)
        num_str = basename[:2]
        num = int(num_str)
        name_part = basename[3:-4]
        title = name_part.replace("_", " ")
        
        testament = "OT" if num <= 39 else "NT"
        books.append({
            "num": num,
            "num_str": num_str,
            "title": title,
            "filename": basename,
            "rel_path": f"books/{basename}",
            "cloud_url": f"{CDN_BASE}/{basename}",
            "pages": len(r.pages),
            "testament": testament
        })
    return front_matter, books

def generate_latex_documents(front_matter, books):
    ot_books = [b for b in books if b["testament"] == "OT"]
    nt_books = [b for b in books if b["testament"] == "NT"]

    # 1. Local Edition (Master_Index.tex) - Remains completely intact for local offline use
    _build_single_tex(
        tex_filename="Master_Index.tex",
        pdf_filename="Master_Index.pdf",
        subtitle_note="Local Offline Edition --- Links open local PDF files in ./books/",
        ot_books=ot_books,
        nt_books=nt_books,
        link_key="rel_path",
        overview_text="Offline Local Edition $\\cdot$ Stored in \\texttt{./books/}",
        front_matter_link="books/00_Front_Matter.pdf"
    )

    # 2. Cloud Edition (Master_Index_Cloud.tex) - CDN Streamed for On-The-Fly Viewing
    _build_single_tex(
        tex_filename="Master_Index_Cloud.tex",
        pdf_filename="Master_Index_Cloud.pdf",
        subtitle_note="Cloud Edition --- Opens on the fly from GitHub CDN (iPhone \\& Mobile Ready)",
        ot_books=ot_books,
        nt_books=nt_books,
        link_key="cloud_url",
        overview_text="Cloud Edition $\\cdot$ High-speed CDN mirror of \\texttt{vtrandal/WordofGod}",
        front_matter_link=f"{CDN_BASE}/00_Front_Matter.pdf"
    )

def _build_single_tex(tex_filename, pdf_filename, subtitle_note, ot_books, nt_books, link_key, overview_text, front_matter_link):
    tex = r"""\documentclass[10pt,letterpaper]{article}
\usepackage[top=0.6in,bottom=0.6in,left=0.75in,right=0.75in]{geometry}
\usepackage{pdfpages}
\usepackage{xcolor}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage[hidelinks]{hyperref}

\hypersetup{
    colorlinks=true,
    linkcolor=black,
    urlcolor=blue!70!black,
    citecolor=black,
    pdfauthor={Holy Bible (KJV 1769)},
    pdftitle={The Holy Bible - Master Directory}
}

\renewcommand{\arraystretch}{0.93}

\begin{document}

% 1. Include Front Matter from original document (4 pages)
\includepdf[pages=-]{books/00_Front_Matter.pdf}

% 2. Master Interactive Directory Page
\pagestyle{empty}

\begin{center}
    {\LARGE\bfseries The Holy Bible}\\[0.2em]
    {\normalsize Authorized King James Version (1769)}\\[0.25em]
    {\footnotesize\itshape """ + subtitle_note + r"""}\\[0.4em]
    \rule{0.85\linewidth}{0.4pt}
\end{center}

\vspace{-0.2em}

\noindent
\begin{minipage}[t]{0.485\textwidth}
\centering
{\bfseries\scshape The Old Testament \footnotesize(39 Books)}\\[0.4em]
\begin{tabularx}{\linewidth}{r X r}
\toprule
\textbf{\#} & \textbf{Book} & \textbf{Pages} \\
\midrule
"""
    for b in ot_books:
        tex += f"{b['num']:02d} & \\href{{{b[link_key]}}}{{{b['title']}}} & {b['pages']} pp. \\\\\n"

    tex += r"""\bottomrule
\end{tabularx}
\end{minipage}\hfill
\begin{minipage}[t]{0.485\textwidth}
\centering
{\bfseries\scshape The New Testament \footnotesize(27 Books)}\\[0.4em]
\begin{tabularx}{\linewidth}{r X r}
\toprule
\textbf{\#} & \textbf{Book} & \textbf{Pages} \\
\midrule
"""
    for b in nt_books:
        tex += f"{b['num']:02d} & \\href{{{b[link_key]}}}{{{b['title']}}} & {b['pages']} pp. \\\\\n"

    tex += r"""\bottomrule
\end{tabularx}

\vspace{2em}
\begin{center}
    \small
    \fbox{\parbox{0.88\linewidth}{\centering\vspace{0.4em}
    \textbf{Library Overview}\\
    \footnotesize
    \vspace{0.2em}
    Total: 66 Canonical Books $\cdot$ 1,437 Pages\\
    """ + overview_text + r"""\\
    Front Matter: \href{""" + front_matter_link + r"""}{\textit{00\_Front\_Matter.pdf}}
    \vspace{0.4em}}}
\end{center}

\end{minipage}

\vfill
\begin{center}
    \footnotesize\color{gray}
    Generated with LaTeX $\cdot$ Click links to launch individual book PDFs
\end{center}

\end{document}
"""
    with open(tex_filename, "w") as f:
        f.write(tex)
    print(f"Generated {tex_filename}")

    print(f"Compiling {tex_filename} via pdflatex...")
    result = subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully generated {pdf_filename}!")
        base_name = os.path.splitext(tex_filename)[0]
        for ext in [".aux", ".log", ".out"]:
            aux_f = f"{base_name}{ext}"
            if os.path.exists(aux_f):
                os.remove(aux_f)
    else:
        print(f"pdflatex compilation failed for {tex_filename}. Error log:")
        print(result.stdout[-1000:])

def generate_html_bookshelf(front_matter, books):
    ot_books = [b for b in books if b["testament"] == "OT"]
    nt_books = [b for b in books if b["testament"] == "NT"]

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Holy Bible — KJV (1769) Bookshelf</title>
    <style>
        :root {
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --accent: #1e3a8a;
            --accent-light: #eff6ff;
            --border: #e2e8f0;
            --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
            --shadow-hover: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0f172a;
                --card-bg: #1e293b;
                --text-primary: #f1f5f9;
                --text-secondary: #94a3b8;
                --accent: #60a5fa;
                --accent-light: #172554;
                --border: #334155;
                --shadow: 0 1px 3px rgba(0,0,0,0.4);
                --shadow-hover: 0 4px 8px rgba(0,0,0,0.5);
            }
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text-primary);
            line-height: 1.5;
            padding: 2.5rem 1rem;
        }
        .container {
            max-width: 1050px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        h1 {
            font-size: 2.4rem;
            font-family: Georgia, Cambria, "Times New Roman", Times, serif;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 0.35rem;
            letter-spacing: -0.02em;
        }
        .subtitle {
            color: var(--text-secondary);
            font-size: 1.15rem;
            margin-bottom: 1.25rem;
        }
        .meta-badges {
            display: flex;
            gap: 0.75rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }
        .badge {
            background-color: var(--accent-light);
            color: var(--accent);
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid var(--border);
        }
        .actions-bar {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.65rem 1.35rem;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            font-size: 0.95rem;
            transition: all 0.15s ease-in-out;
        }
        .btn-primary {
            background-color: var(--accent);
            color: #ffffff;
        }
        .btn-primary:hover {
            opacity: 0.92;
            transform: translateY(-1px);
        }
        .btn-cloud {
            background-color: #0284c7;
            color: #ffffff;
        }
        .btn-cloud:hover {
            background-color: #0369a1;
            transform: translateY(-1px);
        }
        .btn-outline {
            background-color: var(--card-bg);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        .btn-outline:hover {
            background-color: var(--accent-light);
            border-color: var(--accent);
        }
        .search-container {
            margin-bottom: 2rem;
            display: flex;
            justify-content: center;
        }
        .search-box {
            width: 100%;
            max-width: 520px;
            padding: 0.8rem 1.25rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--card-bg);
            color: var(--text-primary);
            font-size: 1rem;
            outline: none;
            box-shadow: var(--shadow);
            transition: border-color 0.15s;
        }
        .search-box:focus {
            border-color: var(--accent);
        }
        .grid-sections {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }
        @media (max-width: 768px) {
            .grid-sections {
                grid-template-columns: 1fr;
            }
        }
        .section-header {
            font-size: 1.35rem;
            font-family: Georgia, serif;
            color: var(--accent);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }
        .section-header span {
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-family: sans-serif;
            font-weight: normal;
        }
        .books-list {
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }
        .book-card {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            text-decoration: none;
            color: var(--text-primary);
            box-shadow: var(--shadow);
            transition: all 0.15s ease-in-out;
        }
        .book-card:hover {
            transform: translateX(4px);
            border-color: var(--accent);
            box-shadow: var(--shadow-hover);
        }
        .book-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .book-num {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--text-secondary);
            width: 1.75rem;
        }
        .book-title {
            font-size: 0.95rem;
            font-weight: 600;
        }
        .book-pages {
            font-size: 0.8rem;
            color: var(--text-secondary);
            background: var(--accent-light);
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
        }
        footer {
            margin-top: 3.5rem;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>The Holy Bible</h1>
            <div class="subtitle">Authorized King James Version (1769 Standard Text)</div>
            <div class="meta-badges">
                <span class="badge">66 Books</span>
                <span class="badge">1,437 Pages</span>
                <span class="badge">Hosted on GitHub: vtrandal/WordofGod</span>
            </div>
            <div class="actions-bar">
                <a href="Master_Index_Cloud.pdf" class="btn btn-cloud" target="_blank">
                    ☁️ Open Cloud Master Index (iPhone / Web)
                </a>
                <a href="Master_Index.pdf" class="btn btn-primary" target="_blank">
                    📄 Open Local Master Index
                </a>
                <a href="books/00_Front_Matter.pdf" class="btn btn-outline" target="_blank">
                    📖 Read Front Matter
                </a>
            </div>
        </header>

        <div class="search-container">
            <input type="text" id="searchBox" class="search-box" placeholder="Quick search book by name (e.g. Genesis, Matthew, Romans)..." oninput="filterBooks()">
        </div>

        <div class="grid-sections">
            <!-- Old Testament -->
            <div class="section-col">
                <div class="section-header">
                    The Old Testament
                    <span>39 Books</span>
                </div>
                <div class="books-list" id="otList">
"""
    for b in ot_books:
        html += f"""                    <a href="{b['cloud_url']}" class="book-card" data-title="{b['title'].lower()}" target="_blank">
                        <div class="book-info">
                            <span class="book-num">{b['num']:02d}</span>
                            <span class="book-title">{b['title']}</span>
                        </div>
                        <span class="book-pages">{b['pages']} pp.</span>
                    </a>
"""

    html += """                </div>
            </div>

            <!-- New Testament -->
            <div class="section-col">
                <div class="section-header">
                    The New Testament
                    <span>27 Books</span>
                </div>
                <div class="books-list" id="ntList">
"""
    for b in nt_books:
        html += f"""                    <a href="{b['cloud_url']}" class="book-card" data-title="{b['title'].lower()}" target="_blank">
                        <div class="book-info">
                            <span class="book-num">{b['num']:02d}</span>
                            <span class="book-title">{b['title']}</span>
                        </div>
                        <span class="book-pages">{b['pages']} pp.</span>
                    </a>
"""

    html += """                </div>
            </div>
        </div>

        <footer>
            <p>Word of God &bull; Individual PDFs generated from 1769 King James text &bull; GitHub Cloud Hosted &bull; Standalone</p>
        </footer>
    </div>

    <script>
        function filterBooks() {
            const query = document.getElementById('searchBox').value.trim().toLowerCase();
            const cards = document.querySelectorAll('.book-card');
            cards.forEach(card => {
                const title = card.getAttribute('data-title');
                if (title.includes(query)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""
    with open("index.html", "w") as f:
        f.write(html)
    print("Generated index.html")

if __name__ == "__main__":
    front_matter, books = get_book_metadata()
    generate_latex_documents(front_matter, books)
    generate_html_bookshelf(front_matter, books)
