# EmosiFloww

A decentralized time-capsule platform for storing encrypted digital memories and unlocking them at a scheduled time using blockchain smart contracts.

## Features

* Time-locked multimedia storage
* Client-side AES-256 encryption
* Decentralized storage using Walrus
* Smart-contract-based scheduled unlocking
* ERC-721 NFT tokenization
* MetaMask wallet integration
* Images, videos, audio, and document support

## Tech Stack

* **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS
* **Blockchain:** Ethereum Sepolia, Hedera SDK
* **Storage:** Walrus Protocol
* **Encryption:** AES-256, SHA-256, PBKDF2
* **NFTs:** ERC-721
* **Web3:** ethers.js
* **UI:** Three.js, React Three Fiber, Motion

## Architecture

```text
File Upload
    ↓
Client-Side Encryption
    ↓
Walrus Decentralized Storage
    ↓
Smart Contract Time Lock
    ↓
ERC-721 NFT Minting
    ↓
Scheduled Decryption
```

## Setup

```bash
git clone https://github.com/aaditya3301/EmosiFloww.git
cd EmosiFloww
npm install
cp .env.example .env.local
npm run dev
```

Open:

```text
http://localhost:3000
```

## Environment Variables

```env
WALRUS_PUBLISHER_URL=your_walrus_publisher_url
WALRUS_AGGREGATOR_URL=your_walrus_aggregator_url
ETHEREUM_RPC_URL=your_sepolia_rpc_url
TIME_CAPSULE_CONTRACT=your_contract_address
```

## Project Structure

```text
EmosiFloww/
├── src/app/        # Next.js pages
├── src/components/ # UI components
├── src/lib/        # Encryption, NFT and blockchain logic
├── contracts/      # Solidity smart contracts
└── public/         # Static assets
```

## License

Licensed under the MIT License.
