"""
PARALLEL SESSION COORDINATOR
Manages multiple Claude sessions working in parallel
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict


class TaskType(Enum):
    """Types of tasks for delegation"""
    PLANNING = "planning"          # Claude Projects
    CODING = "coding"              # Claude Code
    FILE_OPS = "file_operations"   # Knowmad agents
    RESEARCH = "research"          # Research agent
    QUALITY = "quality_control"    # QCM/Compliance agents
    DATABASE = "database"          # KB ingestion
    

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    TESTING = "testing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class Task:
    """Individual task definition"""
    id: str
    name: str
    type: TaskType
    assignee: str  # claude_projects | claude_code | agent_name
    description: str
    dependencies: List[str]  # List of task IDs this depends on
    priority: TaskPriority
    estimated_duration: str  # e.g., "30m", "2h"
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['type'] = self.type.value
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data


class SessionCoordinator:
    """
    Coordinates parallel execution across multiple Claude sessions and agents
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.tasks: Dict[str, Task] = {}
        self.execution_log: List[Dict] = []
    
    def add_task(self, task: Task):
        """Add task to coordination queue"""
        self.tasks[task.id] = task
        self.log_event('task_added', {'task_id': task.id, 'name': task.name})
    
    def add_tasks(self, tasks: List[Task]):
        """Add multiple tasks"""
        for task in tasks:
            self.add_task(task)
    
    def delegate_tasks(self) -> Dict[str, List[Task]]:
        """
        Delegate tasks to appropriate executors
        
        Returns:
            Dictionary mapping executor to tasks
        """
        delegation = {
            'claude_projects': [],
            'claude_code': [],
            'agents': []
        }
        
        for task in self.tasks.values():
            if task.type == TaskType.PLANNING:
                delegation['claude_projects'].append(task)
            elif task.type == TaskType.CODING:
                delegation['claude_code'].append(task)
            else:
                delegation['agents'].append(task)
        
        return delegation
    
    def get_ready_tasks(self) -> List[Task]:
        """
        Get tasks ready for execution (dependencies met)
        
        Returns:
            List of tasks with all dependencies complete
        """
        ready = []
        
        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
            
            # Check if all dependencies complete
            deps_met = all(
                self.tasks.get(dep_id, Task(id=dep_id, name="", type=TaskType.PLANNING, 
                                           assignee="", description="", dependencies=[], 
                                           priority=TaskPriority.LOW, estimated_duration="")).status == TaskStatus.COMPLETE
                for dep_id in task.dependencies
            )
            
            if deps_met:
                ready.append(task)
        
        # Sort by priority
        ready.sort(key=lambda t: t.priority.value)
        return ready
    
    def get_parallel_batches(self) -> List[List[Task]]:
        """
        Organize tasks into parallel execution batches
        
        Returns:
            List of task batches that can run in parallel
        """
        batches = []
        remaining_tasks = set(self.tasks.keys())
        
        while remaining_tasks:
            batch = []
            
            for task_id in list(remaining_tasks):
                task = self.tasks[task_id]
                
                # Check if dependencies in previous batches or complete
                deps_satisfied = all(
                    dep_id not in remaining_tasks or 
                    self.tasks[dep_id].status == TaskStatus.COMPLETE
                    for dep_id in task.dependencies
                )
                
                if deps_satisfied:
                    batch.append(task)
                    remaining_tasks.remove(task_id)
            
            if batch:
                batches.append(batch)
            else:
                # Circular dependency or blocked tasks
                break
        
        return batches
    
    def start_task(self, task_id: str):
        """Mark task as started"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.IN_PROGRESS
            self.tasks[task_id].started_at = datetime.now().isoformat()
            self.log_event('task_started', {'task_id': task_id})
    
    def complete_task(self, task_id: str, result: Dict):
        """Mark task as complete with result"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETE
            self.tasks[task_id].result = result
            self.tasks[task_id].completed_at = datetime.now().isoformat()
            self.log_event('task_completed', {'task_id': task_id})
    
    def fail_task(self, task_id: str, error: str):
        """Mark task as failed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.FAILED
            self.tasks[task_id].error = error
            self.log_event('task_failed', {'task_id': task_id, 'error': error})
    
    def block_task(self, task_id: str, reason: str):
        """Mark task as blocked"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.BLOCKED
            self.tasks[task_id].error = reason
            self.log_event('task_blocked', {'task_id': task_id, 'reason': reason})
    
    def log_event(self, event_type: str, data: Dict):
        """Add event to execution log"""
        self.execution_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': event_type,
            'data': data
        })
    
    def get_status_report(self) -> Dict:
        """Generate comprehensive status report"""
        total = len(self.tasks)
        by_status = {}
        
        for task in self.tasks.values():
            status = task.status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            'project': self.project_name,
            'total_tasks': total,
            'by_status': by_status,
            'completion_rate': by_status.get('complete', 0) / total if total > 0 else 0,
            'ready_tasks': len(self.get_ready_tasks()),
            'blocked_tasks': by_status.get('blocked', 0)
        }
    
    def save_coordination_plan(self, output_path: str):
        """Save complete coordination plan to file"""
        plan = {
            'project': self.project_name,
            'created': datetime.now().isoformat(),
            'tasks': [task.to_dict() for task in self.tasks.values()],
            'parallel_batches': [
                [task.to_dict() for task in batch]
                for batch in self.get_parallel_batches()
            ],
            'delegation': {
                executor: [task.to_dict() for task in tasks]
                for executor, tasks in self.delegate_tasks().items()
            },
            'execution_log': self.execution_log
        }
        
        with open(output_path, 'w') as f:
            json.dump(plan, f, indent=2)
        
        return output_path


