import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Processing...',
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <Loader2 className="w-12 h-12 text-primary-600 animate-spin mb-4" />
      <p className="text-gray-700 dark:text-gray-300 font-medium">{message}</p>
    </div>
  );
};
