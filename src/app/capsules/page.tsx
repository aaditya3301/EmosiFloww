"use client";

import React, { useState, useEffect } from "react";
import { Vortex } from "@/components/ui/vortex";
import Navbar from "@/components/ui/navbar";
import { CanvasRevealEffect } from "@/components/ui/canvas-reveal-effect";
import { AnimatePresence, motion } from "motion/react";
import { LoaderFive } from "@/components/ui/loader";
import { ethers } from 'ethers';

// Contract configurations
const NFT_CONTRACTS = {
  old: {
    address: '0xfb42a2c4b5eb535cfe704ef64da416f1cf69bde3',
    name: 'Public TimeCapsule NFT (Immediate Access)'
  },
  timeLocked: {
    address: '0x508bbc0cf873c11dbf9d72bfcea3dc1e69739c38',
    name: 'Time-Locked TimeCapsule NFT (Scheduled)'
  }
};

// Contract ABIs
const NFT_ABI = [
  "function tokenURI(uint256 tokenId) public view returns (string memory)",
  "function getEncryptedBlobId(uint256 tokenId) public view returns (string memory)", 
  "function getCreator(uint256 tokenId) public view returns (address)",
  "function balanceOf(address owner) public view returns (uint256)",
  "function ownerOf(uint256 tokenId) public view returns (address)",
  "function tokenOfOwnerByIndex(address owner, uint256 index) public view returns (uint256)"
];

const TIME_LOCKED_ABI = [
  "function getTimeCapsule(uint256 _capsuleId) external view returns (uint256 capsuleId, string memory encryptedBlobId, address owner, uint256 unlockTime, bool isUnlocked, string memory decryptionKey)",
  "function getUserCapsules(address _user) external view returns (uint256[] memory)",
  "function isReadyToUnlock(uint256 _capsuleId) external view returns (bool)"
];

// Type definitions
interface CapsuleData {
  id: number;
  type: 'immediate' | 'scheduled';
  contractAddress: string;
  title: string;
  description: string;
  status: string;
  statusColor: string;
  fileCount: string;
  canDownload: boolean;
  downloadUrl?: string | null;
  createdDate?: string;
  unlockDate?: string;
  unlockTime?: any;
  isUnlocked?: boolean;
  capsuleId?: string;
  metadata?: any;
  encryptedBlobId?: string;
}

interface NFTMetadata {
  name?: string;
  description?: string;
  capsuleId?: string;
  attributes?: Array<{
    trait_type: string;
    value: string;
  }>;
}

