# Trajanus KB MCP Server - HTTP Deployment Guide

## WHAT THIS SOLVES
Allows web chat (claude.ai) to access your Supabase knowledge base via HTTP MCP protocol.

## ARCHITECTURE
```
Web Chat (claude.ai) → HTTP MCP Server (your machine/cloud) → Supabase → Knowledge Base
```

## DEPLOYMENT OPTIONS

### Option 1: Run on Your Local Machine (RECOMMENDED FOR TESTING)

**Step 1: Copy files to Scripts folder**
```powershell
# Navigate to Scripts folder
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts"

# Files should be here:
# - kb_mcp_server_http.py
# - requirements_http_mcp.txt
# - .env (with credentials)
```

**Step 2: Install dependencies**
```powershell
pip install -r requirements_http_mcp.txt --break-system-packages
```

**Step 3: Create/verify .env file**
```env
OPENAI_API_KEY=your_openai_key_here
SUPABASE_URL=https://iaxtwrswinygwwwdkvok.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
PORT=5000
```

**Step 4: Start the server**
```powershell
python kb_mcp_server_http.py
```

**Expected output:**
```
Starting Trajanus KB MCP Server on port 5000
SSE endpoint: http://localhost:5000/sse
Message endpoint: http://localhost:5000/message
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

**Step 5: Test it works**
Open new PowerShell window:
```powershell
# Test health check
curl http://localhost:5000/health

# Should return: {"status":"healthy","server":"trajanus-kb-http"}
```

**Step 6: Expose to internet (for web chat access)**

Option A: Use ngrok (easiest)
```powershell
# Install ngrok: https://ngrok.com/download
ngrok http 5000

# You'll get a URL like: https://abc123.ngrok.io
# This is your MCP server URL for web chat
```

Option B: Use CloudFlare Tunnel
```powershell
cloudflared tunnel --url http://localhost:5000
```

Option C: Configure port forwarding on your router (advanced)

**Step 7: Connect web chat to MCP server**

Currently, web chat MCP connection requires Anthropic support. The architecture is ready, but connection method depends on their implementation.

**For now, use Claude Code CLI which works perfectly:**
```powershell
# Already configured:
claude mcp add --scope user trajanus-kb python "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\kb_mcp_server.py"
```

---

### Option 2: Deploy to Cloud (PRODUCTION)

**Cloud Platforms:**
- AWS EC2 / Lambda
- Google Cloud Run
- Azure App Service
- Railway
- Heroku

**Example: Railway Deployment**
1. Create Railway account
2. Connect GitHub repo
3. Add environment variables
4. Deploy automatically
5. Get public URL: https://trajanus-kb.railway.app

**Example: AWS EC2**
```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance

# Install Python 3
sudo yum install python3 -y

# Clone/upload files
cd /opt
sudo mkdir trajanus-kb
cd trajanus-kb

# Copy files and install deps
sudo pip3 install -r requirements_http_mcp.txt

# Create systemd service
sudo nano /etc/systemd/system/trajanus-kb.service

# Service file content:
[Unit]
Description=Trajanus KB MCP Server
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/trajanus-kb
Environment="PATH=/usr/local/bin:/usr/bin"
ExecStart=/usr/bin/python3 kb_mcp_server_http.py
Restart=always

[Install]
WantedBy=multi-user.target

# Start service
sudo systemctl daemon-reload
sudo systemctl start trajanus-kb
sudo systemctl enable trajanus-kb

# Configure nginx reverse proxy with SSL
```

---

## TESTING THE SERVER

**Test 1: Health Check**
```bash
curl http://localhost:5000/health
# Expected: {"status":"healthy","server":"trajanus-kb-http"}
```

**Test 2: Tools List**
```bash
curl -X POST http://localhost:5000/message \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

**Test 3: Search Query**
```bash
curl -X POST http://localhost:5000/message \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "search_knowledge_base",
      "arguments": {
        "query": "December 9 accomplishments",
        "max_results": 3
      }
    }
  }'
```

---

## SECURITY CONSIDERATIONS

**For Local Development:**
- ✅ Runs on localhost only
- ✅ Not exposed to internet by default
- ✅ API keys in .env file (don't commit!)

**For Production:**
- 🔒 Use HTTPS (SSL certificate)
- 🔒 Add authentication (API key header)
- 🔒 Rate limiting
- 🔒 IP whitelist (if needed)
- 🔒 Monitor logs
- 🔒 Keep dependencies updated

---

## CONNECTING WEB CHAT (FUTURE)

Once Anthropic enables HTTP MCP for web chat:

```json
// In Claude settings (hypothetical)
{
  "mcpServers": {
    "trajanus-kb": {
      "transport": "sse",
      "url": "https://your-server-url/sse"
    }
  }
}
```

**Current Status:**
- ✅ CLI: Works perfectly (stdio transport)
- ⏳ Web: Architecture ready, awaiting Anthropic support
- 🎯 Hub: Will embed directly (no MCP needed)

---

## IMMEDIATE NEXT STEPS

1. **Test locally first**
   ```powershell
   cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts"
   python kb_mcp_server_http.py
   ```

2. **Verify health endpoint**
   ```powershell
   curl http://localhost:5000/health
   ```

3. **Test search with curl** (see Test 3 above)

4. **If needed for web access:**
   - Install ngrok
   - Run: `ngrok http 5000`
   - Get public URL

5. **Document public URL** in your protocols

---

## TROUBLESHOOTING

**Port already in use:**
```powershell
# Change PORT in .env to 5001 or 8000
```

**Module not found:**
```powershell
pip install -r requirements_http_mcp.txt --break-system-packages
```

**Connection refused:**
```powershell
# Check firewall
# Verify server is running: netstat -ano | findstr 5000
```

**Supabase errors:**
```powershell
# Verify .env credentials
# Test Supabase connection separately
```

---

## FILES CREATED

1. `kb_mcp_server_http.py` - HTTP/SSE server
2. `requirements_http_mcp.txt` - Dependencies
3. `DEPLOYMENT_GUIDE.md` - This file
4. `.env` - Credentials (create if missing)

---

**READY TO DEPLOY. START WITH LOCAL TESTING.**
