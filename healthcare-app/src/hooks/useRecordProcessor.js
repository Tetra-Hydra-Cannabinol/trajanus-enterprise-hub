/**
 * useRecordProcessor - React hook for medical record processing workflow
 * HEALTHCARE-04: Full integration of PDF upload → processor → AI → display
 *
 * @author Trajanus USA
 * @location Jacksonville, Florida
 */

import { useState, useCallback } from 'react';
import PDFProcessor from '../utils/pdf-processor';
import MedicalSummarizer from '../utils/medical-summarizer';

// Processing step definitions
const STEPS = {
  IDLE: 'idle',
  UPLOADING: 'uploading',
  EXTRACTING: 'extracting',
  ANALYZING: 'analyzing',
  GENERATING: 'generating',
  COMPLETE: 'complete',
  ERROR: 'error'
};

/**
 * Custom hook for medical record processing
 * @returns {Object} Processing state and methods
 */
export function useRecordProcessor() {
  const [status, setStatus] = useState(STEPS.IDLE);
  const [progress, setProgress] = useState({ current: 0, total: 0, message: '' });
  const [records, setRecords] = useState([]);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  // Initialize processors
  const pdfProcessor = new PDFProcessor();
  const summarizer = new MedicalSummarizer();

  /**
   * Process uploaded medical records
   * @param {FileList|File[]} files - Files to process
   * @param {Object} patientInfo - Patient information
   * @param {boolean} userConsent - HIPAA consent flag
   */
  const processRecords = useCallback(async (files, patientInfo, userConsent = false) => {
    // Validate consent
    if (!userConsent) {
      setError('User consent required for AI-powered medical record processing.');
      setStatus(STEPS.ERROR);
      return;
    }

    // Validate inputs
    if (!files || files.length === 0) {
      setError('No files selected for processing.');
      setStatus(STEPS.ERROR);
      return;
    }

    if (!patientInfo || !patientInfo.firstName || !patientInfo.lastName) {
      setError('Patient information is required.');
      setStatus(STEPS.ERROR);
      return;
    }

    try {
      // Reset state
      setError(null);
      setSummary(null);
      setRecords([]);

      // Step 1: Extract text from files
      setStatus(STEPS.EXTRACTING);
      setProgress({ current: 0, total: files.length, message: 'Extracting text from documents...' });

      const extractedRecords = await pdfProcessor.processFiles(
        files,
        (current, total, filename) => {
          setProgress({
            current,
            total,
            message: `Processing ${filename} (${current}/${total})`
          });
        }
      );

      setRecords(extractedRecords);

      // Check if any records were successfully extracted
      const validRecords = extractedRecords.filter(r => r.content && !r.error);
      if (validRecords.length === 0) {
        throw new Error('No text could be extracted from the uploaded files.');
      }

      // Step 2: Generate AI summary
      setStatus(STEPS.GENERATING);
      setProgress({ current: 1, total: 1, message: 'Generating AI-powered clinical summary...' });

      const patientData = {
        id: patientInfo.mrn || `PAT-${Date.now()}`,
        name: `${patientInfo.firstName} ${patientInfo.lastName}`,
        dob: patientInfo.dob || 'Not provided',
        complaint: patientInfo.reason || 'Medical records review'
      };

      const recordTexts = validRecords.map(r => r.content);
      const generatedSummary = await summarizer.generateSummary(patientData, recordTexts);

      setSummary({
        content: generatedSummary,
        patientInfo: patientData,
        recordCount: validRecords.length,
        generatedAt: new Date().toISOString()
      });

      setStatus(STEPS.COMPLETE);
      setProgress({ current: 1, total: 1, message: 'Processing complete!' });

    } catch (err) {
      console.error('Record processing error:', err.message);
      setError(err.message);
      setStatus(STEPS.ERROR);
    }
  }, []);

  /**
   * Export summary to file
   * @param {string} format - Export format ('txt', 'json', 'html')
   */
  const exportSummary = useCallback((format = 'txt') => {
    if (!summary) {
      setError('No summary available to export.');
      return;
    }

    let content, mimeType, extension;

    switch (format) {
      case 'json':
        content = JSON.stringify(summary, null, 2);
        mimeType = 'application/json';
        extension = 'json';
        break;

      case 'html':
        content = `<!DOCTYPE html>
<html>
<head>
  <title>Patient Summary - ${summary.patientInfo.name}</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
    h1 { color: #00AAFF; border-bottom: 2px solid #00AAFF; padding-bottom: 10px; }
    .meta { color: #666; font-size: 0.9em; margin-bottom: 20px; }
    .content { line-height: 1.6; white-space: pre-wrap; }
    .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 0.8em; color: #999; }
  </style>
</head>
<body>
  <h1>Patient Clinical Summary</h1>
  <div class="meta">
    <p><strong>Patient:</strong> ${summary.patientInfo.name}</p>
    <p><strong>DOB:</strong> ${summary.patientInfo.dob}</p>
    <p><strong>MRN:</strong> ${summary.patientInfo.id}</p>
    <p><strong>Generated:</strong> ${new Date(summary.generatedAt).toLocaleString()}</p>
    <p><strong>Records Processed:</strong> ${summary.recordCount}</p>
  </div>
  <div class="content">${summary.content}</div>
  <div class="footer">
    <p>Generated by Trajanus Healthcare Records Processor</p>
    <p>Trajanus USA | Jacksonville, Florida</p>
    <p>This summary is for clinical decision support only. Verify against source documents.</p>
  </div>
</body>
</html>`;
        mimeType = 'text/html';
        extension = 'html';
        break;

      default: // txt
        content = `PATIENT CLINICAL SUMMARY
========================
Generated by Trajanus Healthcare Records Processor

Patient: ${summary.patientInfo.name}
DOB: ${summary.patientInfo.dob}
MRN: ${summary.patientInfo.id}
Generated: ${new Date(summary.generatedAt).toLocaleString()}
Records Processed: ${summary.recordCount}

------------------------

${summary.content}

------------------------
Trajanus USA | Jacksonville, Florida
This summary is for clinical decision support only.
`;
        mimeType = 'text/plain';
        extension = 'txt';
    }

    // Create and download file
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `patient-summary-${summary.patientInfo.id}-${Date.now()}.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [summary]);

  /**
   * Reset processor state
   */
  const reset = useCallback(() => {
    setStatus(STEPS.IDLE);
    setProgress({ current: 0, total: 0, message: '' });
    setRecords([]);
    setSummary(null);
    setError(null);
  }, []);

  return {
    // State
    status,
    progress,
    records,
    summary,
    error,
    isProcessing: [STEPS.EXTRACTING, STEPS.ANALYZING, STEPS.GENERATING].includes(status),
    isComplete: status === STEPS.COMPLETE,
    isError: status === STEPS.ERROR,

    // Methods
    processRecords,
    exportSummary,
    reset,

    // Constants
    STEPS
  };
}

export default useRecordProcessor;
