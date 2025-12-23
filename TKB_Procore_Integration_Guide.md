# PROCORE INTEGRATION - TRAJANUS KNOWLEDGE BASE

**Document Type:** Integration Guide  
**Category:** Construction Management Systems  
**Last Updated:** 2025-12-14  
**Applicable To:** Federal Construction Projects, Commercial Construction  

---

## EXECUTIVE SUMMARY

Procore is a cloud-based construction management platform providing comprehensive project management, financials, quality/safety, and field productivity tools. This guide documents API integration approaches for Trajanus Enterprise Hub.

**Key Architecture:** RESTful API with OAuth 2.0 authentication, extensive endpoint coverage across all modules.

---

## API OVERVIEW

### Procore API Structure

**Base Architecture:**
- RESTful API design
- OAuth 2.0 authentication
- JSON data format
- Rate limiting enforced
- Webhook support for real-time events

**API Documentation:** https://developers.procore.com

**API Versions:**
- Current: REST v1.0
- Updates: Frequent additions, backwards compatible
- Deprecation: 6-month notice policy

### Authentication

**OAuth 2.0 Flow:**
```javascript
// Step 1: Authorization Request
const authURL = `https://login.procore.com/oauth/authorize?` +
  `client_id=${CLIENT_ID}` +
  `&response_type=code` +
  `&redirect_uri=${REDIRECT_URI}`;

// Step 2: Exchange Code for Token
const tokenResponse = await fetch('https://login.procore.com/oauth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    grant_type: 'authorization_code',
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    code: authorizationCode,
    redirect_uri: REDIRECT_URI
  })
});

const { access_token, refresh_token } = await tokenResponse.json();

// Step 3: API Calls
const response = await fetch('https://api.procore.com/rest/v1.0/projects', {
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Procore-Company-Id': COMPANY_ID
  }
});
```

**Token Management:**
- Access tokens expire (typically 2 hours)
- Refresh tokens valid for extended period
- Implement automatic refresh logic
- Store securely (environment variables, vault)

---

## KEY API MODULES

### 1. PROJECT MANAGEMENT

**Projects Endpoint:**
```javascript
// List Projects
GET /rest/v1.0/projects
Headers: Authorization, Procore-Company-Id

// Get Project Details
GET /rest/v1.0/projects/{project_id}

// Create Project
POST /rest/v1.0/projects
Body: {
  name: "Project Name",
  project_number: "2024-001",
  address: "123 Construction St",
  city: "City",
  state_code: "FL",
  zip: "32601",
  start_date: "2024-01-01",
  completion_date: "2025-12-31"
}

// Update Project
PATCH /rest/v1.0/projects/{project_id}
```

**Key Fields:**
- name, project_number
- address, city, state_code, zip
- start_date, completion_date
- project_stage_id, project_type_id
- owner_id, timezone

### 2. RFIs (REQUESTS FOR INFORMATION)

**RFI Endpoints:**
```javascript
// List RFIs
GET /rest/v1.0/projects/{project_id}/rfis

// Create RFI
POST /rest/v1.0/projects/{project_id}/rfis
Body: {
  subject: "Foundation Detail Clarification",
  question: "Specify rebar spacing for grid A-1",
  assignee_id: user_id,
  responsible_contractor_id: company_id,
  due_date: "2024-12-20",
  drawing_number: "S-101"
}

// Update RFI
PATCH /rest/v1.0/rfis/{rfi_id}

// Get RFI Attachments
GET /rest/v1.0/rfis/{rfi_id}/attachments
```

**RFI Workflow:**
1. Create RFI → Status: Draft
2. Submit → Status: Open
3. Respond → Add official response
4. Close → Status: Closed

### 3. SUBMITTALS

**Submittal Endpoints:**
```javascript
// List Submittals
GET /rest/v1.0/projects/{project_id}/submittals

// Create Submittal
POST /rest/v1.0/projects/{project_id}/submittals
Body: {
  title: "Structural Steel Shop Drawings",
  spec_section: "05 12 00",
  submittal_type: "Shop Drawing",
  received_from_id: contractor_id,
  ball_in_court_id: engineer_id,
  due_date: "2024-12-25"
}

