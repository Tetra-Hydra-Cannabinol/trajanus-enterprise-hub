# Technical Journal - November 25, 2025

## Entry #001 - Right Panel Implementation

**Added to index.html:**
- CSS lines 795-867 (`.right-panel`, `.rp-*` classes)
- HTML lines 1019-1041 (panel structure)
- JS functions: `rpToggle`, `rpAddFile`, `rpRender`, `rpSelect`, `rpSave`, `rpLoad`
- Modified `downloadFileAndAdd()` to trigger panel update
- Modified `loadProject()` to call `rpLoad()` on project switch

**Key fix:** `flex-shrink: 0` on `.right-panel` to prevent squeeze-out

**Storage:** localStorage per project using key `rpFiles_${projectName}`

## Entry #002 - Drive Browser Issue

Browser works once then breaks. Terminal shows valid JSON but parser fails. Refresh button errors. Home button resets. Root cause unknown - existed before panel changes but may have worsened.
