# TRAJANUS KNOWLEDGE BASE QUERY TOOL

## Quick Start

**From any PowerShell window:**
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts"
.\QUERY_KB.ps1
```

This will:
1. Set required environment variables
2. Launch the interactive query tool

## Available Commands

Once in the query tool, use:

- **`sources`** - List all knowledge sources and chunk counts
- **`search <query>`** - Semantic search (e.g., `search LangChain`)
- **`recent`** - Show recent sessions
- **`source <name>`** - Get docs from specific source
- **`exit`** - Quit

## Examples

```
Query> sources
[Shows all 10 knowledge sources with chunk counts]

Query> search Excel formulas
[Returns relevant chunks about Excel]

Query> search USACE standards
[Returns construction standards info]

Query> exit
```

## Current Database Stats (as of 2025-12-21)

**Total: ~1000 chunks across 10 sources**

- Session History: 410 chunks
- Living Documents: 351 chunks
- Core Protocols: 216 chunks
- YouTube Transcripts: 8 chunks (SMALL FILES ONLY)
- Protocols: 5 chunks
- Code: 3 chunks
- EOS Docs: 3 chunks
- Research: 2 chunks
- SQL: 1 chunk
- Test Data: 1 chunk

## What's Missing

**Large video transcripts NOT yet ingested:**
- LangChain courses (~1.5 MB, 6 files)
- Microsoft Office courses (~2.5 MB, 8+ files)

These are moved to 13-Knowledge-Base/Transcripts/ but NOT in database.

Expected after ingestion: ~1400-1500 total chunks

## Troubleshooting

If QUERY_KB.ps1 fails:

**Error: "Execution Policy"**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\QUERY_KB.ps1
```

**Error: "Missing SUPABASE_URL"**
- Script should set this automatically
- If not, check that script is in 05-Scripts folder

## File Location

```
G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\QUERY_KB.ps1
```
