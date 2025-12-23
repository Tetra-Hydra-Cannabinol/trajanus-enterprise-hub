# Trajanus Enterprise Hub - GitHub Collaboration Setup

**Date:** December 18, 2025  
**Purpose:** Professional development collaboration between Trajanus Principals  
**Developers:** Bill King (PM/Frontend), Chris Bochman (Database/Backend)

---

## REPOSITORY OVERVIEW

**Repository Name:** `trajanus-enterprise-hub`  
**Organization:** Trajanus USA  
**Privacy:** Private (company intellectual property)  
**License:** Proprietary

**Principals:**
- **Bill King** - CEO, PM Domain Expert, Frontend/Integration
- **Chris Bochman** - Principal Developer, Database Architecture, Backend Logic

---

## REPOSITORY STRUCTURE

```
trajanus-enterprise-hub/
│
├── README.md                           # Project overview
├── ARCHITECTURE.md                     # System architecture documentation
├── CONTRIBUTING.md                     # Contribution guidelines
├── CHANGELOG.md                        # Version history
├── LICENSE.md                          # Proprietary license
│
├── docs/
│   ├── 01-Getting-Started/
│   │   ├── ONBOARDING.md              # New developer setup
│   │   ├── DEVELOPMENT_ENVIRONMENT.md  # IDE, tools, dependencies
│   │   └── FIRST_RUN.md               # How to run the app
│   │
│   ├── 02-Architecture/
│   │   ├── SYSTEM_OVERVIEW.md         # High-level architecture
│   │   ├── DATABASE_DESIGN.md         # Supabase schema, pgvector
│   │   ├── ELECTRON_PYTHON_BRIDGE.md  # UI to backend communication
│   │   ├── FILE_STRUCTURE.md          # Codebase organization
│   │   └── TECH_STACK.md              # Technologies used
│   │
│   ├── 03-Standards/
│   │   ├── CODING_STANDARDS.md        # Code style, conventions
│   │   ├── BRANDING_GUIDE.md          # Trajanus visual standards
│   │   ├── COMMIT_CONVENTIONS.md      # Git commit format
│   │   └── TESTING_PROTOCOLS.md       # Testing requirements
│   │
│   ├── 04-Domain-Knowledge/
│   │   ├── CONSTRUCTION_PM_CONTEXT.md # Industry background
│   │   ├── FEDERAL_COMPLIANCE.md      # USACE, NAVFAC requirements
│   │   ├── BILLS_POV.md               # Bill's operational methodology
│   │   └── WORKSPACE_CONCEPTS.md      # PM, QCM, SSHO workspaces
│   │
│   └── 05-API-Reference/
│       ├── GOOGLE_DRIVE_API.md        # Drive integration
│       ├── SUPABASE_API.md            # Database operations
│       ├── ANTHROPIC_API.md           # Claude integration
│       └── ELECTRON_IPC.md            # Inter-process communication
│
├── src/
│   ├── electron/
│   │   ├── main.js                    # Electron main process
│   │   ├── preload.js                 # Preload scripts
│   │   └── index.html                 # Main application UI
│   │
│   ├── components/                    # Reusable UI components
│   │   ├── file-picker/               # File management components
│   │   ├── workspaces/                # Workspace layouts
│   │   └── shared/                    # Shared utilities
│   │
│   ├── backend/                       # Python backend services
│   │   ├── database/
│   │   │   ├── supabase_client.py    # Database connection
│   │   │   ├── models.py             # Data models
│   │   │   └── migrations/           # Schema migrations
│   │   │
│   │   ├── services/
│   │   │   ├── document_processor.py # Document ingestion
│   │   │   ├── embedding_service.py  # OpenAI embeddings
│   │   │   ├── rag_engine.py        # RAG query system
│   │   │   └── google_drive.py      # Drive operations
│   │   │
│   │   └── agents/
│   │       ├── qcm_agent.py         # QCM automation
│   │       ├── pm_agent.py          # PM toolkit automation
│   │       └── research_agent.py    # Research automation
│   │
│   ├── workspaces/                    # Workspace implementations
│   │   ├── developer-tools/
│   │   ├── pm-toolkit/
│   │   ├── qcm/
│   │   ├── ssho/
│   │   └── traffic-studies/
│   │
│   └── assets/
│       ├── fonts/                     # Architectural fonts
│       ├── icons/                     # Application icons
│       └── branding/                  # Trajanus branding assets
│
├── tests/
│   ├── unit/                          # Unit tests
│   ├── integration/                   # Integration tests
│   └── e2e/                          # End-to-end tests (Playwright)
│
├── scripts/
│   ├── setup/
│   │   ├── install_dependencies.sh   # Development setup
│   │   └── init_database.sql        # Database initialization
│   │
│   ├── automation/
│   │   ├── file_conversion.ps1      # MD to GDOC conversion
│   │   └── batch_operations.py      # Bulk file operations
│   │
│   └── deployment/
│       ├── build.sh                  # Build application
│       └── package.sh                # Create installers
│
├── database/
│   ├── schema/
│   │   ├── supabase_schema.sql      # Complete schema
│   │   └── migrations/              # Version-controlled migrations
│   │
│   ├── seed-data/                    # Test data
│   └── backups/                      # Backup procedures
│
└── research/
    ├── spikes/                       # Proof-of-concept code
    ├── benchmarks/                   # Performance testing
    └── investigations/               # Technical research
```

