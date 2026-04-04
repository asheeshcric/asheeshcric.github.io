<div align="center">

# 🌐 jashish.com.np

**Personal website & research portfolio of Ashish Jaiswal**

Research Scientist @ Meta · Applied AI · LLMs · Content Understanding

[![Live Site](https://img.shields.io/badge/🔗_Live-jashish.com.np-2563EB?style=for-the-badge)](https://jashish.com.np)
[![Google Scholar](https://img.shields.io/badge/Scholar-3k+_citations-4285F4?style=for-the-badge&logo=googlescholar&logoColor=white)](https://scholar.google.com/citations?user=sCo50tYAAAAJ&hl=en)

</div>

---

## ⚡ Stack

Static site — zero frameworks, zero build step, instant load.

| Layer | Tech |
|-------|------|
| **Markup** | Semantic HTML5 with JSON-LD structured data |
| **Styles** | Vanilla CSS with custom properties + dark mode |
| **Scripts** | ~80 lines of vanilla JS (theme toggle, scroll reveal, mobile nav) |
| **Fonts** | [Inter](https://rsms.me/inter/) via Google Fonts |
| **Hosting** | GitHub Pages with custom domain |
| **CI** | GitHub Actions — weekly citation count sync via Semantic Scholar API |

## 🎨 Features

- 🌙 **Dark/light mode** — flash-free, persisted via `localStorage`
- 📱 **Mobile-first** — responsive layout, smart nav hide/show on scroll
- 📚 **Publications** — 10 selected papers with live citation badges
- 🔄 **Auto-updating citations** — GitHub Actions fetches from Semantic Scholar weekly
- ♿ **Accessible** — skip-link, semantic landmarks, ARIA labels, motion-safe animations
- 🔍 **SEO** — Open Graph, Twitter cards, canonical URL, JSON-LD Person schema

## 📂 Structure

```
├── index.html              # Single-page site
├── css/style.css           # All styles (~400 lines)
├── js/main.js              # Theme, nav, scroll reveal (~80 lines)
├── img/                    # Profile photos, favicons
├── files/                  # CV, resume PDFs
├── scripts/                # Citation updater (Python)
├── .github/workflows/      # Weekly citation sync
└── CNAME                   # Custom domain config
```

## 🚀 Local Development

```bash
# Just open it
open index.html

# Or serve locally
python3 -m http.server 8000
```

## 📄 License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
<sub>Built with vanilla HTML/CSS/JS. No React. No Tailwind. No build step. Just fast.</sub>
</div>
