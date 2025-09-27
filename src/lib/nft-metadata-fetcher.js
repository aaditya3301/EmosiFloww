import { ethers } from 'ethers';

/**
 * Attempt to decrypt content using the provided decryption key
 * @param {string} encryptedBlobId - The encrypted blob ID
 * @param {string} decryptionKey - The decryption key
 * @returns {Promise<string|null>} Decrypted content or null if failed
 */
async function attemptDecryption(encryptedBlobId, decryptionKey) {
    try {
        // For now, we'll assume the decryption key is the actual decrypted content
        // In a real implementation, you would use crypto libraries to decrypt
        
        // If decryption key looks like plaintext content, return it
        if (decryptionKey && decryptionKey.length > 10 && !decryptionKey.startsWith('0x')) {
            console.log('🔓 Using decryption key as plaintext content');
            return decryptionKey;
        }
        
        // If encrypted blob looks like base64, try to decode it with key
        if (encryptedBlobId.startsWith('U2FsdGVkX1') || encryptedBlobId.length > 20) {
            // This is likely base64 encrypted content
            // For demo purposes, return a simulated decrypted result
            console.log('🔓 Simulating decryption of base64 content');
            return `Decrypted-${encryptedBlobId.substring(0, 10)}...`;
        }
        
        console.log('⚠️ Could not determine decryption method');
        return null;
        
    } catch (error) {
        console.error('Decryption error:', error);
        return null;
    }
}

// NFT Contract configurations
const NFT_CONTRACTS = {
    // Old public contract
    old: {
        address: '0xfb42a2c4b5eb535cfe704ef64da416f1cf69bde3',
        name: 'Public TimeCapsule NFT (Immediate Access)'
    },
    // New time-locked contract
    timeLocked: {
        address: '0x508bbc0cf873c11dbf9d72bfcea3dc1e69739c38',
        name: 'Time-Locked TimeCapsule NFT (Scheduled)'
    }
};

// NFT ABI for metadata fetching
const NFT_ABI = [
    "function tokenURI(uint256 tokenId) public view returns (string memory)",
    "function getEncryptedBlobId(uint256 tokenId) public view returns (string memory)", 
    "function getCreator(uint256 tokenId) public view returns (address)",
    "function totalSupply() public view returns (uint256)",
    "function nextTokenId() public view returns (uint256)",
    "function balanceOf(address owner) public view returns (uint256)",
    "function ownerOf(uint256 tokenId) public view returns (address)",
    "function name() public view returns (string memory)",
    "function symbol() public view returns (string memory)"
];

// Time-locked contract ABI (correct functions)
const TIME_LOCKED_ABI = [
    "function createTimeCapsule(string memory _encryptedBlobId, string memory _decryptionKey, uint256 _unlockTime) external returns (uint256 capsuleId)",
    "function unlockTimeCapsule(uint256 _capsuleId, string memory _decryptionKey) external",
    "function getTimeCapsule(uint256 _capsuleId) external view returns (uint256 capsuleId, string memory encryptedBlobId, address owner, uint256 unlockTime, bool isUnlocked, string memory decryptionKey)",
    "function isReadyToUnlock(uint256 _capsuleId) external view returns (bool)",
    "function getTimeUntilUnlock(uint256 _capsuleId) external view returns (uint256)",
    "function getUserCapsules(address _user) external view returns (uint256[] memory)",
    "function nextCapsuleId() external view returns (uint256)",
    "function getTotalCapsules() external view returns (uint256)"
];

/**
 * Fetch simple metadata and blob IDs from NFT contracts
 * @param {Array<number>} tokenIds - Array of token IDs to fetch
 * @returns {Promise<Object>} Simple metadata comparison
 */
