/**
 * FileUpload Component
 * Handles PDF file upload
 */
'use client';

import { useState } from 'react';

interface FileUploadProps {
  chatId: string;
  onUploadSuccess: (filename: string) => void;
}

export default function FileUpload({ chatId, onUploadSuccess }: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    console.log('[FILE UPLOAD] Selected file:', file.name);
    console.log('[FILE UPLOAD] Chat ID:', chatId);

    // Validate file type
    if (!file.name.endsWith('.pdf')) {
      setError('Please upload a PDF file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('chat_id', chatId);

      console.log('[FILE UPLOAD] Uploading to:', 'http://localhost:8000/api/v1/messages/upload-pdf');

      const response = await fetch('http://localhost:8000/api/v1/messages/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      console.log('[FILE UPLOAD] Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('[FILE UPLOAD] Error:', errorData);
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      console.log('[FILE UPLOAD] Success:', data);
      onUploadSuccess(file.name);
      
      // Reset file input
      event.target.value = '';
    } catch (err) {
      console.error('[FILE UPLOAD] Exception:', err);
      setError('Failed to upload PDF. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <label htmlFor="pdf-upload" className="file-upload-button">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
        </svg>
        <span>Upload PDF</span>
        <input
          id="pdf-upload"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          disabled={uploading}
          style={{ display: 'none' }}
        />
      </label>
      {uploading && <span className="upload-status">Uploading...</span>}
      {error && <span className="upload-error">{error}</span>}
    </div>
  );
}
