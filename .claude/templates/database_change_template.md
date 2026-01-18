# Database Change Template

## Change Information
- **Change Type:** [New Table/New Column/Index/Migration/Query]
- **Database:** Supabase PostgreSQL
- **Affected Table(s):** [Table names]
- **Risk Level:** [Low/Medium/High]

---

## CRITICAL: Pre-Change Protocol

### NEVER ASSUME SCHEMA
```sql
-- ALWAYS verify schema FIRST
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'your_table'
ORDER BY ordinal_position;
```

### Test Before Integration
1. Test query in Supabase SQL Editor
2. Document actual schema vs. assumptions
3. Create standalone test script
4. THEN integrate into application

---

## Change Details

### Current State
```sql
-- Current schema/query (document what exists NOW)
```

### Proposed Change
```sql
-- New schema/query
```

### Rollback Plan
```sql
-- How to undo if needed
```

---

## Implementation Checklist

### Pre-Implementation
- [ ] Verified current schema via information_schema
- [ ] Tested query in Supabase SQL Editor
- [ ] Confirmed RLS policies won't block
- [ ] Backup taken if modifying data

### Implementation
- [ ] Migration script written
- [ ] Applied to development/branch first
- [ ] Verified data integrity
- [ ] Updated application code

### Post-Implementation
- [ ] Verified in Supabase dashboard
- [ ] Tested from application
- [ ] Performance acceptable
- [ ] No RLS errors

---

## Supabase Connection Info

### MCP Access
```
Tool: mcp__plugin_supabase_supabase__execute_sql
Project ID: [Get from mcp__plugin_supabase_supabase__list_projects]
```

### Direct Access (Python scripts)
```python
# Location: G:\...\00-Command-Center\.env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
```

---

## Common Queries

### List All Tables
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### Check Table Structure
```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'knowledge_base'
ORDER BY ordinal_position;
```

### Check RLS Policies
```sql
SELECT * FROM pg_policies
WHERE tablename = 'your_table';
```

### Check Indexes
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'your_table';
```

---

## Acceptance Criteria

### Schema
```
[ ] Schema matches specification
[ ] Constraints correctly defined
[ ] Indexes created for query patterns
[ ] RLS policies appropriate
```

### Data Integrity
```
[ ] Existing data preserved
[ ] New data validates correctly
[ ] Foreign keys intact
[ ] No orphaned records
```

### Performance
```
[ ] Queries execute in <100ms
[ ] Indexes used (EXPLAIN ANALYZE)
[ ] No full table scans on large tables
```

### Application
```
[ ] App queries work correctly
[ ] Error handling for DB errors
[ ] UI reflects data changes
```

---

## Documentation Updates

- [ ] Update relevant .claude.md with new schema info
- [ ] Update architecture.md if structural change
- [ ] Document in CHANGELOG.md if significant

---

## Lessons Learned Reference

### From CHANGELOG.md (2025-12-XX)
> **NEVER ASSUME SCHEMA**
> 1. Query information_schema FIRST
> 2. Test in Supabase SQL editor
> 3. Document actual vs. assumed schema
> 4. Create standalone test before integration

---

## Notes
[Schema decisions, migration considerations, performance observations]
