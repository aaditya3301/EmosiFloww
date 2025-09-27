# EmosiFloww - Advanced Decentralized Time-Capsule Platform

## 🌟 Overview

**EmosiFloww** is a revolutionary Next.js 15-based decentralized time-capsule platform that combines cutting-edge blockchain technology with beautiful UI/UX design. Users can create time-locked digital memories by uploading multimedia files with encrypted storage, scheduled decryption, and NFT tokenization - all powered by a sophisticated multi-chain infrastructure.

## ✨ Key Features

### 🎯 Core Functionality
- **🔐 Time-Locked Storage**: True blockchain-based time-locking with smart contracts
- **📁 Multimedia Upload**: Support for images, videos, audio, and documents
- **⏰ Scheduled Release**: Set precise future dates/times for content unlock
- **🎨 NFT Tokenization**: Each time capsule becomes a tradeable NFT
- **🔒 Double Encryption**: Content encrypted with unique keys + blockchain security
- **📱 Responsive Design**: Modern UI with stunning visual effects

### 🎮 User Experience
- **Interactive Vortex Backgrounds**: Immersive 3D particle animations
- **Canvas Reveal Effects**: Smooth hover animations and transitions
- **Real-time Progress**: Live upload and processing status
- **Wallet Integration**: Seamless MetaMask connection with JWT sessions
- **Mobile Optimized**: Fully responsive design across all devices

## 🏗️ Advanced Technical Architecture

### 🔗 Multi-Chain Workflow (5-Step Process)

#### 1. **Walrus Decentralized Storage** 🦭
```javascript
// Upload to Walrus testnet with configurable epochs
const walrusResult = await walrus(file, epochs);
// Returns: { blobId, fileUrl }
```
- **Network**: Walrus Testnet Publisher
- **Endpoint**: `https://publisher.walrus-testnet.walrus.space/v1/blobs`
- **Storage**: Decentralized file storage with content addressing
- **Retrieval**: `https://aggregator.walrus-testnet.walrus.space/v1/{blobId}`

#### 2. **Advanced Encryption System** 🔐
```javascript
// Multi-layer encryption for time-locked security
const encryptedContent = encryptContent(metadata, uniqueKey);
const encryptedBlobId = encryptBlobIdWithKey(blobId, uniqueKey);
```
- **AES-256 Encryption**: Industry-standard encryption
- **Unique Key Generation**: Per-capsule encryption keys
- **Double Encryption**: Content + Blob ID encryption layers

#### 3. **Smart Contract Time-Locking** ⏰
```solidity
// Ethereum smart contract deployment
contract HederaTimeCapsule {
    function createTimeCapsule(
        string memory _encryptedBlobId,
        string memory _decryptionKey,
        uint256 _unlockTime
    ) external returns (uint256 capsuleId)
}
```
- **Contract Address**: `0x508bbc0cf873c11dbf9d72bfcea3dc1e69739c38`
- **Network**: Ethereum Sepolia Testnet
- **Features**: Automated time-based unlocking, ownership verification

#### 4. **NFT Minting & Tokenization** 🎨
```javascript
// Create tradeable NFT for each time capsule
const nftResult = await mintTimeCapsuleNFT(encryptedBlobId, capsuleId, metadata);
```
- **ERC-721 Standard**: Fully compliant NFT implementation
- **Metadata Storage**: Rich metadata with file information
- **Tradeable Assets**: Time capsules become valuable digital collectibles

#### 5. **Scheduled Unlock System** 🗓️
```javascript
// Automated decryption at specified time
const hederaResult = await timeCapsuleScheduler.createScheduledTimeCapsule(
    encryptedBlobId, decryptionKey, unlockTime
);
```
- **Precise Timing**: Unix timestamp-based unlocking
- **Automated Process**: No manual intervention required
- **Verification System**: Cryptographic proof of authenticity

## 🛠️ Modern Technology Stack

### Frontend Framework
- **⚡ Next.js 15.5.4** - Latest React framework with App Router
- **⚛️ React 19.1.0** - Modern React with concurrent features
- **🎨 TypeScript 5** - Type-safe development environment
- **🌊 Tailwind CSS 4** - Utility-first styling with latest features
- **📱 Mobile-First Design** - Responsive across all devices

