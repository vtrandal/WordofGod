import os
import glob
import subprocess
import json
from pypdf import PdfReader

CDN_BASE = "https://cdn.jsdelivr.net/gh/vtrandal/WordofGod@main/books"

GENESIS_1_VERSES = [
    "In the beginning God created the heaven and the earth.",
    "And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.",
    "And God said, Let there be light: and there was light.",
    "And God saw the light, that it was good: and God divided the light from the darkness.",
    "And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.",
    "And God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters.",
    "And God made the firmament, and divided the waters which were under the firmament from the waters which were above the firmament: and it was so.",
    "And God called the firmament Heaven. And the evening and the morning were the second day.",
    "And God said, Let the waters under the heaven be gathered together unto one place, and let the dry land appear: and it was so.",
    "And God called the dry land Earth; and the gathering together of the waters called he Seas: and God saw that it was good.",
    "And God said, Let the earth bring forth grass, the herb yielding seed, and the fruit tree yielding fruit after his kind, whose seed is in itself, upon the earth: and it was so.",
    "And the earth brought forth grass, and herb yielding seed after his kind, and the tree yielding fruit, whose seed was in itself, after his kind: and God saw that it was good.",
    "And the evening and the morning were the third day.",
    "And God said, Let there be lights in the firmament of the heaven to divide the day from the night; and let them be for signs, and for seasons, and for days, and years:",
    "And let them be for lights in the firmament of the heaven to give light upon the earth: and it was so.",
    "And God made two great lights; the greater light to rule the day, and the lesser light to rule the night: he made the stars also.",
    "And God set them in the firmament of the heaven to give light upon the earth,",
    "And to rule over the day and over the night, and to divide the light from the darkness: and God saw that it was good.",
    "And the evening and the morning were the fourth day.",
    "And God said, Let the waters bring forth abundantly the moving creature that hath life, and fowl that may fly above the earth in the open firmament of heaven.",
    "And God created great whales, and every living creature that moveth, which the waters brought forth abundantly, after their kind, and every winged fowl after his kind: and God saw that it was good.",
    "And God blessed them, saying, Be fruitful, and multiply, and fill the waters in the seas, and let fowl multiply in the earth.",
    "And the evening and the morning were the fifth day.",
    "And God said, Let the earth bring forth the living creature after his kind, cattle, and creeping thing, and beast of the earth after his kind: and it was so.",
    "And God made the beast of the earth after his kind, and cattle after their kind, and every thing that creepeth upon the earth after his kind: and God saw that it was good.",
    "And God said, Let us make man in our image, after our likeness: and let them have dominion over the fish of the sea, and over the fowl of the air, and over the cattle, and over all the earth, and over every creeping thing that creepeth upon the earth.",
    "So God created man in his own image, in the image of God created he him; male and female created he them.",
    "And God blessed them, and God said unto them, Be fruitful, and multiply, and replenish the earth, and subdue it: and have dominion over the fish of the sea, and over the fowl of the air, and over every living thing that moveth upon the earth.",
    "And God said, Behold, I have given you every herb bearing seed, which is upon the face of all the earth, and every tree, in the which is the fruit of a tree yielding seed; to you it shall be for meat.",
    "And to every beast of the earth, and to every fowl of the air, and to every thing that creepeth upon the earth, wherein there is life, I have given every green herb for meat: and it was so.",
    "And God saw every thing that he had made, and, behold, it was very good. And the evening and the morning were the sixth day."
]

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

    # 1. Local Edition (Master_Index.tex)
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

    # 2. Cloud Edition (Master_Index_Cloud.tex)
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

    result = subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], capture_output=True, text=True)
    if result.returncode == 0:
        base_name = os.path.splitext(tex_filename)[0]
        for ext in [".aux", ".log", ".out"]:
            aux_f = f"{base_name}{ext}"
            if os.path.exists(aux_f):
                os.remove(aux_f)
    else:
        print(f"Compilation error in {tex_filename}:", result.stdout[-500:])