export default function CapsulesPage() {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [userCapsules, setUserCapsules] = useState<CapsuleData[]>([]);
  const [isFetching, setIsFetching] = useState(false);

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  // Fetch user's NFTs when wallet is connected
  useEffect(() => {
    if (isConnected && walletAddress) {
      fetchUserCapsules();
    }
  }, [isConnected, walletAddress]);

  const fetchUserCapsules = async () => {
    if (!walletAddress || !((window as any).ethereum)) return;
    
    setIsFetching(true);
    
    try {
      const provider = new ethers.BrowserProvider((window as any).ethereum);
      const capsules: CapsuleData[] = [];

      // Fetch from immediate access NFT contract
      try {
        const oldContract = new ethers.Contract(NFT_CONTRACTS.old.address, NFT_ABI, provider);
        const balance = await oldContract.balanceOf(walletAddress);
        
        console.log(`📊 Found ${balance} immediate access NFTs`);
        
        for (let i = 0; i < Number(balance); i++) {
          try {
            const tokenId = await oldContract.tokenOfOwnerByIndex(walletAddress, i);
            const [tokenURI, encryptedBlobId] = await Promise.all([
              oldContract.tokenURI(tokenId),
              oldContract.getEncryptedBlobId(tokenId)
            ]);

            let metadata: NFTMetadata = {};
            if (tokenURI.startsWith('data:application/json;base64,')) {
              const base64Data = tokenURI.split(',')[1];
              const jsonData = atob(base64Data);
              metadata = JSON.parse(jsonData);
            }

            // Decrypt the blob ID to get download URL
            let downloadUrl = null;
            try {
              const decrypted = await decryptBlobId(encryptedBlobId);
              downloadUrl = decrypted.walrusUrl;
            } catch (e) {
              console.warn('Could not decrypt blob ID:', e);
            }

            capsules.push({
              id: Number(tokenId),
              type: 'immediate',
              contractAddress: NFT_CONTRACTS.old.address,
              title: metadata.name || `Capsule #${tokenId}`,
              description: metadata.description || 'Time capsule content',
              status: 'Unlocked',
              statusColor: 'text-green-400 bg-green-500/20',
              createdDate: metadata.attributes?.find((a: any) => a.trait_type === 'Created')?.value || 'Unknown',
              fileCount: '1 file',
              canDownload: true,
              downloadUrl: downloadUrl,
              capsuleId: metadata.capsuleId,
              metadata: metadata
            });
          } catch (error) {
            console.error(`Error fetching NFT ${i}:`, error);
          }
        }
      } catch (error) {
        console.error('Error fetching immediate access NFTs:', error);
      }

      // Fetch from time-locked contract
      try {
        const timeLockContract = new ethers.Contract(NFT_CONTRACTS.timeLocked.address, TIME_LOCKED_ABI, provider);
        const userCapsuleIds = await timeLockContract.getUserCapsules(walletAddress);
        
        console.log(`📊 Found ${userCapsuleIds.length} time-locked capsules`);
        
        for (const capsuleId of userCapsuleIds) {
          try {
            const capsuleData = await timeLockContract.getTimeCapsule(capsuleId);
            
            // Handle both array and object formats
            let id, encryptedBlobId, owner, unlockTime, isUnlocked, decryptionKey;
            if (Array.isArray(capsuleData)) {
              [id, encryptedBlobId, owner, unlockTime, isUnlocked, decryptionKey] = capsuleData;
            } else {
              ({ capsuleId: id, encryptedBlobId, owner, unlockTime, isUnlocked, decryptionKey } = capsuleData);
            }

            const unlockDate = new Date(Number(unlockTime) * 1000);
            const now = new Date();
            const canDownload = isUnlocked;
            
            let downloadUrl = null;
            if (isUnlocked && decryptionKey) {
              // For unlocked capsules, try to get the download URL
              try {
                if (decryptionKey.startsWith('http')) {
                  downloadUrl = decryptionKey;
                } else {
                  // Try to decrypt if it's an encrypted blob
                  const decrypted = await decryptBlobId(encryptedBlobId);
                  downloadUrl = decrypted.walrusUrl;
                }
              } catch (e) {
                console.warn('Could not get download URL:', e);
              }
            }

            let status, statusColor;
            if (isUnlocked) {
              status = 'Unlocked';
              statusColor = 'text-green-400 bg-green-500/20';
            } else if (unlockDate <= now) {
              status = 'Ready to Unlock';
              statusColor = 'text-yellow-400 bg-yellow-500/20';
            } else {
              status = 'Locked';
              statusColor = 'text-red-400 bg-red-500/20';
            }

            capsules.push({
              id: Number(id),
              type: 'scheduled',
              contractAddress: NFT_CONTRACTS.timeLocked.address,
              title: `Time Capsule #${id}`,
              description: isUnlocked ? 'Unlocked time capsule' : `Unlocks: ${unlockDate.toLocaleDateString()}`,
              status: status,
              statusColor: statusColor,
              unlockTime: unlockTime,
              unlockDate: unlockDate.toLocaleDateString(),
              isUnlocked: isUnlocked,
              canDownload: canDownload,
              downloadUrl: downloadUrl,
              fileCount: '1 file',
              encryptedBlobId: encryptedBlobId
            });
          } catch (error) {
            console.error(`Error fetching capsule ${capsuleId}:`, error);
          }
        }
      } catch (error) {
        console.error('Error fetching time-locked capsules:', error);
      }

      setUserCapsules(capsules);
      console.log(`✅ Total capsules found: ${capsules.length}`);
      
    } catch (error) {
      console.error('Error fetching user capsules:', error);
    } finally {
      setIsFetching(false);
    }
  };

  // Decrypt blob ID function
  const decryptBlobId = async (encryptedBlobId: string) => {
    try {
      const CryptoJS = await import('crypto-js') as any;
      const secretKey = 'tempris-time-capsule-secret-2025';
      
      const decryptedBytes = CryptoJS.AES.decrypt(encryptedBlobId, secretKey);
      const originalBlobId = decryptedBytes.toString(CryptoJS.enc.Utf8);
      
      return {
        originalBlobId: originalBlobId,
        walrusUrl: `https://aggregator.walrus-testnet.walrus.space/v1/${originalBlobId}`
      };
    } catch (error) {
      throw error;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center w-full h-screen">
        <LoaderFive text="Loading Capsules..." />
      </div>
    );
  }

  const handleConnectWallet = async () => {
    if (isConnecting || isConnected) return;
    
    setIsConnecting(true);
    
    try {
      // Check if wallet is available
      if (typeof window !== 'undefined' && (window as any).ethereum) {
        // Request wallet connection
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

  // Handle wallet restoration from JWT
  const handleWalletRestore = (address: string) => {
    setIsConnected(true);
    setWalletAddress(address);
    console.log('Wallet restored from JWT:', address);
  };

  // Handle wallet disconnection
  const handleWalletDisconnect = () => {
    setIsConnected(false);
    setWalletAddress("");
    console.log('Wallet disconnected');
  };

  return (
    <div className="w-full h-screen overflow-hidden">
      <Navbar
        isConnected={isConnected}
        walletAddress={walletAddress}
        isConnecting={isConnecting}
        handleConnectWallet={handleConnectWallet}
        formatAddress={formatAddress}
        onWalletRestore={handleWalletRestore}
        onWalletDisconnect={handleWalletDisconnect}
      />
      
      {/* Vortex Background */}
      <div className="w-full h-full">
        <Vortex
          backgroundColor="black"
          rangeY={800}
          particleCount={500}
          baseHue={120}
          className="flex flex-col items-center justify-center px-6 md:px-16 py-4 w-full h-full pt-20"
        >
            {/* Capsules Content */}
            <div className="w-full flex-1 flex flex-col items-center justify-center">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-white mb-2">
                  My Time Capsules
                </h2>
                <p className="text-gray-400 text-sm">
                  {isConnected 
                    ? `Found ${userCapsules.length} capsules in your wallet`
                    : "Connect your wallet to view your stored memories"
                  }
                </p>
                
                {isConnected && isFetching && (
                  <div className="mt-4">
                    <LoaderFive text="Loading your capsules..." />
                  </div>
                )}
              </div>

              {/* Connect Wallet Message */}
              {!isConnected && (
                <div className="max-w-md mx-auto text-center">
                  <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-6">
                    <div className="text-blue-400 text-4xl mb-4">🔗</div>
                    <h3 className="text-white font-medium text-lg mb-2">Connect Your Wallet</h3>
                    <p className="text-gray-400 text-sm mb-4">
                      Connect your MetaMask wallet to view and manage your time capsules stored as NFTs.
                    </p>
                  </div>
                </div>
              )}

              {/* Capsules Grid */}
              {isConnected && !isFetching && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 max-w-7xl w-full">
                  
                  {/* User's Actual Capsules */}
                  {userCapsules.map((capsule) => (
                    <CapsuleCard
                      key={`${capsule.contractAddress}-${capsule.id}`}
                      capsule={capsule}
                    />
                  ))}

                  {/* Create New Capsule Card */}
                  <CreateCapsuleCard />

                  {/* Empty State */}
                  {userCapsules.length === 0 && (
                    <div className="col-span-full text-center py-12">
                      <div className="text-gray-400 text-6xl mb-4">📦</div>
                      <h3 className="text-white font-medium text-lg mb-2">No Capsules Found</h3>
                      <p className="text-gray-400 text-sm mb-6">
                        You haven't created any time capsules yet. Start by creating your first one!
                      </p>
                      <a 
                        href="/deploy" 
                        className="inline-block px-6 py-3 bg-blue-500/20 border border-blue-500/30 text-blue-300 rounded-lg hover:bg-blue-500/30 transition-colors"
                      >
                        Create Your First Capsule
                      </a>
                    </div>
                  )}

                </div>
              )}
            </div>
        </Vortex>
      </div>
    </div>
  );
}

// Capsule Card Component
const CapsuleCard = ({
  capsule
}: {
  capsule: CapsuleData;
}) => {
  const [hovered, setHovered] = React.useState(false);
  
  const getCanvasEffect = (type: string, status: string) => {
    if (type === 'immediate') {
      return (
        <CanvasRevealEffect
          animationSpeed={3}
          containerClassName="bg-green-900"
          colors={[[34, 197, 94], [22, 163, 74]]}
          dotSize={2}
        />
      );
    } else if (status === 'Unlocked') {
      return (
        <CanvasRevealEffect
          animationSpeed={3}
          containerClassName="bg-purple-900"
          colors={[[168, 85, 247], [124, 58, 237]]}
          dotSize={2.5}
        />
      );
    } else {
      return (
        <CanvasRevealEffect
          animationSpeed={0.3}
          containerClassName="bg-red-900"
          colors={[[239, 68, 68]]}
          dotSize={2}
        />
      );
    }
  };

  const handleDownload = () => {
    if (capsule.canDownload && capsule.downloadUrl) {
      window.open(capsule.downloadUrl, '_blank');
    }
  };

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="border border-white/20 group/canvas-card flex items-center justify-center max-w-sm w-full mx-auto p-4 relative h-64 rounded-lg cursor-pointer"
    >
      <AnimatePresence>
        {hovered && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="h-full w-full absolute inset-0"
          >
            {getCanvasEffect(capsule.type, capsule.status)}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="relative z-20 w-full h-full flex flex-col justify-between">
        <div className="flex justify-between items-start group-hover/canvas-card:opacity-0 transition duration-200">
          <div className="flex-1">
            <h3 className="text-white font-medium text-sm mb-1 truncate">{capsule.title}</h3>
            <div className="text-xs text-gray-400">#{capsule.id} • {capsule.type === 'immediate' ? 'Immediate' : 'Time-Locked'}</div>
          </div>
          <span className={`text-xs px-2 py-1 rounded ${capsule.statusColor}`}>
            {capsule.status}
          </span>
        </div>
        
        <div className="group-hover/canvas-card:opacity-0 transition duration-200">
          <p className="text-gray-400 text-xs mb-3 line-clamp-2">{capsule.description}</p>
          <div className="flex justify-between items-end text-xs text-gray-400">
            <div>
              <div>{capsule.fileCount}</div>
              {capsule.createdDate && (
                <div className="text-xs text-gray-500">{capsule.createdDate}</div>
              )}
              {capsule.unlockDate && (
                <div className="text-xs text-gray-500">Unlocks: {capsule.unlockDate}</div>
              )}
            </div>
            {capsule.canDownload && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDownload();
                }}
                className="text-blue-400 hover:text-blue-300 text-xs underline"
              >
                Download
              </button>
            )}
          </div>
        </div>

        {/* Hover content */}
        <div className="absolute inset-0 flex flex-col justify-center items-center opacity-0 group-hover/canvas-card:opacity-100 transition duration-200">
          <h2 className="text-white text-lg font-bold mb-2 text-center group-hover/canvas-card:-translate-y-4 transition duration-200 line-clamp-2">
            {capsule.title}
          </h2>
          <p className="text-gray-300 text-sm text-center mb-4 line-clamp-2">{capsule.description}</p>
          
          {capsule.canDownload ? (
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDownload();
              }}
              className="px-4 py-2 bg-blue-500/20 border border-blue-500/30 text-blue-300 rounded-lg hover:bg-blue-500/30 transition-colors text-sm"
            >
              📥 Download Content
            </button>
          ) : (
            <div className="px-4 py-2 bg-red-500/20 border border-red-500/30 text-red-300 rounded-lg text-sm">
              🔒 {capsule.status}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Create Capsule Card Component
const CreateCapsuleCard = () => {
  const [hovered, setHovered] = React.useState(false);
  
  const handleCreateNew = () => {
    window.location.href = '/deploy';
  };

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={handleCreateNew}
      className="border border-white/30 border-dashed group/canvas-card flex items-center justify-center max-w-sm w-full mx-auto p-4 relative h-64 rounded-lg cursor-pointer hover:border-white/50 transition-all"
    >
      <AnimatePresence>
        {hovered && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="h-full w-full absolute inset-0"
          >
            <CanvasRevealEffect
              animationSpeed={0.4}
              containerClassName="bg-slate-900"
              colors={[[255, 255, 255]]}
              dotSize={1.5}
              opacities={[0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4]}
            />
          </motion.div>
        )}
      </AnimatePresence>

      <div className="relative z-20 flex flex-col items-center justify-center text-center">
        <div className="text-gray-400 text-4xl mb-4 group-hover/canvas-card:-translate-y-4 group-hover/canvas-card:opacity-0 transition duration-200">
          +
        </div>
        <h3 className="text-white font-medium text-sm mb-2 opacity-0 group-hover/canvas-card:opacity-100 group-hover/canvas-card:-translate-y-2 transition duration-200">
          Create New Capsule
        </h3>
        <p className="text-gray-500 text-xs opacity-0 group-hover/canvas-card:opacity-100 transition duration-200">
          Store your memories for the future
        </p>
      </div>
    </div>
  );
};
