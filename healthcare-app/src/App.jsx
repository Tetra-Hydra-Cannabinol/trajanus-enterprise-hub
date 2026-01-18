import { useState } from 'react'
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

function App() {
    const [activeTab, setActiveTab] = useState('app') // app, progress, feedback
    const [currentStep, setCurrentStep] = useState('upload') // upload, processing, complete
    const [patientData, setPatientData] = useState(null)
    const [processingStatus, setProcessingStatus] = useState([])
    const [summaryData, setSummaryData] = useState(null)
    const [uploadedFiles, setUploadedFiles] = useState([])

    const handleFileUpload = (files) => {
        setUploadedFiles(prev => [...prev, ...files])
    }

    const handlePatientSubmit = (data) => {
        setPatientData(data)
        startProcessing()
    }

    const startProcessing = () => {
        setCurrentStep('processing')

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
                        generateSummary()
                    }, 1500)
                }
            }, (index + 1) * 2000)
        })
    }

    const generateSummary = () => {
        setSummaryData({
            patientName: patientData?.firstName + ' ' + patientData?.lastName || 'John Doe',
            dateOfBirth: patientData?.dob || '1985-03-15',
            mrn: 'MRN-' + Math.random().toString(36).substr(2, 9).toUpperCase(),
            visitDate: new Date().toISOString().split('T')[0],
            chiefComplaint: 'Routine pediatric checkup',
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
            documentsProcessed: uploadedFiles.length
        })
        setCurrentStep('complete')
    }

    const resetWorkflow = () => {
        setCurrentStep('upload')
        setPatientData(null)
        setProcessingStatus([])
        setSummaryData(null)
        setUploadedFiles([])
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
            {activeTab === 'app' && <HIPAABanner />}

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
                                <AIProcessingStatus steps={processingStatus} />
                            )}
                            {currentStep === 'complete' && summaryData && (
                                <SummaryReport
                                    data={summaryData}
                                    onReset={resetWorkflow}
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
        </div>
    )
}

export default App
