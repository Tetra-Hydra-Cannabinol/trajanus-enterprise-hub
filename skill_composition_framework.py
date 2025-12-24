"""
SKILL COMPOSITION FRAMEWORK
Build complex agents from composable, reusable skills
"""

from typing import Dict, List, Callable, Any
from abc import ABC, abstractmethod


class Skill(ABC):
    """Base class for composable skills"""
    
    def __init__(self, name: str):
        self.name = name
        self.dependencies: List[str] = []
    
    @abstractmethod
    def execute(self, context: Dict) -> Any:
        """Execute the skill with given context"""
        pass
    
    def requires(self, *skill_names: str):
        """Declare dependencies on other skills"""
        self.dependencies.extend(skill_names)
        return self


# ============================================================================
# FILE OPERATION SKILLS
# ============================================================================

class FileExistsSkill(Skill):
    """Check if file exists"""
    
    def __init__(self):
        super().__init__("file_exists")
    
    def execute(self, context: Dict) -> bool:
        from pathlib import Path
        filepath = Path(context['filepath'])
        return filepath.exists()


class FileHashSkill(Skill):
    """Compute file hash"""
    
    def __init__(self):
        super().__init__("file_hash")
    
    def execute(self, context: Dict) -> str:
        import hashlib
        from pathlib import Path
        
        filepath = Path(context['filepath'])
        if not filepath.exists():
            return None
        
        return hashlib.sha256(filepath.read_bytes()).hexdigest()


class FileMoveSkill(Skill):
    """Move file from source to destination"""
    
    def __init__(self):
        super().__init__("file_move")
        self.requires("file_exists")
    
    def execute(self, context: Dict) -> Dict:
        from pathlib import Path
        
        source = Path(context['source'])
        destination = Path(context['destination'])
        
        source.rename(destination)
        
        return {
            'moved_from': str(source),
            'moved_to': str(destination)
        }


class FileBackupSkill(Skill):
    """Create backup of file"""
    
    def __init__(self):
        super().__init__("file_backup")
        self.requires("file_exists")
    
    def execute(self, context: Dict) -> str:
        from pathlib import Path
        from datetime import datetime
        
        filepath = Path(context['filepath'])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{filepath.stem}_backup_{timestamp}{filepath.suffix}"
        backup_path = filepath.parent / backup_name
        
        filepath.rename(backup_path)
        
        return str(backup_path)


# ============================================================================
# VERIFICATION SKILLS
# ============================================================================

class StateVerificationSkill(Skill):
    """Verify current state against expected state"""
    
    def __init__(self):
        super().__init__("state_verification")
    
    def execute(self, context: Dict) -> Dict:
        """
        Compare current state with expected state
        
        Returns:
            Dictionary with 'matches' (bool) and 'differences' (list)
        """
        current = context.get('current_state', {})
        expected = context.get('expected_state', {})
        
        differences = []
        
        for key in expected:
            if key not in current:
                differences.append(f"Missing key: {key}")
            elif current[key] != expected[key]:
                differences.append(f"Mismatch {key}: {current[key]} != {expected[key]}")
        
        return {
            'matches': len(differences) == 0,
            'differences': differences
        }


class WorkAlreadyDoneSkill(Skill):
    """Check if work is already complete"""
    
    def __init__(self):
        super().__init__("work_already_done")
    
    def execute(self, context: Dict) -> Dict:
        """
        Check completion status
        
        Returns:
            Dictionary with 'complete' (bool) and 'reason' (str)
        """
        check_function = context.get('check_function')
        check_params = context.get('check_params', {})
        
        if check_function:
            is_complete = check_function(**check_params)
            return {
                'complete': is_complete,
                'reason': 'Work already complete' if is_complete else 'Work needed'
            }
        
        return {
            'complete': False,
            'reason': 'No verification function provided'
        }


# ============================================================================
# MONITORING SKILLS
# ============================================================================

class ProgressMonitoringSkill(Skill):
    """Monitor progress across multiple items"""
    
    def __init__(self):
        super().__init__("progress_monitoring")
    
    def execute(self, context: Dict) -> Dict:
        """
        Generate progress report
        
        Returns:
            Dictionary with counts and percentages
        """
        items = context.get('items', [])
        check_function = context.get('check_function')
        
        if not check_function:
            return {'error': 'No check function provided'}
        
        complete = sum(1 for item in items if check_function(item))
        total = len(items)
        
        return {
            'total': total,
            'complete': complete,
            'remaining': total - complete,
            'percentage': (complete / total * 100) if total > 0 else 0
        }


class StatusReportSkill(Skill):
    """Generate comprehensive status report"""
    
    def __init__(self):
        super().__init__("status_report")
        self.requires("progress_monitoring")
    
    def execute(self, context: Dict) -> str:
        """Generate formatted status report"""
        
        report_lines = [
            "="*60,
            f"STATUS REPORT: {context.get('title', 'Untitled')}",
            "="*60,
            ""
        ]
        
        progress = context.get('progress', {})
        report_lines.extend([
            f"Total items: {progress.get('total', 0)}",
            f"Complete: {progress.get('complete', 0)}",
            f"Remaining: {progress.get('remaining', 0)}",
            f"Progress: {progress.get('percentage', 0):.1f}%",
            ""
        ])
        
        if context.get('details'):
            report_lines.append("Details:")
            for detail in context['details']:
                report_lines.append(f"  - {detail}")
        
        report_lines.append("="*60)
        
        return "\n".join(report_lines)


# ============================================================================
# COORDINATION SKILLS
# ============================================================================

