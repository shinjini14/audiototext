import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onRetry: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  const getErrorType = (message: string): 'network' | 'file' | 'server' | 'unknown' => {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('network') || lowerMessage.includes('connection') || lowerMessage.includes('fetch')) {
      return 'network';
    }
    if (lowerMessage.includes('file') || lowerMessage.includes('format') || lowerMessage.includes('upload')) {
      return 'file';
    }
    if (lowerMessage.includes('server') || lowerMessage.includes('500') || lowerMessage.includes('api')) {
      return 'server';
    }
    return 'unknown';
  };

  const getErrorSuggestion = (type: string): string => {
    switch (type) {
      case 'network':
        return 'Please check your internet connection and try again.';
      case 'file':
        return 'Please ensure your file is a valid audio format (MP3, WAV, M4A, etc.) and under 100MB.';
      case 'server':
        return 'Our servers are experiencing issues. Please try again in a few moments.';
      default:
        return 'Please try again or contact support if the problem persists.';
    }
  };

  const errorType = getErrorType(message);
  const suggestion = getErrorSuggestion(errorType);

  return (
    <div className="card border-error-200 bg-error-50">
      <div className="text-center space-y-6">
        {/* Error Icon */}
        <div className="flex justify-center">
          <div className="bg-error-100 p-4 rounded-full">
            <AlertTriangle className="w-12 h-12 text-error-600" />
          </div>
        </div>

        {/* Error Content */}
        <div className="space-y-3">
          <h3 className="text-xl font-semibold text-error-800">
            Oops! Something went wrong
          </h3>
          
          <div className="bg-white rounded-lg p-4 border border-error-200">
            <p className="text-error-700 font-medium mb-2">Error Details:</p>
            <p className="text-error-600 text-sm break-words">{message}</p>
          </div>
          
          <p className="text-error-600">{suggestion}</p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            onClick={onRetry}
            className="flex items-center justify-center space-x-2 bg-error-600 hover:bg-error-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-error-500 focus:ring-offset-2"
          >
            <RefreshCw size={18} />
            <span>Try Again</span>
          </button>
          
          <button
            onClick={() => window.location.reload()}
            className="flex items-center justify-center space-x-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            <Home size={18} />
            <span>Start Over</span>
          </button>
        </div>

        {/* Help Text */}
        <div className="text-sm text-gray-600 bg-white rounded-lg p-3 border">
          <p className="font-medium mb-1">Need help?</p>
          <p>
            Make sure the backend server is running on{' '}
            <code className="bg-gray-100 px-1 rounded">localhost:8000</code> and your audio file is accessible.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
