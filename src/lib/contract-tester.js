import { ethers } from 'ethers';

// Contract configuration
const TIME_CAPSULE_CONTRACT_ADDRESS = '0x508bbc0cf873c11dbf9d72bfcea3dc1e69739c38';
const TIME_CAPSULE_ABI = [
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
 * Test the time capsule contract
 */
export async function testTimeCapsuleContract() {
    try {
        if (!window.ethereum) {
            throw new Error('MetaMask not found');
        }

        console.log('🧪 Testing Time Capsule Contract...');
        console.log('📍 Contract Address:', TIME_CAPSULE_CONTRACT_ADDRESS);

        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        const contract = new ethers.Contract(TIME_CAPSULE_CONTRACT_ADDRESS, TIME_CAPSULE_ABI, signer);

        // Test 1: Get contract stats
        console.log('\n📊 Contract Statistics:');
        try {
            const totalCapsules = await contract.getTotalCapsules();
            const nextCapsuleId = await contract.nextCapsuleId();
            console.log(`Total Capsules: ${totalCapsules}`);
            console.log(`Next Capsule ID: ${nextCapsuleId}`);
        } catch (e) {
            console.error('❌ Failed to get contract stats:', e.message);
        }

        // Test 2: Try to get user's capsules
        console.log('\n👤 User Capsules:');
        try {
            const userAddress = await signer.getAddress();
            const userCapsules = await contract.getUserCapsules(userAddress);
            console.log(`User Address: ${userAddress}`);
            console.log(`User Capsules: [${userCapsules.join(', ')}]`);
        } catch (e) {
            console.error('❌ Failed to get user capsules:', e.message);
        }

        // Test 3: Try to fetch capsules 0-10 (extended range)
        console.log('\n🔍 Testing Capsule Fetching (IDs 0-10):');
        let existingCapsules = [];
        
        for (let i = 0; i <= 10; i++) {
            try {
                const capsule = await contract.getTimeCapsule(i);
                
                // Check if capsule actually exists (has non-zero owner)
                if (capsule.owner && capsule.owner !== '0x0000000000000000000000000000000000000000') {
                    existingCapsules.push(i);
                    console.log(`✅ Capsule #${i}:`, {
                        capsuleId: capsule.capsuleId.toString(),
                        encryptedBlobId: capsule.encryptedBlobId.substring(0, 30) + '...',
                        owner: capsule.owner,
                        unlockTime: new Date(Number(capsule.unlockTime) * 1000).toLocaleString(),
                        isUnlocked: capsule.isUnlocked,
                        hasDecryptionKey: capsule.decryptionKey.length > 0,
                        decryptionKeyPreview: capsule.decryptionKey.substring(0, 20) + '...'
                    });
                } else {
                    console.log(`❌ Capsule #${i}: Empty (zero address owner)`);
                }
            } catch (e) {
                console.log(`❌ Capsule #${i}: ${e.message.includes('execution reverted') ? 'Does not exist (reverted)' : e.message}`);
            }
        }
        
        console.log(`\n📊 Summary: Found ${existingCapsules.length} existing capsules: [${existingCapsules.join(', ')}]`);

        // Test 4: Create a test capsule (if user wants)
        console.log('\n💡 To create a test capsule, use:');
        console.log('await testCreateCapsule()');

        return { success: true, contract };

    } catch (error) {
        console.error('🚫 Contract test failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Create a test time capsule
 */
export async function testCreateCapsule() {
    try {
        if (!window.ethereum) {
            throw new Error('MetaMask not found');
        }

        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        const contract = new ethers.Contract(TIME_CAPSULE_CONTRACT_ADDRESS, TIME_CAPSULE_ABI, signer);

        // Create test capsule with unlock time 1 minute from now
        const unlockTime = Math.floor(Date.now() / 1000) + 60; // 1 minute from now
        const testBlobId = "QmTestBlobId123456789";
        const testDecryptionKey = "test-key-123";

        console.log('🚀 Creating test capsule...');
        console.log(`Unlock time: ${new Date(unlockTime * 1000).toLocaleString()}`);
        
        const tx = await contract.createTimeCapsule(testBlobId, testDecryptionKey, unlockTime);
        console.log('📝 Transaction sent:', tx.hash);
        
        const receipt = await tx.wait();
        console.log('✅ Transaction confirmed:', receipt.transactionHash);
        
        // Get the capsule ID from the logs or next ID
        const nextId = await contract.nextCapsuleId();
        const createdId = Number(nextId) - 1;
        
        console.log(`🎉 Created capsule #${createdId}`);
        
        return { success: true, capsuleId: createdId, txHash: receipt.transactionHash };

    } catch (error) {
        console.error('🚫 Failed to create test capsule:', error);
        return { success: false, error: error.message };
    }
}

// Make functions available globally for browser console testing
if (typeof window !== 'undefined') {
    window.testTimeCapsuleContract = testTimeCapsuleContract;
    window.testCreateCapsule = testCreateCapsule;
}