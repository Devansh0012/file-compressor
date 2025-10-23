import React from 'react';
import { Download, CheckCircle, FileDown } from 'lucide-react';
import { CompressionResponse } from '../types';
import { formatBytes } from '../utils/fileUtils';

interface ResultDisplayProps {
  result: CompressionResponse;
  onDownload: () => void;
  onReset: () => void;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({
  result,
  onDownload,
  onReset,
}) => {
  return (
    <div className="card">
      <div className="text-center mb-6">
        <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Compression Successful!
        </h2>
        <p className="text-gray-600 dark:text-gray-400">{result.message}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
            Original Size
          </p>
          <p className="text-xl font-semibold text-gray-900 dark:text-white">
            {formatBytes(result.original_size)}
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
            Compressed Size
          </p>
          <p className="text-xl font-semibold text-green-600">
            {formatBytes(result.compressed_size)}
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
            Size Reduced
          </p>
          <p className="text-xl font-semibold text-primary-600">
            {result.reduction_percentage.toFixed(2)}%
          </p>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-3">
        <button onClick={onDownload} className="btn-primary flex-1 flex items-center justify-center gap-2">
          <Download className="w-5 h-5" />
          Download Compressed File
        </button>
        <button onClick={onReset} className="btn-secondary flex items-center justify-center gap-2">
          <FileDown className="w-5 h-5" />
          Compress Another File
        </button>
      </div>
    </div>
  );
};
