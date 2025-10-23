import React, { useState, useEffect } from 'react';
import { FileUpload } from './components/FileUpload';
import { CompressionControls } from './components/CompressionControls';
import { ResultDisplay } from './components/ResultDisplay';
import { LoadingSpinner } from './components/LoadingSpinner';
import { compressionService } from './services/api';
import { CompressionStrategy, CompressionResponse, APIInfo } from './types';
import { Minimize2, AlertCircle } from 'lucide-react';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [strategy, setStrategy] = useState<CompressionStrategy>(
    CompressionStrategy.QUALITY
  );
  const [quality, setQuality] = useState(75);
  const [targetSize, setTargetSize] = useState(1.0);
  const [reductionPercentage, setReductionPercentage] = useState(50);
  const [isCompressing, setIsCompressing] = useState(false);
  const [result, setResult] = useState<CompressionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiInfo, setApiInfo] = useState<APIInfo | null>(null);

  useEffect(() => {
    // Fetch API info on component mount
    compressionService
      .getInfo()
      .then(setApiInfo)
      .catch((err) => console.error('Failed to fetch API info:', err));
  }, []);

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
    setError(null);
    setResult(null);
  };

  const handleCompress = async () => {
    if (!file) return;

    setIsCompressing(true);
    setError(null);

    try {
      const compressionRequest: any = {
        strategy,
      };

      if (strategy === CompressionStrategy.QUALITY) {
        compressionRequest.quality = quality;
      } else if (strategy === CompressionStrategy.TARGET_SIZE) {
        compressionRequest.target_size_mb = targetSize;
      } else if (strategy === CompressionStrategy.PERCENTAGE) {
        compressionRequest.reduction_percentage = reductionPercentage;
      }

      const response = await compressionService.compressFile(
        file,
        compressionRequest
      );
      setResult(response);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Failed to compress file. Please try again.'
      );
    } finally {
      setIsCompressing(false);
    }
  };

  const handleDownload = () => {
    if (!result) return;
    window.location.href = result.download_url;
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  const getAllSupportedFormats = (): string[] => {
    if (!apiInfo) return [];
    return [
      ...apiInfo.supported_formats.images,
      ...apiInfo.supported_formats.videos,
      ...apiInfo.supported_formats.audio,
      ...apiInfo.supported_formats.documents,
    ];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Minimize2 className="w-12 h-12 text-primary-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            File Compressor
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Compress images, videos, audio files, and documents with ease
          </p>
        </div>

        {/* Main Content */}
        {!result ? (
          <div className="card space-y-6">
            {/* File Upload */}
            <FileUpload
              onFileSelect={handleFileSelect}
              acceptedFormats={getAllSupportedFormats()}
              maxSize={apiInfo?.max_file_size_mb ? apiInfo.max_file_size_mb * 1024 * 1024 : undefined}
            />

            {/* Compression Controls */}
            {file && (
              <>
                <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                  <CompressionControls
                    strategy={strategy}
                    onStrategyChange={setStrategy}
                    quality={quality}
                    onQualityChange={setQuality}
                    targetSize={targetSize}
                    onTargetSizeChange={setTargetSize}
                    reductionPercentage={reductionPercentage}
                    onReductionPercentageChange={setReductionPercentage}
                  />
                </div>

                {/* Error Message */}
                {error && (
                  <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                    <div className="flex items-start gap-3">
                      <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <p className="text-red-800 dark:text-red-200">{error}</p>
                    </div>
                  </div>
                )}

                {/* Compress Button */}
                <button
                  onClick={handleCompress}
                  disabled={isCompressing}
                  className="btn-primary w-full py-3 text-lg"
                >
                  {isCompressing ? (
                    <span className="flex items-center justify-center gap-2">
                      <LoadingSpinner message="" />
                      Compressing...
                    </span>
                  ) : (
                    'Compress File'
                  )}
                </button>
              </>
            )}
          </div>
        ) : (
          <ResultDisplay
            result={result}
            onDownload={handleDownload}
            onReset={handleReset}
          />
        )}

        {/* Footer Info */}
        {apiInfo && (
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Supported formats: Images ({apiInfo.supported_formats.images.join(', ')}),
              Videos ({apiInfo.supported_formats.videos.join(', ')}),
              Audio ({apiInfo.supported_formats.audio.join(', ')}),
              Documents ({apiInfo.supported_formats.documents.join(', ')})
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
