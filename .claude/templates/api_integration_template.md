# API Integration Template

## Integration Information
- **API Name:** [Name]
- **Type:** [REST/GraphQL/WebSocket]
- **Purpose:** [What this integration enables]
- **Workspace(s) Affected:** [List workspaces]

---

## API Details

### Endpoint Information
```
Base URL: [URL]
Authentication: [API Key/OAuth/None]
Rate Limits: [If applicable]
```

### Required Credentials
```
Environment Variable: [VAR_NAME]
Location: G:\My Drive\00 - Trajanus USA\00-Command-Center\.env
```

---

## Implementation Checklist

### Pre-Implementation
- [ ] API documentation reviewed
- [ ] Test API call in Postman/curl
- [ ] Verify credentials work
- [ ] Understand rate limits and quotas

### Backend (Tauri/Rust)
- [ ] Add Rust command in lib.rs (if needed)
- [ ] Handle authentication securely
- [ ] Implement error handling
- [ ] Add timeout handling

### Frontend (JavaScript)
- [ ] Create API wrapper function
- [ ] Handle loading states
- [ ] Handle error responses
- [ ] Implement browser fallback

---

## Code Pattern

### Tauri Invoke Pattern
```javascript
async function callApi(params) {
    const invoke = getInvoke();
    if (!invoke) {
        // Browser fallback
        showNotification('Requires desktop app', 'warning');
        return null;
    }

    try {
        Terminal.info('Calling API...');
        const result = await invoke('api_command', { ...params });
        Terminal.success('API call successful');
        return result;
    } catch (e) {
        Terminal.error(`API error: ${e}`);
        return null;
    }
}
```

### Direct API Pattern (Browser)
```javascript
async function callApiDirect(params) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    } catch (e) {
        console.error('API error:', e);
        return null;
    }
}
```

---

## Acceptance Criteria

### Functionality
```
[ ] API calls succeed with valid params
[ ] Errors handled gracefully
[ ] Loading states shown during calls
[ ] Results displayed correctly
```

### Security
```
[ ] Credentials not exposed in frontend
[ ] API keys in .env file only
[ ] HTTPS used for all calls
[ ] No sensitive data logged
```

### Performance
```
[ ] Timeout handling implemented
[ ] Rate limiting respected
[ ] Caching implemented (if appropriate)
```

### Fallback
```
[ ] Browser mode handled appropriately
[ ] Offline mode considered
[ ] Clear user messaging for failures
```

---

## Testing

### Manual Tests
- [ ] Success case with valid data
- [ ] Error case with invalid data
- [ ] Network timeout simulation
- [ ] Rate limit handling

### Edge Cases
- [ ] Empty response handling
- [ ] Large response handling
- [ ] Concurrent request handling

---

## Documentation

### Update Required
- [ ] Workspace .claude.md updated
- [ ] architecture.md updated (if major integration)
- [ ] .env.example updated with new vars

---

## Notes
[Authentication quirks, API limitations, decisions made]
