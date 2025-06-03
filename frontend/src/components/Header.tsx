import React from 'react';
import { AudioLines, Github, ExternalLink } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <AudioLines className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">AudioToText</h1>
              <p className="text-sm text-gray-500">AI-Powered Transcription</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors"
            >
              <ExternalLink size={16} />
              <span className="hidden sm:inline">API Docs</span>
            </a>
            
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors"
            >
              <Github size={16} />
              <span className="hidden sm:inline">GitHub</span>
            </a>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