### Advanced UI Components
- **🌪️ Vortex Effects** - Interactive 3D particle backgrounds
- **🎭 Canvas Reveal** - Smooth hover animations and transitions
- **📤 Drag & Drop Upload** - Intuitive file upload interface
- **🔄 Real-time Loaders** - Multiple loading states and animations
- **🧭 Dynamic Navigation** - Context-aware navigation system

### Blockchain Infrastructure
- **🦭 Walrus Network** - Decentralized storage layer
- **⚡ Ethereum/Sepolia** - Smart contract execution layer
- **🔐 AES Encryption** - Client-side encryption system
- **🎨 ERC-721 NFTs** - Tokenization and ownership layer
- **🔗 ethers.js 6.15.0** - Blockchain interaction library

### Advanced Libraries
```json
{
  "@hashgraph/sdk": "^2.73.2",           // Hedera integration
  "@hashgraph/cryptography": "^1.11.0",  // Advanced cryptography
  "@react-three/fiber": "^9.0.0-alpha.8", // 3D graphics
  "crypto-js": "^4.2.0",                 // Encryption utilities
  "react-dropzone": "^14.3.8",          // File upload handling
  "motion": "^12.23.22",                 // Advanced animations
  "three": "^0.180.0"                    // 3D rendering engine
}
```

## 📁 Project Structure

```
EmosiFloww/
├── src/
│   ├── app/                    # Next.js 15 App Router
│   │   ├── page.tsx           # Landing page with Google Gemini effect
│   │   ├── capsules/          # Time capsule management
│   │   ├── deploy/            # Creation and upload interface
│   │   ├── decode/            # NFT decoding and decryption
│   │   ├── comparison/        # Metadata analysis tools
│   │   ├── docs/              # Documentation and guides
│   │   └── status/            # System status monitoring
│   │
│   ├── components/ui/         # Reusable UI components
│   │   ├── vortex.tsx        # Interactive particle backgrounds
│   │   ├── canvas-reveal-effect.tsx  # Hover animations
│   │   ├── file-upload.tsx   # Drag & drop upload
│   │   ├── loaders.tsx       # Loading animations
│   │   └── navbar.tsx        # Dynamic navigation
│   │
│   ├── lib/                   # Core functionality
│   │   ├── hedera-scheduler.js    # Smart contract integration
│   │   ├── encryption.js          # AES encryption system
│   │   ├── nft.js                 # NFT minting and metadata
│   │   ├── nft-decoder.js         # Decryption utilities
│   │   └── contract-tester.js     # Development tools
│   │
│   └── store/
│       └── functions.js       # Main API functions
│
├── contracts/                 # Smart contracts
│   ├── HederaTimeCapsule.sol # Time-locking contract
│   └── PublicTimeCapsuleNFT.sol # NFT implementation
│
└── public/                   # Static assets
```

## 🚀 Getting Started

### Prerequisites
```bash
# Required software
Node.js 18+
npm/yarn/pnpm package manager
MetaMask or compatible Web3 wallet

# Blockchain requirements
Ethereum/Sepolia testnet access
Testnet ETH for gas fees
Walrus testnet access
```

### Quick Setup

1. **Clone and Install**
```bash
git clone https://github.com/aaditya3301/EmosiFloww.git
cd EmosiFloww
npm install
```

2. **Environment Configuration**
```bash
# Create environment file
cp .env.example .env.local

# Configure blockchain connections
WALRUS_PUBLISHER_URL=https://publisher.walrus-testnet.walrus.space
WALRUS_AGGREGATOR_URL=https://aggregator.walrus-testnet.walrus.space
ETHEREUM_RPC_URL=your_sepolia_rpc_url
TIME_CAPSULE_CONTRACT=0x508bbc0cf873c11dbf9d72bfcea3dc1e69739c38
```

3. **Development Server**
```bash
npm run dev
# Visit http://localhost:3000
```

4. **Production Build**
```bash
npm run build
npm run start
```

## 🎯 Platform Features

### 📤 Time Capsule Creation (`/deploy`)
- **Multi-file Upload**: Drag & drop interface with progress tracking
- **Metadata Enhancement**: Rich descriptions, titles, and notes
- **Time Selection**: Precise date/time picker for unlock scheduling
- **Immediate vs Scheduled**: Choose instant or time-locked storage
- **Real-time Feedback**: Live status updates through entire process