def generate_html_pwa_app(front_matter, books):
    ot_books = [b for b in books if b["testament"] == "OT"]
    nt_books = [b for b in books if b["testament"] == "NT"]

    verses_json = json.dumps(GENESIS_1_VERSES)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Word of God — Holy Bible (KJV 1769)</title>

    <!-- PWA Manifest & Meta Tags -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#1e3a8a">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Word of God">
    <link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
    <link rel="icon" type="image/svg+xml" href="icons/icon.svg">
    <link rel="icon" type="image/png" href="icons/icon-192.png">

    <style>
        :root {{
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent: #1e3a8a;
            --accent-light: #eff6ff;
            --gold: #d97706;
            --gold-light: #fef3c7;
            --border: #e2e8f0;
            --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
            --shadow-hover: 0 6px 12px -2px rgba(0,0,0,0.12), 0 3px 6px -2px rgba(0,0,0,0.08);
            --font-reader: Georgia, Cambria, "Times New Roman", Times, serif;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg: #0b0f19;
                --card-bg: #151d30;
                --text-primary: #f8fafc;
                --text-secondary: #94a3b8;
                --accent: #60a5fa;
                --accent-light: #172554;
                --gold: #f59e0b;
                --gold-light: #451a03;
                --border: #1e293b;
                --shadow: 0 2px 4px rgba(0,0,0,0.5);
                --shadow-hover: 0 8px 16px rgba(0,0,0,0.6);
            }}
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text-primary);
            line-height: 1.5;
            padding-bottom: 5rem;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1050px;
            margin: 0 auto;
            padding: 1.5rem 1rem;
        }}
        /* PWA Header Bar */
        .app-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.5rem 0 1.25rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.5rem;
        }}
        .app-brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .app-icon-img {{
            width: 36px;
            height: 36px;
            border-radius: 8px;
            box-shadow: var(--shadow);
        }}
        .app-brand-text h2 {{
            font-size: 1.25rem;
            font-family: var(--font-reader);
            font-weight: 700;
            color: var(--accent);
            line-height: 1.1;
        }}
        .app-brand-text span {{
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}
        .pwa-controls {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .badge-status {{
            font-size: 0.75rem;
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            background: #dcfce7;
            color: #15803d;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }}
        @media (prefers-color-scheme: dark) {{
            .badge-status {{ background: #064e3b; color: #6ee7b7; }}
        }}
        .btn-install {{
            background: var(--gold);
            color: #ffffff;
            border: none;
            padding: 0.4rem 0.85rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            display: none;
        }}
        /* Hero Section */
        .hero {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .hero h1 {{
            font-size: 2.3rem;
            font-family: var(--font-reader);
            color: var(--accent);
            letter-spacing: -0.01em;
            margin-bottom: 0.35rem;
        }}
        .hero p {{
            color: var(--text-secondary);
            font-size: 1rem;
            margin-bottom: 1.25rem;
        }}
        .actions-bar {{
            display: flex;
            justify-content: center;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }}
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.6rem 1.15rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .btn-primary {{ background: var(--accent); color: #fff; }}
        .btn-cloud {{ background: #0284c7; color: #fff; }}
        .btn-listen {{ background: var(--gold); color: #fff; }}
        .btn-outline {{ background: var(--card-bg); color: var(--text-primary); border: 1px solid var(--border); }}
        .btn:hover {{ opacity: 0.92; transform: translateY(-1px); }}

        /* Live Demonstration Banner */
        .demo-card {{
            background: linear-gradient(135deg, rgba(30,58,138,0.08), rgba(217,119,6,0.12));
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .demo-info h3 {{
            font-family: var(--font-reader);
            font-size: 1.15rem;
            color: var(--accent);
            margin-bottom: 0.25rem;
        }}
        .demo-info p {{
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        /* Search Input */
        .search-container {{
            margin-bottom: 2rem;
            display: flex;
            justify-content: center;
        }}
        .search-box {{
            width: 100%;
            max-width: 520px;
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--card-bg);
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            box-shadow: var(--shadow);
        }}
        .search-box:focus {{ border-color: var(--accent); }}

        /* Testament Columns */
        .grid-sections {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }}
        @media (max-width: 768px) {{
            .grid-sections {{ grid-template-columns: 1fr; }}
            .hero h1 {{ font-size: 1.85rem; }}
        }}
        .section-header {{
            font-size: 1.25rem;
            font-family: var(--font-reader);
            color: var(--accent);
            padding-bottom: 0.5rem;
            margin-bottom: 0.85rem;
            border-bottom: 2px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}
        .section-header span {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-family: sans-serif;
        }}
        .books-list {{
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }}
        .book-card {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.6rem 0.9rem;
            text-decoration: none;
            color: var(--text-primary);
            box-shadow: var(--shadow);
            transition: transform 0.15s, border-color 0.15s;
        }}
        .book-card:hover {{
            transform: translateX(3px);
            border-color: var(--accent);
        }}
        .book-info {{
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }}
        .book-num {{
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-secondary);
            width: 1.6rem;
        }}
        .book-title {{
            font-size: 0.95rem;
            font-weight: 600;
        }}
        .book-actions {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .btn-sm {{
            font-size: 0.75rem;
            padding: 0.25rem 0.55rem;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 600;
        }}
        .btn-read {{
            background: var(--gold-light);
            color: var(--gold);
            border: 1px solid rgba(217, 119, 6, 0.3);
        }}
        .btn-pdf {{
            background: var(--accent-light);
            color: var(--accent);
        }}

        /* Reader / Audio Modal */
        .reader-modal {{
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: var(--bg);
            z-index: 9999;
            overflow-y: auto;
            padding: 1rem;
        }}
        .reader-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 1rem 0 6rem;
        }}
        .reader-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            background: var(--bg);
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border);
            z-index: 10;
        }}
        .btn-close {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }}
        .reader-typography-controls {{
            display: flex;
            gap: 0.5rem;
        }}
        .btn-font {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 0.3rem 0.6rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
            color: var(--text-primary);
        }}
        .reader-content {{
            margin-top: 1.5rem;
            font-family: var(--font-reader);
            font-size: 1.15rem;
            line-height: 1.85;
        }}
        .reader-title {{
            font-size: 1.8rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}
        .verse {{
            padding: 0.4rem 0.6rem;
            margin-bottom: 0.35rem;
            border-radius: 6px;
            transition: all 0.25s ease-in-out;
        }}
        .verse-num {{
            font-weight: 700;
            font-size: 0.75rem;
            color: var(--gold);
            vertical-align: super;
            margin-right: 0.35rem;
        }}
        .verse.active {{
            background-color: var(--gold-light);
            box-shadow: 0 0 0 2px var(--gold);
            transform: scale(1.01);
        }}
        /* Audio Player Bar */
        .audio-bar {{
            position: fixed;
            bottom: 0; left: 0; right: 0;
            background: var(--card-bg);
            border-top: 1px solid var(--border);
            padding: 0.75rem 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
            z-index: 100;
        }}
        .btn-play {{
            background: var(--accent);
            color: #fff;
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            font-size: 1.1rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow);
        }}
        .audio-track-info {{
            font-size: 0.85rem;
        }}
        .audio-track-info .track-title {{
            font-weight: 700;
            color: var(--text-primary);
        }}
        .audio-track-info .track-sub {{
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}
        .speed-select {{
            background: var(--bg);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 0.3rem 0.5rem;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- PWA Top App Bar -->
        <div class="app-bar">
            <div class="app-brand">
                <img src="icons/icon-192.png" class="app-icon-img" alt="App Icon">
                <div class="app-brand-text">
                    <h2>Word of God</h2>
                    <span>Holy Bible &bull; KJV 1769 Authorized Version</span>
                </div>
            </div>
            <div class="pwa-controls">
                <span class="badge-status" id="offlineStatus">● Offline Ready</span>
                <button class="btn-install" id="installBtn" onclick="installPWA()">📲 Install App</button>
            </div>
        </div>

        <header class="hero">
            <h1>The Holy Bible</h1>
            <p>66 Canonical Books &bull; 1,437 Pages &bull; Progressive Web App (PWA)</p>
            <div class="actions-bar">
                <a href="Master_Index_Cloud.pdf" class="btn btn-cloud" target="_blank">
                    ☁️ Cloud Master Index (iPhone)
                </a>
                <a href="Master_Index.pdf" class="btn btn-primary" target="_blank">
                    📄 Local Master Index
                </a>
                <a href="books/00_Front_Matter.pdf" class="btn btn-outline" target="_blank">
                    📖 Front Matter
                </a>
            </div>
        </header>

        <!-- Live Audio Synchronization Demonstration Card -->
        <div class="demo-card">
            <div class="demo-info">
                <h3>🎙️ "Word of Promise" Experience Demo</h3>
                <p>Listen to Genesis Chapter 1 with live, synchronized real-time verse highlighting and automatic scrolling.</p>
            </div>
            <button class="btn btn-listen" onclick="openReader('Genesis', 1)">
                ▶ Read &amp; Listen: Genesis 1
            </button>
        </div>

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
        # If Genesis, offer Read in App + View PDF; for others offer Read / PDF
        is_demo = (b["num"] == 1)
        btn_read = f'<button class="btn-sm btn-read" onclick="openReader(\'{b["title"]}\', 1)">▶ Listen</button>' if is_demo else ''
        html += f"""                    <div class="book-card" data-title="{b['title'].lower()}">
                        <div class="book-info">
                            <span class="book-num">{b['num']:02d}</span>
                            <span class="book-title">{b['title']}</span>
                        </div>
                        <div class="book-actions">
                            {btn_read}
                            <a href="{b['cloud_url']}" class="btn-sm btn-pdf" target="_blank">{b['pages']} pp. ↗</a>
                        </div>
                    </div>
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
        html += f"""                    <div class="book-card" data-title="{b['title'].lower()}">
                        <div class="book-info">
                            <span class="book-num">{b['num']:02d}</span>
                            <span class="book-title">{b['title']}</span>
                        </div>
                        <div class="book-actions">
                            <a href="{b['cloud_url']}" class="btn-sm btn-pdf" target="_blank">{b['pages']} pp. ↗</a>
                        </div>
                    </div>
"""

    html += f"""                </div>
            </div>
        </div>
    </div>

    <!-- PWA Interactive Scripture & Audio Reader Modal -->
    <div id="readerModal" class="reader-modal">
        <div class="reader-container">
            <div class="reader-header">
                <button class="btn-close" onclick="closeReader()">&larr; Back to Library</button>
                <div class="reader-typography-controls">
                    <button class="btn-font" onclick="changeFontSize(-1)">A-</button>
                    <button class="btn-font" onclick="changeFontSize(1)">A+</button>
                </div>
            </div>

            <div class="reader-content" id="readerContent">
                <div class="reader-title" id="modalBookTitle">The First Book of Moses, called Genesis</div>
                <h3 style="color: var(--text-secondary); margin-bottom: 1.5rem; font-family: sans-serif; font-size: 1rem;">Chapter 1</h3>

                <div id="versesContainer"></div>
            </div>
        </div>

        <!-- Sticky Floating Audio Control Bar -->
        <div class="audio-bar">
            <button class="btn-play" id="playBtn" onclick="togglePlayAudio()">▶</button>
            <div class="audio-track-info">
                <div class="track-title" id="trackTitle">Genesis 1:1</div>
                <div class="track-sub">King James Authorized Version (1769)</div>
            </div>
            <select class="speed-select" id="speedSelect" onchange="changeSpeed(this.value)">
                <option value="0.75">0.75x</option>
                <option value="1.0" selected>1.0x</option>
                <option value="1.25">1.25x</option>
                <option value="1.5">1.5x</option>
            </select>
        </div>
    </div>

    <script>
        const GENESIS_VERSES = {verses_json};

        let currentVerseIndex = -1;
        let isPlaying = false;
        let synth = window.speechSynthesis;
        let currentUtterance = null;
        let speechSpeed = 1.0;
        let fontSizePx = 18;

        // Register Service Worker for PWA
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('./sw.js')
                    .then(() => {{
                        document.getElementById('offlineStatus').innerText = '● Offline Ready';
                    }})
                    .catch(() => {{
                        document.getElementById('offlineStatus').innerText = 'Online';
                    }});
            }});
        }}

        // Handle PWA Installation
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            const btn = document.getElementById('installBtn');
            if (btn) btn.style.display = 'inline-block';
        }});

        function installPWA() {{
            if (deferredPrompt) {{
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(() => {{
                    deferredPrompt = null;
                    document.getElementById('installBtn').style.display = 'none';
                }});
            }} else {{
                alert('On iPhone: Tap the Share button at the bottom of Safari and select "Add to Home Screen" to install!');
            }}
        }}

        function filterBooks() {{
            const query = document.getElementById('searchBox').value.trim().toLowerCase();
            const cards = document.querySelectorAll('.book-card');
            cards.forEach(card => {{
                const title = card.getAttribute('data-title');
                card.style.display = title.includes(query) ? 'flex' : 'none';
            }});
        }}

        function openReader(bookTitle, chapterNum) {{
            const modal = document.getElementById('readerModal');
            modal.style.display = 'block';
            window.scrollTo(0, 0);

            const container = document.getElementById('versesContainer');
            container.innerHTML = '';

            GENESIS_VERSES.forEach((vText, idx) => {{
                const div = document.createElement('div');
                div.className = 'verse';
                div.id = 'v-' + (idx + 1);
                div.innerHTML = '<span class="verse-num">' + (idx + 1) + '</span> ' + vText;
                div.onclick = () => jumpToVerse(idx);
                container.appendChild(div);
            }});

            // Setup MediaSession API (Lock screen info)
            if ('mediaSession' in navigator) {{
                navigator.mediaSession.metadata = new MediaMetadata({{
                    title: 'Genesis Chapter 1',
                    artist: 'King James Version (1769)',
                    album: 'Word of God'
                }});
                navigator.mediaSession.setActionHandler('play', togglePlayAudio);
                navigator.mediaSession.setActionHandler('pause', togglePlayAudio);
            }}
        }}

        function closeReader() {{
            stopAudio();
            document.getElementById('readerModal').style.display = 'none';
        }}

        function changeFontSize(delta) {{
            fontSizePx = Math.max(14, Math.min(28, fontSizePx + delta * 2));
            document.getElementById('readerContent').style.fontSize = fontSizePx + 'px';
        }}

        let verseOffsets = [];
        let verseDurations = [];
        let playbackStartTime = 0;
        let fallbackTimer = null;
        let hasNativeBoundary = false;

        function highlightVerse(idx) {{
            currentVerseIndex = idx;
            document.getElementById('trackTitle').innerText = 'Genesis 1:' + (idx + 1);

            // Highlight current verse in UI
            document.querySelectorAll('.verse').forEach(el => el.classList.remove('active'));
            const activeEl = document.getElementById('v-' + (idx + 1));
            if (activeEl) {{
                activeEl.classList.add('active');
                activeEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}

            // Lock screen MediaSession integration
            if ('mediaSession' in navigator) {{
                navigator.mediaSession.metadata = new MediaMetadata({{
                    title: 'Genesis 1:' + (idx + 1),
                    artist: 'King James Version (1769)',
                    album: 'Word of God'
                }});
            }}
        }}

        function changeSpeed(val) {{
            speechSpeed = parseFloat(val);
            if (isPlaying) {{
                const idx = currentVerseIndex >= 0 ? currentVerseIndex : 0;
                stopAudio();
                playContinuousAudio(idx);
            }}
        }}

        function togglePlayAudio() {{
            if (isPlaying) {{
                stopAudio();
            }} else {{
                const startIdx = (currentVerseIndex >= 0 && currentVerseIndex < GENESIS_VERSES.length) ? currentVerseIndex : 0;
                playContinuousAudio(startIdx);
            }}
        }}

        function jumpToVerse(idx) {{
            stopAudio();
            playContinuousAudio(idx);
        }}

        function playContinuousAudio(startIdx) {{
            if (startIdx >= GENESIS_VERSES.length) {{
                stopAudio();
                return;
            }}

            // Stop any existing speech session
            if (synth) {{
                synth.cancel();
            }}

            isPlaying = true;
            hasNativeBoundary = false;
            clearInterval(fallbackTimer);
            document.getElementById('playBtn').innerText = '⏸';

            // 1. Build a single continuous string and timing profile
            let fullText = "";
            verseOffsets = [];
            verseDurations = [];
            let accumulatedMs = 0;

            for (let i = startIdx; i < GENESIS_VERSES.length; i++) {{
                const vText = GENESIS_VERSES[i].trim();
                const startChar = fullText.length;
                fullText += vText + " ";
                const endChar = fullText.length;
                verseOffsets.push({{
                    index: i,
                    startChar: startChar,
                    endChar: endChar
                }});

                // Compute estimated duration based on word count:
                // Standard speaking rate: ~140 words per minute (2.33 words/second) at 1.0x
                const words = vText.split(/\\s+/).length;
                const durationMs = Math.max(1200, (words / 140) * 60 * 1000 / speechSpeed);
                verseDurations.push({{
                    index: i,
                    startMs: accumulatedMs,
                    endMs: accumulatedMs + durationMs
                }});
                accumulatedMs += durationMs;
            }}

            // Immediately highlight the starting verse
            highlightVerse(startIdx);
            playbackStartTime = Date.now();

            // 2. Cross-platform fallback timer: for browsers (like Linux Chrome) where onboundary is disabled
            fallbackTimer = setInterval(() => {{
                if (!isPlaying || hasNativeBoundary) return;
                const elapsed = Date.now() - playbackStartTime;
                for (let vd of verseDurations) {{
                    if (elapsed >= vd.startMs && elapsed < vd.endMs) {{
                        if (currentVerseIndex !== vd.index) {{
                            highlightVerse(vd.index);
                        }}
                        break;
                    }}
                }}
            }}, 200);

            // 3. Play as ONE single continuous utterance to bypass iOS gesture-expiration limits
            if (synth) {{
                currentUtterance = new SpeechSynthesisUtterance(fullText);
                currentUtterance.rate = speechSpeed;
                currentUtterance.pitch = 0.95; // Warm biblical cadence

                // Keep reference on window to prevent WebKit garbage collection
                window._activeUtterance = currentUtterance;

                // Native boundary tracking (active on iOS Safari, macOS, etc.)
                currentUtterance.onboundary = (event) => {{
                    if (!isPlaying) return;
                    hasNativeBoundary = true;
                    const charIdx = event.charIndex;
                    for (let r of verseOffsets) {{
                        if (charIdx >= r.startChar && charIdx < r.endChar) {{
                            if (currentVerseIndex !== r.index) {{
                                highlightVerse(r.index);
                            }}
                            break;
                        }}
                    }}
                }};

                currentUtterance.onend = () => {{
                    stopAudio();
                }};

                currentUtterance.onerror = (e) => {{
                    console.warn('SpeechSynthesis error:', e);
                    stopAudio();
                }};

                synth.speak(currentUtterance);
            }}
        }}

        function stopAudio() {{
            isPlaying = false;
            clearInterval(fallbackTimer);
            document.getElementById('playBtn').innerText = '▶';
            if (synth) {{
                synth.cancel();
            }}
            window._activeUtterance = null;
        }}
    </script>
</body>
</html>
"""
    with open("index.html", "w") as f:
        f.write(html)
    print("Generated PWA index.html with Interactive Audio Reader")

if __name__ == "__main__":
    front_matter, books = get_book_metadata()
    generate_latex_documents(front_matter, books)
    generate_html_pwa_app(front_matter, books)
