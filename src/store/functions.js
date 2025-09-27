import { encryptBlobId, generateCapsuleId } from '../lib/encryption.js';
import { mintTimeCapsuleNFT } from '../lib/nft.js';

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