// Update Status
PATCH /rest/v1.0/submittals/{submittal_id}
Body: {
  status: "Approved",
  returned_date: "2024-12-18"
}
```

**Submittal Types:**
- Shop Drawings
- Product Data
- Samples
- Mix Designs
- Closeout Submittals

### 4. DOCUMENTS

**Document Management:**
```javascript
// List Documents
GET /rest/v1.0/projects/{project_id}/documents

// Upload Document
POST /rest/v1.0/projects/{project_id}/documents
Headers: Content-Type: multipart/form-data
Body: FormData with file

// Create Folder
POST /rest/v1.0/folders
Body: {
  name: "Submittals - December",
  parent_id: parent_folder_id
}

// Get Document Versions
GET /rest/v1.0/documents/{document_id}/versions
```

**Document Organization:**
- Hierarchical folder structure
- Version control automatic
- Permissions per folder
- Search by metadata

### 5. BUDGETS & FINANCIALS

**Budget Endpoints:**
```javascript
// Get Budget
GET /rest/v1.0/projects/{project_id}/budget

// Get Budget Line Items
GET /rest/v1.0/budget_line_items

// Create Budget Line Item
POST /rest/v1.0/budget_line_items
Body: {
  description: "Foundation Work",
  cost_code: "03-1000",
  budgeted_total_cost: 150000.00
}

// Budget Snapshot
POST /rest/v1.0/projects/{project_id}/budget_snapshots
```

**Financial Tracking:**
- Budget vs Actual
- Committed costs
- Forecast to complete
- Change orders impact

### 6. CHANGE ORDERS

**Change Order Endpoints:**
```javascript
// List Change Orders
GET /rest/v1.0/projects/{project_id}/change_orders

// Create Change Order Package
POST /rest/v1.0/projects/{project_id}/change_order_packages
Body: {
  title: "Site Grading Modifications",
  change_order_package_type: "Potential Change Order"
}

// Create Commitment Change Order
POST /rest/v1.0/commitment_change_orders
Body: {
  number: "PCO-001",
  title: "Additional Excavation",
  amount: 25000.00
}
```

### 7. SCHEDULE/TASKS

**Schedule Integration:**
```javascript
// List Schedule Tasks  
GET /rest/v1.0/projects/{project_id}/schedule

// Create Task
POST /rest/v1.0/projects/{project_id}/tasks
Body: {
  name: "Pour Foundation",
  start_date: "2024-12-20",
  due_date: "2024-12-22",
  assignee_ids: [user_id]
}

// Update Task Status
PATCH /rest/v1.0/tasks/{task_id}
Body: {
  status: "complete",
  percent_complete: 100
}
```

### 8. USERS & PERMISSIONS

**User Management:**
```javascript
// List Project Users
GET /rest/v1.0/projects/{project_id}/users

// Add User to Project
POST /rest/v1.0/projects/{project_id}/users
Body: {
  user_id: user_id,
  permission_template_id: template_id
}

// Get User Permissions
GET /rest/v1.0/users/{user_id}/permissions
```

---

## WEBHOOK EVENTS

**Real-Time Notifications:**

**Available Events:**
- RFI created/updated/deleted
- Submittal created/updated
- Document uploaded
- Budget snapshot created
- Change order events
- Daily log entries

**Webhook Setup:**
```javascript
// Register Webhook
POST /rest/v1.0/webhooks/hooks
Body: {
  hook: {
    api_version: "v1.0",
    destination_url: "https://trajanus.com/webhooks/procore",
    resource_name: "RFIs",
    event_type: "create"
  }
}

// Webhook Payload Example
{
  "id": "webhook_id",
  "resource_name": "RFIs",
  "event_type": "create",
  "company_id": 12345,
  "project_id": 67890,
  "resource_id": 111,
  "timestamp": "2024-12-14T10:30:00Z",
  "metadata": { ... }
}
```

**Processing Webhooks:**
1. Verify webhook signature
2. Parse payload
3. Update local database
4. Trigger workflows (notifications, sync, etc.)
5. Return 200 OK quickly (process async)

---

## INTEGRATION WITH TRAJANUS HUB

### Architecture

```
Procore Cloud ← → OAuth 2.0 ← → Trajanus Middleware ← → 
← → Local Database ← → QCM Workspace UI
```

**Middleware Layer (Node.js):**
```javascript
// procore-service.js
class ProcoreService {
  constructor(accessToken, companyId) {
    this.token = accessToken;
    this.companyId = companyId;
    this.baseURL = 'https://api.procore.com/rest/v1.0';
  }

