# AudioToText Frontend

A beautiful, modern React frontend for the AudioToText transcription service.

## Features

🎨 **Modern UI/UX**
- Clean, responsive design with Tailwind CSS
- Beautiful animations and transitions
- Mobile-friendly interface

🎵 **Dual Input Methods**
- Upload audio files (drag & drop support)
- Provide audio URLs from the internet
- Support for multiple audio formats

📊 **Rich Results Display**
- Formatted transcript with metadata
- Confidence scores and word counts
- Copy to clipboard and download options

⚡ **Real-time Feedback**
- Progress indicators during transcription
- Error handling with helpful messages
- Network status monitoring

## Quick Start

### Prerequisites
- Node.js 16+ and npm
- Backend server running on `localhost:8000`

### Installation & Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```
   
   Or use the Windows batch script:
   ```bash
   ./start.bat
   ```

3. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Usage

### Upload Audio File
1. Click the "Upload File" tab
2. Drag and drop an audio file or click to browse
3. Supported formats: MP3, WAV, M4A, MP4, WebM, FLAC
4. Maximum file size: 100MB
5. Click "Transcribe File"

### Use Audio URL
1. Click the "Audio URL" tab
2. Paste a public URL to an audio file
3. Click "Transcribe from URL"

### View Results
- See transcription progress in real-time
- View detailed metadata (confidence, word count, duration)
- Copy transcript to clipboard
- Download transcript as text file
- Start a new transcription

## Project Structure

```
frontend/
├── public/
│   ├── index.html          # HTML template
│   └── manifest.json       # PWA manifest
├── src/
│   ├── components/         # React components
│   │   ├── AudioInput.tsx  # File upload & URL input
│   │   ├── TranscriptionResult.tsx  # Results display
│   │   ├── LoadingSpinner.tsx       # Progress indicator
│   │   ├── ErrorMessage.tsx         # Error handling
│   │   └── Header.tsx      # App header
│   ├── services/
│   │   └── api.ts          # API service layer
│   ├── types/
│   │   └── index.ts        # TypeScript interfaces
│   ├── utils/
│   │   └── index.ts        # Utility functions
│   ├── App.tsx             # Main app component
│   ├── index.tsx           # React entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies & scripts
├── tailwind.config.js      # Tailwind CSS config
├── tsconfig.json           # TypeScript config
└── start.bat              # Windows startup script
```

## Technologies Used

- **React 18** - Modern React with hooks
- **TypeScript** - Type safety and better DX
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icon library
- **Fetch API** - HTTP requests to backend

## Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### API Integration
The frontend communicates with the backend via:
- `POST /transcribe-url` - For URL-based transcription
- `POST /transcribe-file` - For file upload transcription

## Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Customization

**Colors & Theming:**
Edit `tailwind.config.js` to customize the color scheme.

**API Endpoint:**
Update `src/services/api.ts` to change the backend URL.

**Styling:**
Modify `src/index.css` for global styles or component files for specific styling.

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Common Issues

1. **"Cannot connect to backend"**
   - Ensure backend server is running on port 8000
   - Check CORS configuration in backend

2. **File upload fails**
   - Check file format and size limits
   - Ensure file is not corrupted

3. **Styling issues**
   - Clear browser cache
   - Ensure Tailwind CSS is properly configured

### Performance Tips

- Use modern browsers for best performance
- Ensure stable internet connection for URL transcription
- Keep audio files under 100MB for faster processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the AudioToText application suite.
