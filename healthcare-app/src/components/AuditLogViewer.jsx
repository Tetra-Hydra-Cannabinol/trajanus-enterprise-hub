/**
 * AuditLogViewer - Display HIPAA audit log
 * HEALTHCARE-05: Audit log display
 */

function AuditLogViewer({ auditLog, onClose, onExport }) {
    const formatTimestamp = (timestamp) => {
        return new Date(timestamp).toLocaleString()
    }

    const getActionBadgeClass = (action) => {
        switch (action) {
            case 'CONSENT_GIVEN':
                return 'badge-success'
            case 'CONSENT_DECLINED':
                return 'badge-error'
            case 'PATIENT_DATA_ACCESSED':
            case 'RECORD_PROCESSED':
                return 'badge-warning'
            case 'SUMMARY_EXPORTED':
                return 'badge-info'
            default:
                return 'badge-default'
        }
    }

    return (
        <div className="consent-modal-overlay">
            <div className="consent-modal audit-modal">
                <div className="consent-header">
                    <span className="consent-icon">📊</span>
                    <h2>HIPAA Audit Log</h2>
                </div>

                <div className="consent-content audit-content">
                    <div className="audit-summary">
                        <div className="audit-stat">
                            <span className="audit-stat-value">{auditLog.length}</span>
                            <span className="audit-stat-label">Total Actions</span>
                        </div>
                        <div className="audit-stat">
                            <span className="audit-stat-value">
                                {auditLog.filter(e => e.action.includes('PATIENT')).length}
                            </span>
                            <span className="audit-stat-label">Patient Access</span>
                        </div>
                        <div className="audit-stat">
                            <span className="audit-stat-value">
                                {auditLog.filter(e => e.action === 'SUMMARY_EXPORTED').length}
                            </span>
                            <span className="audit-stat-label">Exports</span>
                        </div>
                    </div>

                    <div className="audit-log-list">
                        {auditLog.length === 0 ? (
                            <div className="audit-empty">
                                <span>📝</span>
                                <p>No audit log entries yet</p>
                            </div>
                        ) : (
                            auditLog.map((entry, idx) => (
                                <div key={entry.id || idx} className="audit-entry">
                                    <div className="audit-entry-header">
                                        <span className={`audit-action-badge ${getActionBadgeClass(entry.action)}`}>
                                            {entry.action}
                                        </span>
                                        <span className="audit-timestamp">
                                            {formatTimestamp(entry.timestamp)}
                                        </span>
                                    </div>
                                    <div className="audit-entry-details">
                                        <span className="audit-detail">
                                            <strong>User:</strong> {entry.userId}
                                        </span>
                                        {entry.patientId && entry.patientId !== 'N/A' && (
                                            <span className="audit-detail">
                                                <strong>Patient:</strong> {entry.patientId}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

                <div className="consent-actions">
                    <button
                        className="consent-btn consent-btn-decline"
                        onClick={() => onExport('txt')}
                    >
                        📥 Export Log
                    </button>
                    <button
                        className="consent-btn consent-btn-accept"
                        onClick={onClose}
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    )
}

export default AuditLogViewer