---

## COLLABORATION WORKFLOW

### FOR CHRIS (Database/Backend Developer):

**Initial Setup:**
```bash
# Clone repository
git clone git@github.com:trajanus-usa/trajanus-enterprise-hub.git
cd trajanus-enterprise-hub

# Install dependencies
npm install
pip install -r requirements.txt --break-system-packages

# Configure environment
cp .env.example .env
# Edit .env with Supabase credentials, API keys

# Initialize database
psql -h [supabase-host] -U postgres -f database/schema/supabase_schema.sql

# Run application
npm run dev
```

**Development Workflow:**
```bash
# Create feature branch
git checkout -b feature/database-optimization

# Make changes in src/backend/database/
# Write tests in tests/unit/database/

# Test locally
pytest tests/unit/database/

# Commit with conventional format
git add .
git commit -m "feat(database): optimize vector similarity queries

- Add index on embedding column
- Implement connection pooling
- Add query result caching

Improves RAG query performance by 40%"

# Push to GitHub
git push origin feature/database-optimization

# Create Pull Request on GitHub
# Bill reviews and merges
```

### FOR BILL (PM Domain/Frontend):

**Development Workflow:**
```bash
# Create feature branch
git checkout -b feature/qcm-workspace

# Make changes in src/workspaces/qcm/
# Update UI components

# Test in Electron
npm run dev

# Commit and push
git add .
git commit -m "feat(qcm): add submittal review interface

- Implement three-panel layout
- Add document upload capability
- Integrate with backend RAG system"

git push origin feature/qcm-workspace

# Create Pull Request
# Chris reviews backend integration
# Merge when approved
```

---

## AREAS OF RESPONSIBILITY

### CHRIS BOCHMAN - Backend/Database Architecture

**Primary Focus:**
- Supabase PostgreSQL database design
- pgvector implementation for RAG
- Python backend services
- Database migrations and optimization
- API endpoint design
- Data models and schemas
- Performance optimization
- Backup and recovery procedures

**Key Files:**
- `src/backend/database/*`
- `src/backend/services/*`
- `database/schema/*`
- `database/migrations/*`

**Tech Stack:**
- PostgreSQL + pgvector
- Python 3.11+
- Supabase
- OpenAI Embeddings API
- SQL

### BILL KING - Frontend/PM Domain Integration

**Primary Focus:**
- Electron application UI
- Workspace implementations
- PM domain logic
- User experience design
- Claude/AI integration
- Document workflows
- Government compliance requirements
- Industry-specific features

**Key Files:**
- `src/electron/*`
- `src/components/*`
- `src/workspaces/*`
- `docs/04-Domain-Knowledge/*`

**Tech Stack:**
- Electron
- HTML/CSS/JavaScript
- Node.js
- Claude API (Anthropic)
- Google Drive API

---

## COMMUNICATION CHANNELS

**Technical Discussions:**
- GitHub Issues (for features, bugs, architecture decisions)
- Pull Request comments (for code review)
- GitHub Discussions (for broader topics)

**Quick Questions:**
- Email: bill@trajanus-usa.com, chris@trajanus-usa.com
- [Your preferred method - Slack, Discord, etc.]

**Weekly Sync:**
- [Schedule weekly video call for alignment]
- Review PRs together
- Discuss architectural decisions
- Plan next sprint

---

## PULL REQUEST GUIDELINES

### Creating a PR:

