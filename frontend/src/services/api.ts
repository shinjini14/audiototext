import { TranscriptionResponse, ApiError } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData: ApiError = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`
      }));
      throw new Error(errorData.detail);
    }
    return response.json();
  }

  async transcribeUrl(audioUrl: string): Promise<TranscriptionResponse> {
    const formData = new FormData();
    formData.append('audio_url', audioUrl);

    const response = await fetch(`${API_BASE_URL}/transcribe-url`, {
      method: 'POST',
      body: formData,
    });

    return this.handleResponse<TranscriptionResponse>(response);
  }

  async transcribeFile(file: File): Promise<TranscriptionResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/transcribe-file`, {
      method: 'POST',
      body: formData,
    });

    return this.handleResponse<TranscriptionResponse>(response);
  }

  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/docs`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const apiService = new ApiService();
