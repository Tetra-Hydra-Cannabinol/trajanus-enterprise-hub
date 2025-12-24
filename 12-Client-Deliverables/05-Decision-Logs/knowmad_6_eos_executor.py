#!/usr/bin/env python3
"""
KNOWMAD-6: EOS FILE ORGANIZATION EXECUTOR
Agent that executes file organization workflow with minimal user input
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import subprocess

class EOSFileOrganizer:
    """Agent that executes complete file organization workflow"""
    
    def __init__(self):
        self.base_path = Path("G:/My Drive/00 - Trajanus USA")
        self.results = {
            'status': 'pending',
            'files_analyzed': 0,
            'files_moved': 0,
            'errors': [],
            'timestamp': datetime.now().isoformat()
        }
    
    def find_latest_eos_folder(self):
        """Find most recent EOS Files folder"""
        eos_base = self.base_path / "08-EOS-Files"
        
        # Look for folders matching "EOS Files DD-MM-YYYY" or "EOS Files - DD-MM-YYYY"
        folders = []
        for folder in eos_base.glob("EOS Files*"):
            if folder.is_dir():
                folders.append(folder)
        
        if not folders:
            return None
        
        # Sort by modification time, get most recent
        folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return folders[0]
    
    def execute_workflow(self, folder_path=None, auto_approve=False):
        """Execute complete organization workflow"""
        
        print("=" * 70)
        print("KNOWMAD-6: EOS FILE ORGANIZATION EXECUTOR")
        print("=" * 70)
        print("")
        
        # Step 1: Determine folder
        if folder_path is None:
            folder_path = self.find_latest_eos_folder()
            if folder_path is None:
                self.results['status'] = 'error'
                self.results['errors'].append("No EOS folder found")
                print("❌ ERROR: No EOS folder found")
                return self.results
            print(f"📁 Auto-detected folder: {folder_path}")
        else:
            folder_path = Path(folder_path)
            print(f"📁 Using folder: {folder_path}")
        
        print("")
        
        # Step 2: Run analysis
        print("🔍 Analyzing files...")
        try:
            result = subprocess.run(
                ['python', 'knowmad_5_file_organizer.py', str(folder_path)],
                capture_output=True,
                text=True,
                cwd=str(self.base_path / "00-Command-Center")
            )
            
            if result.returncode != 0:
                self.results['status'] = 'error'
                self.results['errors'].append(f"Analysis failed: {result.stderr}")
                print(f"❌ Analysis failed: {result.stderr}")
                return self.results
            
            print("✓ Analysis complete")
            print("")
            
        except Exception as e:
            self.results['status'] = 'error'
            self.results['errors'].append(f"Analysis error: {str(e)}")
            print(f"❌ Analysis error: {str(e)}")
            return self.results
        
        # Step 3: Review (if not auto-approved)
        if not auto_approve:
            print("📄 Review FILE_ORGANIZATION_REPORT.txt")
            print("")
            print("⚠️  Approval required to proceed")
            approval = input("Execute file moves? (yes/no): ").lower()
            
            if approval not in ['yes', 'y']:
                self.results['status'] = 'cancelled'
                print("❌ Cancelled by user")
                return self.results
        else:
            print("✓ Auto-approved (agent mode)")
        
        print("")
        
        # Step 4: Execute moves
        print("🚀 Executing file moves...")
        try:
            move_script = self.base_path / "00-Command-Center" / "EXECUTE_FILE_MOVES.ps1"
            result = subprocess.run(
                ['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(move_script)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.results['status'] = 'error'
                self.results['errors'].append(f"Move failed: {result.stderr}")
                print(f"❌ Move failed: {result.stderr}")
                return self.results
            
            print(result.stdout)
            self.results['status'] = 'success'
            print("")
            print("=" * 70)
            print("✅ FILE ORGANIZATION COMPLETE")
            print("=" * 70)
            
        except Exception as e:
            self.results['status'] = 'error'
            self.results['errors'].append(f"Execution error: {str(e)}")
            print(f"❌ Execution error: {str(e)}")
            return self.results
        
        return self.results
    
    def save_results(self):
        """Save execution results"""
        results_file = self.base_path / "00-Command-Center" / "eos_org_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        return results_file


def main():
    """Main execution"""
    
    # Parse arguments
    folder_path = None
    auto_approve = False
    
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    
    if '--auto-approve' in sys.argv or '-y' in sys.argv:
        auto_approve = True
    
    # Execute workflow
    agent = EOSFileOrganizer()
    results = agent.execute_workflow(folder_path, auto_approve)
    
    # Save results
    results_file = agent.save_results()
    print(f"\n📊 Results saved: {results_file}")
    
    # Return exit code
    return 0 if results['status'] == 'success' else 1


if __name__ == "__main__":
    sys.exit(main())