# Predefined workflow templates
class WorkflowTemplates:
    """Common workflow patterns"""
    
    @staticmethod
    def qcm_implementation_workflow() -> List[Task]:
        """Complete QCM workflow implementation"""
        return [
            Task(
                id='qcm-01',
                name='Design QCM Workflow Architecture',
                type=TaskType.PLANNING,
                assignee='claude_projects',
                description='Design complete workflow from file selection to report delivery',
                dependencies=[],
                priority=TaskPriority.CRITICAL,
                estimated_duration='1h'
            ),
            Task(
                id='qcm-02',
                name='Implement Template Selection UI',
                type=TaskType.CODING,
                assignee='claude_code',
                description='Build template dropdown and reference doc browser',
                dependencies=['qcm-01'],
                priority=TaskPriority.HIGH,
                estimated_duration='2h'
            ),
            Task(
                id='qcm-03',
                name='Implement Claude Review Engine',
                type=TaskType.CODING,
                assignee='claude_code',
                description='Build API integration for document review',
                dependencies=['qcm-01'],
                priority=TaskPriority.HIGH,
                estimated_duration='3h'
            ),
            Task(
                id='qcm-04',
                name='Implement Report Generation',
                type=TaskType.CODING,
                assignee='claude_code',
                description='Generate and save compliance reports',
                dependencies=['qcm-03'],
                priority=TaskPriority.MEDIUM,
                estimated_duration='2h'
            ),
            Task(
                id='qcm-05',
                name='Test with Real Submittals',
                type=TaskType.QUALITY,
                assignee='qcm-agent',
                description='Test workflow with actual project submittals',
                dependencies=['qcm-02', 'qcm-04'],
                priority=TaskPriority.HIGH,
                estimated_duration='1h'
            )
        ]
    
    @staticmethod
    def knowledge_base_expansion_workflow() -> List[Task]:
        """Expand knowledge base with new content"""
        return [
            Task(
                id='kb-01',
                name='Download YouTube Transcripts',
                type=TaskType.RESEARCH,
                assignee='youtube-crawler',
                description='Bulk download Office automation tutorials',
                dependencies=[],
                priority=TaskPriority.HIGH,
                estimated_duration='2h'
            ),
            Task(
                id='kb-02',
                name='Convert to Google Docs',
                type=TaskType.FILE_OPS,
                assignee='knowmad-5',
                description='Convert markdown transcripts to .gdoc format',
                dependencies=['kb-01'],
                priority=TaskPriority.MEDIUM,
                estimated_duration='30m'
            ),
            Task(
                id='kb-03',
                name='Ingest to Supabase',
                type=TaskType.DATABASE,
                assignee='kb-ingestion',
                description='Generate embeddings and store in KB',
                dependencies=['kb-01'],
                priority=TaskPriority.HIGH,
                estimated_duration='1h'
            ),
            Task(
                id='kb-04',
                name='Verify Ingestion',
                type=TaskType.QUALITY,
                assignee='db-audit',
                description='Confirm all documents properly ingested',
                dependencies=['kb-03'],
                priority=TaskPriority.CRITICAL,
                estimated_duration='15m'
            )
        ]


# Example usage
if __name__ == "__main__":
    print("Session Coordinator - Parallel Execution Management")
    print("="*60)
    
    # Create coordinator
    coordinator = SessionCoordinator("QCM Implementation")
    
    # Add workflow
    coordinator.add_tasks(WorkflowTemplates.qcm_implementation_workflow())
    
    # Get parallel batches
    batches = coordinator.get_parallel_batches()
    
    print(f"\nProject: {coordinator.project_name}")
    print(f"Total tasks: {len(coordinator.tasks)}")
    print(f"\nParallel execution plan ({len(batches)} batches):")
    
    for i, batch in enumerate(batches, 1):
        print(f"\nBatch {i} (can run in parallel):")
        for task in batch:
            print(f"  - {task.name} ({task.assignee})")
    
    # Generate status report
    status = coordinator.get_status_report()
    print(f"\nStatus: {status}")
    
    # Save plan
    plan_file = coordinator.save_coordination_plan('/home/claude/coordination_plan.json')
    print(f"\nCoordination plan saved: {plan_file}")
