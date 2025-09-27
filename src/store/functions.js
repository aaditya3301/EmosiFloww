import { 
  encryptBlobId, 
  generateCapsuleId, 
  generateUniqueKey, 
  generateDecryptionKey, 
  encryptBlobIdWithKey,
  encryptContent 
} from '../lib/encryption.js';
import { mintTimeCapsuleNFT } from '../lib/nft.js';
import timeCapsuleScheduler from '../lib/hedera-scheduler.js';

/**
 * Upload a single file to Walrus storage.
 * @param {File} file - Single file to upload
 * @param {number} epochs - Number of epochs to store (default: 1)
 * @returns {Promise<{blobId: string, fileUrl: string}>} Blob ID and download URL
 */
export async function walrus(file, epochs = 1) {
  try {
    if (!file) {
      throw new Error("No file provided");
    }

    console.log(`Uploading ${file.name} to Walrus...`);

    // Use the exact Walrus testnet publisher endpoint from curl command
    const walrusUrl = `https://publisher.walrus-testnet.walrus.space/v1/blobs?epochs=${epochs}`;
    
    const response = await fetch(walrusUrl, {
      method: "PUT",
      body: file, // Upload file directly as binary data (equivalent to --upload-file)
      headers: {
        'Content-Type': file.type || 'application/octet-stream'
      }
    });

    if (!response.ok) {
      throw new Error(`Walrus upload failed: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Walrus response:", data);

    let blobId;
    if (data.newlyCreated) {
      blobId = data.newlyCreated.blobObject.blobId;
    } else if (data.alreadyCertified) {
      blobId = data.alreadyCertified.blobId;
    } else {
      throw new Error("No blob ID found in Walrus response");
    }

    // Generate download URL using aggregator
    const fileUrl = `https://aggregator.walrus-testnet.walrus.space/v1/${blobId}`;

    return {
      blobId: blobId,
      fileUrl: fileUrl,
    };
  } catch (err) {
    console.error("Walrus upload error:", err);
    throw err;
  }
}

/**
 * Complete time capsule creation: Upload to Walrus + Encrypt + Mint NFT
 * @param {File} file - File to upload
 * @param {number} epochs - Storage epochs (default: 5)
 * @param {object} metadata - Additional metadata for the NFT
 * @returns {Promise<{blobId: string, fileUrl: string, encryptedBlobId: string, capsuleId: string, nftResult: object}>}
 */
export async function createTimeCapsule(file, epochs = 5, metadata = {}) {
  try {
    console.log(`🚀 Creating time capsule for ${file.name}...`);
    
    // Step 1: Upload file to Walrus
    console.log('📁 Step 1: Uploading to Walrus...');
    const walrusResult = await walrus(file, epochs);
    
    // Step 2: Encrypt the blob ID
    console.log('🔐 Step 2: Encrypting blob ID...');
    const encryptedBlobId = encryptBlobId(walrusResult.blobId);
    
    // Step 3: Generate unique capsule ID
    const capsuleId = generateCapsuleId();
    
    // Step 4: Mint NFT with encrypted blob ID
    console.log('🎨 Step 3: Minting NFT...');
    const nftResult = await mintTimeCapsuleNFT(
      encryptedBlobId, 
      capsuleId,
      {
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type,
        uploadDate: new Date().toISOString(),
        storageEpochs: epochs,
        ...metadata
      }
    );
    
    if (!nftResult.success) {
      throw new Error(`NFT minting failed: ${nftResult.error}`);
    }
    
    console.log('✅ Time capsule created successfully!');
    console.log('📦 Capsule ID:', capsuleId);
    console.log('🔗 Blob ID:', walrusResult.blobId);
    console.log('🔐 Encrypted:', encryptedBlobId.substring(0, 20) + '...');
    console.log('🎨 NFT Token ID:', nftResult.tokenId);
    console.log('💎 Transaction:', nftResult.txHash);
    
    return {
      // Original Walrus data
      blobId: walrusResult.blobId,
      fileUrl: walrusResult.fileUrl,
      // Encryption data
      encryptedBlobId: encryptedBlobId,
      capsuleId: capsuleId,
      // NFT data
      nftResult: nftResult
    };
    
  } catch (error) {
    console.error('❌ Time capsule creation failed:', error);
    throw error;
  }
}

/**
 * Create a scheduled time capsule using Hedera for true time-locking
 * @param {File} file - File to upload
 * @param {number} unlockTime - Unix timestamp when capsule unlocks
 * @param {string} userAddress - User's wallet address
 * @param {number} epochs - Storage epochs (default: 10 for long-term storage)
 * @param {object} metadata - Additional metadata for the NFT
 * @returns {Promise<object>} Complete time capsule creation result
 */
export async function createScheduledTimeCapsule(file, unlockTime, userAddress, epochs = 10, metadata = {}) {
  try {
    console.log(`⏰ Creating scheduled time capsule for ${file.name}...`);
    console.log(`🔓 Unlock time: ${new Date(unlockTime * 1000).toLocaleString()}`);
    
    // Step 1: Generate unique identifiers and keys
    const capsuleId = generateCapsuleId();
    const decryptionKey = generateDecryptionKey();
    const uniqueKey = generateUniqueKey(capsuleId, unlockTime, userAddress);
    
    console.log('🔑 Generated unique encryption key for capsule');
    
    // Step 2: Prepare content with metadata
    const contentData = {
      fileName: file.name,
      fileSize: file.size,
      fileType: file.type,
      uploadDate: new Date().toISOString(),
      unlockTime: unlockTime,
      owner: userAddress,
      storageEpochs: epochs,
      ...metadata
    };
    
    // Step 3: Encrypt the entire content
    console.log('🔐 Step 1: Encrypting content with unique key...');
    const encryptedContent = encryptContent(contentData, uniqueKey);
    
    // Create a blob with encrypted content and original file
    const combinedData = {
      encryptedMetadata: encryptedContent,
      file: file
    };
    
    // Convert combined data to blob for upload
    const combinedBlob = new Blob([JSON.stringify(combinedData)], { 
      type: 'application/json' 
    });
    
    // Step 4: Upload encrypted content to Walrus
    console.log('📁 Step 2: Uploading encrypted content to Walrus...');
    const walrusResult = await walrus(combinedBlob, epochs);
    
    // Step 5: Encrypt the blob ID with the unique key
    console.log('🔐 Step 3: Double-encrypting blob ID...');
    const encryptedBlobId = encryptBlobIdWithKey(walrusResult.blobId, uniqueKey);
    
    // Step 6: Create scheduled time capsule on Hedera
    console.log('⏰ Step 4: Creating scheduled time capsule on Ethereum...');
    const hederaResult = await timeCapsuleScheduler.createScheduledTimeCapsule(
      encryptedBlobId,
      decryptionKey,
      unlockTime
    );
    
    if (!hederaResult.success) {
      throw new Error(`Hedera scheduling failed: ${hederaResult.error}`);
    }
    
    // Step 7: Mint NFT with Hedera capsule information
    console.log('🎨 Step 5: Minting NFT with time-lock data...');
    const nftMetadata = {
      fileName: file.name,
      fileSize: file.size,
      fileType: file.type,
      uploadDate: new Date().toISOString(),
      unlockTime: unlockTime,
      unlockDate: new Date(unlockTime * 1000).toISOString(),
      storageEpochs: epochs,
      hederaCapsuleId: hederaResult.capsuleId,
      scheduleId: hederaResult.scheduleId,
      isScheduled: true,
      ...metadata
    };
    
    const nftResult = await mintTimeCapsuleNFT(
      encryptedBlobId, 
      capsuleId,
      nftMetadata
    );
    
    if (!nftResult.success) {
      throw new Error(`NFT minting failed: ${nftResult.error}`);
    }
    
    console.log('✅ Scheduled time capsule created successfully!');
    console.log('📦 Capsule ID:', capsuleId);
    console.log('⏰ Hedera Capsule ID:', hederaResult.capsuleId);
    console.log('📅 Schedule ID:', hederaResult.scheduleId);
    console.log('🔗 Encrypted Blob ID:', walrusResult.blobId);
    console.log('🎨 NFT Token ID:', nftResult.tokenId);
    console.log('🔓 Unlocks at:', new Date(unlockTime * 1000).toLocaleString());
    
    return {
      // Original data
      blobId: walrusResult.blobId,
      fileUrl: walrusResult.fileUrl,
      capsuleId: capsuleId,
      // Hedera data
      hederaCapsuleId: hederaResult.capsuleId,
      scheduleId: hederaResult.scheduleId,
      unlockTime: unlockTime,
      // Encryption data
      encryptedBlobId: encryptedBlobId,
      uniqueKey: uniqueKey, // Store for later verification
      decryptionKey: decryptionKey, // Store securely
      // NFT data
      nftResult: nftResult,
      // Status
      isScheduled: true,
      isTimeLocked: true
    };
    
  } catch (error) {
    console.error('❌ Scheduled time capsule creation failed:', error);
    throw error;
  }
}

/**
 * Check the status of a scheduled time capsule
 * @param {number} hederaCapsuleId - Hedera capsule ID
 * @returns {Promise<object>} Capsule status information
 */
export async function checkTimeCapsuleStatus(hederaCapsuleId) {
  try {
    console.log(`🔍 Checking status for Hedera capsule ${hederaCapsuleId}...`);
    
    const capsuleData = await timeCapsuleScheduler.getTimeCapsule(hederaCapsuleId);
    const isReady = await timeCapsuleScheduler.isReadyToUnlock(hederaCapsuleId);
    const timeUntilUnlock = await timeCapsuleScheduler.getTimeUntilUnlock(hederaCapsuleId);
    
    return {
      capsuleId: capsuleData.capsuleId,
      encryptedBlobId: capsuleData.encryptedBlobId,
      owner: capsuleData.owner,
      unlockTime: capsuleData.unlockTime,
      isUnlocked: capsuleData.isUnlocked,
      isReady: isReady,
      timeUntilUnlock: timeUntilUnlock,
      decryptionKey: capsuleData.decryptionKey // Only available if unlocked
    };
  } catch (error) {
    console.error('❌ Failed to check time capsule status:', error);
    throw error;
  }
}

/**
 * Unlock a scheduled time capsule manually (if time has passed)
 * @param {number} hederaCapsuleId - Hedera capsule ID
 * @param {string} decryptionKey - The decryption key
 * @returns {Promise<object>} Unlock result
 */
export async function unlockScheduledTimeCapsule(hederaCapsuleId, decryptionKey) {
  try {
    console.log(`🔓 Attempting to unlock Hedera capsule ${hederaCapsuleId}...`);
    
    const result = await timeCapsuleScheduler.manualUnlockTimeCapsule(hederaCapsuleId, decryptionKey);
    
    if (result.success) {
      console.log('✅ Time capsule unlocked successfully!');
      console.log('💎 Transaction:', result.transactionId);
    }
    
    return result;
  } catch (error) {
    console.error('❌ Failed to unlock time capsule:', error);
    throw error;
  }
}