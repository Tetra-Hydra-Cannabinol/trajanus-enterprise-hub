"""
IDEMPOTENT AGENT BASE CLASS
Provides verification, error recovery, audit trails, and validation gates
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional
from abc import ABC, abstractmethod


class ValidationError(Exception):
    """Raised when pre-execution validation fails"""
    pass


class RecoveryError(Exception):
    """Raised when error recovery fails"""
    pass


class AuditEntry:
    """Single audit log entry"""
    
    def __init__(self, action: str, input_data: Any, output: Any, 
                 duration: float, status: str, error: Optional[str] = None):
        self.timestamp = datetime.now().isoformat()
        self.action = action
        self.input = str(input_data)[:500]  # Truncate for storage
        self.output = str(output)[:500] if output else None
        self.duration = duration
        self.status = status  # success | failed | skipped
        self.error = error
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'action': self.action,
            'input': self.input,
            'output': self.output,
            'duration': self.duration,
            'status': self.status,
            'error': self.error
        }


class IdempotentAgent(ABC):
    """
    Base class for all idempotent agents
    
    Provides:
    - Verification before execution
    - Error recovery workflows
    - Complete audit trails
    - Validation gates
    - Composable skills
    """
    
    def __init__(self, name: str, requires_approval: bool = True):
        self.name = name
        self.requires_approval = requires_approval
        self.audit_log: List[AuditEntry] = []
        self.results = {'status': 'pending', 'actions': []}
        self.skills = self._register_skills()
    
    @abstractmethod
    def _register_skills(self) -> Dict[str, Callable]:
        """
        Register available skills for this agent
        
        Returns:
            Dictionary mapping skill names to callable methods
        """
        pass
    
    @abstractmethod
    def verify_state(self, context: Dict) -> Dict:
        """
        Verify current state and determine what needs doing
        
        Args:
            context: Current context/inputs for the operation
        
        Returns:
            Dictionary with 'needs_action' (bool) and 'items' (list)
        """
        pass
    
    @abstractmethod
    def execute_action(self, item: Any) -> Any:
        """
        Execute the actual work on a single item
        
        Args:
            item: Single item to process
        
        Returns:
            Result of the operation
        """
        pass
    
    def validate_prerequisites(self, context: Dict) -> bool:
        """
        Validate all prerequisites before execution
        
        Override in subclass to add specific validations
        """
        # Default validation: context exists
        return context is not None
    
    def suggest_recovery(self, error: Exception, context: Dict) -> Dict:
        """
        Suggest recovery action when operation fails
        
        Override in subclass for specific recovery strategies
        """
        return {
            'action': 'manual_intervention',
            'message': f'Operation failed: {str(error)}',
            'suggestion': 'Review error and retry with corrected inputs'
        }
    
    def log_action(self, action: str, input_data: Any, output: Any,
                   duration: float, status: str, error: Optional[str] = None):
        """Add entry to audit log"""
        entry = AuditEntry(action, input_data, output, duration, status, error)
        self.audit_log.append(entry)
    
    def save_audit_trail(self, output_path: Optional[Path] = None):
        """Save complete audit trail to file"""
        if output_path is None:
            output_path = Path(f"/home/claude/audit_{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        audit_data = {
            'agent': self.name,
            'execution_time': datetime.now().isoformat(),
            'total_actions': len(self.audit_log),
            'entries': [entry.to_dict() for entry in self.audit_log]
        }
        
        output_path.write_text(json.dumps(audit_data, indent=2))
        return output_path
    
    def run_with_validation(self, context: Dict, auto_approve: bool = False) -> Dict:
        """
        Execute agent with full validation, recovery, and audit trail
        
        Args:
            context: Execution context
            auto_approve: Skip approval gate if True
        
        Returns:
            Results dictionary with status and actions taken
        """
        start_time = datetime.now()
        
        try:
            # VALIDATION GATE
            if not self.validate_prerequisites(context):
                raise ValidationError("Prerequisites not met")
            
            # VERIFICATION SKILL
            verification = self.verify_state(context)
            
            if not verification['needs_action']:
                self.results = {
                    'status': 'skipped',
                    'reason': 'No action needed - already complete',
                    'verified_items': verification.get('items', [])
                }
                self.log_action(
                    action='verification',
                    input_data=context,
                    output=verification,
                    duration=0,
                    status='skipped'
                )
                return self.results
            
            items_to_process = verification['items']
            
            # APPROVAL GATE (if required)
            if self.requires_approval and not auto_approve:
                print(f"\n{'='*60}")
                print(f"AGENT: {self.name}")
                print(f"{'='*60}")
                print(f"\nItems requiring action ({len(items_to_process)}):")
                for i, item in enumerate(items_to_process, 1):
                    print(f"  {i}. {item}")
                
                response = input("\nProceed with execution? (yes/no): ").lower()
                if response != 'yes':
                    self.results = {
                        'status': 'cancelled',
                        'reason': 'User declined execution',
                        'pending_items': items_to_process
                    }
                    return self.results
            
            # EXECUTION WITH ERROR RECOVERY
            processed = []
            failed = []
            
            for item in items_to_process:
                item_start = datetime.now()
                try:
                    result = self.execute_action(item)
                    duration = (datetime.now() - item_start).total_seconds()
                    
                    self.log_action(
                        action='execute',
                        input_data=item,
                        output=result,
                        duration=duration,
                        status='success'
                    )
                    processed.append({'item': item, 'result': result})
                    
                except Exception as e:
                    duration = (datetime.now() - item_start).total_seconds()
                    
                    # RECOVERY WORKFLOW
                    recovery = self.suggest_recovery(e, {'item': item})
                    
                    self.log_action(
                        action='execute',
                        input_data=item,
                        output=None,
                        duration=duration,
                        status='failed',
                        error=str(e)
                    )
                    
                    failed.append({
                        'item': item,
                        'error': str(e),
                        'recovery': recovery
                    })
            
            total_duration = (datetime.now() - start_time).total_seconds()
            
            self.results = {
                'status': 'complete' if not failed else 'partial',
                'processed': len(processed),
                'failed': len(failed),
                'items': processed,
                'failures': failed,
                'duration': total_duration
            }
            
            return self.results
            
        except ValidationError as e:
            self.results = {
                'status': 'validation_failed',
                'error': str(e)
            }
            self.log_action(
                action='validation',
                input_data=context,
                output=None,
                duration=0,
                status='failed',
                error=str(e)
            )
            return self.results
        
        except Exception as e:
            # GLOBAL ERROR RECOVERY
            recovery = self.suggest_recovery(e, context)
            
            self.results = {
                'status': 'error',
                'error': str(e),
                'recovery': recovery
            }
            self.log_action(
                action='agent_execution',
                input_data=context,
                output=None,
                duration=(datetime.now() - start_time).total_seconds(),
                status='failed',
                error=str(e)
            )
            return self.results


class FileOperationAgent(IdempotentAgent):
    """
    Example implementation: File operation agent with composable skills
    """
    
    def _register_skills(self) -> Dict[str, Callable]:
        return {
            'verify': self.verify_state,
            'hash': self._compute_hash,
            'exists': self._check_exists,
            'move': self._move_file,
            'backup': self._create_backup
        }
    
    def _compute_hash(self, filepath: Path) -> str:
        """Compute SHA256 hash of file"""
        if not filepath.exists():
            return None
        return hashlib.sha256(filepath.read_bytes()).hexdigest()
    
    def _check_exists(self, filepath: Path) -> bool:
        """Check if file exists"""
        return filepath.exists()
    
    def _move_file(self, source: Path, destination: Path):
        """Move file with backup"""
        if destination.exists():
            self.skills['backup'](destination)
        source.rename(destination)
    
    def _create_backup(self, filepath: Path):
        """Create timestamped backup"""
        if filepath.exists():
            backup_name = f"{filepath.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{filepath.suffix}"
            backup_path = filepath.parent / backup_name
            filepath.rename(backup_path)
    
    def verify_state(self, context: Dict) -> Dict:
        """Verify which files need operations"""
        source_files = context.get('source_files', [])
        target_dir = Path(context.get('target_dir', '.'))
        
        needs_action = []
        for source in source_files:
            source_path = Path(source)
            target_path = target_dir / source_path.name
            
            # Check if already in target
            if self.skills['exists'](target_path):
                # Check if identical
                source_hash = self.skills['hash'](source_path)
                target_hash = self.skills['hash'](target_path)
                
                if source_hash != target_hash:
                    needs_action.append({
                        'source': source_path,
                        'target': target_path,
                        'reason': 'hash_mismatch'
                    })
            else:
                needs_action.append({
                    'source': source_path,
                    'target': target_path,
                    'reason': 'missing'
                })
        
        return {
            'needs_action': len(needs_action) > 0,
            'items': needs_action
        }
    
    def execute_action(self, item: Dict) -> Dict:
        """Execute file move operation"""
        source = item['source']
        target = item['target']
        
        self.skills['move'](source, target)
        
        return {
            'moved': str(source),
            'to': str(target),
            'hash': self.skills['hash'](target)
        }
    
    def validate_prerequisites(self, context: Dict) -> bool:
        """Validate file operation prerequisites"""
        # Check source files exist
        source_files = context.get('source_files', [])
        if not source_files:
            raise ValidationError("No source files specified")
        
        for source in source_files:
            if not Path(source).exists():
                raise ValidationError(f"Source file not found: {source}")
        
        # Check target directory exists
        target_dir = Path(context.get('target_dir', '.'))
        if not target_dir.exists():
            raise ValidationError(f"Target directory not found: {target_dir}")
        
        return True
    
    def suggest_recovery(self, error: Exception, context: Dict) -> Dict:
        """Suggest recovery for file operations"""
        if "Permission denied" in str(error):
            return {
                'action': 'check_permissions',
                'message': 'Permission denied during file operation',
                'suggestion': 'Verify file permissions and close any programs using the files'
            }
        elif "No such file" in str(error):
            return {
                'action': 'verify_paths',
                'message': 'File or directory not found',
                'suggestion': 'Verify all file paths are correct and files exist'
            }
        else:
            return super().suggest_recovery(error, context)


# Usage example
if __name__ == "__main__":
    print("Idempotent Agent Framework")
    print("="*60)
    print("\nFeatures:")
    print("✓ Verification before execution")
    print("✓ Idempotent operations (safe to run multiple times)")
    print("✓ Error recovery workflows")
    print("✓ Complete audit trails")
    print("✓ Validation gates")
    print("✓ Composable skills")
    print("✓ Approval gates for safety")
    
    print("\n\nExample Usage:")
    print("""
agent = FileOperationAgent(name='file-mover', requires_approval=True)

context = {
    'source_files': ['file1.txt', 'file2.txt'],
    'target_dir': '/path/to/destination'
}

results = agent.run_with_validation(context)
agent.save_audit_trail()
""")
