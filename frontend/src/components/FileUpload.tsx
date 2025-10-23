import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File as FileIcon } from 'lucide-react';
import { formatBytes } from '../utils/fileUtils';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  acceptedFormats?: string[];
  maxSize?: number;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  acceptedFormats,
  maxSize = 500 * 1024 * 1024, // 500MB default
}) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } =
    useDropzone({
      onDrop,
      multiple: false,
      maxSize,
    });

  const selectedFile = acceptedFiles[0];

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
          transition-all duration-200
          ${
            isDragActive
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500'
          }
        `}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center space-y-4">
          <Upload
            className={`w-16 h-16 ${
              isDragActive ? 'text-primary-500' : 'text-gray-400'
            }`}
          />
          <div>
            <p className="text-lg font-semibold text-gray-700 dark:text-gray-200">
              {isDragActive
                ? 'Drop your file here'
                : 'Drag & drop your file here'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              or click to browse
            </p>
          </div>
          {acceptedFormats && (
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Supported formats: {acceptedFormats.join(', ')}
            </p>
          )}
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Max file size: {formatBytes(maxSize)}
          </p>
        </div>
      </div>

      {selectedFile && (
        <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div className="flex items-center space-x-3">
            <FileIcon className="w-8 h-8 text-primary-500" />
            <div className="flex-1">
              <p className="font-medium text-gray-900 dark:text-white">
                {selectedFile.name}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {formatBytes(selectedFile.size)}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