**Title Format:**
```
<type>(<scope>): <description>

Examples:
feat(database): add vector similarity search
fix(qcm): resolve file upload timeout
docs(architecture): update database schema diagram
refactor(backend): optimize embedding generation
```

**PR Description Template:**
```markdown
## Summary
Brief description of what this PR does.

## Changes
- List of changes made
- Each change on its own line

## Testing
How this was tested:
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI changes)
[Add screenshots]

## Related Issues
Closes #123
Related to #456

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or breaking changes documented)
```

### Reviewing a PR:

**For Chris reviewing Bill's frontend:**
- Does the UI call backend APIs correctly?
- Are database queries optimized?
- Is error handling robust?

**For Bill reviewing Chris's backend:**
- Does this support the PM workflows needed?
- Is the API intuitive to use from frontend?
- Does this meet compliance requirements?

**Both review for:**
- Code quality and readability
- Test coverage
- Documentation completeness
- Security considerations

---

## BRANCH STRATEGY

**Main Branches:**
- `main` - Production-ready code (protected)
- `develop` - Integration branch for features (protected)

**Feature Branches:**
- `feature/[name]` - New features
- `fix/[name]` - Bug fixes
- `refactor/[name]` - Code refactoring
- `docs/[name]` - Documentation updates
- `test/[name]` - Test improvements

**Workflow:**
```
feature/database-optimization
    ↓
  develop (merge via PR)
    ↓
  main (merge after testing)
```

**Protected Branch Rules:**
- `main` and `develop` require PR approval
- Cannot push directly
- Must pass CI/CD checks (when implemented)
- At least 1 approval required

---

## CODING STANDARDS

**Python (Chris):**
```python
# Use type hints
def get_embeddings(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Generate embeddings for text using OpenAI API.
    
    Args:
        text: Input text to embed
        model: OpenAI model name
        
    Returns:
        List of embedding values (1536 dimensions)
    """
    # Implementation
    pass

# Follow PEP 8
# Use docstrings for all functions
# Type hints on all function signatures
# pytest for testing
```

**JavaScript (Bill):**
```javascript
// Use modern ES6+ syntax
// Clear function names
// JSDoc comments for complex functions

/**
 * Upload files to project folder
 * @param {File[]} files - Array of files to upload
 * @param {string} destination - Folder path
 * @returns {Promise<void>}
 */
async function uploadFiles(files, destination) {
    // Implementation
}

// Trajanus branding colors
const TRAJANUS_BROWN = '#9B7E52';
const TRAJANUS_DARK = '#7B6142';
```

**SQL (Chris):**
```sql
-- Use meaningful table and column names
-- Add comments for complex queries
-- Create indexes for performance

-- Create documents table with vector embeddings
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI text-embedding-3-small
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for vector similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

---

## ENVIRONMENT SETUP

**Required Tools:**

**Both Developers:**
- Git (version control)
- GitHub account
- VS Code (recommended IDE)

**Chris (Backend):**
- Python 3.11+
- PostgreSQL client
- Supabase CLI
- pip, virtualenv

**Bill (Frontend):**
- Node.js 18+
- npm or yarn
- Electron

**Shared Credentials:**
- Supabase project credentials (shared securely)
- OpenAI API key (shared securely)
- Google Drive API credentials (shared securely)

**Environment Variables:**
```bash
# .env file (DO NOT COMMIT)
SUPABASE_URL=https://[project].supabase.co
SUPABASE_ANON_KEY=[key]
OPENAI_API_KEY=[key]
GOOGLE_DRIVE_CLIENT_ID=[id]
GOOGLE_DRIVE_CLIENT_SECRET=[secret]
```

---

## SECURITY CONSIDERATIONS

**Secrets Management:**
- Never commit API keys or credentials
- Use `.env` files (add to `.gitignore`)
- Share credentials via secure channel (1Password, LastPass, etc.)

**Code Review:**
- All code reviewed before merge
- Check for security vulnerabilities
- Validate user inputs
- Sanitize database queries

**Access Control:**
- Repository is private
- Only Trajanus principals have access
- Use SSH keys for GitHub authentication

---

## TESTING STRATEGY

**Unit Tests (Both):**
- Test individual functions/components
- Mock external dependencies
- Fast execution (<1 second per test)

**Integration Tests (Chris):**
- Test database operations
- Test API endpoints
- Test service interactions

**E2E Tests (Bill):**
- Test complete user workflows
- Use Playwright for UI testing
- Test across different workspaces

**Test Commands:**
```bash
# Python backend tests
pytest tests/unit/
pytest tests/integration/

