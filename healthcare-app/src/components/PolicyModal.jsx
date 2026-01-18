/**
 * PolicyModal - HIPAA data handling policy display
 * HEALTHCARE-05: Data handling policy display
 */

function PolicyModal({ onClose }) {
    return (
        <div className="consent-modal-overlay">
            <div className="consent-modal policy-modal">
                <div className="consent-header">
                    <span className="consent-icon">📋</span>
                    <h2>Data Handling Policy</h2>
                </div>

                <div className="consent-content policy-content">
                    <section className="policy-section">
                        <h3>1. Data Processing</h3>
                        <p>
                            All medical records are processed entirely within your web browser
                            using client-side JavaScript. Text extraction occurs locally using
                            PDF.js library. No document data is transmitted to external servers
                            except for AI summarization via encrypted API calls.
                        </p>
                    </section>

                    <section className="policy-section">
                        <h3>2. AI Processing</h3>
                        <p>
                            Clinical summaries are generated using Claude AI (Anthropic). Data
                            is transmitted via TLS-encrypted HTTPS connections. Anthropic does
                            not store or train on healthcare data submitted through their API.
                        </p>
                    </section>

                    <section className="policy-section">
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

                    <section className="policy-section">
                        <h3>4. Encryption</h3>
                        <p>
                            All data transmission uses TLS 1.2+ encryption. API calls to AI
                            services are made over HTTPS only. No unencrypted data is ever transmitted.
                        </p>
                    </section>

                    <section className="policy-section">
                        <h3>5. Access Logging</h3>
                        <p>
                            Access to patient records is logged in-memory for audit purposes
                            during your session. These logs include timestamps, actions performed,
                            and anonymized user identifiers.
                        </p>
                    </section>

                    <section className="policy-section">
                        <h3>6. Your Responsibilities</h3>
                        <ul>
                            <li>Ensure you are authorized to access the medical records you upload</li>
                            <li>Do not share exported summaries with unauthorized parties</li>
                            <li>Close your browser when finished to clear all session data</li>
                            <li>Report any suspected security incidents immediately</li>
                        </ul>
                    </section>
                </div>

                <div className="consent-actions">
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

export default PolicyModal
