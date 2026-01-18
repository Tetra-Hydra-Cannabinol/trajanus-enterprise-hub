function SummaryReport({ data, onReset }) {
    const handleExport = (format) => {
        // In a real app, this would generate and download the file
        alert(`Exporting report as ${format.toUpperCase()}...`)
    }

    const handlePrint = () => {
        window.print()
    }

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

                {/* Vitals */}
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

                {/* Assessment */}
                <section className="summary-section">
                    <h3>Assessment</h3>
                    <p>{data.assessment}</p>
                </section>

                {/* Plan */}
                <section className="summary-section">
                    <h3>Plan</h3>
                    <ul className="plan-list">
                        {data.plan.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </section>

                {/* Documents Processed */}
                <section className="summary-section summary-meta">
                    <div className="meta-item">
                        <span className="meta-icon">📄</span>
                        <span>{data.documentsProcessed} document(s) processed</span>
                    </div>
                    <div className="meta-item">
                        <span className="meta-icon">🤖</span>
                        <span>AI-generated summary</span>
                    </div>
                    <div className="meta-item">
                        <span className="meta-icon">✓</span>
                        <span>HIPAA compliant processing</span>
                    </div>
                </section>
            </div>

            {/* Actions */}
            <div className="summary-actions">
                <div className="export-buttons">
                    <button
                        className="action-btn secondary"
                        onClick={() => handleExport('pdf')}
                    >
                        📥 Export PDF
                    </button>
                    <button
                        className="action-btn secondary"
                        onClick={() => handleExport('docx')}
                    >
                        📄 Export DOCX
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
