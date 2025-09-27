import { ethers } from 'ethers';

// Your contract details
const CONTRACT_ADDRESS = '0xfb42a2c4b5eb535cfe704ef64da416f1cf69bde3';
const CONTRACT_ABI = [
  "function tokenURI(uint256 tokenId) public view returns (string memory)",
  "function getEncryptedBlobId(uint256 tokenId) public view returns (string memory)",
  "function getCreator(uint256 tokenId) public view returns (address)",
  "function ownerOf(uint256 tokenId) public view returns (address)"
];

/**
 * Decode NFT metadata and show encrypted content
 * @param {number} tokenId - The NFT token ID
 */
export async function decodeNFTData(tokenId) {
  try {
    if (!window.ethereum) {
      throw new Error('MetaMask not found');
    }

    const provider = new ethers.BrowserProvider(window.ethereum);   
    const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, provider);
    
    console.log(`🔍 Decoding NFT Token ID: ${tokenId}`);
    console.log('📍 Contract:', CONTRACT_ADDRESS);
    
    // Get basic NFT info
    const owner = await contract.ownerOf(tokenId);
    const creator = await contract.getCreator(tokenId);
    const encryptedBlobId = await contract.getEncryptedBlobId(tokenId);
    const tokenURI = await contract.tokenURI(tokenId);
    
    console.log('👤 Owner:', owner);
    console.log('🎨 Creator:', creator);
    console.log('🔐 Encrypted Blob ID:', encryptedBlobId);
    
    // Decode metadata URI
    if (tokenURI.startsWith('data:application/json;base64,')) {
      const base64Data = tokenURI.replace('data:application/json;base64,', '');
      const jsonData = JSON.parse(atob(base64Data));
      
      console.log('📋 NFT Metadata:');
      console.log('- Name:', jsonData.name);
      console.log('- Description:', jsonData.description);
      console.log('- Capsule ID:', jsonData.capsuleId);
      console.log('- Encrypted Blob ID (from metadata):', jsonData.encryptedBlobId);
      console.log('- Creation Date:', jsonData.attributes?.find(a => a.trait_type === 'Created')?.value);
      
      return {
        tokenId: tokenId,
        owner: owner,
        creator: creator,
        encryptedBlobId: encryptedBlobId,
        metadata: jsonData,
        capsuleId: jsonData.capsuleId
      };
    }
    
    return {
      tokenId: tokenId,
      owner: owner,
      creator: creator,
      encryptedBlobId: encryptedBlobId,
      tokenURI: tokenURI
    };
    
  } catch (error) {
    console.error('❌ Error decoding NFT:', error);
    return { error: error.message };
  }
}

/**
 * Decrypt the encrypted blob ID to get the original Walrus CID
 * @param {string} encryptedBlobId - The encrypted blob ID from NFT
 */
export async function decryptBlobId(encryptedBlobId) {
  try {
    const CryptoJS = await import('crypto-js');
    const secretKey = 'tempris-time-capsule-secret-2025'; // Same key used for encryption
    
    console.log('🔓 Decrypting blob ID...');
    console.log('🔐 Encrypted:', encryptedBlobId);
    
    const decryptedBytes = CryptoJS.AES.decrypt(encryptedBlobId, secretKey);
    const originalBlobId = decryptedBytes.toString(CryptoJS.enc.Utf8);
    
    console.log('✅ Original Walrus Blob ID:', originalBlobId);
    
    // Generate Walrus download URL
    const walrusUrl = `https://aggregator.walrus-testnet.walrus.space/v1/blobs/${originalBlobId}`;
    console.log('🔗 Walrus Download URL:', walrusUrl);
    
    return {
      originalBlobId: originalBlobId,
      walrusUrl: walrusUrl,
      encryptedBlobId: encryptedBlobId
    };
    
  } catch (error) {
    console.error('❌ Decryption failed:', error);
    return { error: error.message };
  }
}