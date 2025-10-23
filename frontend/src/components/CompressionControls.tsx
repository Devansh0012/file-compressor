import React from 'react';
import { CompressionStrategy } from '../types';

interface CompressionControlsProps {
  strategy: CompressionStrategy;
  onStrategyChange: (strategy: CompressionStrategy) => void;
  quality: number;
  onQualityChange: (quality: number) => void;
  targetSize: number;
  onTargetSizeChange: (size: number) => void;
  reductionPercentage: number;
  onReductionPercentageChange: (percentage: number) => void;
}

export const CompressionControls: React.FC<CompressionControlsProps> = ({
  strategy,
  onStrategyChange,
  quality,
  onQualityChange,
  targetSize,
  onTargetSizeChange,
  reductionPercentage,
  onReductionPercentageChange,
}) => {
  return (
    <div className="space-y-6">
      {/* Strategy Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Compression Strategy
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            type="button"
            onClick={() => onStrategyChange(CompressionStrategy.QUALITY)}
            className={`p-4 rounded-lg border-2 transition-all ${
              strategy === CompressionStrategy.QUALITY
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'
            }`}
          >
            <div className="text-left">
              <h3 className="font-semibold text-gray-900 dark:text-white">Quality</h3>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Set compression quality level
              </p>
            </div>
          </button>

          <button
            type="button"
            onClick={() => onStrategyChange(CompressionStrategy.TARGET_SIZE)}
            className={`p-4 rounded-lg border-2 transition-all ${
              strategy === CompressionStrategy.TARGET_SIZE
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'
            }`}
          >
            <div className="text-left">
              <h3 className="font-semibold text-gray-900 dark:text-white">Target Size</h3>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Compress to specific size
              </p>
            </div>
          </button>

          <button
            type="button"
            onClick={() => onStrategyChange(CompressionStrategy.PERCENTAGE)}
            className={`p-4 rounded-lg border-2 transition-all ${
              strategy === CompressionStrategy.PERCENTAGE
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'
            }`}
          >
            <div className="text-left">
              <h3 className="font-semibold text-gray-900 dark:text-white">Percentage</h3>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Reduce by percentage
              </p>
            </div>
          </button>
        </div>
      </div>

      {/* Strategy-specific Controls */}
      <div>
        {strategy === CompressionStrategy.QUALITY && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Quality: {quality}%
            </label>
            <input
              type="range"
              min="1"
              max="100"
              value={quality}
              onChange={(e) => onQualityChange(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              title="Adjust quality percentage"
              aria-label="Quality percentage slider"
            />
            <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
              <span>Low Quality</span>
              <span>High Quality</span>
            </div>
          </div>
        )}

        {strategy === CompressionStrategy.TARGET_SIZE && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Target Size (MB)
            </label>
            <input
              type="number"
              min="0.1"
              step="0.1"
              value={targetSize}
              onChange={(e) => onTargetSizeChange(parseFloat(e.target.value))}
              className="input-field"
              placeholder="Enter target size in MB"
              title="Enter target size in MB"
              aria-label="Target size in megabytes"
            />
          </div>
        )}

        {strategy === CompressionStrategy.PERCENTAGE && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Reduction: {reductionPercentage}%
            </label>
            <input
              type="range"
              min="1"
              max="99"
              value={reductionPercentage}
              onChange={(e) => onReductionPercentageChange(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              title="Adjust reduction percentage"
              aria-label="Reduction percentage slider"
            />
            <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
              <span>1% Reduction</span>
              <span>99% Reduction</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
