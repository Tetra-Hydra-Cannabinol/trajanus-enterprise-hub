function SummaryReport({ data, onReset, onExport }) {
    const handleExport = (format) => {
        if (onExport) {
            onExport(format)
        } else {
            alert(`Exporting report as ${format.toUpperCase()}...`)
        }
    }

    const handlePrint = () => {
        window.print()
    }

    // Determine if this is an AI-generated summary
    const isAISummary = data.isAI || data.aiSummary

    return (
        <div className="card summary-card">
            <div className="card-header">
                <h2>Clinical Summary Report</h2>
                <span className="status-badge success">Complete</span>
            </div>

            <div className="summary-content">
                {/* Patient Demographics */}
                <section className="summary-section">
                    <h3>Patient Demographics</h3>
                    <div className="summary-grid">
                        <div className="summary-item">
                            <label>Patient Name</label>
                            <span>{data.patientName}</span>
                        </div>
                        <div className="summary-item">
                            <label>Date of Birth</label>
                            <span>{data.dateOfBirth}</span>
                        </div>
                        <div className="summary-item">
                            <label>Medical Record #</label>
                            <span>{data.mrn}</span>
                        </div>
                        <div className="summary-item">
                            <label>Visit Date</label>
                            <span>{data.visitDate}</span>
                        </div>
                    </div>
                </section>

                {/* Chief Complaint */}
                <section className="summary-section">
                    <h3>Chief Complaint</h3>
                    <p>{data.chiefComplaint}</p>
                </section>

                {/* AI Summary - shown for real AI processing */}
                {isAISummary && data.aiSummary && (
                    <section className="summary-section ai-summary">
                        <h3>
                            <span className="ai-badge">🤖 AI</span>
                            Clinical Summary
                        </h3>
                        <div className="ai-summary-content">
                            {data.aiSummary.split('\n').map((paragraph, idx) => (
                                <p key={idx}>{paragraph}</p>
                            ))}
                        </div>
                    </section>
                )}

                {/* Vitals - shown for demo mode */}
                {!isAISummary && data.vitals && (
                    <section className="summary-section">
                        <h3>Vital Signs</h3>
                        <div className="vitals-grid">
                            {Object.entries(data.vitals).map(([key, value]) => (
                                <div key={key} className="vital-item">
                                    <span className="vital-label">
                                        {key.replace(/([A-Z])/g, ' $1').trim()}
                                    </span>
                                    <span className="vital-value">{value}</span>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {/* Assessment - shown for demo mode */}
                {!isAISummary && data.assessment && (
                    <section className="summary-section">
                        <h3>Assessment</h3>
                        <p>{data.assessment}</p>
                    </section>
                )}

                {/* Plan - shown for demo mode */}
                {!isAISummary && data.plan && (
                    <section className="summary-section">
                        <h3>Plan</h3>
                        <ul className="plan-list">
                            {data.plan.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </section>
                )}

                {/* Documents Processed */}
                <section className="summary-section summary-meta">
                    <div className="meta-item">
                        <span className="meta-icon">📄</span>
                        <span>{data.documentsProcessed} document(s) processed</span>
                    </div>
                    <div className="meta-item">
                        <span className="meta-icon">🤖</span>
                        <span>{isAISummary ? 'AI-generated summary (Claude)' : 'Demo summary'}</span>
                    </div>
                    <div className="meta-item">
                        <span className="meta-icon">✓</span>
                        <span>HIPAA compliant processing</span>
                    </div>
                    {data.generatedAt && (
                        <div className="meta-item">
                            <span className="meta-icon">🕐</span>
                            <span>Generated: {new Date(data.generatedAt).toLocaleString()}</span>
                        </div>
                    )}
                </section>
            </div>

            {/* Actions */}
            <div className="summary-actions">
                <div className="export-buttons">
                    <button
                        className="action-btn secondary"
                        onClick={() => handleExport('txt')}
                    >
                        📥 Export TXT
                    </button>
                    <button
                        className="action-btn secondary"
                        onClick={() => handleExport('html')}
                    >
                        📄 Export HTML
                    </button>
                    <button
                        className="action-btn secondary"
                        onClick={handlePrint}
                    >
                        🖨️ Print
                    </button>
                </div>
                <button
                    className="action-btn primary"
                    onClick={onReset}
                >
                    ➕ Process New Records
                </button>
            </div>
        </div>
    )
}

export default SummaryReport
