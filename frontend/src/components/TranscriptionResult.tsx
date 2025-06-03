import React, { useState } from 'react';
import { 
  Copy, 
  Download, 
  RotateCcw, 
  CheckCircle, 
  Clock, 
  FileText, 
  BarChart3,
  Globe,
  Hash,
  Eye,
  EyeOff
} from 'lucide-react';
import { TranscriptionResponse } from '../types';
import { formatDuration, formatConfidence, copyToClipboard, downloadAsText } from '../utils';

interface TranscriptionResultProps {
  result: TranscriptionResponse;
  onReset: () => void;
}

const TranscriptionResult: React.FC<TranscriptionResultProps> = ({ result, onReset }) => {
  const [copied, setCopied] = useState(false);
  const [showMetadata, setShowMetadata] = useState(true);

  const handleCopy = async () => {
    const success = await copyToClipboard(result.transcript);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    const filename = result.metadata.filename 
      ? `transcript_${result.metadata.filename.replace(/\.[^/.]+$/, '')}.txt`
      : `transcript_${result.metadata.transcription_id.slice(0, 8)}.txt`;
    
    downloadAsText(result.transcript, filename);
  };

  const getStatusColor = (status: string) => {
    if (status.includes('completed')) return 'text-success-600 bg-success-100';
    if (status.includes('error')) return 'text-error-600 bg-error-100';
    return 'text-warning-600 bg-warning-100';
  };

  const getStatusIcon = (status: string) => {
    if (status.includes('completed')) return <CheckCircle size={16} />;
    return <Clock size={16} />;
  };

  return (
    <div className="space-y-6">
      {/* Success Header */}
      <div className="card bg-gradient-to-r from-success-50 to-primary-50 border-success-200">
        <div className="text-center">
          <div className="flex justify-center mb-4">
            <div className="bg-success-100 p-3 rounded-full">
              <CheckCircle className="w-8 h-8 text-success-600" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Transcription Complete!
          </h2>
          <p className="text-gray-600">
            Your audio has been successfully transcribed. You can copy, download, or start a new transcription.
          </p>
        </div>
      </div>

      {/* Metadata Panel */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <BarChart3 size={20} />
            <span>Transcription Details</span>
          </h3>
          <button
            onClick={() => setShowMetadata(!showMetadata)}
            className="text-gray-500 hover:text-gray-700 transition-colors"
          >
            {showMetadata ? <EyeOff size={20} /> : <Eye size={20} />}
          </button>
        </div>

        {showMetadata && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-1">
                <div className={`px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getStatusColor(result.metadata.status)}`}>
                  {getStatusIcon(result.metadata.status)}
                  <span>Status</span>
                </div>
              </div>
              <p className="text-sm text-gray-600 capitalize">
                {result.metadata.status.replace('TranscriptStatus.', '')}
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-1">
                <Hash size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">Word Count</span>
              </div>
              <p className="text-lg font-semibold text-gray-900">
                {result.metadata.word_count?.toLocaleString() || 'N/A'}
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-1">
                <BarChart3 size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">Confidence</span>
              </div>
              <p className="text-lg font-semibold text-gray-900">
                {formatConfidence(result.metadata.confidence)}
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-1">
                <Clock size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">Duration</span>
              </div>
              <p className="text-lg font-semibold text-gray-900">
                {formatDuration(result.metadata.audio_duration)}
              </p>
            </div>

            {result.metadata.language_code && (
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-1">
                  <Globe size={16} className="text-gray-500" />
                  <span className="text-sm font-medium text-gray-700">Language</span>
                </div>
                <p className="text-lg font-semibold text-gray-900">
                  {result.metadata.language_code.toUpperCase()}
                </p>
              </div>
            )}

            <div className="bg-gray-50 rounded-lg p-3 md:col-span-2 lg:col-span-3">
              <div className="flex items-center space-x-2 mb-1">
                <FileText size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">Source</span>
              </div>
              <p className="text-sm text-gray-600 break-all">
                {result.metadata.filename || result.metadata.audio_url || 'Unknown'}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Transcript Display */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <FileText size={20} />
            <span>Transcript</span>
          </h3>
          
          <div className="flex space-x-2">
            <button
              onClick={handleCopy}
              className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200 ${
                copied 
                  ? 'bg-success-100 text-success-700' 
                  : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
              }`}
            >
              {copied ? <CheckCircle size={16} /> : <Copy size={16} />}
              <span className="text-sm">{copied ? 'Copied!' : 'Copy'}</span>
            </button>
            
            <button
              onClick={handleDownload}
              className="flex items-center space-x-2 bg-primary-100 hover:bg-primary-200 text-primary-700 px-3 py-2 rounded-lg transition-colors duration-200"
            >
              <Download size={16} />
              <span className="text-sm">Download</span>
            </button>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
          <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
            {result.transcript || 'No transcript available.'}
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center">
        <button
          onClick={onReset}
          className="flex items-center space-x-2 btn-primary"
        >
          <RotateCcw size={18} />
          <span>Transcribe Another File</span>
        </button>
      </div>
    </div>
  );
};

export default TranscriptionResult;
