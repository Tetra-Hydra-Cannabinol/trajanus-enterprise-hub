function AIProcessingStatus({ steps }) {
    const completedSteps = steps.filter(s => s.status === 'complete').length
    const progress = (completedSteps / steps.length) * 100

    return (
        <div className="card processing-card">
            <div className="card-header">
                <h2>AI Processing</h2>
                <span className="progress-badge">{Math.round(progress)}%</span>
            </div>

            <div className="progress-bar-container">
                <div
                    className="progress-bar-fill"
                    style={{ width: `${progress}%` }}
                />
            </div>

            <div className="processing-steps">
                {steps.map((step) => (
                    <div
                        key={step.id}
                        className={`processing-step ${step.status}`}
                    >
                        <div className="step-indicator">
                            {step.status === 'complete' && '✓'}
                            {step.status === 'active' && (
                                <span className="spinner"></span>
                            )}
                            {step.status === 'pending' && step.id}
                        </div>
                        <div className="step-content">
                            <span className="step-label">{step.label}</span>
                            <span className="step-status">
                                {step.status === 'complete' && 'Complete'}
                                {step.status === 'active' && 'In Progress...'}
                                {step.status === 'pending' && 'Pending'}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="processing-footer">
                <span className="processing-info">
                    <span className="info-icon">ℹ️</span>
                    Processing typically takes 30-60 seconds depending on document complexity.
                </span>
            </div>
        </div>
    )
}

export default AIProcessingStatus