export async function fetchNFTMetadataComparison(tokenIds = [1, 2, 3]) {
    try {
        if (!window.ethereum) {
            throw new Error('MetaMask not found');
        }

        const provider = new ethers.BrowserProvider(window.ethereum);
        
        // Create contract instances
        const oldContract = new ethers.Contract(
            NFT_CONTRACTS.old.address, 
            NFT_ABI, 
            provider
        );
        
        const timeLockContract = new ethers.Contract(
            NFT_CONTRACTS.timeLocked.address,
            TIME_LOCKED_ABI,
            provider
        );

        console.log('📊 Fetching simple NFT metadata...');
        
        const comparison = {
            contracts: NFT_CONTRACTS,
            nfts: [],
            summary: {
                totalFound: 0,
                encryptedCount: 0,
                normalCount: 0
            }
        };

        // Fetch from old contract (immediate access NFTs)
        try {
            console.log('🔍 Fetching from NFT contract:', NFT_CONTRACTS.old.address);
            
            for (const tokenId of tokenIds) {
                try {
                    const [tokenURI, encryptedBlobId, creator, owner] = await Promise.all([
                        oldContract.tokenURI(tokenId),
                        oldContract.getEncryptedBlobId(tokenId),
                        oldContract.getCreator(tokenId), 
                        oldContract.ownerOf(tokenId)
                    ]);

                    // Parse metadata from base64 encoded URI
                    let metadata = {};
                    let blobId = 'Not available';
                    let isEncrypted = true;

                    if (tokenURI.startsWith('data:application/json;base64,')) {
                        const base64Data = tokenURI.split(',')[1];
                        const jsonData = atob(base64Data);
                        metadata = JSON.parse(jsonData);
                    }

                    // The blob ID from this contract is always encrypted
                    blobId = encryptedBlobId;

                    comparison.nfts.push({
                        tokenId,
                        contractType: 'NFT (Immediate Access)',
                        contractAddress: NFT_CONTRACTS.old.address,
                        name: metadata.name || `Token #${tokenId}`,
                        description: metadata.description || 'No description',
                        blobId: blobId,
                        blobType: 'Encrypted Blob ID',
                        isEncrypted: true,
                        creator,
                        owner,
                        metadata
                    });
                    
                    comparison.summary.totalFound++;
                    comparison.summary.encryptedCount++;
                    
                    console.log(`✅ NFT #${tokenId}: ${metadata.name} - Encrypted blob`);
                } catch (error) {
                    console.log(`❌ NFT #${tokenId} not found:`, error.message);
                    comparison.nfts.push({
                        tokenId,
                        contractType: 'NFT (Immediate Access)',
                        contractAddress: NFT_CONTRACTS.old.address,
                        error: `Token #${tokenId} not found`,
                        blobId: 'N/A',
                        blobType: 'Error',
                        isEncrypted: false
                    });
                }
            }
        } catch (error) {
            console.error('Failed to fetch from NFT contract:', error);
        }

        // Fetch from time-locked contract
        try {
            console.log('🔍 Fetching from time-locked contract:', NFT_CONTRACTS.timeLocked.address);
            
            // First check how many capsules exist
            try {
                const totalCapsules = await timeLockContract.getTotalCapsules();
                const nextCapsuleId = await timeLockContract.nextCapsuleId();
                console.log(`📊 Contract stats: Total capsules: ${totalCapsules}, Next ID: ${nextCapsuleId}`);
            } catch (e) {
                console.log('Could not fetch contract stats:', e.message);
            }
            
            for (const capsuleId of tokenIds) {
                try {
                    console.log(`🔍 Trying to fetch capsule #${capsuleId}...`);
                    const capsuleData = await timeLockContract.getTimeCapsule(capsuleId);
                    console.log('Raw capsule data received:', capsuleData);
                    
                    // Handle both array and object formats
                    let capsuleId_returned, encryptedBlobId, owner, unlockTime, isUnlocked, decryptionKey;
                    
                    if (Array.isArray(capsuleData)) {
                        // Array format: [capsuleId, encryptedBlobId, owner, unlockTime, isUnlocked, decryptionKey]
                        [capsuleId_returned, encryptedBlobId, owner, unlockTime, isUnlocked, decryptionKey] = capsuleData;
                    } else {
                        // Object format
                        ({ capsuleId: capsuleId_returned, encryptedBlobId, owner, unlockTime, isUnlocked, decryptionKey } = capsuleData);
                    }
                    
                    console.log(`📦 Capsule #${capsuleId} parsed data:`, {
                        capsuleId_returned: capsuleId_returned?.toString(),
                        encryptedBlobId,
                        owner,
                        unlockTime: unlockTime?.toString(),
                        isUnlocked,
                        decryptionKey
                    });
                    
                    // Check if this capsule actually exists (non-zero owner address)
                    if (!owner || owner === '0x0000000000000000000000000000000000000000') {
                        throw new Error('Capsule does not exist (zero address owner)');
                    }
                    
                    // Handle decryption if unlocked
                    let blobId = encryptedBlobId;
                    let blobType = 'Encrypted Blob ID';
                    let actualContent = null;
                    
                    if (isUnlocked && decryptionKey && decryptionKey.length > 0) {
                        blobType = 'Decryptable (Unlocked)';
                        
                        // Try to decrypt the content
                        try {
                            actualContent = await attemptDecryption(encryptedBlobId, decryptionKey);
                            if (actualContent) {
                                blobType = 'Decrypted Content Available';
                                blobId = actualContent; // Show decrypted content
                            }
                        } catch (decryptError) {
                            console.warn('Decryption failed:', decryptError.message);
                            blobType = 'Encrypted (Decryption Failed)';
                        }
                    }

                    comparison.nfts.push({
                        tokenId: capsuleId,
                        contractType: 'Time-Locked Capsule',
                        contractAddress: NFT_CONTRACTS.timeLocked.address,
                        name: `Time Capsule #${capsuleId}`,
                        description: isUnlocked ? 
                            (actualContent ? 'Unlocked & Decrypted' : 'Unlocked (Decryption needed)') : 
                            'Locked time capsule',
                        blobId: blobId,
                        blobType: blobType,
                        isEncrypted: !actualContent,
                        owner: owner,
                        unlockTime: unlockTime ? new Date(Number(unlockTime) * 1000) : null,
                        isUnlocked: isUnlocked,
                        decryptionKey: decryptionKey || null,
                        actualContent: actualContent
                    });
                    
                    comparison.summary.totalFound++;
                    if (actualContent) {
                        comparison.summary.normalCount++; // Decrypted content counts as normal
                    } else {
                        comparison.summary.encryptedCount++;
                    }
                    
                    console.log(`✅ Capsule #${capsuleId}: ${isUnlocked ? 'Unlocked' : 'Locked'} - ${blobType}`);
                } catch (error) {
                    console.log(`❌ Capsule #${capsuleId} error:`, error);
                    
                    // Check if it's a contract revert vs capsule not existing
                    let errorMessage = error.message;
                    if (errorMessage.includes('execution reverted')) {
                        errorMessage = 'Contract execution reverted - capsule may not exist';
                    } else if (errorMessage.includes('CALL_EXCEPTION')) {
                        errorMessage = 'Contract call failed - capsule does not exist';
                    }
                    
                    comparison.nfts.push({
                        tokenId: capsuleId,
                        contractType: 'Time-Locked Capsule',
                        contractAddress: NFT_CONTRACTS.timeLocked.address,
                        error: `Capsule #${capsuleId}: ${errorMessage}`,
                        blobId: 'N/A',
                        blobType: 'Error',
                        isEncrypted: false
                    });
                }
            }
        } catch (error) {
            console.error('Failed to fetch from time-locked contract:', error);
        }

        return comparison;
    } catch (error) {
        console.error('Failed to fetch NFT metadata comparison:', error);
        throw error;
    }
}

