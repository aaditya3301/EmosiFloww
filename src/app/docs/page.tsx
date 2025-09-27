"use client";

import React, { useState, useEffect } from "react";
import Navbar from "@/components/ui/navbar";
import { PulseLoader } from "@/components/ui/loaders";

export default function DocsPage() {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);
  const [activeSection, setActiveSection] = useState("introduction");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time for documentation
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2200);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <PulseLoader />;
  }

  const handleConnectWallet = async () => {
    if (isConnecting || isConnected) return;
    
    setIsConnecting(true);
    
    try {
      if (typeof window !== 'undefined' && (window as any).ethereum) {
        const accounts = await (window as any).ethereum.request({
          method: 'eth_requestAccounts'
        });
        
        if (accounts.length > 0) {
          setIsConnected(true);
          setWalletAddress(accounts[0]);
          console.log('Wallet connected:', accounts[0]);
        }
      } else {
        alert('Please install MetaMask or another Web3 wallet');
      }
    } catch (error: any) {
      console.error('Failed to connect wallet:', error);
      if (error?.code === 4001) {
        alert('Wallet connection was rejected by user');
      } else {
        alert('Failed to connect wallet. Please try again.');
      }
    } finally {
      setIsConnecting(false);
    }
  };

  const formatAddress = (address: string) => {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  const sections = [
    {
      title: "Getting Started",
      items: [
        { id: "introduction", title: "Introduction" },
        { id: "quickstart", title: "Quick Start" },
        { id: "installation", title: "Installation" },
      ]
    },
    {
      title: "Core Concepts",
      items: [
        { id: "time-capsules", title: "Time Capsules" },
        { id: "encryption", title: "Encryption" },
        { id: "blockchain", title: "Blockchain Integration" },
      ]
    },
    {
      title: "API Reference",
      items: [
        { id: "create-capsule", title: "Create Capsule" },
        { id: "retrieve-capsule", title: "Retrieve Capsule" },
        { id: "smart-contracts", title: "Smart Contracts" },
      ]
    },
    {
      title: "Advanced",
      items: [
        { id: "security", title: "Security" },
        { id: "deployment", title: "Deployment" },
        { id: "troubleshooting", title: "Troubleshooting" },
      ]
    }
  ];

  const renderContent = () => {
    switch (activeSection) {
      case "introduction":
        return (
          <div className="space-y-6">
            <h1 className="text-4xl font-bold text-white mb-4">Introduction</h1>
            <p className="text-gray-300 text-lg leading-relaxed">
              EmosiFloww is a decentralized time-capsule platform that allows you to store digital assets and messages on-chain, encrypted for the future. Built on blockchain technology, EmosiFloww ensures your memories are preserved securely and immutably.
            </p>
            
            <h2 className="text-2xl font-semibold text-white mt-8 mb-4">What is EmosiFloww?</h2>
            <p className="text-gray-300 leading-relaxed">
              EmosiFloww enables users to create digital time capsules that can contain files, messages, and even cryptocurrency. These capsules are locked with smart contracts and can only be opened at a predetermined time or when specific conditions are met.
            </p>

            <h2 className="text-2xl font-semibold text-white mt-8 mb-4">Key Features</h2>
            <ul className="text-gray-300 space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span><strong>Decentralized Storage:</strong> Your data is stored on IPFS and secured by blockchain</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span><strong>Time-locked Access:</strong> Capsules can only be opened at specified future dates</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span><strong>End-to-end Encryption:</strong> All content is encrypted using advanced cryptography</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span><strong>Multi-asset Support:</strong> Store files, messages, and cryptocurrency together</span>
              </li>
            </ul>
          </div>
        );
      
      case "quickstart":
        return (
          <div className="space-y-6">
            <h1 className="text-4xl font-bold text-white mb-4">Quick Start</h1>
            <p className="text-gray-300 text-lg leading-relaxed">
              Get started with EmosiFloww in just a few steps.
            </p>
            
            <h2 className="text-2xl font-semibold text-white mt-8 mb-4">Step 1: Connect Your Wallet</h2>
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <p className="text-gray-300 mb-2">Make sure you have MetaMask or another Web3 wallet installed:</p>
              <code className="text-blue-400">window.ethereum.request({`{ method: 'eth_requestAccounts' }`})</code>
            </div>

            <h2 className="text-2xl font-semibold text-white mt-8 mb-4">Step 2: Create Your First Capsule</h2>
            <ol className="text-gray-300 space-y-4">
              <li className="flex gap-3">
                <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">1</span>
                <span>Navigate to the "Create Capsule" page</span>
              </li>
              <li className="flex gap-3">
                <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">2</span>
                <span>Fill in the capsule details (title, description, unlock date)</span>
              </li>
              <li className="flex gap-3">
                <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">3</span>
                <span>Upload your files and add any messages</span>
              </li>
              <li className="flex gap-3">
                <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">4</span>
                <span>Optionally add ETH to your capsule</span>
              </li>
              <li className="flex gap-3">
                <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">5</span>
                <span>Deploy the capsule to the blockchain</span>
              </li>
            </ol>
          </div>
        );

      case "time-capsules":
        return (
          <div className="space-y-6">
            <h1 className="text-4xl font-bold text-white mb-4">Time Capsules</h1>
            <p className="text-gray-300 text-lg leading-relaxed">
              Understanding how EmosiFloww time capsules work and their lifecycle.
            </p>
            
            <h2 className="text-2xl font-semibold text-white mt-8 mb-4">Capsule Structure</h2>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <pre className="text-green-400 text-sm overflow-x-auto">
{`{
  "id": "capsule_123456",
  "title": "My Birthday Memories",
  "description": "Photos and videos from my 25th birthday",
  "creator": "0x1234...5678",
  "createdAt": "2025-09-27T10:00:00Z",
  "unlockDate": "2026-09-27T10:00:00Z",
  "files": [
    {
      "name": "birthday_photo.jpg",
      "hash": "QmX...abc123",
      "size": 2048576,
      "encrypted": true
    }
  ],
  "message": "Happy 26th birthday to future me!",
  "ethAmount": "0.1",
  "status": "locked"
}`}
              </pre>
            </div>

            <h2 className="text-2xl font-semibold text-white mt-8 mb-4">Capsule States</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
                <h3 className="text-yellow-400 font-semibold mb-2">Locked</h3>
                <p className="text-gray-300 text-sm">Capsule is sealed and cannot be accessed until unlock date</p>
              </div>
              <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                <h3 className="text-green-400 font-semibold mb-2">Unlocked</h3>
                <p className="text-gray-300 text-sm">Capsule can be opened and contents accessed</p>
              </div>
              <div className="bg-gray-500/10 border border-gray-500/30 rounded-lg p-4">
                <h3 className="text-gray-400 font-semibold mb-2">Expired</h3>
                <p className="text-gray-300 text-sm">Capsule has been opened and contents retrieved</p>
              </div>
            </div>
          </div>
        );

      case "smart-contracts":
        return (
          <div className="space-y-6">
            <h1 className="text-4xl font-bold text-white mb-4">Smart Contracts</h1>
            <p className="text-gray-300 text-lg leading-relaxed">
              Learn about the smart contracts powering EmosiFloww time capsules.
            </p>

            <h2 className="text-2xl font-semibold text-white mt-8 mb-4">Contract Architecture</h2>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <pre className="text-blue-400 text-sm overflow-x-auto">
{`// TimeCapsule Contract
pragma solidity ^0.8.19;

contract TimeCapsule {
    struct Capsule {
        address creator;
        string metadataHash;
        uint256 unlockTime;
        uint256 ethAmount;
        bool isOpened;
    }
    
    mapping(uint256 => Capsule) public capsules;
    uint256 public nextCapsuleId;
    
    function createCapsule(
        string memory _metadataHash,
        uint256 _unlockTime
    ) external payable {
        require(_unlockTime > block.timestamp, "Unlock time must be in future");
        
        capsules[nextCapsuleId] = Capsule({
            creator: msg.sender,
            metadataHash: _metadataHash,
            unlockTime: _unlockTime,
            ethAmount: msg.value,
            isOpened: false
        });
        
        nextCapsuleId++;
    }
    
    function openCapsule(uint256 _capsuleId) external {
        Capsule storage capsule = capsules[_capsuleId];
        require(capsule.creator == msg.sender, "Not capsule owner");
        require(block.timestamp >= capsule.unlockTime, "Capsule still locked");
        require(!capsule.isOpened, "Capsule already opened");
        
        capsule.isOpened = true;
        
        if (capsule.ethAmount > 0) {
            payable(msg.sender).transfer(capsule.ethAmount);
        }
    }
}`}
              </pre>
            </div>
          </div>
        );

      default:
        return (
          <div className="space-y-6">
            <h1 className="text-4xl font-bold text-white mb-4">Documentation</h1>
            <p className="text-gray-300 text-lg">
              Select a topic from the sidebar to view detailed documentation.
            </p>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="fixed top-0 left-0 right-0 z-50">
        <Navbar
          isConnected={isConnected}
          walletAddress={walletAddress}
          isConnecting={isConnecting}
          handleConnectWallet={handleConnectWallet}
          formatAddress={formatAddress}
        />
      </div>
      
      <div className="flex pt-20">
        {/* Sidebar */}
        <div className="w-64 bg-gray-900/50 border-r border-gray-700 min-h-screen p-6 fixed left-0 top-20 overflow-y-auto">
          <h2 className="text-xl font-bold text-white mb-6">Documentation</h2>
          
          {sections.map((section, sectionIndex) => (
            <div key={sectionIndex} className="mb-6">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
                {section.title}
              </h3>
              <ul className="space-y-2">
                {section.items.map((item) => (
                  <li key={item.id}>
                    <button
                      onClick={() => setActiveSection(item.id)}
                      className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                        activeSection === item.id
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-300 hover:text-white hover:bg-gray-800'
                      }`}
                    >
                      {item.title}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div className="flex-1 ml-64 p-8">
          <div className="max-w-4xl">
            {renderContent()}
          </div>
        </div>
      </div>
    </div>
  );
}
