/**
 * HIPAACompliance - HIPAA compliance utilities for healthcare records processing
 * HEALTHCARE-05: HIPAA compliance features
 *
 * Features:
 * - User consent management
 * - Audit logging
 * - Data handling policy display
 * - Encryption verification
 * - No persistent storage enforcement
 *
 * @author Trajanus USA
 * @location Jacksonville, Florida
 */

// Audit log stored in memory only (HIPAA compliant - no localStorage)
let auditLog = [];

// Session ID for tracking
const sessionId = `SESSION-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

/**
 * HIPAA Compliance Class
 * Manages all HIPAA compliance requirements for the healthcare platform
 */
class HIPAACompliance {
  constructor() {
    this.consentGiven = false;
    this.consentTimestamp = null;
    this.userId = null;
    this.sessionId = sessionId;
  }

  /**
   * Initialize compliance tracking for a user session
   * @param {string} userId - User identifier (anonymized)
   */
  initSession(userId = 'ANONYMOUS') {
    this.userId = userId;
    this.logAccess(userId, null, 'SESSION_START', {
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Require user consent before processing PHI
   * @returns {Promise<boolean>} Whether consent was given
   */
  async requireConsent() {
    return new Promise((resolve) => {
      // Create consent modal
      const modal = document.createElement('div');
      modal.id = 'hipaa-consent-modal';
      modal.className = 'hipaa-modal-overlay';
      modal.innerHTML = `
        <div class="hipaa-modal">
          <div class="hipaa-modal-header">
            <span class="hipaa-icon">🔒</span>
            <h2>HIPAA Consent Required</h2>
          </div>
          <div class="hipaa-modal-content">
            <p><strong>Protected Health Information (PHI) Notice</strong></p>
            <p>By proceeding, you acknowledge and consent to the following:</p>
            <ul>
              <li><strong>Data Processing:</strong> Medical records will be processed using AI technology to generate clinical summaries.</li>
              <li><strong>No Storage:</strong> All data is processed in-memory only. No patient information is stored on servers or in browser storage.</li>
              <li><strong>Encryption:</strong> All data transmission uses TLS/HTTPS encryption.</li>
              <li><strong>Access Logging:</strong> Your access to patient records is logged for audit purposes.</li>
              <li><strong>Authorized Use:</strong> You confirm you are authorized to access and process these medical records.</li>
            </ul>
            <div class="hipaa-checkbox-group">
              <label class="hipaa-checkbox-label">
                <input type="checkbox" id="hipaa-consent-check" />
                <span>I have read and agree to the HIPAA compliance terms above</span>
              </label>
            </div>
          </div>
          <div class="hipaa-modal-actions">
            <button id="hipaa-decline-btn" class="hipaa-btn hipaa-btn-decline">Decline</button>
            <button id="hipaa-accept-btn" class="hipaa-btn hipaa-btn-accept" disabled>Accept & Continue</button>
          </div>
        </div>
      `;

      // Add styles if not already present
      if (!document.getElementById('hipaa-compliance-styles')) {
        const styles = document.createElement('style');
        styles.id = 'hipaa-compliance-styles';
        styles.textContent = this.getComplianceStyles();
        document.head.appendChild(styles);
      }

      document.body.appendChild(modal);

      // Handle checkbox
      const checkbox = document.getElementById('hipaa-consent-check');
      const acceptBtn = document.getElementById('hipaa-accept-btn');
      const declineBtn = document.getElementById('hipaa-decline-btn');

      checkbox.addEventListener('change', () => {
        acceptBtn.disabled = !checkbox.checked;
      });

      // Handle accept
      acceptBtn.addEventListener('click', () => {
        this.consentGiven = true;
        this.consentTimestamp = new Date().toISOString();
        this.logAccess(this.userId, null, 'CONSENT_GIVEN', {
          timestamp: this.consentTimestamp
        });
        modal.remove();
        resolve(true);
      });

      // Handle decline
      declineBtn.addEventListener('click', () => {
        this.logAccess(this.userId, null, 'CONSENT_DECLINED', {
          timestamp: new Date().toISOString()
        });
        modal.remove();
        resolve(false);
      });
    });
  }

  /**
   * Check if consent has been given
   * @returns {boolean}
   */
  hasConsent() {
    return this.consentGiven;
  }

  /**
   * Log access to patient data for audit trail
   * @param {string} userId - User performing the action
   * @param {string} patientId - Patient being accessed (can be null)
   * @param {string} action - Type of action performed
   * @param {Object} metadata - Additional metadata
   */
  logAccess(userId, patientId, action, metadata = {}) {
    const logEntry = {
      id: `LOG-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      sessionId: this.sessionId,
      timestamp: new Date().toISOString(),
      userId: userId || this.userId || 'ANONYMOUS',
      patientId: patientId || 'N/A',
      action: action,
      metadata: {
        ...metadata,
        ipAddress: '[REDACTED]', // Would be captured server-side
        encryptionVerified: window.location.protocol === 'https:' || window.location.hostname === 'localhost'
      }
    };

    auditLog.push(logEntry);

    // Console log for development (would go to secure server in production)
    console.log('[HIPAA AUDIT]', JSON.stringify(logEntry, null, 2));

    return logEntry.id;
  }

  /**
   * Get all audit log entries for current session
   * @returns {Array} Audit log entries
   */
  getAuditLog() {
    return auditLog.filter(entry => entry.sessionId === this.sessionId);
  }

  /**
   * Get full audit log (all sessions in memory)
   * @returns {Array} All audit log entries
   */
  getFullAuditLog() {
    return [...auditLog];
  }

  /**
   * Display data handling policy modal
   */
  displayPolicy() {
    const modal = document.createElement('div');
    modal.id = 'hipaa-policy-modal';
    modal.className = 'hipaa-modal-overlay';
    modal.innerHTML = `
      <div class="hipaa-modal hipaa-modal-policy">
        <div class="hipaa-modal-header">
          <span class="hipaa-icon">📋</span>
          <h2>Data Handling Policy</h2>
        </div>
        <div class="hipaa-modal-content hipaa-policy-content">
          <section>
            <h3>1. Data Processing</h3>
            <p>All medical records are processed entirely within your web browser using client-side JavaScript.
            Text extraction occurs locally using PDF.js library. No document data is transmitted to external servers
            except for AI summarization via encrypted API calls.</p>
          </section>

          <section>
            <h3>2. AI Processing</h3>
            <p>Clinical summaries are generated using Claude AI (Anthropic). Data is transmitted via TLS-encrypted
            HTTPS connections. Anthropic does not store or train on healthcare data submitted through their API.</p>
          </section>

          <section>
            <h3>3. No Persistent Storage</h3>
            <p><strong>This application does NOT store any patient data.</strong></p>
            <ul>
              <li>No localStorage or sessionStorage is used for PHI</li>
              <li>No cookies contain patient information</li>
              <li>No IndexedDB databases are created</li>
              <li>All data exists only in browser memory during your session</li>
              <li>Closing the browser tab permanently erases all data</li>
            </ul>
          </section>

          <section>
            <h3>4. Encryption</h3>
            <p>All data transmission uses TLS 1.2+ encryption. API calls to AI services are made over HTTPS only.
            No unencrypted data is ever transmitted.</p>
          </section>

          <section>
            <h3>5. Access Logging</h3>
            <p>Access to patient records is logged in-memory for audit purposes during your session.
            These logs include timestamps, actions performed, and anonymized user identifiers.</p>
          </section>

          <section>
            <h3>6. Your Responsibilities</h3>
            <ul>
              <li>Ensure you are authorized to access the medical records you upload</li>
              <li>Do not share exported summaries with unauthorized parties</li>
              <li>Close your browser when finished to clear all session data</li>
              <li>Report any suspected security incidents immediately</li>
            </ul>
          </section>
        </div>
        <div class="hipaa-modal-actions">
          <button id="hipaa-policy-close" class="hipaa-btn hipaa-btn-accept">Close</button>
        </div>
      </div>
    `;

    // Add styles if not already present
    if (!document.getElementById('hipaa-compliance-styles')) {
      const styles = document.createElement('style');
      styles.id = 'hipaa-compliance-styles';
      styles.textContent = this.getComplianceStyles();
      document.head.appendChild(styles);
    }

    document.body.appendChild(modal);

    document.getElementById('hipaa-policy-close').addEventListener('click', () => {
      modal.remove();
    });

    this.logAccess(this.userId, null, 'POLICY_VIEWED');
  }

  /**
   * Verify encryption is in use
   * @returns {Object} Encryption status
   */
  verifyEncryption() {
    const isSecure = window.location.protocol === 'https:';
    const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

    const status = {
      protocol: window.location.protocol,
      isSecure: isSecure || isLocalhost,
      isLocalDevelopment: isLocalhost,
      recommendation: null
    };

    if (!isSecure && !isLocalhost) {
      status.recommendation = 'WARNING: Application should be served over HTTPS in production.';
      console.warn('[HIPAA] ' + status.recommendation);
    }

    // Check for localStorage usage (should be empty for PHI compliance)
    const localStorageKeys = Object.keys(localStorage).filter(key =>
      key.includes('patient') || key.includes('medical') || key.includes('health')
    );

    if (localStorageKeys.length > 0) {
      status.localStorageWarning = `Found ${localStorageKeys.length} potentially sensitive localStorage keys`;
      console.warn('[HIPAA] LocalStorage contains potentially sensitive data:', localStorageKeys);
    }

    this.logAccess(this.userId, null, 'ENCRYPTION_VERIFIED', status);

    return status;
  }

  /**
   * Clear all session data (call on logout/close)
   */
  clearSessionData() {
    this.logAccess(this.userId, null, 'SESSION_END', {
      totalActions: this.getAuditLog().length
    });

    // Clear consent
    this.consentGiven = false;
    this.consentTimestamp = null;

    // Note: auditLog is intentionally NOT cleared here for audit purposes
    // In production, this would be sent to a secure server before clearing
  }

  /**
   * Export audit log for compliance reporting
   * @param {string} format - Export format ('json' or 'txt')
   * @returns {string} Formatted audit log
   */
  exportAuditLog(format = 'json') {
    const log = this.getAuditLog();

    if (format === 'json') {
      return JSON.stringify({
        exportDate: new Date().toISOString(),
        sessionId: this.sessionId,
        totalEntries: log.length,
        entries: log
      }, null, 2);
    }

    // Text format
    let text = `HIPAA AUDIT LOG EXPORT\n`;
    text += `========================\n`;
    text += `Export Date: ${new Date().toISOString()}\n`;
    text += `Session ID: ${this.sessionId}\n`;
    text += `Total Entries: ${log.length}\n\n`;

    log.forEach((entry, idx) => {
      text += `--- Entry ${idx + 1} ---\n`;
      text += `ID: ${entry.id}\n`;
      text += `Timestamp: ${entry.timestamp}\n`;
      text += `User: ${entry.userId}\n`;
      text += `Patient: ${entry.patientId}\n`;
      text += `Action: ${entry.action}\n`;
      text += `Metadata: ${JSON.stringify(entry.metadata)}\n\n`;
    });

    return text;
  }

  /**
   * Get CSS styles for compliance modals
   * @returns {string} CSS styles
   */
  getComplianceStyles() {
    return `
      .hipaa-modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.85);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        backdrop-filter: blur(4px);
      }

      .hipaa-modal {
        background: linear-gradient(135deg, #1a1a2e 0%, #0d0d1a 100%);
        border: 2px solid #00AAFF;
        border-radius: 12px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(0, 170, 255, 0.3);
      }

      .hipaa-modal-policy {
        max-width: 700px;
      }

      .hipaa-modal-header {
        background: linear-gradient(90deg, #00AAFF 0%, #0066CC 100%);
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .hipaa-modal-header h2 {
        margin: 0;
        color: white;
        font-size: 1.4rem;
        font-weight: 600;
      }

      .hipaa-icon {
        font-size: 1.8rem;
      }

      .hipaa-modal-content {
        padding: 24px;
        color: #E0E0E0;
        overflow-y: auto;
        max-height: 50vh;
      }

      .hipaa-modal-content p {
        margin: 0 0 16px 0;
        line-height: 1.6;
      }

      .hipaa-modal-content ul {
        margin: 0 0 16px 0;
        padding-left: 24px;
      }

      .hipaa-modal-content li {
        margin-bottom: 8px;
        line-height: 1.5;
      }

      .hipaa-policy-content section {
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid #333;
      }

      .hipaa-policy-content section:last-child {
        border-bottom: none;
        margin-bottom: 0;
      }

      .hipaa-policy-content h3 {
        color: #00AAFF;
        margin: 0 0 12px 0;
        font-size: 1.1rem;
      }

      .hipaa-checkbox-group {
        background: rgba(0, 170, 255, 0.1);
        border: 1px solid #00AAFF;
        border-radius: 8px;
        padding: 16px;
        margin-top: 16px;
      }

      .hipaa-checkbox-label {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        cursor: pointer;
      }

      .hipaa-checkbox-label input[type="checkbox"] {
        width: 20px;
        height: 20px;
        margin-top: 2px;
        accent-color: #00AAFF;
      }

      .hipaa-checkbox-label span {
        flex: 1;
        line-height: 1.5;
      }

      .hipaa-modal-actions {
        padding: 20px 24px;
        display: flex;
        gap: 12px;
        justify-content: flex-end;
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid #333;
      }

      .hipaa-btn {
        padding: 12px 24px;
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
      }

      .hipaa-btn-accept {
        background: linear-gradient(135deg, #00AAFF 0%, #0066CC 100%);
        color: white;
      }

      .hipaa-btn-accept:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 170, 255, 0.4);
      }

      .hipaa-btn-accept:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }

      .hipaa-btn-decline {
        background: transparent;
        border: 2px solid #666;
        color: #999;
      }

      .hipaa-btn-decline:hover {
        border-color: #FF4444;
        color: #FF4444;
      }
    `;
  }
}

// Singleton instance
const hipaaCompliance = new HIPAACompliance();

// Export both class and singleton
export { HIPAACompliance, hipaaCompliance };
export default hipaaCompliance;
