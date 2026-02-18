"""
ORCHESTRATOR PROMPT TEMPLATES
For Claude Projects to create optimized prompts for Claude Code and specialized agents
"""

class PromptTemplate:
    """Base class for all orchestrator prompt templates"""
    
    @staticmethod
    def create_cc_prompt(task_name: str, context: dict, requirements: list, 
                        success_criteria: list, constraints: list = None) -> str:
        """
        Generate comprehensive prompt for Claude Code
        
        Args:
            task_name: Clear description of what to build/implement
            context: Dictionary with project_state, completed_items, pending_items
            requirements: List of specific requirements
            success_criteria: List of how to verify completion
            constraints: Optional list of limitations/restrictions
        """
        
        prompt = f"""# CLAUDE CODE TASK: {task_name}

## CONTEXT

**Current Project State:**
{context.get('project_state', 'Not specified')}

**Already Completed:**
{chr(10).join(f"✓ {item}" for item in context.get('completed', []))}

**Pending/In Progress:**
{chr(10).join(f"○ {item}" for item in context.get('pending', []))}

---

## REQUIREMENTS

"""
        for i, req in enumerate(requirements, 1):
            prompt += f"{i}. {req}\n"
        
        prompt += "\n---\n\n## SUCCESS CRITERIA\n\nTask is complete when:\n\n"
        
        for i, criterion in enumerate(success_criteria, 1):
            prompt += f"{i}. {criterion}\n"
        
        if constraints:
            prompt += "\n---\n\n## CONSTRAINTS & LIMITATIONS\n\n"
            for i, constraint in enumerate(constraints, 1):
                prompt += f"{i}. {constraint}\n"
        
        prompt += """
---

## EXECUTION PROTOCOL

1. Read all requirements carefully before starting
2. Implement incrementally with testing at each step
3. Report progress: [in_progress | blocked | testing | complete]
4. If blocked, specify exact blocker and proposed solution
5. When complete, verify all success criteria met

## REPORTING FORMAT

**Status:** [in_progress | blocked | testing | complete]
**Completed:** [List what's done]
**Remaining:** [List what's left]
**Issues:** [Any problems encountered]
**Next Steps:** [What happens next]

---

**BEGIN EXECUTION**
"""
        return prompt
    
    @staticmethod
    def create_agent_prompt(agent_name: str, operation: str, inputs: dict,
                           approval_required: bool = True) -> str:
        """Generate prompt for specialized agent execution"""
        
        prompt = f"""# AGENT EXECUTION: {agent_name}

## OPERATION
{operation}

## INPUTS

"""
        for key, value in inputs.items():
            prompt += f"**{key}:** {value}\n"
        
        if approval_required:
            prompt += """
---

## APPROVAL PROTOCOL

1. Agent will verify current state
2. Agent will report what needs doing
3. **WAIT FOR USER APPROVAL** before executing
4. Execute only approved items
5. Report completion status

"""
        else:
            prompt += """
---

## AUTO-EXECUTION MODE

Agent will:
1. Verify current state
2. Execute only necessary operations (idempotent)
3. Report completion status

"""
        
        prompt += """
---

**EXECUTE AGENT**
"""
        return prompt
    
    @staticmethod
    def create_research_prompt(topics: list, depth: str = "standard",
                              output_format: str = "summary") -> str:
        """Generate prompt for research agent"""
        
        prompt = f"""# RESEARCH TASK

## TOPICS TO RESEARCH

"""
        for i, topic in enumerate(topics, 1):
            prompt += f"{i}. {topic}\n"
        
        prompt += f"""
---

## RESEARCH PARAMETERS

**Depth:** {depth}
- shallow: Quick overview, 2-3 sources per topic
- standard: Comprehensive, 5-10 sources per topic
- deep: Exhaustive, 15+ sources per topic

**Output Format:** {output_format}
- summary: Key findings only
- detailed: Complete findings with source citations
- report: Formatted document with analysis

---

## DELIVERABLES

1. Findings categorized by topic
2. Source citations with URLs
3. Key insights and actionable recommendations
4. Date-stamped for currency tracking

---

**BEGIN RESEARCH**
"""
        return prompt
    
    @staticmethod
    def create_parallel_workflow(tasks: list) -> str:
        """Generate prompt for coordinating parallel execution"""
        
        prompt = """# PARALLEL WORKFLOW COORDINATION

## TASK BREAKDOWN

"""
        for i, task in enumerate(tasks, 1):
            prompt += f"""
### Task {i}: {task['name']}
**Assignee:** {task.get('assignee', 'Claude Code')}
**Dependencies:** {', '.join(task.get('dependencies', ['None']))}
**Estimated Duration:** {task.get('duration', 'Unknown')}
**Priority:** {task.get('priority', 'Medium')}

"""
        
        prompt += """
---

## COORDINATION PROTOCOL

1. Execute independent tasks in parallel
2. Monitor dependencies before starting dependent tasks
3. Report progress from each track
4. Consolidate results when all complete

---

## PROGRESS TRACKING

Track each task:
- [ ] Task 1
- [ ] Task 2
...

Update as tasks complete.

---

**BEGIN PARALLEL EXECUTION**
"""
        return prompt