# JavaScript tests
npm test

# E2E tests
npm run test:e2e
```

---

## DOCUMENTATION REQUIREMENTS

**Code Documentation:**
- Function docstrings (Python)
- JSDoc comments (JavaScript)
- SQL comments for complex queries
- README in each major directory

**Architecture Documentation:**
- Update ARCHITECTURE.md for major changes
- Document design decisions
- Keep database schema docs current

**User Documentation:**
- Update user guides as features are added
- Document new workflows
- Create video tutorials for complex features

---

## DEPLOYMENT PROCESS

**Development → Staging → Production**

**Development:**
- Local testing on both machines
- Frequent commits to feature branches
- PR reviews and merges to `develop`

**Staging:**
- Merge `develop` → `main` when stable
- Test complete application
- Verify all integrations work

**Production:**
- Build Electron app
- Create installers (Windows, Mac)
- Distribute to end users (eventually)

---

## ONBOARDING CHECKLIST FOR CHRIS

**Week 1: Setup & Familiarization**
- [ ] Clone repository
- [ ] Install development environment
- [ ] Run application locally
- [ ] Review architecture documentation
- [ ] Read Bills_POV.md (understand PM domain)
- [ ] Review current database schema
- [ ] Set up Supabase access
- [ ] Make first commit (small improvement)

**Week 2: First Contributions**
- [ ] Review RAG implementation
- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Implement connection pooling
- [ ] Write unit tests for database layer
- [ ] Create first PR

**Week 3: Integration**
- [ ] Work on backend API endpoints
- [ ] Coordinate with Bill on frontend integration
- [ ] Implement embedding generation pipeline
- [ ] Add batch processing capabilities

**Ongoing:**
- [ ] Weekly sync with Bill
- [ ] Review and merge PRs
- [ ] Monitor database performance
- [ ] Plan architecture improvements

---

## PROJECT GOALS & TIMELINE

**Phase 1: Foundation (Weeks 1-4)**
- Stable database architecture
- Core RAG system working
- Basic Electron UI functional
- Developer workflow established

**Phase 2: Workspace Implementation (Weeks 5-12)**
- QCM workspace complete
- PM Toolkit operational
- File picker template deployed
- All workspaces integrated

**Phase 3: Automation (Weeks 13-20)**
- Python agents functional
- Document automation working
- Schedule generation automated
- Testing comprehensive

**Phase 4: Refinement (Weeks 21-26)**
- Performance optimization
- User testing
- Bug fixes
- Documentation complete

**Phase 5: Launch (Week 27+)**
- First client deployment
- Tom onboarded as user
- Support procedures in place
- Iterative improvements

---

## SUCCESS METRICS

**Technical:**
- Database queries < 100ms average
- RAG accuracy > 85%
- Zero data loss
- Application uptime > 99%

**Collaboration:**
- Weekly PR merges from both developers
- Code review turnaround < 24 hours
- Clean git history
- Comprehensive documentation

**Business:**
- First client using system by Q2 2026
- Positive user feedback
- Reduced PM time by 40%
- Scalable to multiple clients

---

## NEXT STEPS

**Immediate (This Week):**
1. Create GitHub repository
2. Upload existing codebase to `main`
3. Chris clones and sets up environment
4. First sync call to align on priorities
5. Chris reviews database schema
6. Bill prepares first backend integration task

**Short Term (Next 2 Weeks):**
1. Establish PR review rhythm
2. Chris optimizes database layer
3. Bill builds file picker UI
4. Integration testing
5. Document any architecture changes

**Long Term (Next 3 Months):**
1. Complete all core workspaces
2. Implement Python automation agents
3. Comprehensive testing suite
4. First client pilot program

---

## CONTACT & QUESTIONS

**Bill King**
- Email: bill@trajanus-usa.com
- Role: CEO, PM Domain Expert
- Focus: Frontend, UX, Claude Integration

**Chris Bochman**
- Email: chris@trajanus-usa.com
- Role: Principal Developer
- Focus: Database, Backend, Logic

**Repository:**
- GitHub: https://github.com/trajanus-usa/trajanus-enterprise-hub (to be created)

---

**Welcome to the team, Chris. Let's build something exceptional.**

---

**Document Version:** 1.0  
**Last Updated:** December 18, 2025  
**Next Review:** January 1, 2026
