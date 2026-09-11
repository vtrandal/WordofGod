# Project Ideas & Architecture: Word of God (KJV Bible)

This document tracks both the solutions that have been **implemented** in this repository and the **unimplemented ideas** for future exploration.

---

## 1. Implemented Solutions

The following components have been developed, tested, and are currently functional in the repository:

### A. PDF Book Extraction & Slicing
* **Status**: Implemented & Verified
* **Script**: [`split_bible.py`](file:///home/vtrandal/Documents/projects/WordofGod/split_bible.py)
* **Output Folder**: [`books/`](file:///home/vtrandal/Documents/projects/WordofGod/books/) (67 PDF files total)
* **Details**:
  * Extracted 66 canonical books of the King James Bible (1769 Authorized Version) from [`KJV-Holy-Bible-1769.pdf`](file:///home/vtrandal/Documents/projects/WordofGod/KJV-Holy-Bible-1769.pdf).
  * Automatically detected book boundaries using the PDF's internal outline/bookmarks tree.
  * Verified clean page transitions (every book starts on its own fresh page with no overlap).
  * Extracted [`00_Front_Matter.pdf`](file:///home/vtrandal/Documents/projects/WordofGod/books/00_Front_Matter.pdf) containing the original title, public domain statement, and original printed table of contents.
  * Numbered all books with zero-padded prefixes (`01_Genesis.pdf` through `66_Revelation.pdf`) to preserve canonical ordering in file systems.

### B. LaTeX Master Directory PDF
* **Status**: Implemented & Compiled
* **Source**: [`Master_Index.tex`](file:///home/vtrandal/Documents/projects/WordofGod/Master_Index.tex)
* **Output**: [`Master_Index.pdf`](file:///home/vtrandal/Documents/projects/WordofGod/Master_Index.pdf)
* **Details**:
  * 5-page document compiled via `pdflatex`.
  * Pages 1–4 embed the original front matter using `pdfpages`.
  * Page 5 features an interactive two-column directory (Old Testament on left, New Testament on right).
  * Each book title is an embedded hyperlink using the PDF `/GoToR` (Remote Destination) standard pointing directly to the individual PDF in `./books/`.

### C. Digital Web Bookshelf
* **Status**: Implemented & Verified
* **File**: [`index.html`](file:///home/vtrandal/Documents/projects/WordofGod/index.html)
* **Details**:
  * Lightweight, offline-capable HTML5 reading portal.
  * Divided into Old Testament (39 books) and New Testament (27 books) with book numbers and page counts.
  * Includes a real-time live search filter to instantly find any book by name.
  * Directly links to individual book PDFs and the master index.
  * Free of browser sandbox security warnings.

### D. Automated Index Generator
* **Status**: Implemented & Verified
* **Script**: [`generate_indexes.py`](file:///home/vtrandal/Documents/projects/WordofGod/generate_indexes.py)
* **Details**:
  * Inspects the [`books/`](file:///home/vtrandal/Documents/projects/WordofGod/books/) directory to dynamically gather exact page counts and titles.
  * Automatically generates and compiles [`Master_Index.tex`](file:///home/vtrandal/Documents/projects/WordofGod/Master_Index.tex) into [`Master_Index.pdf`](file:///home/vtrandal/Documents/projects/WordofGod/Master_Index.pdf).
  * Generates the updated [`index.html`](file:///home/vtrandal/Documents/projects/WordofGod/index.html) bookshelf.

---

## 2. Unimplemented Ideas

The following three ideas represent creative, automated ways to achieve complete portability using programming:

### Idea 1: Embed All 66 PDFs Inside the Master PDF (The 1-File Portable Package)
* **Concept**: Use LaTeX's `embedfile` package (already installed on the system) to compile a single master PDF that packs all 66 individual book PDFs directly inside itself as embedded attachments.
* **Key Properties**:
  * **100% Portable**: You have one single file (`Master_Bible.pdf`).
  * No `./books/` folder needed when sharing or moving it.
  * You can email that one file, copy it to a tablet or flash drive, and all 66 books travel inside it.
  * When opened in any standard PDF reader (Acrobat, Evince, Okular, etc.), clicking a book extracts and opens that book's standalone PDF on demand.
  * **Effort**: Zero manual work—the script generates it automatically.

### Idea 2: Web URL Links to the PDFs (Cloud/GitHub Hosted)
* **Concept**: Host the 66 PDFs on a GitHub repository or cloud host, and embed standard `http://` or `https://` web hyperlinks in LaTeX:
  ```latex
  \href{https://.../books/01_Genesis.pdf}{Genesis}
  ```
* **Key Properties**:
  * Each book has a permanent web URL directly to the PDF (e.g., `https://.../books/01_Genesis.pdf`).
  * **Universal Compatibility**: Works on any device in the world (phones, laptops, iPads, browsers).
  * When the reader clicks a link, the browser/reader immediately streams that specific book PDF directly with zero local file dependencies.

### Idea 3: The Single Self-Contained Master Volume with Instant Internal Jumps
* **Concept**: Create a single file where clicking a book instantly jumps to that book's text with no external file dependencies at all.
* **Key Properties**:
  * Built using LaTeX and `pdfpages` with internal PDF destinations (`\hyperlink` / `\hypertarget`).
  * The front matter contains the master index; clicking any book jumps internally to that book's start page with zero delay and zero security popups.
