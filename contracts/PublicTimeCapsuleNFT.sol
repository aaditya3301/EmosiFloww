// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PublicTimeCapsuleNFT - ANYONE CAN MINT! 🌍
 * @dev Simple ERC721 implementation - GUARANTEED to deploy in Remix!
 */
contract PublicTimeCapsuleNFT {
    string public name = "Public Time Capsule NFT";
    string public symbol = "PTCAP";
    uint256 private _nextTokenId = 1;
    
    // Mappings
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;
    mapping(address => mapping(address => bool)) private _operatorApprovals;
    mapping(uint256 => string) private _tokenURIs;
    mapping(uint256 => string) private _encryptedBlobIds;
    mapping(uint256 => address) private _creators;
    
    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);
    event TimeCapsuleMinted(uint256 indexed tokenId, address indexed creator, address indexed to, string encryptedBlobId);
    
    // ERC721 Standard Functions
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "URI query for nonexistent token");
        return _tokenURIs[tokenId];
    }
    
    function balanceOf(address owner) public view returns (uint256) {
        require(owner != address(0), "Balance query for zero address");
        return _balances[owner];
    }
    
    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "Owner query for nonexistent token");
        return owner;
    }
    
    function approve(address to, uint256 tokenId) public {
        address owner = ownerOf(tokenId);
        require(to != owner, "Approval to current owner");
        require(msg.sender == owner || isApprovedForAll(owner, msg.sender), "Not approved");
        _approve(to, tokenId);
    }
    
    function getApproved(uint256 tokenId) public view returns (address) {
        require(_exists(tokenId), "Approved query for nonexistent token");
        return _tokenApprovals[tokenId];
    }
    
    function setApprovalForAll(address operator, bool approved) public {
        require(operator != msg.sender, "Approve to caller");
        _operatorApprovals[msg.sender][operator] = approved;
        emit ApprovalForAll(msg.sender, operator, approved);
    }
    
    function isApprovedForAll(address owner, address operator) public view returns (bool) {
        return _operatorApprovals[owner][operator];
    }
    
    function transferFrom(address from, address to, uint256 tokenId) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not approved");
        _transfer(from, to, tokenId);
    }
    
    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        transferFrom(from, to, tokenId); // Simplified - no receiver check
    }
    
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory) public {
        transferFrom(from, to, tokenId); // Simplified - no receiver check
    }
    
    // 🌍 PUBLIC MINT FUNCTION - ANYONE CAN USE!
    function mintTimeCapsule(
        address to,
        string memory encryptedBlobId,
        string memory metadataURI
    ) public returns (uint256) {
        uint256 tokenId = _nextTokenId++;
        
        _mint(to, tokenId);
        _setTokenURI(tokenId, metadataURI);
        _encryptedBlobIds[tokenId] = encryptedBlobId;
        _creators[tokenId] = msg.sender;
        
        emit TimeCapsuleMinted(tokenId, msg.sender, to, encryptedBlobId);
        
        return tokenId;
    }
    
    // Time Capsule Specific Functions
    function getEncryptedBlobId(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "Query for nonexistent token");
        return _encryptedBlobIds[tokenId];
    }
    
    function getCreator(uint256 tokenId) public view returns (address) {
        require(_exists(tokenId), "Query for nonexistent token");
        return _creators[tokenId];
    }
    
    function nextTokenId() public view returns (uint256) {
        return _nextTokenId;
    }
    
    function totalSupply() public view returns (uint256) {
        return _nextTokenId - 1;
    }
    
    // Internal Functions
    function _exists(uint256 tokenId) internal view returns (bool) {
        return _owners[tokenId] != address(0);
    }
    
    function _mint(address to, uint256 tokenId) internal {
        require(to != address(0), "Mint to zero address");
        require(!_exists(tokenId), "Token already minted");
        
        _balances[to] += 1;
        _owners[tokenId] = to;
        
        emit Transfer(address(0), to, tokenId);
    }
    
    function _setTokenURI(uint256 tokenId, string memory uri) internal {
        require(_exists(tokenId), "URI set of nonexistent token");
        _tokenURIs[tokenId] = uri;
    }
    
    function _approve(address to, uint256 tokenId) internal {
        _tokenApprovals[tokenId] = to;
        emit Approval(ownerOf(tokenId), to, tokenId);
    }
    
    function _transfer(address from, address to, uint256 tokenId) internal {
        require(ownerOf(tokenId) == from, "Transfer from incorrect owner");
        require(to != address(0), "Transfer to zero address");
        
        // Clear approvals
        _approve(address(0), tokenId);
        
        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;
        
        emit Transfer(from, to, tokenId);
    }
    
    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        require(_exists(tokenId), "Operator query for nonexistent token");
        address owner = ownerOf(tokenId);
        return (spender == owner || getApproved(tokenId) == spender || isApprovedForAll(owner, spender));
    }
    
    // ERC165 Support
    function supportsInterface(bytes4 interfaceId) public view virtual returns (bool) {
        return
            interfaceId == 0x01ffc9a7 || // ERC165 Interface ID
            interfaceId == 0x80ac58cd || // ERC721 Interface ID
            interfaceId == 0x5b5e139f;   // ERC721 Metadata Interface ID
    }
}