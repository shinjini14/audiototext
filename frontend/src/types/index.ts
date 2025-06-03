export interface TranscriptionMetadata {
  transcription_id: string;
  audio_url?: string;
  filename?: string;
  status: string;
  word_count: number | null;
  confidence: number | null;
  language_code: string | null;
  audio_duration: number | null;
}

export interface TranscriptionResponse {
  transcript: string;
  metadata: TranscriptionMetadata;
}

export interface TranscriptionState {
  isLoading: boolean;
  result: TranscriptionResponse | null;
  error: string | null;
  progress: number;
}

export type InputMode = 'url' | 'file';

export interface AudioFile {
  file: File;
  name: string;
  size: number;
  type: string;
  url: string;
}

export interface ApiError {
  detail: string;
}