### 📋 Capsule Management (`/capsules`)
- **Portfolio View**: Grid layout of all created time capsules
- **Status Indicators**: Visual locked/unlocked status badges
- **Interactive Cards**: Hover effects with Canvas Reveal animations
- **File Counts**: Display number of files per capsule
- **Quick Actions**: Direct access to capsule contents

### 🔍 NFT Decoding (`/decode`)
- **Token Analysis**: Decode any NFT token ID for metadata
- **Decryption Tools**: Unlock time capsule content when available
- **Metadata Viewer**: Comprehensive NFT data display
- **Developer Tools**: Technical information for debugging

### 📊 Metadata Analysis (`/comparison`)
- **NFT Comparison**: Side-by-side metadata analysis
- **Contract Testing**: Smart contract function testing interface
- **Time Capsule Status**: Check unlock eligibility and timing
- **Developer Console**: Advanced debugging and testing tools

### 📚 Documentation (`/docs`)
- **Interactive Guide**: Step-by-step usage instructions
- **Technical Docs**: API and integration documentation
- **FAQ Section**: Common questions and troubleshooting
- **Smart Contract Info**: Contract addresses and ABIs

## 🔒 Security Features

### 🛡️ Multi-Layer Security
- **Client-Side Encryption**: Files encrypted before upload
- **Unique Key Generation**: Per-capsule encryption keys
- **Smart Contract Verification**: Blockchain-verified time locks
- **Decentralized Storage**: No single point of failure
- **Ownership Verification**: NFT-based access control

### 🔐 Encryption Standards
- **AES-256 Encryption**: Industry-standard encryption
- **SHA-256 Hashing**: Secure key derivation
- **PBKDF2 Key Stretching**: Enhanced security
- **Cryptographic Signatures**: Integrity verification

## 🌍 Use Cases

### Personal Applications
- **📝 Digital Diaries**: Future messages to yourself
- **🎓 Milestone Memories**: Graduation, achievements, celebrations
- **👨‍👩‍👧‍👦 Family Archives**: Multi-generational memory sharing
- **💑 Relationship Capsules**: Anniversary and special moment preservation

### Business Applications
- **📢 Marketing Campaigns**: Time-released announcements
- **📈 Financial Records**: Encrypted document storage
- **🏢 Corporate Communications**: Scheduled internal messages
- **📋 Legal Documents**: Time-locked contract execution

### Educational & Creative
- **🎨 Art Projects**: Time-released digital art collections
- **📚 Educational Content**: Scheduled learning materials
- **🎮 Gaming**: Achievement unlocks and rewards
- **🎪 Events**: Conference and festival content release

## 🔧 Development & Testing

### Testing Tools
- **Contract Tester**: Smart contract function testing interface
- **NFT Decoder**: Token metadata analysis and debugging
- **Metadata Fetcher**: Bulk NFT data comparison
- **Status Monitor**: Real-time system health checks

### Development Features
- **Hot Reload**: Instant development feedback
- **TypeScript**: Full type safety and IntelliSense
- **ESLint**: Code quality and consistency
- **Console Logging**: Detailed operation tracking

## 🚀 Deployment

### Production Deployment
```bash
# Build for production
npm run build

# Start production server
npm run start

# Deploy to Vercel (recommended)
vercel --prod
```