class ApprovalGateSkill(Skill):
    """Request user approval before proceeding"""
    
    def __init__(self):
        super().__init__("approval_gate")
    
    def execute(self, context: Dict) -> bool:
        """
        Show plan and get approval
        
        Returns:
            True if approved, False otherwise
        """
        plan = context.get('plan', [])
        message = context.get('message', 'Proceed with execution?')
        
        print("\n" + "="*60)
        print("APPROVAL REQUIRED")
        print("="*60)
        
        if plan:
            print("\nPlanned actions:")
            for i, action in enumerate(plan, 1):
                print(f"  {i}. {action}")
        
        print()
        response = input(f"{message} (yes/no): ").lower()
        
        return response == 'yes'


class ErrorRecoverySkill(Skill):
    """Suggest recovery actions for errors"""
    
    def __init__(self):
        super().__init__("error_recovery")
    
    def execute(self, context: Dict) -> Dict:
        """
        Analyze error and suggest recovery
        
        Returns:
            Dictionary with recovery suggestions
        """
        error = context.get('error', '')
        error_type = context.get('error_type', 'unknown')
        
        recovery_map = {
            'permission': {
                'action': 'check_permissions',
                'message': 'Permission denied',
                'suggestion': 'Verify file permissions and close programs using the files'
            },
            'not_found': {
                'action': 'verify_paths',
                'message': 'File or directory not found',
                'suggestion': 'Verify all paths are correct and items exist'
            },
            'network': {
                'action': 'retry',
                'message': 'Network connection failed',
                'suggestion': 'Check internet connection and retry'
            },
            'timeout': {
                'action': 'increase_timeout',
                'message': 'Operation timed out',
                'suggestion': 'Increase timeout value or break into smaller operations'
            }
        }
        
        return recovery_map.get(error_type, {
            'action': 'manual_intervention',
            'message': f'Error: {error}',
            'suggestion': 'Review error and determine appropriate action'
        })


# ============================================================================
# SKILL COMPOSER
# ============================================================================

class SkillComposer:
    """Compose multiple skills into complex agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.skills: Dict[str, Skill] = {}
    
    def add_skill(self, skill: Skill):
        """Add skill to composer"""
        self.skills[skill.name] = skill
        return self
    
    def use_skill(self, skill_name: str, context: Dict) -> Any:
        """Execute a specific skill"""
        if skill_name not in self.skills:
            raise ValueError(f"Skill '{skill_name}' not found")
        
        skill = self.skills[skill_name]
        
        # Check dependencies
        for dep in skill.dependencies:
            if dep not in self.skills:
                raise ValueError(f"Skill '{skill_name}' requires '{dep}' but it's not registered")
        
        return skill.execute(context)
    
    def create_workflow(self, steps: List[Dict]) -> Callable:
        """
        Create workflow from skill sequence
        
        Args:
            steps: List of dicts with 'skill' and 'context' keys
        
        Returns:
            Callable workflow function
        """
        def workflow(initial_context: Dict) -> List[Any]:
            results = []
            context = initial_context.copy()
            
            for step in steps:
                skill_name = step['skill']
                step_context = {**context, **step.get('context', {})}
                
                result = self.use_skill(skill_name, step_context)
                results.append(result)
                
                # Update context with result for next step
                context['previous_result'] = result
            
            return results
        
        return workflow


# ============================================================================
# EXAMPLE COMPOSITIONS
# ============================================================================

class SafeFileMoverAgent:
    """Example: File mover using composed skills"""
    
    def __init__(self):
        self.composer = SkillComposer("safe-file-mover")
        
        # Register skills
        self.composer.add_skill(FileExistsSkill())
        self.composer.add_skill(FileHashSkill())
        self.composer.add_skill(FileBackupSkill())
        self.composer.add_skill(FileMoveSkill())
        self.composer.add_skill(ApprovalGateSkill())
    
    def move_with_verification(self, source: str, destination: str) -> Dict:
        """Move file with full verification and approval"""
        
        # Step 1: Verify source exists
        exists = self.composer.use_skill('file_exists', {'filepath': source})
        if not exists:
            return {'error': 'Source file not found'}
        
        # Step 2: Compute hash before move
        hash_before = self.composer.use_skill('file_hash', {'filepath': source})
        
        # Step 3: Get approval
        approved = self.composer.use_skill('approval_gate', {
            'plan': [f"Move {source} to {destination}"],
            'message': 'Proceed with file move?'
        })
        
        if not approved:
            return {'status': 'cancelled'}
        
        # Step 4: Backup if destination exists
        dest_exists = self.composer.use_skill('file_exists', {'filepath': destination})
        if dest_exists:
            backup_path = self.composer.use_skill('file_backup', {'filepath': destination})
            print(f"Created backup: {backup_path}")
        
        # Step 5: Execute move
        move_result = self.composer.use_skill('file_move', {
            'source': source,
            'destination': destination
        })
        
        # Step 6: Verify hash after move
        hash_after = self.composer.use_skill('file_hash', {'filepath': destination})
        
        return {
            'status': 'success',
            'hash_verified': hash_before == hash_after,
            'result': move_result
        }


# Usage example
if __name__ == "__main__":
    print("Skill Composition Framework")
    print("="*60)
    print("\nRegistered Skill Categories:")
    print("  - File Operations: exists, hash, move, backup")
    print("  - Verification: state check, work done check")
    print("  - Monitoring: progress, status reports")
    print("  - Coordination: approval gates, error recovery")
    
    print("\n\nExample: Safe File Mover Agent")
    print("="*60)
    
    agent = SafeFileMoverAgent()
    print("\nAgent skills:")
    for skill_name in agent.composer.skills:
        print(f"  ✓ {skill_name}")
    
    print("\n\nWorkflow:")
    print("  1. Verify source exists")
    print("  2. Compute hash before move")
    print("  3. Get user approval")
    print("  4. Backup destination if exists")
    print("  5. Execute move")
    print("  6. Verify hash after move")
