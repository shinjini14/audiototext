import React, { useState, useEffect } from 'react';
import { AudioLines, Wifi, WifiOff } from 'lucide-react';
import { TranscriptionState, InputMode } from './types';
import { apiService } from './services/api';
import AudioInput from './components/AudioInput';
import TranscriptionResult from './components/TranscriptionResult';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import Header from './components/Header';

function App() {
  const [transcriptionState, setTranscriptionState] = useState<TranscriptionState>({
    isLoading: false,
    result: null,
    error: null,
    progress: 0,
  });
  
  const [inputMode, setInputMode] = useState<InputMode>('url');
  const [isOnline, setIsOnline] = useState(true);

  // Check API health and network status
  useEffect(() => {
    const checkConnection = async () => {
      const online = navigator.onLine;
      setIsOnline(online);
      
      if (online) {
        try {
          await apiService.checkHealth();
        } catch {
          setIsOnline(false);
        }
      }
    };

    checkConnection();
    
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const handleTranscription = async (input: string | File) => {
    setTranscriptionState({
      isLoading: true,
      result: null,
      error: null,
      progress: 0,
    });

    // Simulate progress updates
    const progressInterval = setInterval(() => {
      setTranscriptionState(prev => ({
        ...prev,
        progress: Math.min(prev.progress + Math.random() * 15, 90)
      }));
    }, 1000);

    try {
      let result;
      if (typeof input === 'string') {
        result = await apiService.transcribeUrl(input);
      } else {
        result = await apiService.transcribeFile(input);
      }

      clearInterval(progressInterval);
      setTranscriptionState({
        isLoading: false,
        result,
        error: null,
        progress: 100,
      });
    } catch (error) {
      clearInterval(progressInterval);
      setTranscriptionState({
        isLoading: false,
        result: null,
        error: error instanceof Error ? error.message : 'An unexpected error occurred',
        progress: 0,
      });
    }
  };

  const handleReset = () => {
    setTranscriptionState({
      isLoading: false,
      result: null,
      error: null,
      progress: 0,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header />
      
      {/* Connection Status */}
      {!isOnline && (
        <div className="bg-error-500 text-white px-4 py-2 text-center text-sm flex items-center justify-center gap-2">
          <WifiOff size={16} />
          <span>No internet connection. Please check your network.</span>
        </div>
      )}

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-primary-100 p-4 rounded-full">
              <AudioLines className="w-12 h-12 text-primary-600" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-4">
            Audio to Text Transcription
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform your audio files into accurate text transcriptions using advanced AI technology.
            Upload a file or provide a URL to get started.
          </p>
        </div>

        {/* Main Content */}
        <div className="space-y-8">
          {!transcriptionState.result && !transcriptionState.isLoading && (
            <AudioInput
              mode={inputMode}
              onModeChange={setInputMode}
              onSubmit={handleTranscription}
              disabled={!isOnline}
            />
          )}

          {transcriptionState.isLoading && (
            <LoadingSpinner progress={transcriptionState.progress} />
          )}

          {transcriptionState.error && (
            <ErrorMessage 
              message={transcriptionState.error} 
              onRetry={handleReset}
            />
          )}

          {transcriptionState.result && (
            <TranscriptionResult
              result={transcriptionState.result}
              onReset={handleReset}
            />
          )}
        </div>

        {/* Features Section */}
        {!transcriptionState.result && !transcriptionState.isLoading && (
          <div className="mt-16 grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-success-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <AudioLines className="w-8 h-8 text-success-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">High Accuracy</h3>
              <p className="text-gray-600">Advanced AI models ensure precise transcription with confidence scores.</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Wifi className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Multiple Formats</h3>
              <p className="text-gray-600">Support for MP3, WAV, M4A, MP4, WebM, and FLAC audio formats.</p>
            </div>
            
            <div className="text-center">
              <div className="bg-warning-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <AudioLines className="w-8 h-8 text-warning-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Fast Processing</h3>
              <p className="text-gray-600">Quick turnaround time with real-time progress tracking.</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
