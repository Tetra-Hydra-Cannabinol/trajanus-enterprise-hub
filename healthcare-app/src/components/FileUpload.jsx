import { useState, useRef } from 'react'

function FileUpload({ onUpload, uploadedFiles, disabled }) {
    const [isDragging, setIsDragging] = useState(false)
    const fileInputRef = useRef(null)

    const handleDragOver = (e) => {
        e.preventDefault()
        if (!disabled) {
            setIsDragging(true)
        }
    }

    const handleDragLeave = (e) => {
        e.preventDefault()
        setIsDragging(false)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setIsDragging(false)
        if (!disabled) {
            const files = Array.from(e.dataTransfer.files).filter(
                file => file.type === 'application/pdf' ||
                        file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
                        file.name.endsWith('.pdf') ||
                        file.name.endsWith('.docx')
            )
            if (files.length > 0) {
                onUpload(files.map(f => ({
                    name: f.name,
                    size: f.size,
                    type: f.type,
                    file: f
                })))
            }
        }
    }

    const handleFileSelect = (e) => {
        const files = Array.from(e.target.files)
        if (files.length > 0) {
            onUpload(files.map(f => ({
                name: f.name,
                size: f.size,
                type: f.type,
                file: f
            })))
        }
        // Reset input to allow selecting same file again
        e.target.value = ''
    }

    const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + ' B'
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    }

    const getFileIcon = (fileName) => {
        if (fileName.endsWith('.pdf')) return '📕'
        if (fileName.endsWith('.docx')) return '📘'
        return '📄'
    }

    return (
        <div className={`card upload-card ${disabled ? 'disabled' : ''}`}>
            <div className="card-header">
                <h2>Medical Records Upload</h2>
                <span className="card-badge">{uploadedFiles.length} file(s)</span>
            </div>

            <div
                className={`upload-zone ${isDragging ? 'dragging' : ''} ${disabled ? 'disabled' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => !disabled && fileInputRef.current?.click()}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.docx"
                    multiple
                    onChange={handleFileSelect}
                    disabled={disabled}
                    style={{ display: 'none' }}
                />
                <div className="upload-icon">📁</div>
                <div className="upload-text">
                    <strong>Drop files here</strong>
                    <span>or click to browse</span>
                </div>
                <div className="upload-formats">
                    Supported: PDF, DOCX
                </div>
            </div>

            {uploadedFiles.length > 0 && (
                <div className="uploaded-files">
                    <h4>Uploaded Files</h4>
                    <ul className="file-list">
                        {uploadedFiles.map((file, index) => (
                            <li key={index} className="file-item">
                                <span className="file-icon">{getFileIcon(file.name)}</span>
                                <div className="file-info">
                                    <span className="file-name">{file.name}</span>
                                    <span className="file-size">{formatFileSize(file.size)}</span>
                                </div>
                                <span className="file-status">✓</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    )
}

export default FileUpload
