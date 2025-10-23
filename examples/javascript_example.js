/**
 * Example JavaScript/Node.js Script: Using the File Compressor API
 * 
 * This script demonstrates how to use the File Compressor API from JavaScript.
 * Run with: node javascript_example.js
 */

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * File Compressor API Client
 */
class FileCompressorClient {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get API information and supported formats
   */
  async getInfo() {
    const response = await axios.get(`${this.baseUrl}/compress/info`);
    return response.data;
  }

  /**
   * Compress a file using specified strategy
   * 
   * @param {string} filePath - Path to file to compress
   * @param {Object} compressionData - Compression parameters
   * @returns {Object} Compression result with download URL
   */
  async compressFile(filePath, compressionData) {
    const formData = new FormData();
    
    // Add file
    formData.append('file', fs.createReadStream(filePath));
    
    // Add compression data
    formData.append('compression_data', JSON.stringify(compressionData));
    
    // Make request
    const response = await axios.post(
      `${this.baseUrl}/compress/`,
      formData,
      {
        headers: formData.getHeaders(),
      }
    );
    
    return response.data;
  }

  /**
   * Download a compressed file
   * 
   * @param {string} downloadUrl - URL returned from compressFile
   * @param {string} outputPath - Path where to save the file
   */
  async downloadFile(downloadUrl, outputPath) {
    const fullUrl = `http://localhost:8000${downloadUrl}`;
    
    const response = await axios.get(fullUrl, {
      responseType: 'stream',
    });
    
    const writer = fs.createWriteStream(outputPath);
    response.data.pipe(writer);
    
    return new Promise((resolve, reject) => {
      writer.on('finish', () => {
        console.log(`File saved to: ${outputPath}`);
        resolve();
      });
      writer.on('error', reject);
    });
  }
}

/**
 * Example 1: Compress image with quality strategy
 */
async function exampleCompressImageQuality() {
  console.log('\n=== Example 1: Compress Image by Quality ===');
  
  const client = new FileCompressorClient();
  
  try {
    // Compress with quality 75
    const result = await client.compressFile('sample_image.jpg', {
      strategy: 'quality',
      quality: 75,
    });
    
    console.log(`Original size: ${(result.original_size / 1024).toFixed(2)} KB`);
    console.log(`Compressed size: ${(result.compressed_size / 1024).toFixed(2)} KB`);
    console.log(`Reduction: ${result.reduction_percentage.toFixed(2)}%`);
    
    // Download compressed file
    await client.downloadFile(result.download_url, 'compressed_image.jpg');
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

/**
 * Example 2: Compress video to target size
 */
async function exampleCompressVideoTargetSize() {
  console.log('\n=== Example 2: Compress Video to Target Size ===');
  
  const client = new FileCompressorClient();
  
  try {
    // Compress to 10MB
    const result = await client.compressFile('sample_video.mp4', {
      strategy: 'target_size',
      target_size_mb: 10.0,
    });
    
    console.log(`Original size: ${(result.original_size / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`Compressed size: ${(result.compressed_size / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`Reduction: ${result.reduction_percentage.toFixed(2)}%`);
    
    await client.downloadFile(result.download_url, 'compressed_video.mp4');
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

/**
 * Example 3: Compress audio by percentage
 */
async function exampleCompressAudioPercentage() {
  console.log('\n=== Example 3: Compress Audio by Percentage ===');
  
  const client = new FileCompressorClient();
  
  try {
    // Reduce by 50%
    const result = await client.compressFile('sample_audio.mp3', {
      strategy: 'percentage',
      reduction_percentage: 50,
    });
    
    console.log(`Original size: ${(result.original_size / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`Compressed size: ${(result.compressed_size / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`Reduction: ${result.reduction_percentage.toFixed(2)}%`);
    
    await client.downloadFile(result.download_url, 'compressed_audio.mp3');
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

/**
 * Example 4: Batch compress multiple files
 */
async function exampleBatchCompress() {
  console.log('\n=== Example 4: Batch Compress Multiple Files ===');
  
  const client = new FileCompressorClient();
  
  const filesToCompress = [
    { path: 'image1.jpg', strategy: 'quality', params: { quality: 80 } },
    { path: 'image2.png', strategy: 'quality', params: { quality: 75 } },
    { path: 'video.mp4', strategy: 'target_size', params: { target_size_mb: 5.0 } },
  ];
  
  const results = [];
  
  for (const file of filesToCompress) {
    try {
      const compressionData = { strategy: file.strategy, ...file.params };
      const result = await client.compressFile(file.path, compressionData);
      
      results.push({
        file: file.path,
        success: true,
        reduction: result.reduction_percentage,
      });
      
      // Download with prefix
      const outputName = `compressed_${path.basename(file.path)}`;
      await client.downloadFile(result.download_url, outputName);
      
    } catch (error) {
      results.push({
        file: file.path,
        success: false,
        error: error.response?.data?.detail || error.message,
      });
    }
  }
  
  // Print summary
  console.log('\nBatch Compression Summary:');
  results.forEach((r) => {
    if (r.success) {
      console.log(`✅ ${r.file}: ${r.reduction.toFixed(2)}% reduction`);
    } else {
      console.log(`❌ ${r.file}: ${r.error}`);
    }
  });
}

/**
 * Example 5: Get API information
 */
async function exampleGetApiInfo() {
  console.log('\n=== Example 5: Get API Information ===');
  
  const client = new FileCompressorClient();
  
  try {
    const info = await client.getInfo();
    
    console.log(`Max file size: ${info.max_file_size_mb} MB`);
    console.log('\nSupported formats:');
    Object.entries(info.supported_formats).forEach(([category, formats]) => {
      console.log(`  ${category}: ${formats.join(', ')}`);
    });
    console.log(`\nCompression strategies: ${info.compression_strategies.join(', ')}`);
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

/**
 * Main function
 */
async function main() {
  console.log('File Compressor API - Usage Examples');
  console.log('='.repeat(50));
  
  // Get API info first
  await exampleGetApiInfo();
  
  // Note: Uncomment examples below if you have sample files
  // await exampleCompressImageQuality();
  // await exampleCompressVideoTargetSize();
  // await exampleCompressAudioPercentage();
  // await exampleBatchCompress();
  
  console.log('\n' + '='.repeat(50));
  console.log('Examples complete!');
  console.log('\nNote: Make sure the API server is running at http://localhost:8000');
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { FileCompressorClient };
