# Tempris - Decentralized Time-Capsule Platform

## Overview

**Tempris** is a revolutionary Next.js-based frontend application that creates decentralized time-capsules using blockchain technology. Users can upload multimedia files with future notes that are encrypted and scheduled for automatic decryption at specified times, utilizing a sophisticated multi-chain infrastructure.

## 🚀 Features

### Frontend Capabilities
- **File Upload Interface**: Upload multimedia files (images, videos, audio, documents)
- **Time Selection**: Set future dates and times for message delivery
- **Future Notes**: Add personalized messages to accompany your multimedia
- **Real-time Upload Progress**: Track the multi-stage upload and processing workflow
- **Decentralized Storage**: Your files are stored across multiple decentralized networks

## 🏗️ Technical Architecture

### Multi-Chain Workflow

The application follows a sophisticated 6-step process to ensure secure, decentralized, and time-locked storage:

#### 1. **Walrus Upload** 🦭
- Multimedia files are first uploaded to **Walrus** (decentralized storage network)
- Walrus generates a unique Content Identifier (CID) for the uploaded multimedia
- Provides fast, reliable storage for large media files

#### 2. **JSON Metadata Creation** 📄
- A JSON object is created containing:
  - Future note/message text
  - Walrus CID reference
  - Timestamp information
  - User metadata

#### 3. **Filecoin Storage** 🗃️
- The JSON metadata is uploaded to **Filecoin** network
- Filecoin generates a secondary CID for the metadata
- Ensures long-term, persistent storage with economic incentives

#### 4. **NFT Minting** 🎨
- An NFT is minted using the **Filecoin CID** as the token identifier
- The NFT name is derived from the Filecoin CID
- Creates a unique, tradeable digital asset representing the time-capsule

#### 5. **Hedera Smart Contract Encryption** 🔐
- **Hedera Hashgraph** smart contracts encrypt the Filecoin CID within the NFT
- The CID becomes inaccessible until the scheduled time
- Provides enterprise-grade security and consensus

#### 6. **Scheduled Decryption** ⏰
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
tempris/
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
git clone https://github.com/aaditya3301/Tempris.git
cd Tempris
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
2. Open an [Issue](https://github.com/aaditya3301/Tempris/issues)
3. Join our [Discord Community](https://discord.gg/tempris)

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

**Built with ❤️ by the Tempris Team**

*Preserving today for tomorrow, powered by blockchain technology.*
