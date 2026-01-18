/**
 * ConsentModal - HIPAA consent modal component
 * HEALTHCARE-05: User consent notice
 */

import { useState } from 'react'

function ConsentModal({ onAccept, onDecline }) {
    const [agreed, setAgreed] = useState(false)

    return (
        <div className="consent-modal-overlay">
            <div className="consent-modal">
                <div className="consent-header">
                    <span className="consent-icon">🔒</span>
                    <h2>HIPAA Consent Required</h2>
                </div>

                <div className="consent-content">
                    <p className="consent-intro">
                        <strong>Protected Health Information (PHI) Notice</strong>
                    </p>
                    <p>By proceeding, you acknowledge and consent to the following:</p>

                    <ul className="consent-list">
                        <li>
                            <strong>Data Processing:</strong> Medical records will be processed
                            using AI technology to generate clinical summaries.
                        </li>
                        <li>
                            <strong>No Storage:</strong> All data is processed in-memory only.
                            No patient information is stored on servers or in browser storage.
                        </li>
                        <li>
                            <strong>Encryption:</strong> All data transmission uses TLS/HTTPS encryption.
                        </li>
                        <li>
                            <strong>Access Logging:</strong> Your access to patient records is
                            logged for audit purposes.
                        </li>
                        <li>
                            <strong>Authorized Use:</strong> You confirm you are authorized to
                            access and process these medical records.
                        </li>
                    </ul>

                    <div className="consent-checkbox-group">
                        <label className="consent-checkbox-label">
                            <input
                                type="checkbox"
                                checked={agreed}
                                onChange={(e) => setAgreed(e.target.checked)}
                            />
                            <span>I have read and agree to the HIPAA compliance terms above</span>
                        </label>
                    </div>
                </div>

                <div className="consent-actions">
                    <button
                        className="consent-btn consent-btn-decline"
                        onClick={onDecline}
                    >
                        Decline
                    </button>
                    <button
                        className="consent-btn consent-btn-accept"
                        disabled={!agreed}
                        onClick={onAccept}
                    >
                        Accept & Continue
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ConsentModal
