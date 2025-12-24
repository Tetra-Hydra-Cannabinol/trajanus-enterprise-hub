#!/usr/bin/env python3
"""
KNOWMAD-5: FILE ORGANIZATION AGENT
Analyzes files and proposes proper folder structure with approval workflow
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

class FileOrganizerAgent:
    """Analyzes files and proposes organization structure"""
    
    def __init__(self, source_folder):
        self.source_folder = Path(source_folder)
        self.proposals = []
        
    def analyze_files(self):
        """Scan folder and propose organization"""
        print("=" * 70)
        print("KNOWMAD-5: FILE ORGANIZATION AGENT")
        print("=" * 70)
        print(f"📁 Scanning: {self.source_folder}")
        print("")
        
        # Get all Google Docs created today
        files = [
            "Session_Summary_2025-12-11_Knowmads_System",
            "Technical_Journal_2025-12-11_Knowmads_Entry",
            "Bills_Daily_Diary_2025-12-11",
            "Code_Repository_2025-12-11_Knowmad4_Entry",
            "Session_Summary_FINAL_ENTRY_12-11",
            "Technical_Journal_FINAL_ENTRY_12-11",
            "Bills_Daily_Diary_FINAL_ENTRY_12-11",
            "SUPABASE_INTEGRATION_GUIDE"
        ]
        
        print(f"✓ Found {len(files)} files to organize")
        print("")
        
        # Analyze each file and propose destination
        for filename in files:
            proposal = self._propose_destination(filename)
            self.proposals.append(proposal)
        
        return self.proposals
    
    def _propose_destination(self, filename):
        """Determine correct destination folder based on filename"""
        
        # Parse file type from name
        if "Session_Summary" in filename:
            folder = "03-Living-Documents/Session-Summaries"
            reason = "Session summary document"
            
        elif "Technical_Journal" in filename:
            folder = "03-Living-Documents/Technical-Journal"
            reason = "Technical implementation details"
            
        elif "Bills_Daily_Diary" in filename or "Daily_Diary" in filename:
            folder = "03-Living-Documents/Personal-Diary"
            reason = "Personal reflection and diary entry"
            
        elif "Code_Repository" in filename:
            folder = "03-Living-Documents/Code-Repository"
            reason = "Code documentation and source"
            
        elif "GUIDE" in filename or "Guide" in filename:
            folder = "06-User-Guides"
            reason = "User guide or reference documentation"
            
        elif "HANDOFF" in filename or "Handoff" in filename:
            folder = "08-EOS-Files/Handoffs"
            reason = "Session handoff document"
            
        else:
            folder = "08-EOS-Files/Uncategorized"
            reason = "Unable to determine category"
        
        return {
            'filename': filename,
            'current_location': 'Session-Summaries',
            'proposed_location': folder,
            'reason': reason
        }
    
    def generate_report(self):
        """Generate approval report"""
        
        print("=" * 70)
        print("FILE ORGANIZATION PROPOSAL")
        print("=" * 70)
        print("")
        
        # Group by destination folder
        by_folder = {}
        for prop in self.proposals:
            dest = prop['proposed_location']
            if dest not in by_folder:
                by_folder[dest] = []
            by_folder[dest].append(prop)
        
        # Print organized by destination
        for folder, items in sorted(by_folder.items()):
            print(f"📂 {folder}")
            print(f"   ({len(items)} files)")
            print("")
            for item in items:
                print(f"   ✓ {item['filename']}")
                print(f"      Reason: {item['reason']}")
                print(f"      From: {item['current_location']}")
                print("")
        
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total files: {len(self.proposals)}")
        print(f"Destination folders: {len(by_folder)}")
        print("")
        
        # Save report to file
        report_file = Path("/mnt/user-data/outputs/FILE_ORGANIZATION_REPORT.txt")
        with open(report_file, 'w') as f:
            f.write("FILE ORGANIZATION PROPOSAL\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            for folder, items in sorted(by_folder.items()):
                f.write(f"FOLDER: {folder}\n")
                f.write(f"FILES: {len(items)}\n\n")
                for item in items:
                    f.write(f"  - {item['filename']}\n")
                    f.write(f"    Reason: {item['reason']}\n")
                    f.write(f"    From: {item['current_location']}\n\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("APPROVAL REQUIRED\n")
            f.write("=" * 70 + "\n")
            f.write("Review this report and approve before files are moved.\n")
        
        print(f"📄 Report saved: {report_file}")
        print("")
        print("⚠️  APPROVAL REQUIRED")
        print("Review report and confirm before files are moved.")
        print("")
        
        return report_file
    
    def generate_move_script(self):
        """Generate PowerShell script to execute moves"""
        
        script_file = Path("/mnt/user-data/outputs/EXECUTE_FILE_MOVES.ps1")
        
        with open(script_file, 'w') as f:
            f.write("# FILE ORGANIZATION EXECUTION SCRIPT\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# ONLY RUN AFTER REVIEWING AND APPROVING REPORT\n\n")
            
            f.write('$baseFolder = "G:\\My Drive\\00 - Trajanus USA"\n\n')
            
            for prop in self.proposals:
                f.write(f"# Move: {prop['filename']}\n")
                f.write(f'$source = "$baseFolder\\08-EOS-Files\\Session-Summaries\\{prop["filename"]}"\n')
                f.write(f'$dest = "$baseFolder\\{prop["proposed_location"]}"\n')
                f.write(f'# Reason: {prop["reason"]}\n')
                f.write('Move-Item -Path $source -Destination $dest -Force\n')
                f.write(f'Write-Host "✓ Moved {prop["filename"]}" -ForegroundColor Green\n\n')
            
            f.write('Write-Host "\\nAll files moved successfully!" -ForegroundColor Cyan\n')
        
        print(f"📝 Move script saved: {script_file}")
        print("   Run this script ONLY after approving the report")
        print("")
        
        return script_file


def main():
    if len(sys.argv) < 2:
        folder = "G:\\My Drive\\00 - Trajanus USA\\08-EOS-Files\\EOS Files 12-11-2025"
    else:
        folder = sys.argv[1]
    
    agent = FileOrganizerAgent(folder)
    
    # Analyze files
    proposals = agent.analyze_files()
    
    # Generate report
    report_file = agent.generate_report()
    
    # Generate move script
    script_file = agent.generate_move_script()
    
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Review FILE_ORGANIZATION_REPORT.txt")
    print("2. If approved, run EXECUTE_FILE_MOVES.ps1")
    print("3. Verify files in correct locations")
    print("")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
