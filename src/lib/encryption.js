import CryptoJS from 'crypto-js';

// Hardcoded secret key for encryption (in production, use env variable)
const SECRET_KEY = 'tempris-time-capsule-secret-2025';

/**
 * Encrypt blob ID with simple AES encryption
 * @param {string} blobId - The blob ID from Walrus to encrypt
 * @returns {string} Encrypted blob ID
 */
export function encryptBlobId(blobId) {
  try {
    const encrypted = CryptoJS.AES.encrypt(blobId, SECRET_KEY).toString();
    return encrypted;
  } catch (error) {
    console.error('Encryption error:', error);
    throw new Error('Failed to encrypt blob ID');
  }
}

/**
 * Decrypt blob ID 
 * @param {string} encryptedBlobId - The encrypted blob ID
 * @returns {string} Original blob ID
 */
export function decryptBlobId(encryptedBlobId) {
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedBlobId, SECRET_KEY);
    const originalBlobId = bytes.toString(CryptoJS.enc.Utf8);
    
    if (!originalBlobId) {
      throw new Error('Decryption failed - invalid data');
    }
    
    return originalBlobId;
  } catch (error) {
    console.error('Decryption error:', error);
    throw new Error('Failed to decrypt blob ID');
  }
}

/**
 * Generate a unique capsule ID for the NFT
 * @returns {string} Unique capsule ID
 */
export function generateCapsuleId() {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 15);
  return `capsule_${timestamp}_${random}`;
}