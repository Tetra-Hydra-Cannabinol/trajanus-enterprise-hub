import { useState } from 'react'

function PatientForm({ onSubmit, disabled }) {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        dob: '',
        mrn: '',
        insurance: '',
        visitReason: ''
    })

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        if (!disabled) {
            onSubmit(formData)
        }
    }

    const isFormValid = formData.firstName && formData.lastName && formData.dob

    return (
        <div className={`card patient-form-card ${disabled ? 'disabled' : ''}`}>
            <div className="card-header">
                <h2>Patient Information</h2>
                <span className="card-badge">Required</span>
            </div>
            <form className="patient-form" onSubmit={handleSubmit}>
                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="firstName">First Name *</label>
                        <input
                            type="text"
                            id="firstName"
                            name="firstName"
                            value={formData.firstName}
                            onChange={handleChange}
                            disabled={disabled}
                            placeholder="Enter first name"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="lastName">Last Name *</label>
                        <input
                            type="text"
                            id="lastName"
                            name="lastName"
                            value={formData.lastName}
                            onChange={handleChange}
                            disabled={disabled}
                            placeholder="Enter last name"
                            required
                        />
                    </div>
                </div>
                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="dob">Date of Birth *</label>
                        <input
                            type="date"
                            id="dob"
                            name="dob"
                            value={formData.dob}
                            onChange={handleChange}
                            disabled={disabled}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="mrn">Medical Record # (Optional)</label>
                        <input
                            type="text"
                            id="mrn"
                            name="mrn"
                            value={formData.mrn}
                            onChange={handleChange}
                            disabled={disabled}
                            placeholder="If known"
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label htmlFor="insurance">Insurance Provider (Optional)</label>
                    <input
                        type="text"
                        id="insurance"
                        name="insurance"
                        value={formData.insurance}
                        onChange={handleChange}
                        disabled={disabled}
                        placeholder="Enter insurance provider"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="visitReason">Reason for Visit</label>
                    <textarea
                        id="visitReason"
                        name="visitReason"
                        value={formData.visitReason}
                        onChange={handleChange}
                        disabled={disabled}
                        placeholder="Brief description of visit reason"
                        rows={3}
                    />
                </div>
                <button
                    type="submit"
                    className="submit-btn"
                    disabled={disabled || !isFormValid}
                >
                    <span className="btn-icon">🚀</span>
                    Process Records
                </button>
            </form>
        </div>
    )
}

export default PatientForm
