import React, { useState, useRef, useCallback } from 'react';
import { Upload, Link, FileAudio, X, AlertCircle } from 'lucide-react';
import { InputMode, AudioFile } from '../types';
import { isValidAudioUrl, isValidAudioFile, formatFileSize } from '../utils';

interface AudioInputProps {
  mode: InputMode;
  onModeChange: (mode: InputMode) => void;
  onSubmit: (input: string | File) => void;
  disabled?: boolean;
}

const AudioInput: React.FC<AudioInputProps> = ({
  mode,
  onModeChange,
  onSubmit,
  disabled = false
}) => {
  const [url, setUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState<AudioFile | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [urlError, setUrlError] = useState('');
  const [fileError, setFileError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUrlSubmit = () => {
    if (!url.trim()) {
      setUrlError('Please enter a valid URL');
      return;
    }
    
    if (!isValidAudioUrl(url)) {
      setUrlError('Please enter a valid audio URL (MP3, WAV, M4A, etc.)');
      return;
    }
    
    setUrlError('');
    onSubmit(url);
  };

  const handleFileSubmit = () => {
    if (!selectedFile) {
      setFileError('Please select an audio file');
      return;
    }
    
    setFileError('');
    onSubmit(selectedFile.file);
  };

  const handleFileSelect = useCallback((file: File) => {
    if (!isValidAudioFile(file)) {
      setFileError('Please select a valid audio file (MP3, WAV, M4A, MP4, WebM, FLAC)');
      return;
    }

    if (file.size > 100 * 1024 * 1024) { // 100MB limit
      setFileError('File size must be less than 100MB');
      return;
    }

    setFileError('');
    setSelectedFile({
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      url: URL.createObjectURL(file)
    });
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const clearFile = () => {
    if (selectedFile) {
      URL.revokeObjectURL(selectedFile.url);
    }
    setSelectedFile(null);
    setFileError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="card">
      {/* Mode Selector */}
      <div className="flex bg-gray-100 rounded-lg p-1 mb-6">
        <button
          onClick={() => onModeChange('url')}
          className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-md transition-all ${
            mode === 'url'
              ? 'bg-white text-primary-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
          }`}
          disabled={disabled}
        >
          <Link size={18} />
          <span>Audio URL</span>
        </button>
        <button
          onClick={() => onModeChange('file')}
          className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-md transition-all ${
            mode === 'file'
              ? 'bg-white text-primary-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
          }`}
          disabled={disabled}
        >
          <Upload size={18} />
          <span>Upload File</span>
        </button>
      </div>

      {/* URL Input */}
      {mode === 'url' && (
        <div className="space-y-4">
          <div>
            <label htmlFor="audio-url" className="block text-sm font-medium text-gray-700 mb-2">
              Audio URL
            </label>
            <input
              id="audio-url"
              type="url"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value);
                setUrlError('');
              }}
              placeholder="https://example.com/audio.mp3"
              className={`input-field ${urlError ? 'border-error-500 focus:ring-error-500' : ''}`}
              disabled={disabled}
            />
            {urlError && (
              <div className="flex items-center space-x-2 mt-2 text-error-600 text-sm">
                <AlertCircle size={16} />
                <span>{urlError}</span>
              </div>
            )}
          </div>
          
          <button
            onClick={handleUrlSubmit}
            disabled={disabled || !url.trim()}
            className="btn-primary w-full"
          >
            Transcribe from URL
          </button>
        </div>
      )}

      {/* File Upload */}
      {mode === 'file' && (
        <div className="space-y-4">
          {!selectedFile ? (
            <div
              className={`upload-zone ${dragOver ? 'dragover' : ''}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-lg font-medium text-gray-700 mb-2">
                Drop your audio file here
              </p>
              <p className="text-gray-500 mb-4">
                or click to browse files
              </p>
              <p className="text-sm text-gray-400">
                Supports MP3, WAV, M4A, MP4, WebM, FLAC (max 100MB)
              </p>
              
              <input
                ref={fileInputRef}
                type="file"
                accept="audio/*,.mp3,.wav,.m4a,.mp4,.webm,.flac"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleFileSelect(file);
                }}
                className="hidden"
                disabled={disabled}
              />
            </div>
          ) : (
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <FileAudio className="w-8 h-8 text-primary-600" />
                  <div>
                    <p className="font-medium text-gray-900">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {formatFileSize(selectedFile.size)} • {selectedFile.type || 'Audio file'}
                    </p>
                  </div>
                </div>
                <button
                  onClick={clearFile}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                  disabled={disabled}
                >
                  <X size={20} />
                </button>
              </div>
            </div>
          )}
          
          {fileError && (
            <div className="flex items-center space-x-2 text-error-600 text-sm">
              <AlertCircle size={16} />
              <span>{fileError}</span>
            </div>
          )}
          
          <button
            onClick={handleFileSubmit}
            disabled={disabled || !selectedFile}
            className="btn-primary w-full"
          >
            Transcribe File
          </button>
        </div>
      )}
    </div>
  );
};

export default AudioInput;
