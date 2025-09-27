import CryptoJS from 'crypto-js';

// Base secret for key derivation (in production, use env variable)
const BASE_SECRET = 'tempris-time-capsule-secret-2025';

/**
 * Generate a unique encryption key for each time capsule
 * @param {string} capsuleId - Unique identifier for the capsule
 * @param {number} unlockTime - Timestamp when capsule unlocks
 * @param {string} userAddress - User's wallet address
 * @returns {string} Unique encryption key
 */
export function generateUniqueKey(capsuleId, unlockTime, userAddress) {
  try {
    // Create a unique key by combining multiple factors
    const keyMaterial = `${BASE_SECRET}:${capsuleId}:${unlockTime}:${userAddress}`;
    const uniqueKey = CryptoJS.SHA256(keyMaterial).toString();
    return uniqueKey;
  } catch (error) {
    console.error('Key generation error:', error);
    throw new Error('Failed to generate unique encryption key');
  }
}

/**
 * Generate a random decryption key for Hedera time-locking
 * @returns {string} Random decryption key
 */
export function generateDecryptionKey() {
  try {
    // Generate a cryptographically secure random key
    const randomBytes = CryptoJS.lib.WordArray.random(256/8); // 256-bit key
    return CryptoJS.enc.Hex.stringify(randomBytes);
  } catch (error) {
    console.error('Decryption key generation error:', error);
    throw new Error('Failed to generate decryption key');
  }
}

/**
 * Encrypt blob ID with a unique key for time-locked capsules
 * @param {string} blobId - The blob ID from Walrus to encrypt
 * @param {string} encryptionKey - Unique encryption key for this capsule
 * @returns {string} Encrypted blob ID
 */
export function encryptBlobIdWithKey(blobId, encryptionKey) {
  try {
    const encrypted = CryptoJS.AES.encrypt(blobId, encryptionKey).toString();
    return encrypted;
  } catch (error) {
    console.error('Encryption error:', error);
    throw new Error('Failed to encrypt blob ID');
  }
}

/**
 * Decrypt blob ID with a specific key
 * @param {string} encryptedBlobId - The encrypted blob ID
 * @param {string} decryptionKey - The key to decrypt with
 * @returns {string} Original blob ID
 */
export function decryptBlobIdWithKey(encryptedBlobId, decryptionKey) {
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedBlobId, decryptionKey);
    const originalBlobId = bytes.toString(CryptoJS.enc.Utf8);
    
    if (!originalBlobId) {
      throw new Error('Decryption failed - invalid data or key');
    }
    
    return originalBlobId;
  } catch (error) {
    console.error('Decryption error:', error);
    throw new Error('Failed to decrypt blob ID');
  }
}

/**
 * Legacy encrypt function for backward compatibility
 * @param {string} blobId - The blob ID from Walrus to encrypt
 * @returns {string} Encrypted blob ID
 */
export function encryptBlobId(blobId) {
  try {
    const encrypted = CryptoJS.AES.encrypt(blobId, BASE_SECRET).toString();
    return encrypted;
  } catch (error) {
    console.error('Encryption error:', error);
    throw new Error('Failed to encrypt blob ID');
  }
}

/**
 * Legacy decrypt function for backward compatibility
 * @param {string} encryptedBlobId - The encrypted blob ID
 * @returns {string} Original blob ID
 */
export function decryptBlobId(encryptedBlobId) {
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedBlobId, BASE_SECRET);
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

/**
 * Encrypt content data for storage in Walrus
 * @param {Object} contentData - The content data to encrypt
 * @param {string} encryptionKey - The encryption key
 * @returns {string} Encrypted content
 */
export function encryptContent(contentData, encryptionKey) {
  try {
    const contentString = JSON.stringify(contentData);
    const encrypted = CryptoJS.AES.encrypt(contentString, encryptionKey).toString();
    return encrypted;
  } catch (error) {
    console.error('Content encryption error:', error);
    throw new Error('Failed to encrypt content');
  }
}

/**
 * Decrypt content data from Walrus
 * @param {string} encryptedContent - The encrypted content
 * @param {string} decryptionKey - The decryption key
 * @returns {Object} Decrypted content data
 */
export function decryptContent(encryptedContent, decryptionKey) {
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedContent, decryptionKey);
    const decryptedString = bytes.toString(CryptoJS.enc.Utf8);
    
    if (!decryptedString) {
      throw new Error('Decryption failed - invalid content or key');
    }
    
    return JSON.parse(decryptedString);
  } catch (error) {
    console.error('Content decryption error:', error);
    throw new Error('Failed to decrypt content');
  }
}

/**
 * Hash data for verification purposes
 * @param {string} data - Data to hash
 * @returns {string} SHA256 hash
 */
export function hashData(data) {
  try {
    return CryptoJS.SHA256(data).toString();
  } catch (error) {
    console.error('Hashing error:', error);
    throw new Error('Failed to hash data');
  }
}