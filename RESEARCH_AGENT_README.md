# RESEARCH AGENT PROMPTS - USAGE GUIDE

## TWO VERSIONS AVAILABLE

### 1. `CC_PROMPT_YouTube_Research_Agent.md` (RECOMMENDED)
**Use this for:** Any future research topics

**Features:**
- ✅ Phase 0: Interactive URL source selection
- ✅ Path A: Upload your own URL list
- ✅ Path B: Agent searches YouTube, you select videos
- ✅ Works for ANY topic (construction, AI, programming, etc.)
- ✅ Reusable template

**How to use:**
```bash
# Give this prompt to Claude Code
# CC asks: "Upload URLs OR research?"
# You choose path
# CC handles the rest
```

**Example topics you can use this for:**
- Construction scheduling tutorials
- Primavera P6 training
- AI prompt engineering
- Python programming
- Project management best practices
- Quality control procedures
- Any educational YouTube content

---

### 2. `CC_PROMPT_MSOffice_Expert_Crawler.md` (CURRENT RUN)
**Use this for:** Bill's specific MS Office collection (25 URLs)

**Features:**
- ✅ Same interactive workflow
- ✅ Pre-loaded with Bill's 22 individual videos + 3 playlists
- ✅ MS Office categorization (Excel/Word/Project)
- ✅ Ready to run NOW

**Current execution:**
- CC is processing Bill's MS Office collection
- Building Playwright transcript extractor
- Will save all working code

---

## WORKFLOW COMPARISON

**Old Way (Pre-Phase 0):**
```
1. Hardcode URLs in prompt
2. Run agent
3. Done
```
**Problem:** Not reusable for different topics

**New Way (With Phase 0):**
```
1. Give agent the topic or URL list
2. Agent asks: Upload or research?
3. If research: Agent finds videos, you select
4. If upload: You provide URLs
5. Agent processes
```
**Benefit:** Same prompt works for ANY topic

---

## WHAT CC IS BUILDING RIGHT NOW

**Standalone Script:**
`youtube_research_agent.py`

**Capabilities:**
- Takes `target_urls.json` as input
- Extracts YouTube transcripts (Playwright method)
- Chunks text (1000 chars, 200 overlap)
- Generates embeddings (OpenAI)
- Saves to Supabase knowledge_base
- Auto-categorizes content
- Produces ingestion report

**Future Use:**
```bash
# Create target URLs file
echo '{"individual": ["url1", "url2"], "playlists": ["url3"]}' > target_urls.json

# Run agent
python youtube_research_agent.py target_urls.json

# Wait for completion
# Check knowledge base for new content
```

---

## CURRENT STATUS

✅ **Phase 0 added** - Interactive workflow
✅ **Template created** - Reusable for any topic
✅ **CC is executing** - Building MS Office knowledge base
🔄 **In progress** - Saving working Playwright code
⏳ **Next** - Test standalone script on different topic

---

## RECOMMENDATIONS

**For Bill's immediate MS Office needs:**
- Use `CC_PROMPT_MSOffice_Expert_Crawler.md`
- Let current CC session complete
- Save all working code

**For future research projects:**
- Use `CC_PROMPT_YouTube_Research_Agent.md`
- Provide new topic or URLs
- Reuse proven workflow

**For team deployment:**
- Document the standalone script CC builds
- Create simple "How to run" guide
- Train Tom/Chris on using it

---

## SUCCESS METRICS

**This workflow is successful when:**
1. ✅ Bill can provide ANY topic and get knowledge base
2. ✅ Code is saved and repeatable
3. ✅ Different Claude sessions can run same workflow
4. ✅ No code rewriting needed between runs
5. ✅ Process documented for team use

**Current progress:** 80% complete (Phase 0 added, code being saved, testing needed)

---

*Created: December 20, 2025*
*Last updated: During CC MS Office ingestion session*
