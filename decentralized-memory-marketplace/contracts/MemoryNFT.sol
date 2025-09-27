// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract MemoryNFT is ERC721, ERC721URIStorage, Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    Counters.Counter private _tokenIdCounter;
    
    struct Memory {
        uint256 tokenId;
        address creator;
        string memoryHash;
        uint256 unlockTimestamp;
        uint256 creationTimestamp;
        bool isListed;
        uint256 price;
        string authenticity;
        uint256 valuationScore;
    }
    
    mapping(uint256 => Memory) public memories;
    mapping(uint256 => bool) public authenticityVerified;
    
    uint256 public constant PLATFORM_FEE = 250; // 2.5%
    address public feeRecipient;
    
    event MemoryMinted(
        uint256 indexed tokenId,
        address indexed creator,
        string memoryHash,
        uint256 unlockTimestamp
    );
    
    event MemoryListed(
        uint256 indexed tokenId,
        address indexed seller,
        uint256 price
    );
    
    event MemoryPurchased(
        uint256 indexed tokenId,
        address indexed buyer,
        address indexed seller,
        uint256 price
    );
    
    event AuthenticityVerified(
        uint256 indexed tokenId,
        string authenticity,
        uint256 score
    );

    constructor() ERC721("Memory Capsule NFT", "MEMORY") {
        feeRecipient = msg.sender;
    }

    function mintMemory(
        string memory tokenURI,
        string memory memoryHash,
        uint256 unlockTimestamp
    ) public returns (uint256) {
        require(unlockTimestamp > block.timestamp, "Unlock time must be in future");
        
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
        
        memories[tokenId] = Memory({
            tokenId: tokenId,
            creator: msg.sender,
            memoryHash: memoryHash,
            unlockTimestamp: unlockTimestamp,
            creationTimestamp: block.timestamp,
            isListed: false,
            price: 0,
            authenticity: "pending",
            valuationScore: 0
        });
        
        emit MemoryMinted(tokenId, msg.sender, memoryHash, unlockTimestamp);
        return tokenId;
    }

    function listMemory(uint256 tokenId, uint256 price) public {
        require(ownerOf(tokenId) == msg.sender, "Not the owner");
        require(price > 0, "Price must be greater than zero");
        
        memories[tokenId].isListed = true;
        memories[tokenId].price = price;
        
        emit MemoryListed(tokenId, msg.sender, price);
    }

    function purchaseMemory(uint256 tokenId) public payable nonReentrant {
        Memory storage memory = memories[tokenId];
        require(memory.isListed, "Memory not listed");
        require(msg.value >= memory.price, "Insufficient payment");
        
        address seller = ownerOf(tokenId);
        uint256 platformFee = (memory.price * PLATFORM_FEE) / 10000;
        uint256 sellerAmount = memory.price - platformFee;
        
        memory.isListed = false;
        memory.price = 0;
        
        _transfer(seller, msg.sender, tokenId);
        
        payable(seller).transfer(sellerAmount);
        payable(feeRecipient).transfer(platformFee);
        
        if (msg.value > memory.price) {
            payable(msg.sender).transfer(msg.value - memory.price);
        }
        
        emit MemoryPurchased(tokenId, msg.sender, seller, memory.price);
    }

    function setAuthenticity(
        uint256 tokenId,
        string memory authenticity,
        uint256 score
    ) public onlyOwner {
        memories[tokenId].authenticity = authenticity;
        memories[tokenId].valuationScore = score;
        authenticityVerified[tokenId] = true;
        
        emit AuthenticityVerified(tokenId, authenticity, score);
    }

    function getMemory(uint256 tokenId) public view returns (Memory memory) {
        return memories[tokenId];
    }

    function isMemoryUnlocked(uint256 tokenId) public view returns (bool) {
        return block.timestamp >= memories[tokenId].unlockTimestamp;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function setFeeRecipient(address _feeRecipient) public onlyOwner {
        feeRecipient = _feeRecipient;
    }
}