# Research Finding #107

**Date:** 2025-12-17 08:57
**Topic:** Google Docs API formatting best practices
**Score:** 0.67063034

---

## Using Google Docs' API: Steps & Low-Code Examples (2023) - Rowy

**URL:** https://www.rowy.io/blog/google-docs-api
**Published:** Unknown date

---

## Content

```
const content = row.body.content const size = content.length let md = `#${row.title}\n\n` for(let i = 0 ; i < size ; i++){ const element = content[i] if(element.hasOwnProperty('paragraph')){ const elements = element.paragraph.elements const size_elements = elements.length for(let j = 0 ; j < size_elements ; j++){ const element = elements[j] if(element.hasOwnProperty('textRun')){ const text = element.textRun.content md += `${text}\n` } } md += '\n' } } 
```

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
