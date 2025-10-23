export enum CompressionStrategy {
  QUALITY = 'quality',
  TARGET_SIZE = 'target_size',
  PERCENTAGE = 'percentage',
}

export enum FileType {
  IMAGE = 'image',
  VIDEO = 'video',
  AUDIO = 'audio',
  DOCUMENT = 'document',
}

export interface CompressionRequest {
  strategy: CompressionStrategy;
  target_size_mb?: number;
  reduction_percentage?: number;
  quality?: number;
}

export interface CompressionResponse {
  success: boolean;
  original_size: number;
  compressed_size: number;
  reduction_percentage: number;
  filename: string;
  download_url: string;
  message?: string;
}

export interface SupportedFormats {
  images: string[];
  videos: string[];
  audio: string[];
  documents: string[];
}

export interface APIInfo {
  max_file_size_mb: number;
  supported_formats: SupportedFormats;
  compression_strategies: string[];
}
