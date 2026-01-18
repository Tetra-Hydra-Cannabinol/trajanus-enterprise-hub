import { useState } from 'react'

function HIPAABanner() {
    const [dismissed, setDismissed] = useState(false)

    if (dismissed) return null

    return (
        <div className="hipaa-banner">
            <div className="hipaa-content">
                <span className="hipaa-icon">🔒</span>
                <div className="hipaa-text">
                    <strong>HIPAA Compliance Notice:</strong> This system processes Protected Health Information (PHI)
                    in accordance with HIPAA regulations. All data is encrypted in transit and at rest.
                    Access is logged and audited.
                </div>
                <button
                    className="hipaa-dismiss"
                    onClick={() => setDismissed(true)}
                    title="Dismiss notice"
                >
                    ✕
                </button>
            </div>
        </div>
    )
}

export default HIPAABanner
