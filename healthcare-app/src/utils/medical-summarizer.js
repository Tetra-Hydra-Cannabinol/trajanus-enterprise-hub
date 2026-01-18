/**
 * MedicalSummarizer - AI-powered patient summary generation
 * HEALTHCARE-03: Claude API integration for medical record summarization
 *
 * HIPAA COMPLIANCE:
 * - No data stored (process in-memory only)
 * - No external logging of PHI
 * - Encryption in transit (HTTPS)
 * - User consent required before processing
 *
 * @author Trajanus USA
 * @location Jacksonville, Florida
 */

class MedicalSummarizer {
  constructor(apiKey = null) {
    // API key should come from environment or secure storage
    this.apiKey = apiKey || import.meta.env.VITE_ANTHROPIC_API_KEY;
    this.apiEndpoint = 'https://api.anthropic.com/v1/messages';
    this.model = 'claude-sonnet-4-20250514';
  }

  /**
   * Generate a comprehensive patient summary from medical records
   * @param {Object} patientInfo - Patient demographic information
   * @param {string[]} recordTexts - Array of extracted medical record texts
   * @returns {Promise<string>} Generated medical summary
   */
  async generateSummary(patientInfo, recordTexts) {
    if (!this.apiKey) {
      throw new Error('Anthropic API key not configured. Set VITE_ANTHROPIC_API_KEY environment variable.');
    }

    if (!patientInfo || !recordTexts || recordTexts.length === 0) {
      throw new Error('Patient information and medical records are required.');
    }

    const prompt = this.buildPrompt(patientInfo, recordTexts);

    try {
      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: this.model,
          max_tokens: 2000,
          messages: [{
            role: 'user',
            content: prompt
          }]
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`API request failed: ${response.status} - ${errorData.error?.message || 'Unknown error'}`);
      }

      const data = await response.json();

      if (!data.content || !data.content[0] || !data.content[0].text) {
        throw new Error('Invalid response format from API');
      }

      return data.content[0].text;
    } catch (error) {
      // Log error without PHI
      console.error('Medical summary generation failed:', error.message);
      throw error;
    }
  }

  /**
   * Build the prompt for medical summary generation
   * @param {Object} patientInfo - Patient information object
   * @param {string[]} recordTexts - Array of medical record texts
   * @returns {string} Formatted prompt
   */
  buildPrompt(patientInfo, recordTexts) {
    const sanitizedInfo = this.sanitizePatientInfo(patientInfo);

    return `You are a medical AI assistant helping review pediatric patient records.

Patient Information:
- ID: ${sanitizedInfo.id || 'N/A'}
- Name: ${sanitizedInfo.name || 'N/A'}
- DOB: ${sanitizedInfo.dob || 'N/A'}
- Chief Complaint: ${sanitizedInfo.complaint || 'General review'}

Medical Records:
${recordTexts.join('\n\n---\n\n')}

Please provide a comprehensive patient summary including:
1. Key Medical History
2. Current Conditions
3. Medications
4. Recent Visits/Treatments
5. Clinical Recommendations
6. Follow-up Requirements

Format the summary professionally for physician review. Use clear headings and bullet points where appropriate.

IMPORTANT: This summary is for clinical decision support only. All information should be verified against source documents before clinical use.`;
  }

  /**
   * Sanitize patient information to prevent injection
   * @param {Object} patientInfo - Raw patient info
   * @returns {Object} Sanitized patient info
   */
  sanitizePatientInfo(patientInfo) {
    const sanitize = (str) => {
      if (!str || typeof str !== 'string') return '';
      // Remove potential injection characters
      return str.replace(/[<>{}]/g, '').trim().substring(0, 500);
    };

    return {
      id: sanitize(patientInfo.id),
      name: sanitize(patientInfo.name),
      dob: sanitize(patientInfo.dob),
      complaint: sanitize(patientInfo.complaint)
    };
  }

  /**
   * Validate that user has consented to AI processing
   * @param {boolean} consentGiven - Whether consent was obtained
   * @throws {Error} If consent not given
   */
  validateConsent(consentGiven) {
    if (!consentGiven) {
      throw new Error('User consent required for AI-powered medical record processing.');
    }
  }

  /**
   * Process records with consent validation
   * @param {Object} patientInfo - Patient information
   * @param {string[]} recordTexts - Medical record texts
   * @param {boolean} userConsent - User consent flag
   * @returns {Promise<string>} Generated summary
   */
  async processWithConsent(patientInfo, recordTexts, userConsent) {
    this.validateConsent(userConsent);
    return this.generateSummary(patientInfo, recordTexts);
  }
}

// Export for use in React components
export default MedicalSummarizer;

// Also export as named export for flexibility
export { MedicalSummarizer };
