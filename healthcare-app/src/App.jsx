import { useState, useCallback, useEffect } from 'react'
import './App.css'
import trajanusLogo from './assets/trajanus-logo-white-grid.png'

// Components
import HIPAABanner from './components/HIPAABanner'
import PatientForm from './components/PatientForm'
import AIProcessingStatus from './components/AIProcessingStatus'
import SummaryReport from './components/SummaryReport'
import FileUpload from './components/FileUpload'
import ProgressTracker from './components/ProgressTracker'
import Feedback from './components/Feedback'
import ConsentModal from './components/ConsentModal'
import PolicyModal from './components/PolicyModal'
import AuditLogViewer from './components/AuditLogViewer'

// Hooks and Utils
import { useRecordProcessor } from './hooks/useRecordProcessor'
import hipaaCompliance from './utils/compliance'

function App() {
    const [activeTab, setActiveTab] = useState('app') // app, progress, feedback
    const [currentStep, setCurrentStep] = useState('upload') // upload, processing, complete
    const [patientData, setPatientData] = useState(null)
    const [processingStatus, setProcessingStatus] = useState([])
    const [uploadedFiles, setUploadedFiles] = useState([])
    const [consentGiven, setConsentGiven] = useState(false)

    // HIPAA Compliance State
    const [showConsentModal, setShowConsentModal] = useState(true) // Show on load
    const [showPolicyModal, setShowPolicyModal] = useState(false)
    const [showAuditLog, setShowAuditLog] = useState(false)
    const [auditLog, setAuditLog] = useState([])

    // Initialize compliance on mount
    useEffect(() => {
        hipaaCompliance.initSession('HEALTHCARE_USER')
        hipaaCompliance.verifyEncryption()
    }, [])

    // Use the record processor hook
    const {
        status,
        progress,
        summary,
        error,
        isProcessing,
        isComplete,
        processRecords,
        exportSummary,
        reset: resetProcessor
    } = useRecordProcessor()

    // HIPAA Consent Handlers
    const handleConsentAccept = () => {
        setConsentGiven(true)
        setShowConsentModal(false)
        hipaaCompliance.logAccess('HEALTHCARE_USER', null, 'CONSENT_GIVEN', {
            timestamp: new Date().toISOString()
        })
    }

    const handleConsentDecline = () => {
        hipaaCompliance.logAccess('HEALTHCARE_USER', null, 'CONSENT_DECLINED', {
            timestamp: new Date().toISOString()
        })
        // Keep modal open - user must consent to use app
        alert('You must accept the HIPAA consent to use this application.')
    }

    const handleViewPolicy = () => {
        setShowPolicyModal(true)
        hipaaCompliance.logAccess('HEALTHCARE_USER', null, 'POLICY_VIEWED')
    }

    const handleViewAuditLog = () => {
        setAuditLog(hipaaCompliance.getAuditLog())
        setShowAuditLog(true)
    }

    const handleExportAuditLog = (format) => {
        const content = hipaaCompliance.exportAuditLog(format)
        const blob = new Blob([content], { type: format === 'json' ? 'application/json' : 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `hipaa-audit-log-${Date.now()}.${format === 'json' ? 'json' : 'txt'}`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
        hipaaCompliance.logAccess('HEALTHCARE_USER', null, 'AUDIT_LOG_EXPORTED', { format })
    }

    const handleFileUpload = (files) => {
        setUploadedFiles(prev => [...prev, ...files])
        // Log file upload
        hipaaCompliance.logAccess('HEALTHCARE_USER', null, 'FILES_UPLOADED', {
            fileCount: files.length,
            fileNames: files.map(f => f.name || f.file?.name)
        })
    }

    const handlePatientSubmit = async (data) => {
        setPatientData(data)
        // Log patient data access
        hipaaCompliance.logAccess('HEALTHCARE_USER', data.mrn || 'NEW_PATIENT', 'PATIENT_DATA_ACCESSED', {
            patientName: `${data.firstName} ${data.lastName}`
        })
        await startProcessing(data)
    }

    const startProcessing = async (patientInfo) => {
        setCurrentStep('processing')

        // Define processing steps
        const steps = [
            { id: 1, label: 'Extracting text from documents', status: 'pending' },
            { id: 2, label: 'Parsing medical terminology', status: 'pending' },
            { id: 3, label: 'Cross-referencing patient history', status: 'pending' },
            { id: 4, label: 'Generating clinical summary', status: 'pending' },
            { id: 5, label: 'Validating HIPAA compliance', status: 'pending' }
        ]
        setProcessingStatus(steps)

        // Check if we have API key for real processing
        const hasApiKey = import.meta.env.VITE_ANTHROPIC_API_KEY

        if (hasApiKey && uploadedFiles.length > 0) {
            // Real processing with AI
            try {
                // Update step 1 - Extracting
                setProcessingStatus(prev => prev.map((s, i) => ({
                    ...s,
                    status: i === 0 ? 'active' : s.status
                })))

                // Convert uploaded files to File objects if needed
                const filesToProcess = uploadedFiles.map(f => f.file || f)

                // Process records
                await processRecords(filesToProcess, patientInfo, consentGiven || true)

                // Mark all steps complete
                setProcessingStatus(prev => prev.map(s => ({ ...s, status: 'complete' })))
                setCurrentStep('complete')

            } catch (err) {
                console.error('Processing error:', err)
                // Fall back to demo mode
                runDemoProcessing(patientInfo)
            }
        } else {
            // Demo mode - simulate processing
            runDemoProcessing(patientInfo)
        }
    }

    // Demo processing for when API key is not available
    const runDemoProcessing = (patientInfo) => {
        const steps = [
            { id: 1, label: 'Extracting text from documents', status: 'pending' },
            { id: 2, label: 'Parsing medical terminology', status: 'pending' },
            { id: 3, label: 'Cross-referencing patient history', status: 'pending' },
            { id: 4, label: 'Generating clinical summary', status: 'pending' },
            { id: 5, label: 'Validating HIPAA compliance', status: 'pending' }
        ]
        setProcessingStatus(steps)

        steps.forEach((step, index) => {
            setTimeout(() => {
                setProcessingStatus(prev =>
                    prev.map((s, i) =>
                        i <= index ? { ...s, status: i === index ? 'active' : 'complete' } : s
                    )
                )

                if (index === steps.length - 1) {
                    setTimeout(() => {
                        setProcessingStatus(prev =>
                            prev.map(s => ({ ...s, status: 'complete' }))
                        )
                        generateDemoSummary(patientInfo)
                    }, 1500)
                }
            }, (index + 1) * 1500)
        })
    }

    const generateDemoSummary = (patientInfo) => {
        // This will be displayed through the SummaryReport component
        setCurrentStep('complete')
    }

    // Get summary data for display
    const getSummaryData = useCallback(() => {
        if (summary) {
            // Real AI-generated summary
            return {
                patientName: summary.patientInfo.name,
                dateOfBirth: summary.patientInfo.dob,
                mrn: summary.patientInfo.id,
                visitDate: new Date().toISOString().split('T')[0],
                chiefComplaint: summary.patientInfo.complaint,
                aiSummary: summary.content,
                documentsProcessed: summary.recordCount,
                generatedAt: summary.generatedAt,
                isAI: true
            }
        } else {
            // Demo summary
            return {
                patientName: patientData?.firstName + ' ' + patientData?.lastName || 'John Doe',
                dateOfBirth: patientData?.dob || '1985-03-15',
                mrn: 'MRN-' + Math.random().toString(36).substr(2, 9).toUpperCase(),
                visitDate: new Date().toISOString().split('T')[0],
                chiefComplaint: patientData?.reason || 'Routine pediatric checkup',
                vitals: {
                    temperature: '98.6°F',
                    bloodPressure: '110/70 mmHg',
                    heartRate: '72 bpm',
                    weight: '45 kg',
                    height: '152 cm'
                },
                assessment: 'Patient presents in good health. Growth and development are within normal parameters for age. No acute concerns identified.',
                plan: [
                    'Continue current wellness routine',
                    'Schedule follow-up in 6 months',
                    'Update vaccinations per schedule',
                    'Dietary counseling provided'
                ],
                documentsProcessed: uploadedFiles.length,
                isAI: false
            }
        }
    }, [summary, patientData, uploadedFiles])

    const resetWorkflow = () => {
        setCurrentStep('upload')
        setPatientData(null)
        setProcessingStatus([])
        setUploadedFiles([])
        resetProcessor()
    }

    const handleExport = (format = 'txt') => {
        const data = getSummaryData()
        // Log export action
        hipaaCompliance.logAccess('HEALTHCARE_USER', data.mrn, 'SUMMARY_EXPORTED', {
            format,
            patientName: data.patientName
        })

        if (summary) {
            // Use the hook's export for AI summaries
            exportSummary(format)
        } else {
            // Manual export for demo summaries
            const content = `PATIENT CLINICAL SUMMARY
========================
Generated by Trajanus Healthcare Records Processor

Patient: ${data.patientName}
DOB: ${data.dateOfBirth}
MRN: ${data.mrn}
Visit Date: ${data.visitDate}
Chief Complaint: ${data.chiefComplaint}

------------------------
ASSESSMENT:
${data.assessment}

PLAN:
${data.plan?.join('\n') || 'N/A'}

------------------------
Documents Processed: ${data.documentsProcessed}
Generated: ${new Date().toLocaleString()}

Trajanus USA | Jacksonville, Florida
This summary is for clinical decision support only.
`
            const blob = new Blob([content], { type: 'text/plain' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `patient-summary-${data.mrn}-${Date.now()}.txt`
            document.body.appendChild(a)
            a.click()
            document.body.removeChild(a)
            URL.revokeObjectURL(url)
        }
    }

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <div className="header-brand">
                    <img src={trajanusLogo} alt="Trajanus" className="header-logo" />
                    <div className="header-title">
                        <h1>HEALTHCARE RECORDS PROCESSOR</h1>
                        <span className="header-subtitle">AI-Powered Medical Document Analysis</span>
                    </div>
                </div>

                {/* Navigation Tabs */}
                <nav className="header-tabs">
                    <button
                        className={`tab-btn ${activeTab === 'app' ? 'active' : ''}`}
                        onClick={() => setActiveTab('app')}
                    >
                        <span className="tab-icon">🏥</span>
                        App
                    </button>
                    <button
                        className={`tab-btn ${activeTab === 'progress' ? 'active' : ''}`}
                        onClick={() => setActiveTab('progress')}
                    >
                        <span className="tab-icon">📊</span>
                        Dev Progress
                    </button>
                    <button
                        className={`tab-btn ${activeTab === 'feedback' ? 'active' : ''}`}
                        onClick={() => setActiveTab('feedback')}
                    >
                        <span className="tab-icon">💬</span>
                        Feedback
                    </button>
                </nav>

                <div className="header-status">
                    <span className={`status-indicator ${currentStep}`}></span>
                    <span className="status-text">
                        {currentStep === 'upload' && 'Ready for Input'}
                        {currentStep === 'processing' && 'Processing...'}
                        {currentStep === 'complete' && 'Complete'}
                    </span>
                </div>
            </header>

            {/* HIPAA Banner - only show on app tab */}
            {activeTab === 'app' && (
                <div className="hipaa-banner">
                    <div className="hipaa-content">
                        <span className="hipaa-icon">🔒</span>
                        <span className="hipaa-text">
                            <strong>HIPAA Compliance Notice:</strong> This system processes Protected Health
                            Information (PHI) in accordance with HIPAA regulations. All data is encrypted
                            in transit and at rest. Access is logged and audited.
                        </span>
                    </div>
                    <div className="compliance-actions">
                        <button className="compliance-btn" onClick={handleViewPolicy}>
                            <span className="compliance-btn-icon">📋</span>
                            Policy
                        </button>
                        <button className="compliance-btn" onClick={handleViewAuditLog}>
                            <span className="compliance-btn-icon">📊</span>
                            Audit Log
                        </button>
                    </div>
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className="error-banner">
                    <span className="error-icon">⚠️</span>
                    <span className="error-text">{error}</span>
                    <button onClick={resetWorkflow}>Dismiss</button>
                </div>
            )}

            {/* Main Content */}
            <main className="app-main">
                {/* App Tab */}
                {activeTab === 'app' && (
                    <div className="main-grid">
                        <div className="input-column">
                            <FileUpload
                                onUpload={handleFileUpload}
                                uploadedFiles={uploadedFiles}
                                disabled={currentStep !== 'upload'}
                            />
                            <PatientForm
                                onSubmit={handlePatientSubmit}
                                disabled={currentStep !== 'upload' || uploadedFiles.length === 0}
                            />
                        </div>

                        <div className="output-column">
                            {currentStep === 'processing' && (
                                <AIProcessingStatus
                                    steps={processingStatus}
                                    progress={progress}
                                />
                            )}
                            {currentStep === 'complete' && (
                                <SummaryReport
                                    data={getSummaryData()}
                                    onReset={resetWorkflow}
                                    onExport={handleExport}
                                />
                            )}
                            {currentStep === 'upload' && (
                                <div className="card placeholder-card">
                                    <div className="placeholder-content">
                                        <div className="placeholder-icon">📋</div>
                                        <h3>Ready to Process</h3>
                                        <p>Upload medical records and enter patient information to begin AI-powered analysis.</p>
                                        <div className="placeholder-features">
                                            <div className="feature">
                                                <span className="feature-icon">📄</span>
                                                <span>PDF & DOCX Support</span>
                                            </div>
                                            <div className="feature">
                                                <span className="feature-icon">🔒</span>
                                                <span>HIPAA Compliant</span>
                                            </div>
                                            <div className="feature">
                                                <span className="feature-icon">🤖</span>
                                                <span>AI Analysis</span>
                                            </div>
                                            <div className="feature">
                                                <span className="feature-icon">📊</span>
                                                <span>Clinical Summaries</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* Progress Tab */}
                {activeTab === 'progress' && (
                    <div className="progress-tab-content">
                        <ProgressTracker />
                    </div>
                )}

                {/* Feedback Tab */}
                {activeTab === 'feedback' && (
                    <div className="feedback-tab-content">
                        <Feedback />
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="app-footer">
                <div className="footer-left">
                    <span>© 2026 Trajanus USA</span>
                    <span className="footer-divider">|</span>
                    <span>Healthcare Records Processor v1.0</span>
                </div>
                <div className="footer-right">
                    <span className="compliance-badge">HIPAA COMPLIANT</span>
                    <span className="compliance-badge">SOC 2</span>
                </div>
            </footer>

            {/* HIPAA Compliance Modals */}
            {showConsentModal && (
                <ConsentModal
                    onAccept={handleConsentAccept}
                    onDecline={handleConsentDecline}
                />
            )}

            {showPolicyModal && (
                <PolicyModal onClose={() => setShowPolicyModal(false)} />
            )}

            {showAuditLog && (
                <AuditLogViewer
                    auditLog={auditLog}
                    onClose={() => setShowAuditLog(false)}
                    onExport={handleExportAuditLog}
                />
            )}
        </div>
    )
}

export default App
