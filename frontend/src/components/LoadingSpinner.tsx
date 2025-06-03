import React from 'react';
import { AudioLines, Clock, Zap } from 'lucide-react';

interface LoadingSpinnerProps {
  progress: number;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ progress }) => {
  const getProgressMessage = (progress: number): string => {
    if (progress < 20) return 'Uploading audio file...';
    if (progress < 40) return 'Processing audio...';
    if (progress < 70) return 'Analyzing speech patterns...';
    if (progress < 90) return 'Generating transcript...';
    return 'Finalizing results...';
  };

  const getProgressIcon = (progress: number) => {
    if (progress < 30) return <AudioLines className="w-6 h-6" />;
    if (progress < 70) return <Zap className="w-6 h-6" />;
    return <Clock className="w-6 h-6" />;
  };

  return (
    <div className="card text-center">
      <div className="space-y-6">
        {/* Animated Icon */}
        <div className="flex justify-center">
          <div className="bg-primary-100 p-6 rounded-full animate-pulse-slow">
            <div className="text-primary-600 animate-bounce-slow">
              {getProgressIcon(progress)}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-3">
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">{getProgressMessage(progress)}</span>
            <span className="font-medium text-primary-600">{Math.round(progress)}%</span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-primary-500 to-primary-600 h-full rounded-full transition-all duration-500 ease-out relative"
              style={{ width: `${progress}%` }}
            >
              <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
            </div>
          </div>
        </div>

        {/* Status Message */}
        <div className="text-gray-600">
          <p className="text-lg font-medium mb-2">Transcribing your audio...</p>
          <p className="text-sm">
            This may take a few moments depending on the length of your audio file.
          </p>
        </div>

        {/* Loading Animation */}
        <div className="flex justify-center space-x-2">
          <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