### Smart Contract Deployment
```bash
# Deploy contracts to Sepolia
npx hardhat deploy --network sepolia

# Verify contracts
npx hardhat verify --network sepolia [CONTRACT_ADDRESS]
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines
- Follow TypeScript best practices
- Maintain consistent code style
- Add tests for new features
- Update documentation
- Test across multiple browsers

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Community

- **📧 Email**: support@emosifloww.com
- **🐛 Issues**: [GitHub Issues](https://github.com/aaditya3301/EmosiFloww/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/aaditya3301/EmosiFloww/discussions)
- **🐦 Twitter**: [@EmosiFloww](https://twitter.com/EmosiFloww)

## 🌟 Roadmap

### Phase 1 (Current) ✅
- [x] Core time capsule creation
- [x] Walrus storage integration
- [x] Smart contract deployment
- [x] NFT minting system
- [x] Modern UI/UX design

### Phase 2 (In Progress) 🚧
- [ ] Advanced analytics dashboard
- [ ] Batch upload functionality
- [ ] Social sharing features
- [ ] Mobile app development
- [ ] Multi-language support

### Phase 3 (Planned) 📅
- [ ] DAO governance system
- [ ] Cross-chain compatibility
- [ ] Advanced privacy features
- [ ] Enterprise solutions
- [ ] API marketplace

## ⚡ Performance

- **Upload Speed**: Optimized for large files up to 100MB
- **Encryption**: Client-side processing for security
- **UI Response**: Sub-100ms interactions
- **Blockchain**: Average 15-second confirmation times
- **Storage**: Decentralized redundancy across nodes

---

**Built with ❤️ by [aaditya3301](https://github.com/aaditya3301)**

*"Preserving today for tomorrow, powered by blockchain technology."*

## 🎉 Live Demo

Experience EmosiFloww at: **[https://emosifloww.vercel.app](https://emosifloww.vercel.app)**

---

*Last updated: September 2025 | Version 1.2.0*
- Hedera smart contracts automatically trigger decryption at the user-specified time
- The original CID is revealed, making the time-capsule accessible
- Users can then retrieve their multimedia and future notes

## 🛠️ Technology Stack

### Frontend
- **Next.js 15.5.4** - React-based web framework
- **React 19.1.0** - UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS 4** - Utility-first styling
- **ESLint** - Code linting and quality

### Blockchain Infrastructure
- **Walrus** - Decentralized multimedia storage
- **Filecoin** - Long-term metadata storage
- **NFT Platform** - Tokenization layer
- **Hedera Hashgraph** - Smart contract execution and scheduling

## 📁 Project Structure

```
EmosiFloww/
├── src/app/                 # Next.js app directory
│   ├── page.tsx            # Main application page
│   ├── layout.tsx          # App layout component
│   └── globals.css         # Global styles
├── IPFS/                   # Decentralized storage integrations
│   ├── walrus/             # Walrus storage implementation
│   └── filecoin/           # Filecoin storage implementation
├── public/                 # Static assets
└── package.json            # Project dependencies
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn package manager
- Wallet connections for:
  - Walrus network access
  - Filecoin storage
  - NFT minting capabilities
  - Hedera account

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aaditya3301/EmosiFloww.git
cd EmosiFloww
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
```

4. Configure your blockchain connections in `.env.local`:
```env
WALRUS_API_KEY=your_walrus_key
FILECOIN_PRIVATE_KEY=your_filecoin_key  
HEDERA_ACCOUNT_ID=your_hedera_account
HEDERA_PRIVATE_KEY=your_hedera_private_key
NFT_CONTRACT_ADDRESS=your_nft_contract
```

5. Run the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## 🎯 Use Cases

- **Personal Time Capsules**: Send messages to your future self
- **Family Memories**: Share photos and videos with future generations  
- **Business Communications**: Schedule important announcements or documents
- **Digital Legacy**: Preserve memories and messages for loved ones
- **Educational Content**: Time-release learning materials
- **Legal Documents**: Time-locked contract or will execution

## 🔒 Security Features

- **Multi-Chain Redundancy**: Files stored across multiple decentralized networks
- **Smart Contract Automation**: No human intervention required for decryption
- **Immutable Timestamps**: Blockchain-verified scheduling
- **Encrypted Storage**: CIDs are encrypted until the scheduled time
- **Decentralized Consensus**: Hedera's consensus mechanism ensures reliability

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please:
1. Check our [Documentation](docs/)
2. Open an [Issue](https://github.com/aaditya3301/EmosiFloww/issues)
3. Join our [Discord Community](https://discord.gg/EmosiFloww)

## 🌟 Roadmap

- [ ] Mobile responsive design improvements
- [ ] Batch upload functionality
- [ ] Advanced scheduling options (recurring messages)
- [ ] Integration with additional storage networks
- [ ] Social sharing capabilities
- [ ] Message preview system
- [ ] Analytics dashboard
- [ ] Multi-language support

---

**Built with ❤️ by the EmosiFloww Team**

*Preserving today for tomorrow, powered by blockchain technology.*
