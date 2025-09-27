// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title HederaTimeCapsule
 * @dev A time-locked smart contract for Hedera that stores encrypted time capsule data
 * and allows decryption only after the specified unlock time has passed.
 */
contract HederaTimeCapsule {
    struct TimeCapsule {
        uint256 capsuleId;
        string encryptedBlobId; // Walrus blob ID containing encrypted content
        bytes32 decryptionKeyHash; // Hash of the decryption key for verification
        address owner;
        uint256 unlockTime;
        bool exists;
        bool isUnlocked;
        string decryptionKey; // Will be revealed after unlock time
    }

    // State variables
    mapping(uint256 => TimeCapsule) public timeCapsules;
    mapping(address => uint256[]) public userCapsules;
    uint256 public nextCapsuleId;
    address public contractOwner;

    // Events
    event TimeCapsuleCreated(
        uint256 indexed capsuleId,
        address indexed owner,
        string encryptedBlobId,
        uint256 unlockTime
    );

    event TimeCapsuleUnlocked(
        uint256 indexed capsuleId,
        address indexed owner,
        string decryptionKey
    );

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == contractOwner, "Only contract owner can call this function");
        _;
    }

    modifier capsuleExists(uint256 _capsuleId) {
        require(timeCapsules[_capsuleId].exists, "Time capsule does not exist");
        _;
    }

    modifier onlyCapsuleOwner(uint256 _capsuleId) {
        require(timeCapsules[_capsuleId].owner == msg.sender, "Not the owner of this time capsule");
        _;
    }

    modifier timeHasPassed(uint256 _capsuleId) {
        require(block.timestamp >= timeCapsules[_capsuleId].unlockTime, "Time capsule is still locked");
        _;
    }

    // Constructor
    constructor() {
        contractOwner = msg.sender;
        nextCapsuleId = 1;
    }

    /**
     * @dev Creates a new time capsule with encrypted content
     * @param _encryptedBlobId The Walrus blob ID containing encrypted content
     * @param _decryptionKey The key needed to decrypt the content (stored as hash initially)
     * @param _unlockTime The timestamp when the capsule can be unlocked
     * @return capsuleId The ID of the created time capsule
     */
    function createTimeCapsule(
        string memory _encryptedBlobId,
        string memory _decryptionKey,
        uint256 _unlockTime
    ) external returns (uint256 capsuleId) {
        require(_unlockTime > block.timestamp, "Unlock time must be in the future");
        require(bytes(_encryptedBlobId).length > 0, "Encrypted blob ID cannot be empty");
        require(bytes(_decryptionKey).length > 0, "Decryption key cannot be empty");

        capsuleId = nextCapsuleId++;
        bytes32 keyHash = keccak256(abi.encodePacked(_decryptionKey));

        timeCapsules[capsuleId] = TimeCapsule({
            capsuleId: capsuleId,
            encryptedBlobId: _encryptedBlobId,
            decryptionKeyHash: keyHash,
            owner: msg.sender,
            unlockTime: _unlockTime,
            exists: true,
            isUnlocked: false,
            decryptionKey: "" // Will be set when unlocked
        });

        userCapsules[msg.sender].push(capsuleId);

        emit TimeCapsuleCreated(capsuleId, msg.sender, _encryptedBlobId, _unlockTime);
        return capsuleId;
    }

    /**
     * @dev Unlocks a time capsule and reveals the decryption key
     * @param _capsuleId The ID of the time capsule to unlock
     * @param _decryptionKey The decryption key to verify and store
     */
    function unlockTimeCapsule(uint256 _capsuleId, string memory _decryptionKey)
        external
        capsuleExists(_capsuleId)
        onlyCapsuleOwner(_capsuleId)
        timeHasPassed(_capsuleId)
    {
        TimeCapsule storage capsule = timeCapsules[_capsuleId];
        require(!capsule.isUnlocked, "Time capsule is already unlocked");
        
        // Verify the decryption key
        bytes32 providedKeyHash = keccak256(abi.encodePacked(_decryptionKey));
        require(providedKeyHash == capsule.decryptionKeyHash, "Invalid decryption key");

        // Unlock the capsule
        capsule.isUnlocked = true;
        capsule.decryptionKey = _decryptionKey;

        emit TimeCapsuleUnlocked(_capsuleId, msg.sender, _decryptionKey);
    }

    /**
     * @dev Gets the time capsule data (without decryption key if locked)
     * @param _capsuleId The ID of the time capsule
     */
    function getTimeCapsule(uint256 _capsuleId)
        external
        view
        capsuleExists(_capsuleId)
        returns (
            uint256 capsuleId,
            string memory encryptedBlobId,
            address owner,
            uint256 unlockTime,
            bool isUnlocked,
            string memory decryptionKey
        )
    {
        TimeCapsule memory capsule = timeCapsules[_capsuleId];
        
        // Only return decryption key if capsule is unlocked and time has passed
        string memory key = "";
        if (capsule.isUnlocked && block.timestamp >= capsule.unlockTime) {
            key = capsule.decryptionKey;
        }

        return (
            capsule.capsuleId,
            capsule.encryptedBlobId,
            capsule.owner,
            capsule.unlockTime,
            capsule.isUnlocked,
            key
        );
    }

    /**
     * @dev Gets all time capsule IDs owned by a user
     * @param _user The address of the user
     */
    function getUserCapsules(address _user) external view returns (uint256[] memory) {
        return userCapsules[_user];
    }

    /**
     * @dev Checks if a time capsule is ready to be unlocked
     * @param _capsuleId The ID of the time capsule
     */
    function isReadyToUnlock(uint256 _capsuleId)
        external
        view
        capsuleExists(_capsuleId)
        returns (bool)
    {
        return block.timestamp >= timeCapsules[_capsuleId].unlockTime;
    }

    /**
     * @dev Gets the remaining time until unlock
     * @param _capsuleId The ID of the time capsule
     */
    function getTimeUntilUnlock(uint256 _capsuleId)
        external
        view
        capsuleExists(_capsuleId)
        returns (uint256)
    {
        TimeCapsule memory capsule = timeCapsules[_capsuleId];
        if (block.timestamp >= capsule.unlockTime) {
            return 0;
        }
        return capsule.unlockTime - block.timestamp;
    }

    /**
     * @dev Emergency function to update contract owner (only current owner)
     * @param _newOwner The address of the new owner
     */
    function transferOwnership(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "New owner cannot be zero address");
        contractOwner = _newOwner;
    }

    /**
     * @dev Gets the total number of time capsules created
     */
    function getTotalCapsules() external view returns (uint256) {
        return nextCapsuleId - 1;
    }
}
