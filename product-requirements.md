# Product Requirements Document (PRD): Word of God PWA (`index.html`)

**Document Version:** 1.0.0  
**Target File:** [`index.html`](index.html)  
**Status:** Implemented / Production Verified  
**Deployment URL:** [https://vtrandal.github.io/WordofGod/](https://vtrandal.github.io/WordofGod/)  
**Release Milestone:** `v1.0.0-pwa`  
**Date:** September 2026  

---

## 1. Executive Summary & Product Vision

### 1.1 Purpose
The **Word of God PWA** (`index.html`) serves as the central digital reading portal and interactive audio reader for the 1769 King James Bible (Authorized Version). It modernizes a historical 1,437-page monolithic text into an installable, mobile-optimized web application delivering instant navigation across all 66 canonical books, multi-tier document access (local offline vs. cloud streaming), and synchronized audio narration mimicking the core experience of dramatized audio scripture apps (the "Word of Promise" experience).

### 1.2 Core Problems Solved
1. **The Mobile PDF Pinch-and-Zoom Handicap**: Standard PDF files on mobile screens have fixed coordinate layouts requiring constant horizontal panning and manual zooming. The PWA delivers responsive HTML typography that reflows automatically to any viewport.
2. **The iOS Speech Synthesis 2-Utterance Wall**: Mobile Safari revokes programmatic audio after two verses when chained through asynchronous callbacks. The PWA circumvents this via a single continuous chapter utterance.
3. **Cross-Platform Boundary Inconsistency**: Operating systems (like Linux Chrome) omit native speech word-boundary timing events. The PWA provides a dual-engine tracking system with an automatic timing-assisted fallback.
4. **App Store Overhead & Installation Friction**: Zero compilation binaries, zero developer accounts, and zero App Store fees. The application installs directly from Mobile Safari and Android Chrome to the device home screen.

---

## 2. User Personas & Core Use Cases

| Persona | Primary Environment | Primary Goal | Critical Requirement |
| :--- | :--- | :--- | :--- |
| **Mobile Devotional Reader** | iPhone / iOS Safari | Daily scripture reading & listening on the go | Standalone fullscreen UI, audio narration with lock-screen controls, dynamic text resizing. |
| **Desktop Scholar** | Ubuntu Linux / Chrome / Firefox | Deep study and cross-referencing | Quick book filtering, immediate access to local offline PDFs and cloud-hosted volumes. |
| **Offline Traveler** | Airplane / Low Connectivity | Reading and listening without internet | PWA Service Worker caching app shell and accessed volumes persistently. |

---

## 3. Information Architecture & UI Layout

The interface is structured into three visual tiers:

1. **Top Application Bar & Hero**:
   * App branding and vector iconography.
   * Dynamic Service Worker offline readiness indicator (`● Offline Ready`).
   * PWA Installation trigger button (`📲 Install App`).
   * Quick-launch buttons to master directories:
     * ☁️ Cloud Master Index (`Master_Index_Cloud.pdf`)
     * 📄 Local Master Index (`Master_Index.pdf`)
     * 📖 Original Front Matter (`books/00_Front_Matter.pdf`)

2. **Feature Spotlight & Real-Time Filter**:
   * **"Word of Promise" Experience Demo Card**: Prominent call-to-action launching the interactive Genesis 1 audio reader.
   * **Instant Search Input**: Debounced client-side filter filtering cards across Old and New Testaments in $< 5\text{ms}$.

3. **Two-Column Canonical Bookshelf Grid**:
   * **Old Testament Section**: 39 books (Genesis to Malachi).
   * **New Testament Section**: 27 books (Matthew to Revelation).
   * **Card Elements**:
     * Zero-padded canonical number (e.g., `01`, `40`).
     * Book Title (e.g., `Genesis`, `Matthew`).
     * Audio reader action button (`▶ Listen`) for enabled chapters.
     * High-speed CDN PDF action button (`68 pp. ↗`) returning `Content-Type: application/pdf`.

4. **Interactive Reading & Narration Modal Overlay**:
   * Fullscreen modal (`#readerModal`) with fixed sticky header.
   * Font size adjusters (`A-` and `A+`).
   * Close button (`✕`).
   * Vertically scrollable verse container (`#versesContainer`).
   * Floating bottom audio playback controller with speed toggle (`0.75x` to `1.5x`).

---

## 4. Functional Requirements (FR)

### FR-1: Progressive Web App (PWA) Capabilities
* **FR-1.1 Standalone Display**: Must include `<link rel="manifest" href="manifest.json">` configured with `"display": "standalone"` and `"theme_color": "#1e3a8a"`.
* **FR-1.2 iOS Web App Capable**: Must specify `<meta name="apple-mobile-web-app-capable" content="yes">` and custom iOS springboard touch icons (`icons/apple-touch-icon.png`).
* **FR-1.3 Install Prompt Handling**: Must intercept `beforeinstallprompt` on Chromium browsers to reveal the installation button. If on iOS Safari, clicking the button must present a guide directing the user to the native Safari Share Sheet ("Add to Home Screen").

### FR-2: Client-Side Real-Time Book Filtering
* **FR-2.1 Instant Query Execution**: The search input field (`#searchBox`) must execute an `oninput` filter without requiring a form submission or page reload.
* **FR-2.2 Substring Matching**: The filter must perform case-insensitive substring matching against each card's `data-title` attribute.
* **FR-2.3 DOM State Preservation**: Non-matching cards must be hidden via `display: none` and matching cards revealed via `display: flex` without altering column structure.

### FR-3: Multi-Format Master Document Routing
* **FR-3.1 Cloud Master Index Link**: Header button must route to `Master_Index_Cloud.pdf` with CDN inline streaming endpoints.
* **FR-3.2 Local Master Index Link**: Header button must route to `Master_Index.pdf` using local `/GoToR` filesystem links.
* **FR-3.3 Front Matter Link**: Header button must route to `books/00_Front_Matter.pdf`.

### FR-4: Fullscreen Scripture Reader Modal
* **FR-4.1 Dynamic DOM Injection**: Clicking `▶ Read & Listen: Genesis 1` or `▶ Listen` must invoke `openReader(bookTitle, chapterNum)` to dynamically generate verse DOM elements inside `#versesContainer`.
* **FR-4.2 Numbered Verse Rendering**: Each verse must be rendered within a `.verse` element containing a distinct `.verse-num` badge and verse text.
* **FR-4.3 Viewport Reset**: Opening the modal must automatically reset scroll position to `(0, 0)`.

### FR-5: Dynamic Typography Reflow & Font Scaling
* **FR-5.1 Responsive Text Reflow**: Verse text must reflow naturally to any viewport width (from 320px smartphones to 4K displays).
* **FR-5.2 Scalable Reader Sizing**: The reader toolbar must provide `A-` and `A+` controls dynamically adjusting `#readerContent` font size in 2px increments clamped between `14px` and `28px`.

### FR-6: Continuous Speech Narration Engine
* **FR-6.1 Zero External Runtime Dependencies**: Audio synthesis must use the native browser Web Speech API (`window.speechSynthesis`), requiring zero external audio libraries or pre-recorded MP3 bundles.
* **FR-6.2 Single Continuous Utterance Architecture**: To defeat the iOS WebKit user-gesture timeout (which terminates audio after two verses), all remaining verses from the chosen starting point to the end of the chapter must be assembled into a single continuous text string passed to one `SpeechSynthesisUtterance`.
* **FR-6.3 Garbage Collection Anchor**: The active utterance must be stored on `window._activeUtterance` to prevent browser JavaScript garbage collection from harvesting the speech object mid-chapter.
* **FR-6.4 Speech Parameters**: Narration must execute at a reverent biblical pitch (`0.95`) and respect the user-selected playback rate (`0.75x`, `1.0x`, `1.25x`, `1.5x`).

### FR-7: Dual-Mode Verse Tracking & Auto-Scroll Centering
* **FR-7.1 Primary Tracking (Native Boundary Events)**: As speech progresses, the engine must listen to `currentUtterance.onboundary`. When `event.charIndex` crosses a verse's recorded character offsets (`startChar` to `endChar`), the active verse index must update immediately.
* **FR-7.2 Secondary Tracking (Timing-Assisted Fallback)**: If running on platforms where `onboundary` is unprovided or suppressed (such as Linux Chrome with network-based voices), an internal pace-tracking interval (200ms) must calculate elapsed time against estimated verse durations based on word count (~140 wpm scaled by playback rate) to advance the highlight automatically.
* **FR-7.3 Visual Active Highlighting**: The currently spoken verse must receive the `.active` CSS class (gold accent border and subtle background highlight).
* **FR-7.4 Smooth Auto-Scroll**: The active verse must be scrolled into view using `scrollIntoView({ behavior: 'smooth', block: 'center' })`.

### FR-8: Interactive Verse Jumping & Playback Controls
* **FR-8.1 Direct Verse Tap**: Tapping any verse in the reader view must instantly trigger `jumpToVerse(idx)`, halting existing audio, assembling a new continuous string starting from the tapped verse, and immediately resuming playback.
* **FR-8.2 Play/Pause Toggle**: The floating audio bar button must toggle between `▶` and `⏸`, pausing or resuming continuous speech from the currently active verse.
* **FR-8.3 Rate Switching**: Selecting a new playback speed in the dropdown must immediately restart speech at the active verse at the updated rate.

### FR-9: W3C MediaSession API & Lock-Screen Controls
* **FR-9.1 Track Metadata**: When playback begins, `navigator.mediaSession.metadata` must publish:
  * `title`: Currently active book and verse (e.g., `Genesis 1:1`).
  * `artist`: `King James Version (1769)`.
  * `album`: `Word of God`.
* **FR-9.2 Hardware & Lock-Screen Action Handlers**: Handlers for `'play'` and `'pause'` must bind to `togglePlayAudio()`, allowing playback control from the iOS Control Center, lock screen, and CarPlay.

### FR-10: Service Worker & Offline Cache Architecture
* **FR-10.1 App Shell Caching**: `sw.js` must implement a **Stale-While-Revalidate** strategy for core shell files (`index.html`, `manifest.json`, `icons/*`).
* **FR-10.2 Media & Document Caching**: `sw.js` must implement a **Cache-First** strategy for streaming PDFs and media assets. Once viewed, documents are served from local `CacheStorage` without internet.
* **FR-10.3 Versioned Invalidation**: Service Worker cache versions (e.g., `word-of-god-shell-v4`) must automatically purge obsolete caches on activation.

---

## 5. Non-Functional Requirements (NFR)

| ID | Category | Specification |
| :--- | :--- | :--- |
| **NFR-1** | **Zero Dependencies** | Written strictly in vanilla HTML5, CSS3, and modern ECMAScript. No external JavaScript frameworks (React, Vue, jQuery) or CSS frameworks (Tailwind, Bootstrap). |
| **NFR-2** | **Performance & Latency** | Client-side search filtering across 66 cards must complete in $< 10\text{ms}$. Reader modal DOM instantiation must complete in $< 50\text{ms}$. |
| **NFR-3** | **Responsive Design** | 100% fluid layouts adapting seamlessly from 320px mobile screens to 3840px desktop displays. |
| **NFR-4** | **Theme Adaptation** | Automatically supports OS Light and Dark modes via CSS `prefers-color-scheme` using custom CSS properties. |
| **NFR-5** | **Cross-Platform Compatibility** | Fully functional across Mobile Safari (iOS 16+), Android Chrome, desktop Google Chrome, Mozilla Firefox, and Microsoft Edge. |
| **NFR-6** | **Zero Operational Cost** | Static hosting on GitHub Pages with CDN routing on jsDelivr. Zero cloud server expenses. |

---

## 6. Known Platform Constraints & Mitigated Architectural Traps

### 6.1 The iOS In-App Browser Trap
* **Constraint**: When links are shared via messaging apps (Facebook Messenger, Gmail, Slack), iOS opens them in a sandboxed `WKWebView` where Apple suppresses the "Add to Home Screen" menu.
* **Mitigation**: Documented in `README.md` and PWA alerts: users must long-press the link in Messenger and select **"Open in Safari"** to access the native Share Sheet.

### 6.2 The iOS Universal Link Trap
* **Constraint**: URLs hosted on `github.com` trigger iOS Universal Links, hijacking web traffic into the native GitHub developer mobile app and demanding authentication.
* **Mitigation**: Web app is deployed to GitHub Pages (`vtrandal.github.io/WordofGod`), completely bypassing developer-app interception.

### 6.3 The Linux Chrome `onboundary` Silent Drop
* **Constraint**: Google Chrome on Linux utilizes remote network speech voices that omit native `onboundary` word timing events.
* **Mitigation**: The dual-engine tracking system transparently falls back to an internal word-count-based pace timer (~140 wpm) so highlights advance seamlessly.

### 6.4 The iOS Multi-Utterance Chaining Block
* **Constraint**: iOS Safari treats programmatic calls to `speechSynthesis.speak()` made inside `onend` callbacks as unprompted audio, halting playback after two verses.
* **Mitigation**: Single continuous chapter string architecture ensures the entire chapter plays under the original user tap authorization.

---

## 7. Future Enhancement Backlog

The following capabilities are tracked for subsequent development cycles:

1. **Multi-Chapter Reader Expansion**:
   * Extract and embed Chapter 1 across all 66 books, enabling the `▶ Listen` button on every bookshelf card.
   * Expand chapter selection menus to read all 1,189 biblical chapters.
2. **One-Click Full Library Offline Caching (Idea 4)**:
   * Add a single "Download Entire Bible for Offline Use" button that pre-fetches all 66 book PDFs into persistent Cache API storage.
3. **Studio Dramatized Narration Integration**:
   * Add an audio source selector allowing users to switch between synthetic device speech and studio-recorded human voice actors (public domain dramatized KJV recordings) while maintaining real-time verse auto-scrolling.
