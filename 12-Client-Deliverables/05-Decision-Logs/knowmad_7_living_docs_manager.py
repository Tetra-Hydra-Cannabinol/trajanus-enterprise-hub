#!/usr/bin/env python3
"""
KNOWMAD-7: LIVING DOCUMENTS MANAGER
Multi-skilled agent that monitors, verifies, and maintains Living Documents
Only acts when needed - checks before performing any operation
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import hashlib

class LivingDocumentsManager:
    """
    Multi-skilled agent for Living Documents maintenance
    
    Skills:
    1. Verification - Check if daily entries exist in masters
    2. Appending - Add missing entries to masters
    3. Monitoring - Report on Living Documents status
    4. Validation - Ensure proper structure
    
    Philosophy: CHECK BEFORE ACT
    - Never duplicate work
    - Only append if entry missing
    - Idempotent operations
    - Full audit trail
    """
    
    def __init__(self):
        self.base_path = Path("G:/My Drive/00 - Trajanus USA")
        self.living_docs = self.base_path / "03-Living-Documents"
        
        # Master document locations
        self.masters = {
            'session_summary': self.living_docs / "Session-Summaries" / "Session_Summaries_MASTER.md",
            'technical_journal': self.living_docs / "Technical-Journal" / "Technical_Journal_MASTER.md",
            'personal_diary': self.living_docs / "Personal-Diary" / "Bills_Daily_Diary_MASTER.md",
            'code_repository': self.living_docs / "Code-Repository" / "Code_Repository_MASTER.md"
        }
        
        # Today's date for entry identification
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # Results tracking
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'verifications': [],
            'appends': [],
            'errors': [],
            'status': 'pending'
        }
    
    def verify_entry_exists(self, category, date=None):
        """
        SKILL 1: VERIFICATION
        Check if entry for given date exists in master
        
        Returns: (exists: bool, entry_hash: str)
        """
        if date is None:
            date = self.today
        
        master_file = self.masters.get(category)
        if not master_file or not master_file.exists():
            return False, None
        
        # Read master and check for date marker
        try:
            content = master_file.read_text(encoding='utf-8')
            
            # Look for entry markers like "## ENTRY: 2025-12-11" or "December 11, 2025"
            date_formats = [
                f"## ENTRY: {date}",
                f"### ENTRY: {date}",
                datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y"),
                datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
            ]
            
            exists = any(fmt in content for fmt in date_formats)
            
            if exists:
                # Generate hash of entry for verification
                entry_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            else:
                entry_hash = None
            
            return exists, entry_hash
            
        except Exception as e:
            self.results['errors'].append(f"Verification error ({category}): {str(e)}")
            return False, None
    
    def find_daily_entry(self, category, date=None):
        """
        Find the daily entry file for given category and date
        
        Returns: Path to entry file or None
        """
        if date is None:
            date = self.today
        
        # Search patterns based on category
        patterns = {
            'session_summary': f"Session_Summary_{date}_*.md",
            'technical_journal': f"Technical_Journal_{date}_*.md",
            'personal_diary': f"Bills_Daily_Diary_{date}*.md",
            'code_repository': f"Code_Repository_{date}_*.md"
        }
        
        pattern = patterns.get(category)
        if not pattern:
            return None
        
        # Search in category folder
        category_folder = self.masters[category].parent
        matches = list(category_folder.glob(pattern))
        
        if matches:
            # Return most recent if multiple
            return max(matches, key=lambda p: p.stat().st_mtime)
        
        return None
    
    def append_entry_to_master(self, category, entry_file):
        """
        SKILL 2: APPENDING
        Append daily entry to master document
        Only if not already present
        """
        master_file = self.masters.get(category)
        if not master_file:
            return False, "Master file not defined"
        
        # Create master if doesn't exist
        if not master_file.exists():
            master_file.parent.mkdir(parents=True, exist_ok=True)
            master_file.write_text(f"# {category.upper().replace('_', ' ')} - MASTER DOCUMENT\n\n")
        
        try:
            # Read entry content
            entry_content = entry_file.read_text(encoding='utf-8')
            
            # Read current master
            master_content = master_file.read_text(encoding='utf-8')
            
            # Append entry with separator
            separator = "\n\n" + "="*70 + "\n\n"
            updated_content = master_content + separator + entry_content
            
            # Write back
            master_file.write_text(updated_content, encoding='utf-8')
            
            return True, f"Appended {entry_file.name} to {master_file.name}"
            
        except Exception as e:
            return False, f"Append error: {str(e)}"
    
    def monitor_all_categories(self):
        """
        SKILL 3: MONITORING
        Check status of all Living Document categories
        """
        print("=" * 70)
        print("KNOWMAD-7: LIVING DOCUMENTS MANAGER")
        print("=" * 70)
        print(f"📅 Date: {self.today}")
        print("")
        print("🔍 VERIFICATION PHASE")
        print("=" * 70)
        
        status_report = {}
        
        for category in self.masters.keys():
            print(f"\n📂 Category: {category.replace('_', ' ').title()}")
            
            # Check if entry exists in master
            exists, entry_hash = self.verify_entry_exists(category)
            
            # Find daily entry file
            daily_file = self.find_daily_entry(category)
            
            status = {
                'in_master': exists,
                'entry_hash': entry_hash,
                'daily_file': str(daily_file) if daily_file else None,
                'needs_append': daily_file is not None and not exists
            }
            
            if exists:
                print(f"   ✅ Entry exists in master (hash: {entry_hash})")
            else:
                print(f"   ❌ Entry NOT in master")
            
            if daily_file:
                print(f"   ✅ Daily file found: {daily_file.name}")
            else:
                print(f"   ⚠️  No daily file found")
            
            if status['needs_append']:
                print(f"   🔧 ACTION NEEDED: Append to master")
            elif exists and not daily_file:
                print(f"   ℹ️  Entry already in master, daily file archived/deleted")
            elif not exists and not daily_file:
                print(f"   ℹ️  No entry yet for today")
            else:
                print(f"   ✅ Status: OK")
            
            status_report[category] = status
            self.results['verifications'].append(status)
        
        return status_report
    
    def execute_pending_appends(self, status_report, auto_execute=False):
        """
        SKILL 4: EXECUTION
        Append any entries that need appending
        """
        print("")
        print("🚀 EXECUTION PHASE")
        print("=" * 70)
        
        pending_appends = [
            (cat, stat) for cat, stat in status_report.items() 
            if stat['needs_append']
        ]
        
        if not pending_appends:
            print("✅ No appends needed - all masters up to date!")
            self.results['status'] = 'complete_no_action'
            return True
        
        print(f"\n⚠️  Found {len(pending_appends)} entries needing append:")
        for cat, _ in pending_appends:
            print(f"   - {cat.replace('_', ' ').title()}")
        
        if not auto_execute:
            print("")
            approval = input("Execute appends? (yes/no): ").lower()
            if approval not in ['yes', 'y']:
                print("❌ Cancelled by user")
                self.results['status'] = 'cancelled'
                return False
        
        print("")
        success_count = 0
        
        for category, status in pending_appends:
            daily_file = Path(status['daily_file'])
            print(f"📝 Appending {category.replace('_', ' ').title()}...")
            
            success, message = self.append_entry_to_master(category, daily_file)
            
            if success:
                print(f"   ✅ {message}")
                success_count += 1
                self.results['appends'].append({
                    'category': category,
                    'file': daily_file.name,
                    'success': True
                })
            else:
                print(f"   ❌ {message}")
                self.results['errors'].append(message)
                self.results['appends'].append({
                    'category': category,
                    'file': daily_file.name,
                    'success': False,
                    'error': message
                })
        
        print("")
        print("=" * 70)
        if success_count == len(pending_appends):
            print(f"✅ SUCCESS: All {success_count} entries appended!")
            self.results['status'] = 'complete_success'
            return True
        else:
            print(f"⚠️  PARTIAL: {success_count}/{len(pending_appends)} appended")
            self.results['status'] = 'complete_partial'
            return False
    
    def save_execution_log(self):
        """Save detailed log of execution"""
        log_file = self.base_path / "00-Command-Center" / "living_docs_manager_log.json"
        
        with open(log_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return log_file
    
    def run(self, auto_execute=False):
        """
        Main execution flow
        1. Monitor/Verify all categories
        2. Execute pending appends (with approval)
        3. Save execution log
        """
        try:
            # Monitor
            status_report = self.monitor_all_categories()
            
            # Execute
            success = self.execute_pending_appends(status_report, auto_execute)
            
            # Log
            log_file = self.save_execution_log()
            
            print("")
            print(f"📊 Execution log: {log_file}")
            
            return success
            
        except Exception as e:
            self.results['status'] = 'error'
            self.results['errors'].append(str(e))
            print(f"\n❌ ERROR: {str(e)}")
            return False


def main():
    """Main execution"""
    
    auto_execute = '--auto-execute' in sys.argv or '-y' in sys.argv
    
    manager = LivingDocumentsManager()
    success = manager.run(auto_execute)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
