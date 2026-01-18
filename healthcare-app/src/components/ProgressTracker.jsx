import { useState, useEffect } from 'react'

const developmentChecklists = {
    'Core Features': {
        items: [
            {
                id: 'pdf-upload',
                label: 'PDF/DOCX Upload',
                instructions: 'Implement file upload with drag-and-drop support. Accept PDF and DOCX formats. Validate file types and sizes (max 10MB). Show upload progress indicator.',
                status: 'complete'
            },
            {
                id: 'text-extraction',
                label: 'Text Extraction Engine',
                instructions: 'Use pdf-parse for PDFs and mammoth for DOCX files. Extract all text content preserving structure. Handle multi-page documents and embedded tables.',
                status: 'in-progress'
            },
            {
                id: 'data-parser',
                label: 'Medical Data Parser',
                instructions: 'Parse extracted text to identify patient demographics, vitals, diagnoses, medications, and procedures. Use regex patterns and NLP for medical terminology.',
                status: 'pending'
            },
            {
                id: 'ai-summary',
                label: 'AI Summary Generator',
                instructions: 'Integrate Claude API for intelligent summarization. Create structured clinical summaries with chief complaint, assessment, and plan sections.',
                status: 'pending'
            }
        ]
    },
    'Integrations': {
        items: [
            {
                id: 'emr-connect',
                label: 'EMR Integration',
                instructions: 'Connect to Electronic Medical Records systems via HL7 FHIR API. Support read/write operations for patient records. Implement OAuth2 authentication.',
                status: 'pending'
            },
            {
                id: 'phrsia-connect',
                label: 'PHRSIA Integration',
                instructions: 'Integrate with Personal Health Record System. Enable bidirectional data sync. Support CCD/CDA document formats for interoperability.',
                status: 'pending'
            },
            {
                id: 'azure-health',
                label: 'Azure Health Data Services',
                instructions: 'Configure Azure FHIR server connection. Set up managed identity authentication. Implement data lake storage for analytics.',
                status: 'pending'
            }
        ]
    },
    'Compliance & Security': {
        items: [
            {
                id: 'hipaa-audit',
                label: 'HIPAA Audit Logging',
                instructions: 'Log all PHI access events with user, timestamp, action, and data accessed. Store logs in tamper-proof format. Implement 6-year retention policy.',
                status: 'pending'
            },
            {
                id: 'encryption',
                label: 'End-to-End Encryption',
                instructions: 'Implement AES-256 encryption for data at rest. Use TLS 1.3 for data in transit. Manage encryption keys with Azure Key Vault.',
                status: 'pending'
            },
            {
                id: 'access-control',
                label: 'Role-Based Access Control',
                instructions: 'Define roles: Admin, Provider, Staff, Patient. Implement principle of least privilege. Add MFA for sensitive operations.',
                status: 'pending'
            },
            {
                id: 'baa',
                label: 'BAA Compliance',
                instructions: 'Ensure Business Associate Agreements with all vendors. Document data flow diagrams. Maintain compliance documentation.',
                status: 'pending'
            }
        ]
    },
    'User Interface': {
        items: [
            {
                id: 'patient-form',
                label: 'Patient Intake Form',
                instructions: 'Create comprehensive patient information form with validation. Include demographics, insurance, and visit reason fields.',
                status: 'complete'
            },
            {
                id: 'report-display',
                label: 'Summary Report Display',
                instructions: 'Design clinical summary view with sections for vitals, assessment, plan. Add print and export functionality.',
                status: 'complete'
            },
            {
                id: 'export-options',
                label: 'Export to PDF/DOCX',
                instructions: 'Generate downloadable reports in PDF and DOCX formats. Include clinic letterhead and provider signature fields.',
                status: 'pending'
            },
            {
                id: 'dashboard',
                label: 'Admin Dashboard',
                instructions: 'Create dashboard showing processing statistics, user activity, and system health. Add charts for daily/weekly metrics.',
                status: 'pending'
            }
        ]
    }
}

function ProgressTracker() {
    const [checklists, setChecklists] = useState(developmentChecklists)
    const [expandedItem, setExpandedItem] = useState(null)

    // Load saved state from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('healthcare-dev-progress')
        if (saved) {
            try {
                const parsed = JSON.parse(saved)
                setChecklists(parsed)
            } catch (e) {
                console.error('Failed to load progress:', e)
            }
        }
    }, [])

    // Save state to localStorage
    useEffect(() => {
        localStorage.setItem('healthcare-dev-progress', JSON.stringify(checklists))
    }, [checklists])

    const toggleItemStatus = (category, itemId) => {
        setChecklists(prev => {
            const newChecklists = { ...prev }
            const items = newChecklists[category].items.map(item => {
                if (item.id === itemId) {
                    const statusCycle = {
                        'pending': 'in-progress',
                        'in-progress': 'complete',
                        'complete': 'pending'
                    }
                    return { ...item, status: statusCycle[item.status] }
                }
                return item
            })
            newChecklists[category] = { ...newChecklists[category], items }
            return newChecklists
        })
    }

    const getCategoryProgress = (category) => {
        const items = checklists[category].items
        const complete = items.filter(i => i.status === 'complete').length
        return Math.round((complete / items.length) * 100)
    }

    const getOverallProgress = () => {
        let total = 0
        let complete = 0
        Object.values(checklists).forEach(cat => {
            total += cat.items.length
            complete += cat.items.filter(i => i.status === 'complete').length
        })
        return Math.round((complete / total) * 100)
    }

    const getStatusIcon = (status) => {
        switch (status) {
            case 'complete': return '✓'
            case 'in-progress': return '◐'
            default: return '○'
        }
    }

    return (
        <div className="progress-tracker">
            <div className="tracker-header">
                <h2>Development Progress</h2>
                <div className="overall-progress">
                    <div className="progress-circle">
                        <span className="progress-value">{getOverallProgress()}%</span>
                    </div>
                    <span className="progress-label">Overall</span>
                </div>
            </div>

            <div className="tracker-categories">
                {Object.entries(checklists).map(([category, data]) => (
                    <div key={category} className="tracker-category">
                        <div className="category-header">
                            <h3>{category}</h3>
                            <div className="category-progress">
                                <div className="progress-bar-mini">
                                    <div
                                        className="progress-bar-fill-mini"
                                        style={{ width: `${getCategoryProgress(category)}%` }}
                                    />
                                </div>
                                <span>{getCategoryProgress(category)}%</span>
                            </div>
                        </div>
                        <ul className="tracker-items">
                            {data.items.map(item => (
                                <li key={item.id} className={`tracker-item ${item.status}`}>
                                    <div
                                        className="item-main"
                                        onClick={() => toggleItemStatus(category, item.id)}
                                    >
                                        <span className={`item-status ${item.status}`}>
                                            {getStatusIcon(item.status)}
                                        </span>
                                        <span className="item-label">{item.label}</span>
                                        <button
                                            className="item-info-btn"
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                setExpandedItem(expandedItem === item.id ? null : item.id)
                                            }}
                                        >
                                            {expandedItem === item.id ? '▼' : 'ℹ'}
                                        </button>
                                    </div>
                                    {expandedItem === item.id && (
                                        <div className="item-instructions">
                                            <p>{item.instructions}</p>
                                        </div>
                                    )}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default ProgressTracker
