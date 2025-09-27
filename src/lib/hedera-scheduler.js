import { ethers } from 'ethers';

// Time Capsule Contract Address (deployed on Sepolia/Ethereum)
const TIME_CAPSULE_CONTRACT_ADDRESS = '0x508bbc0cf873c11dbf9d72bfcea3dc1e69739c38';

// Contract ABI for the Time Capsule contract
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
 * Ethereum-based Time Capsule Scheduler
 * Handles time-locked smart contract interactions using your deployed contract
 */

class TimeCapsuleScheduler {
    constructor() {
        this.provider = null;
        this.signer = null;
        this.contract = null;
        this.contractAddress = TIME_CAPSULE_CONTRACT_ADDRESS;
    }

    /**
     * Initialize connection to Ethereum/Sepolia network
     * @param {object} ethereum - Window ethereum object from MetaMask
     * @returns {boolean} Success status
     */
    async initializeClient(ethereum = window.ethereum) {
        try {
            if (!ethereum) {
                throw new Error('MetaMask not found');
            }

            this.provider = new ethers.BrowserProvider(ethereum);
            this.signer = await this.provider.getSigner();
            this.contract = new ethers.Contract(
                this.contractAddress,
                TIME_CAPSULE_ABI,
                this.signer
            );

            console.log('Ethereum client initialized successfully');
            console.log('Contract address:', this.contractAddress);
            return true;
        } catch (error) {
            console.error('Failed to initialize Ethereum client:', error);
            throw error;
        }
    }

    /**
     * Create a time capsule with time-locked unlock
     * @param {string} encryptedBlobId - Walrus blob ID
     * @param {string} decryptionKey - Key for decryption
     * @param {number} unlockTime - Unix timestamp for unlock
     * @returns {Object} Transaction result and capsule ID
     */
    async createScheduledTimeCapsule(encryptedBlobId, decryptionKey, unlockTime) {
        try {
            if (!this.contract) {
                await this.initializeClient();
            }

            console.log('Creating time capsule...');
            console.log('Encrypted Blob ID:', encryptedBlobId);
            console.log('Unlock Time:', new Date(unlockTime * 1000));

            // Call the smart contract function
            const tx = await this.contract.createTimeCapsule(
                encryptedBlobId,
                decryptionKey,
                unlockTime
            );

            console.log('Transaction sent:', tx.hash);
            
            // Wait for transaction to be mined
            const receipt = await tx.wait();
            console.log('Transaction confirmed:', receipt.hash);

            // Get the capsule ID from events or by checking next ID
            const totalCapsules = await this.contract.getTotalCapsules();
            const capsuleId = Number(totalCapsules);

            return {
                success: true,
                transactionId: receipt.hash,
                capsuleId: capsuleId,
                scheduleId: `eth-${capsuleId}-${unlockTime}`, // Mock schedule ID
                encryptedBlobId: encryptedBlobId,
                unlockTime: unlockTime
            };
        } catch (error) {
            console.error('Failed to create time capsule:', error);
            throw error;
        }
    }

    /**
     * Get time capsule information
     * @param {number} capsuleId - Time capsule ID
     * @returns {Object} Time capsule data
     */
    async getTimeCapsule(capsuleId) {
        try {
            if (!this.contract) {
                await this.initializeClient();
            }

            console.log('Getting time capsule info for ID:', capsuleId);

            const result = await this.contract.getTimeCapsule(capsuleId);
            
            return {
                capsuleId: Number(result[0]),
                encryptedBlobId: result[1],
                owner: result[2],
                unlockTime: Number(result[3]),
                isUnlocked: result[4],
                decryptionKey: result[5]
            };
        } catch (error) {
            console.error('Failed to get time capsule:', error);
            throw error;
        }
    }

    /**
     * Check if a time capsule is ready to unlock
     * @param {number} capsuleId - Time capsule ID
     * @returns {boolean} Ready status
     */
    async isReadyToUnlock(capsuleId) {
        try {
            if (!this.contract) {
                await this.initializeClient();
            }

            const result = await this.contract.isReadyToUnlock(capsuleId);
            return result;
        } catch (error) {
            console.error('Failed to check unlock status:', error);
            throw error;
        }
    }

    /**
     * Get remaining time until unlock
     * @param {number} capsuleId - Time capsule ID
     * @returns {number} Seconds until unlock
     */
    async getTimeUntilUnlock(capsuleId) {
        try {
            if (!this.contract) {
                await this.initializeClient();
            }

            const result = await this.contract.getTimeUntilUnlock(capsuleId);
            return Number(result);
        } catch (error) {
            console.error('Failed to get time until unlock:', error);
            throw error;
        }
    }

    /**
     * Get all time capsules for a user
     * @param {string} userAddress - User's address
     * @returns {Array} Array of capsule IDs
     */
    async getUserCapsules(userAddress) {
        try {
            if (!this.contract) {
                await this.initializeClient();
            }

            const result = await this.contract.getUserCapsules(userAddress);
            return result.map(id => Number(id));
        } catch (error) {
            console.error('Failed to get user capsules:', error);
            throw error;
        }
    }

    /**
     * Get the next capsule ID (for internal use)
     * @returns {number} Next capsule ID
     */
    async getNextCapsuleId() {
        try {
            if (!this.contract) {
                await this.initializeClient();
            }

            const result = await this.contract.nextCapsuleId();
            return Number(result);
        } catch (error) {
            console.error('Failed to get next capsule ID:', error);
            throw error;
        }
    }

    /**
     * Manually unlock a time capsule (if time has passed)
     * @param {number} capsuleId - Time capsule ID
     * @param {string} decryptionKey - Decryption key
     * @returns {Object} Transaction result
     */
    async manualUnlockTimeCapsule(capsuleId, decryptionKey) {
        try {
            if (!this.contract) {
                await this.initializeClient();
            }

            console.log('Unlocking time capsule:', capsuleId);

            const tx = await this.contract.unlockTimeCapsule(capsuleId, decryptionKey);
            const receipt = await tx.wait();

            return {
                success: true,
                transactionId: receipt.hash,
                capsuleId: capsuleId
            };
        } catch (error) {
            console.error('Failed to unlock time capsule:', error);
            throw error;
        }
    }

    /**
     * Get account balance
     * @returns {string} Account balance in ETH
     */
    async getAccountBalance() {
        try {
            if (!this.provider || !this.signer) {
                await this.initializeClient();
            }

            const address = await this.signer.getAddress();
            const balance = await this.provider.getBalance(address);
            return ethers.formatEther(balance);
        } catch (error) {
            console.error('Failed to get account balance:', error);
            throw error;
        }
    }

    /**
     * Close the client connection
     */
    close() {
        // No explicit close needed for ethers.js
        this.provider = null;
        this.signer = null;
        this.contract = null;
        console.log('Ethereum client connection closed');
    }
}

// Create a singleton instance
const timeCapsuleScheduler = new TimeCapsuleScheduler();

export default timeCapsuleScheduler;

// Export utility functions for easy access
export const {
    initializeClient,
    createScheduledTimeCapsule,
    getTimeCapsule,
    isReadyToUnlock,
    getTimeUntilUnlock,
    getUserCapsules,
    manualUnlockTimeCapsule,
    getAccountBalance,
    close
} = timeCapsuleScheduler;