class PromptExamples:
    """Real-world prompt examples for common scenarios"""
    
    @staticmethod
    def qcm_workflow_example():
        """Example: QCM submittal review workflow"""
        return PromptTemplate.create_cc_prompt(
            task_name="Implement QCM Submittal Review Workflow",
            context={
                'project_state': 'Enterprise Hub QCM Workspace functional, needs review workflow',
                'completed': [
                    'File browser modal with Google Drive integration',
                    'Document filter (.pdf, .docx, .gdoc, .md)',
                    'Multi-select with checkboxes',
                    'Project workspace panel display'
                ],
                'pending': [
                    'Template selection system',
                    'Reference document browser',
                    'Claude-powered review engine',
                    'Save to Client Deliverables'
                ]
            },
            requirements=[
                'Create template selection dropdown with QCM templates from Templates folder',
                'Add reference document browser to load construction standards',
                'Implement Claude API call for document review using selected template',
                'Generate review report with compliance findings',
                'Save final report to Client Deliverables folder with proper naming'
            ],
            success_criteria=[
                'User can select from available QCM templates',
                'User can load reference documents for comparison',
                'Review executes and returns structured compliance findings',
                'Report saves to correct folder with timestamp and project ID',
                'All files remain accessible after save operation'
            ],
            constraints=[
                'Must maintain brown/orange UI theme (#9B7E52)',
                'Cannot break existing file browser functionality',
                'Claude API calls must include proper error handling',
                'File paths must use forward slashes for Python compatibility'
            ]
        )
    
    @staticmethod
    def research_agent_example():
        """Example: Daily research task"""
        return PromptTemplate.create_research_prompt(
            topics=[
                'Claude Sonnet 4.5 new features December 2025',
                'Construction AI automation platforms',
                'Primavera P6 API integration best practices',
                'Federal contracting AI adoption trends'
            ],
            depth='standard',
            output_format='detailed'
        )
    
    @staticmethod
    def knowledge_base_ingestion_example():
        """Example: KB ingestion task"""
        return PromptTemplate.create_agent_prompt(
            agent_name='kb-ingestion',
            operation='Ingest YouTube transcripts into Supabase KB',
            inputs={
                'source_folder': 'G:/My Drive/00 - Trajanus USA/08-Learning/Office_Automation',
                'file_pattern': '*.txt',
                'category': 'office_automation',
                'embedding_model': 'text-embedding-3-small'
            },
            approval_required=True
        )


# Quick reference guide
PROMPT_GUIDE = """
ORCHESTRATOR PROMPT TEMPLATE GUIDE
==================================

WHEN TO USE EACH TEMPLATE:

1. create_cc_prompt()
   - Building new features in Enterprise Hub
   - Implementing complex workflows
   - Multi-step development tasks
   
2. create_agent_prompt()
   - Running specialized Knowmad agents
   - File operations requiring approval
   - Automated background tasks
   
3. create_research_prompt()
   - Daily intelligence gathering
   - Competitive analysis
   - Technical documentation research
   
4. create_parallel_workflow()
   - Multiple independent tasks
   - Coordinated multi-agent operations
   - Large projects requiring parallelization

BEST PRACTICES:

✓ Always include context about current state
✓ Make requirements specific and testable
✓ Define clear success criteria
✓ List constraints to prevent mistakes
✓ Use approval gates for destructive operations
✓ Include error handling expectations

EXAMPLES:

See PromptExamples class for real-world scenarios.
"""

if __name__ == "__main__":
    print(PROMPT_GUIDE)
    print("\n" + "="*50)
    print("EXAMPLE: QCM Workflow Prompt")
    print("="*50 + "\n")
    print(PromptExamples.qcm_workflow_example())
