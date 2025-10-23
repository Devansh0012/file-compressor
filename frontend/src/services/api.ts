import axios from 'axios';
import { CompressionRequest, CompressionResponse, APIInfo } from '../types';

const API_BASE_URL = '/api';

export const compressionService = {
  async compressFile(
    file: File,
    compressionData: CompressionRequest
  ): Promise<CompressionResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('compression_data', JSON.stringify(compressionData));

    const response = await axios.post<CompressionResponse>(
      `${API_BASE_URL}/compress/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  async getInfo(): Promise<APIInfo> {
    const response = await axios.get<APIInfo>(`${API_BASE_URL}/compress/info`);
    return response.data;
  },

  getDownloadUrl(filename: string): string {
    return `${API_BASE_URL}/compress/download/${filename}`;
  },
};