  async getProjects() {
    const response = await fetch(`${this.baseURL}/projects`, {
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Procore-Company-Id': this.companyId
      }
    });
    return response.json();
  }

  async getRFIs(projectId) {
    const response = await fetch(
      `${this.baseURL}/projects/${projectId}/rfis`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  async createRFI(projectId, rfiData) {
    const response = await fetch(
      `${this.baseURL}/projects/${projectId}/rfis`,
      {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(rfi: rfiData)
      }
    );
    return response.json();
  }

  getHeaders() {
    return {
      'Authorization': `Bearer ${this.token}`,
      'Procore-Company-Id': this.companyId,
      'Content-Type': 'application/json'
    };
  }
}
```

### Data Synchronization

**Pull Strategy (Periodic):**
- Hourly: RFIs, Submittals (active projects)
- Daily: Documents, Budget updates
- Weekly: Full project sync
- Real-time: Webhooks for critical items

**Push Strategy (User Actions):**
- Create RFI from Trajanus → POST to Procore
- Update submittal status → PATCH to Procore
- Upload document → POST with multipart/form-data
- Bi-directional sync enabled

**Conflict Resolution:**
- Procore is source of truth for field data
- Trajanus is source of truth for QC data
- Timestamp-based merge for shared data
- Manual review for conflicts

### Database Schema

**Local Cache Tables:**
```sql
-- Procore Projects
CREATE TABLE procore_projects (
  id SERIAL PRIMARY KEY,
  procore_id INTEGER UNIQUE,
  name VARCHAR(255),
  project_number VARCHAR(50),
  start_date DATE,
  completion_date DATE,
  sync_status VARCHAR(20),
  last_synced TIMESTAMP
);

-- Procore RFIs
CREATE TABLE procore_rfis (
  id SERIAL PRIMARY KEY,
  procore_id INTEGER UNIQUE,
  project_id INTEGER REFERENCES procore_projects(procore_id),
  subject TEXT,
  status VARCHAR(50),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  assignee_id INTEGER,
  due_date DATE
);

-- Sync Log
CREATE TABLE procore_sync_log (
  id SERIAL PRIMARY KEY,
  sync_type VARCHAR(50),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  records_processed INTEGER,
  errors JSON,
  status VARCHAR(20)
);
```

---

## INTEGRATION WITH P6 AND RMS

### Procore + P6 Workflow

**Schedule Synchronization:**
```
P6 (Schedule Authority) → Export to Procore Tasks
Procore (Field Updates) → Update P6 Activity Status
```

**Data Mapping:**
| P6 Field | Procore Field |
|----------|---------------|
| Activity ID | Task ID (custom field) |
| Activity Name | Task Name |
| Start Date | Start Date |
| Finish Date | Due Date |
| % Complete | Percent Complete |
| Resource | Assignee |
| WBS | Folder Structure |

**Integration Script:**
```javascript
async function syncP6ToProcore(p6Schedule, procoreProject) {
  for (const activity of p6Schedule.activities) {
    // Check if task exists in Procore
    const existingTask = await procore.findTaskByP6ID(activity.id);
    
    if (existingTask) {
      // Update
      await procore.updateTask(existingTask.id, {
        percent_complete: activity.percentComplete,
        status: activity.status
      });
    } else {
      // Create new
      await procore.createTask(procoreProject.id, {
        name: activity.name,
        start_date: activity.startDate,
        due_date: activity.finishDate,
        custom_fields: {
          p6_activity_id: activity.id
        }
      });
    }
  }
}
```

### Procore + RMS 3.0 Workflow

**Submittal Coordination:**
```
Procore Submittals → Export to RMS Transmittal System
RMS Approval Status → Update Procore Submittal Status
```

**Payment Application:**
```
Procore Budget/Costs → Feed RMS Pay Estimate
RMS Payment Approved → Update Procore Financial Status
```

---

## API RATE LIMITING

**Limits:**
- 3,600 requests per hour per company
- Burst: 10 requests per second
- Exceeding: 429 Too Many Requests

**Rate Limit Headers:**
```
X-Rate-Limit-Limit: 3600
X-Rate-Limit-Remaining: 3542
X-Rate-Limit-Reset: 1702573200
```

**Handling:**
```javascript
async function makeRequestWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url, options);
    
    if (response.status === 429) {
      const resetTime = response.headers.get('X-Rate-Limit-Reset');
      const waitTime = (resetTime * 1000) - Date.now();
      await sleep(waitTime + 1000); // Wait + buffer
      continue;
    }
    
    return response;
  }
  throw new Error('Max retries exceeded');
}
```

---

## ERROR HANDLING

**Common Errors:**

**401 Unauthorized:**
- Access token expired
- Solution: Refresh token and retry

**403 Forbidden:**
- Insufficient permissions
- Solution: Check user permissions, request access

**404 Not Found:**
- Resource doesn't exist
- Solution: Verify IDs, handle gracefully

**422 Unprocessable Entity:**
- Validation errors
- Solution: Check required fields, data formats

**Example Handler:**
```javascript
async function handleProcoreError(error, response) {
  const errorData = await response.json();
  
  switch (response.status) {
    case 401:
      await refreshAccessToken();
      return 'RETRY';
    
    case 403:
      logger.error('Permission denied:', errorData);
      return 'PERMISSION_ERROR';
    
    case 422:
      logger.error('Validation failed:', errorData.errors);
      return 'VALIDATION_ERROR';
    
    case 429:
      await handleRateLimit(response);
      return 'RETRY';
    
    default:
      logger.error('Unknown error:', errorData);
      return 'UNKNOWN_ERROR';
  }
}
```

---

## IMPLEMENTATION CHECKLIST

### Pre-Implementation
- [ ] Create Procore developer account
- [ ] Register application (get client ID/secret)
- [ ] Set up OAuth redirect URI
- [ ] Determine sync frequency requirements
- [ ] Map data fields (Procore ← → Trajanus)
- [ ] Identify webhook events needed

### Development
- [ ] Implement OAuth 2.0 flow
- [ ] Build middleware API layer
- [ ] Create database schema
- [ ] Develop sync logic (pull/push)
- [ ] Implement webhook receiver
- [ ] Build error handling/retry
- [ ] Add rate limit management

### Testing
- [ ] Test authentication flow
- [ ] Validate data mapping
- [ ] Test webhook processing
- [ ] Error scenario testing
- [ ] Rate limit testing
- [ ] Load testing
- [ ] UAT with sample project

### Deployment
- [ ] Deploy to staging
- [ ] Connect to Procore sandbox
- [ ] Pilot with test project
- [ ] Monitor for 2 weeks
- [ ] Production deployment
- [ ] User training

---

## BEST PRACTICES

### Security
- Store credentials in environment variables
- Use HTTPS for all communications
- Implement OAuth token rotation
- Log all API calls (audit trail)
- Validate webhook signatures

### Performance
- Cache frequently accessed data
- Batch API calls when possible
- Use webhooks > polling
- Implement request queuing
- Monitor API usage

### Data Quality
- Validate before API calls
- Handle partial failures
- Reconcile regularly
- Maintain sync logs
- Alert on sync failures

---

## COST CONSIDERATIONS

**Procore Pricing:**
- Project-based licensing
- Additional modules extra cost
- API access included
- No per-call fees

**Development Costs:**
- Initial integration: 150-300 hours
- Testing: 60-100 hours
- Documentation: 30-50 hours

---

## SUPPORT RESOURCES

**Official:**
- Developer Portal: https://developers.procore.com
- API Reference: https://developers.procore.com/reference
- Support: support@procore.com

**Community:**
- Developer Forum
- Procore University
- Partner Marketplace

---

**END OF DOCUMENT**

**Next Steps:** Proceed to RMS 3.0 integration guide for USACE compliance integration.
