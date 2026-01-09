@echo off
REM ============================================
REM TRAJANUS USA - Claude Code Video Ingestion
REM Transcripts to Supabase ONLY (no file archive)
REM ============================================

echo.
echo ============================================
echo CLAUDE CODE TUTORIAL VIDEO INGESTION
echo Transcripts -^> Supabase AI Memory
echo ============================================
echo.

cd /d "G:\My Drive\00 - Trajanus USA\00-Command-Center"

REM Verified Video IDs
set VIDEO1=6eBSHbLKuN0
set VIDEO2=xOO8Wt_i72s
set VIDEO3=wfiv67NixCY

echo.
echo [1/10] Boris Cherny - 8-Step Workflow
echo       Video ID: %VIDEO1%
python youtube_archive_ingest.py --video %VIDEO1% --category Claude-Code --no-download --supabase-only
if errorlevel 1 echo       FAILED - check manually
echo.

echo [2/10] Patrick Ellis - Playwright MCP UI Designer
echo       Video ID: %VIDEO2%
python youtube_archive_ingest.py --video %VIDEO2% --category Claude-Code --no-download --supabase-only
if errorlevel 1 echo       FAILED - check manually
echo.

echo [3/10] Alex Finn - AI Life Copilot
echo       Video ID: %VIDEO3%
python youtube_archive_ingest.py --video %VIDEO3% --category Claude-Code --no-download --supabase-only
if errorlevel 1 echo       FAILED - check manually
echo.

echo ============================================
echo MANUAL SEARCH REQUIRED FOR REMAINING VIDEOS
echo ============================================
echo.
echo The following videos need YouTube URLs found manually:
echo.
echo [4] Peter Yang - YouTube Research Agent (15 min)
echo     Search: youtube.com "Peter Yang Claude Code YouTube research agent"
echo.
echo [5] Edmund Yong - Sub-agents ^& MCP Tutorial
echo     Search: youtube.com "Edmund Yong Claude Code subagents MCP"
echo.
echo [6] Teresa Torres - Automate Life in 50 Min
echo     Channel: youtube.com/@peteryangyt (Behind the Craft)
echo.
echo [7] 3 Technical Founders - Master Claude Code
echo     Search: youtube.com "Master Claude Code Technical Founders"
echo.
echo [8] Solo Swift Crafter - Skills vs MCP vs Subagents (9 min)
echo     Search: youtube.com "Skills vs MCP vs Subagents Claude"
echo.
echo [9] CS Dojo - Claude Code Masterclass (20 min)
echo     Search: youtube.com "CS Dojo Claude Code masterclass"
echo.
echo [10] Cat Wu - Inside Claude Code
echo      Channel: youtube.com/@peteryangyt (Behind the Craft)
echo.
echo ============================================
echo TO INGEST A VIDEO MANUALLY:
echo ============================================
echo.
echo Step 1: Get the video ID from YouTube URL
echo         Example: youtube.com/watch?v=ABC123 -^> ID is ABC123
echo.
echo Step 2: Run this command:
echo         python youtube_archive_ingest.py --video ABC123 --category Claude-Code --no-download --supabase-only
echo.
echo ============================================
echo REFERENCE CARDS LOCATION:
echo ============================================
echo.
echo TKB Cards HTML: C:\Dev\trajanus-command-center\TKB_DEV_ClaudeCode_Cards.html
echo Copy to: TKB/DEV/Claude-Code/ folder
echo.
pause
