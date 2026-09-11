# Word of God: 1769 King James Bible Digital Library & Audio PWA

A modern, modular, and cloud-streaming digital edition of the 1769 Authorized King James Bible.

This repository transforms a monolithic 1,437-page compilation into 66 modular individual book PDFs, dual interactive Master Index directories (offline desktop and mobile cloud streaming), and an installable Progressive Web App (PWA) with synchronized audio narration and real-time verse tracking.

---

## 🚀 Quick Access

* **📱 Live Progressive Web App (PWA)**: [https://vtrandal.github.io/WordofGod/](https://vtrandal.github.io/WordofGod/)
* **☁️ Cloud Streaming Master Index**: [`Master_Index_Cloud.pdf`](https://cdn.jsdelivr.net/gh/vtrandal/WordofGod@main/Master_Index_Cloud.pdf)
* **📑 Complete Architecture & Design Document**: [`Design_Document.pdf`](Design_Document.pdf)
* **💡 Project Roadmap & Backlog Ideas**: [`IDEAS.md`](IDEAS.md)

---

## ✨ Features & Architecture

### 1. 📱 Progressive Web App (PWA) Scripture & Audio Reader
* **Zero-Store Friction**: Installs directly to your iPhone or Android home screen without App Store approval or compilation binaries.
* **Synchronized Audio Narration (Word-of-Promise Experience)**: Real-time active verse highlighting with smooth auto-scroll centering and playback rate controls (0.75x to 1.5x), demonstrated on Genesis 1.
* **Lock-Screen Media Controls**: Full integration with the W3C `MediaSession` API, showing chapter titles and playback controls on your device lock screen, Control Center, and CarPlay.
* **Dynamic Text Reflow**: Solves the mobile PDF "pinch-and-zoom" problem with responsive typography and adjustable font sizes (`A-` / `A+`).
* **Instant Book Search**: Real-time client-side filter to find any of the 66 books instantly.
* **Offline Caching**: Built-in Service Worker (`sw.js`) caches the application shell and read volumes for uninterrupted offline reading.

### 2. 📚 66 Modular Book PDFs
* Sliced losslessly from the original 1,437-page volume using PDF outline bookmarks.
* Every book begins cleanly on its own title page with zero text overlap.
* Zero-padded canonical prefixes (`01_Genesis.pdf` through `66_Revelation.pdf`) preserve biblical order across all operating systems and file managers.
* Includes standalone [`00_Front_Matter.pdf`](books/00_Front_Matter.pdf) containing the original title page, public domain declaration, and printed index.

### 3. 📑 Dual-Tier Master Directories
* **Local Offline Master Index ([`Master_Index.pdf`](Master_Index.pdf))**:
  * Formal 5-page PDF compiled with LaTeX.
  * Pages 1–4 contain the original front matter.
  * Page 5 features a balanced two-column directory (Old Testament on left, New Testament on right).
  * Direct relative `/GoToR` filesystem links to the local `books/` folder for 100% offline desktop use.
* **Cloud-Streaming Master Index ([`Master_Index_Cloud.pdf`](Master_Index_Cloud.pdf))**:
  * Identical elegant visual layout, but all 67 book links route through a high-speed CDN returning `Content-Type: application/pdf`.
  * Renders books inline instantly on iPhones, iPads, and Android devices without prompting "Where to save this file?".

---

## 📲 How to Install the PWA on Mobile

### On Apple iOS (iPhone / iPad)

> [!IMPORTANT]
> **In-App Messaging Apps (Messenger, Gmail, Slack, etc.) Workaround:**
> If you tap the link inside Facebook Messenger or other messaging apps, iOS opens it in a sandboxed in-app webview (`WKWebView`) where Apple hides the "Add to Home Screen" option.
> 
> **To install:**
> 1. Long-press the link in your messaging app and select **"Open in Safari"** (or tap the compass/Safari icon in the bottom-right corner of the in-app view).
> 2. Once in native **Mobile Safari**, tap the **Share** button (the square with an arrow pointing up).
> 3. Scroll down and tap **"Add to Home Screen"**.
> 4. Tap **Add**.
> 
> The **WordofGod** app icon will appear on your iPhone springboard and launch full-screen as a native app.

### On Android (Chrome / Edge)
1. Navigate to [https://vtrandal.github.io/WordofGod/](https://vtrandal.github.io/WordofGod/) in Google Chrome.
2. Tap the three dots menu (**⋮**) in the top right.
3. Tap **"Install app"** or **"Add to Home screen"**.
4. Launch directly from your home screen or app drawer.

---

## 📂 Repository Structure

```text
WordofGod/
├── books/                     # 67 extracted PDFs (00_Front_Matter + 66 books)
│   ├── 00_Front_Matter.pdf
│   ├── 01_Genesis.pdf
│   └── ... (66_Revelation.pdf)
├── icons/                     # High-resolution PWA icons
│   ├── apple-touch-icon.png   # 180x180 iOS springboard icon
│   ├── icon-192.png           # 192x192 Android / PWA icon
│   ├── icon-512.png           # 512x512 splash screen icon
│   └── icon.svg               # Vector source icon
├── index.html                 # PWA reading portal & audio player
├── manifest.json              # Web App Manifest (standalone display)
├── sw.js                      # Service Worker (offline cache engine)
├── Master_Index.tex           # LaTeX source for local offline directory
├── Master_Index.pdf           # Compiled local master directory
├── Master_Index_Cloud.tex     # LaTeX source for cloud-streaming directory
├── Master_Index_Cloud.pdf     # Compiled cloud-streaming master directory
├── split_bible.py             # Script to extract books from source PDF
├── generate_indexes.py        # Master rebuild orchestrator
├── Design_Document.tex        # Complete Software Design Description (LaTeX)
├── Design_Document.pdf        # Compiled 14-page formal Design Document
├── IDEAS.md                   # Implemented solutions and future backlog
└── KJV-Holy-Bible-1769.pdf    # Original monolithic source PDF (1,437 pages)
```

---

## 🛠️ Automated Rebuilding

To inspect page counts dynamically and rebuild all indexes and formats in a single command:

```bash
python3 generate_indexes.py
```

This single command:
1. Audits all 67 files in `./books/` and verifies exact page numbers.
2. Updates and compiles `Master_Index.pdf` (local relative links).
3. Updates and compiles `Master_Index_Cloud.pdf` (CDN inline stream links).
4. Synchronizes and updates `index.html`.
5. Cleans up all transient LaTeX auxiliary files (`.aux`, `.log`, `.out`).

### Prerequisites
* Python 3.10+
* `pypdf` (`pip install pypdf`)
* TeX Live / `pdflatex` (with `pdfpages`, `tabularx`, and `geometry`)

---

## 📜 Public Domain & License

* **Scripture Text**: The King James Bible (1769 Authorized Version) is in the **Public Domain**.
* **Software Code & Automation**: The Python scripts, LaTeX templates, Service Worker, and PWA codebase in this repository are released under the [MIT License](LICENSE) or dedicated to the public domain.
