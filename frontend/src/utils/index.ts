export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const formatDuration = (seconds: number | null): string => {
  if (!seconds) return 'Unknown';
  
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  }
  
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};

export const formatConfidence = (confidence: number | null): string => {
  if (!confidence) return 'Unknown';
  return `${(confidence * 100).toFixed(1)}%`;
};

export const isValidAudioUrl = (url: string): boolean => {
  try {
    new URL(url);
    const audioExtensions = ['.mp3', '.wav', '.m4a', '.mp4', '.webm', '.flac'];
    const urlLower = url.toLowerCase();
    return audioExtensions.some(ext => urlLower.includes(ext)) || 
           urlLower.includes('audio') || 
           urlLower.includes('sound');
  } catch {
    return false;
  }
};

export const isValidAudioFile = (file: File): boolean => {
  const validTypes = [
    'audio/mpeg',
    'audio/wav', 
    'audio/mp4',
    'audio/m4a',
    'audio/webm',
    'audio/flac',
    'video/mp4' // MP4 can contain audio
  ];
  
  const validExtensions = ['.mp3', '.wav', '.m4a', '.mp4', '.webm', '.flac'];
  const fileName = file.name.toLowerCase();
  
  return validTypes.includes(file.type) || 
         validExtensions.some(ext => fileName.endsWith(ext));
};

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    const success = document.execCommand('copy');
    document.body.removeChild(textArea);
    return success;
  }
};

export const downloadAsText = (text: string, filename: string): void => {
  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};
