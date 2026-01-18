/**
 * PDFProcessor - Extract text from medical record PDFs
 * HEALTHCARE-02: PDF text extraction for medical records
 *
 * Uses pdf.js for client-side PDF parsing
 * HIPAA Compliant: All processing done in-browser, no server upload
 *
 * @author Trajanus USA
 * @location Jacksonville, Florida
 */

// PDF.js library - loaded from CDN in index.html
const pdfjsLib = window.pdfjsLib;

class PDFProcessor {
  constructor() {
    // Configure PDF.js worker
    if (pdfjsLib) {
      pdfjsLib.GlobalWorkerOptions.workerSrc =
        'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    }
  }

  /**
   * Process a single PDF file and extract text
   * @param {File} file - PDF file to process
   * @returns {Promise<Object>} Extracted record with metadata
   */
  async processRecord(file) {
    if (!file || !file.name.toLowerCase().endsWith('.pdf')) {
      throw new Error('Invalid file: Only PDF files are supported');
    }

    try {
      const arrayBuffer = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

      let fullText = '';
      const pageTexts = [];

      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        const pageText = textContent.items
          .map(item => item.str)
          .join(' ')
          .replace(/\s+/g, ' ')
          .trim();

        pageTexts.push(pageText);
        fullText += pageText + '\n\n';
      }

      return {
        filename: file.name,
        pageCount: pdf.numPages,
        content: fullText.trim(),
        pages: pageTexts,
        extractedAt: new Date().toISOString(),
        fileSize: file.size
      };
    } catch (error) {
      console.error(`Error processing PDF ${file.name}:`, error.message);
      throw new Error(`Failed to process ${file.name}: ${error.message}`);
    }
  }

  /**
   * Process multiple PDF files
   * @param {FileList|File[]} files - Array of PDF files
   * @param {Function} onProgress - Progress callback (index, total, filename)
   * @returns {Promise<Object[]>} Array of extracted records
   */
  async processMultipleRecords(files, onProgress = null) {
    const records = [];
    const fileArray = Array.from(files);

    for (let i = 0; i < fileArray.length; i++) {
      const file = fileArray[i];

      if (onProgress) {
        onProgress(i + 1, fileArray.length, file.name);
      }

      try {
        const record = await this.processRecord(file);
        records.push(record);
      } catch (error) {
        // Continue processing other files, log error
        records.push({
          filename: file.name,
          error: error.message,
          content: '',
          extractedAt: new Date().toISOString()
        });
      }
    }

    return records;
  }

  /**
   * Extract text from DOCX file (basic support)
   * @param {File} file - DOCX file
   * @returns {Promise<Object>} Extracted content
   */
  async processDocx(file) {
    if (!file || !file.name.toLowerCase().endsWith('.docx')) {
      throw new Error('Invalid file: Only DOCX files are supported');
    }

    try {
      // Basic DOCX extraction using mammoth.js if available
      if (window.mammoth) {
        const arrayBuffer = await file.arrayBuffer();
        const result = await window.mammoth.extractRawText({ arrayBuffer });

        return {
          filename: file.name,
          content: result.value,
          extractedAt: new Date().toISOString(),
          fileSize: file.size
        };
      } else {
        throw new Error('DOCX processing requires mammoth.js library');
      }
    } catch (error) {
      console.error(`Error processing DOCX ${file.name}:`, error.message);
      throw error;
    }
  }

  /**
   * Process any supported file type
   * @param {File} file - File to process
   * @returns {Promise<Object>} Extracted content
   */
  async processFile(file) {
    const extension = file.name.toLowerCase().split('.').pop();

    switch (extension) {
      case 'pdf':
        return this.processRecord(file);
      case 'docx':
        return this.processDocx(file);
      case 'txt':
        return {
          filename: file.name,
          content: await file.text(),
          extractedAt: new Date().toISOString(),
          fileSize: file.size
        };
      default:
        throw new Error(`Unsupported file type: .${extension}`);
    }
  }

  /**
   * Process multiple files of any supported type
   * @param {FileList|File[]} files - Files to process
   * @param {Function} onProgress - Progress callback
   * @returns {Promise<Object[]>} Extracted records
   */
  async processFiles(files, onProgress = null) {
    const records = [];
    const fileArray = Array.from(files);

    for (let i = 0; i < fileArray.length; i++) {
      const file = fileArray[i];

      if (onProgress) {
        onProgress(i + 1, fileArray.length, file.name);
      }

      try {
        const record = await this.processFile(file);
        records.push(record);
      } catch (error) {
        records.push({
          filename: file.name,
          error: error.message,
          content: '',
          extractedAt: new Date().toISOString()
        });
      }
    }

    return records;
  }
}

export default PDFProcessor;
export { PDFProcessor };