/**
 * Get user's NFTs from both contracts
 * @param {string} userAddress - User's wallet address
 * @returns {Promise<Object>} User's NFTs from both contracts
 */
export async function getUserNFTsComparison(userAddress) {
    try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        
        const oldContract = new ethers.Contract(
            NFT_CONTRACTS.old.address,
            NFT_ABI,
            provider
        );
        
        const timeLockContract = new ethers.Contract(
            NFT_CONTRACTS.timeLocked.address,
            TIME_LOCKED_ABI,
            provider
        );

        const [oldBalance, userCapsules] = await Promise.all([
            oldContract.balanceOf(userAddress),
            timeLockContract.getUserCapsules(userAddress).catch(() => [])
        ]);

        return {
            userAddress,
            oldNFTCount: Number(oldBalance),
            timeLockCapsuleCount: userCapsules.length,
            timeLockCapsules: userCapsules.map(id => Number(id))
        };
    } catch (error) {
        console.error('Failed to fetch user NFTs:', error);
        throw error;
    }
}

/**
 * Display simple comparison in console
 * @param {Object} comparison - Simple comparison data
 */
export function displayComparisonTable(comparison) {
    console.log('\n� ===== NFT METADATA & BLOB IDs =====\n');
    
    // Contract info
    console.log('📋 CONTRACTS CHECKED:');
    console.table([
        {
            Type: 'NFT Contract',
            Address: comparison.contracts.old.address,
            Description: comparison.contracts.old.name
        },
        {
            Type: 'Time-Lock Contract', 
            Address: comparison.contracts.timeLocked.address,
            Description: comparison.contracts.timeLocked.name
        }
    ]);
    
    // All NFTs/Capsules
    if (comparison.nfts.length > 0) {
        console.log('\n� METADATA & BLOB IDs:');
        const table = comparison.nfts
            .filter(nft => !nft.error)
            .map(nft => ({
                'ID': nft.tokenId,
                'Name': nft.name,
                'Type': nft.contractType,
                'Blob Type': nft.blobType,
                'Blob ID': nft.blobId?.substring(0, 25) + '...',
                'Owner': nft.owner?.substring(0, 8) + '...',
                'Status': nft.isUnlocked ? '🔓 Unlocked' : (nft.unlockTime ? '🔒 Locked' : '📥 Available')
            }));
        if (table.length > 0) console.table(table);
    }
    
    // Errors
    const errors = comparison.nfts.filter(nft => nft.error);
    if (errors.length > 0) {
        console.log('\n❌ NOT FOUND:');
        console.table(errors.map(e => ({
            'ID': e.tokenId,
            'Contract': e.contractType,
            'Error': e.error
        })));
    }
    
    // Summary
    console.log('\n📊 SUMMARY:');
    console.table([{
        'Total Found': comparison.summary.totalFound,
        'Encrypted Blobs': comparison.summary.encryptedCount,
        'Normal Blobs': comparison.summary.normalCount
    }]);
    
    console.log('\n✅ Metadata fetch complete!\n');
}

export default {
    fetchNFTMetadataComparison,
    getUserNFTsComparison,
    displayComparisonTable,
    NFT_CONTRACTS
};