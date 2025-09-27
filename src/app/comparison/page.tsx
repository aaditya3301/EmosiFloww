"use client";

import React, { useState, useEffect } from "react";
import { Vortex } from "@/components/ui/vortex";
import Navbar from "@/components/ui/navbar";
import { SpinnerLoader } from "@/components/ui/loaders";
import { fetchNFTMetadataComparison, displayComparisonTable } from "@/lib/nft-metadata-fetcher";
import { testTimeCapsuleContract, testCreateCapsule } from "@/lib/contract-tester";

export default function MetadataChecker() {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [metadata, setMetadata] = useState<any>(null);
  const [isFetching, setIsFetching] = useState(false);
  const [error, setError] = useState('');
  const [tokenId, setTokenId] = useState('1');
  const [unlockingCapsule, setUnlockingCapsule] = useState<number | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <SpinnerLoader />;
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

  const handleWalletRestore = (address: string) => {
    setIsConnected(true);
    setWalletAddress(address);
    console.log('Wallet restored from JWT:', address);
  };

  const handleWalletDisconnect = () => {
    setIsConnected(false);
    setWalletAddress("");
    console.log('Wallet disconnected');
  };

  const checkMetadata = async () => {
    setIsFetching(true);
    setError('');
    setMetadata(null);
    
    try {
      // Parse token ID
      const id = parseInt(tokenId.trim());
      
      if (isNaN(id) || id <= 0) {
        throw new Error('Please enter a valid token ID (e.g., 1)');
      }

      console.log('🔍 Checking metadata for token ID:', id);
      
      // Fetch metadata data
      const metadataData = await fetchNFTMetadataComparison([id]);
      setMetadata(metadataData);
      
      // Display in console
      displayComparisonTable(metadataData);
      
      console.log('✅ Metadata checked successfully! Check console for detailed tables.');
      
    } catch (error) {
      console.error('Failed to check metadata:', error);
      setError(error instanceof Error ? error.message : 'Failed to check metadata');
    } finally {
      setIsFetching(false);
    }
  };

  const handleUnlockCheck = async (capsuleId: number, nft: any) => {
    if (!window.ethereum) {
      alert('Please connect your wallet first');
      return;
    }

    setUnlockingCapsule(capsuleId);
    
    try {
      console.log(`🔍 Checking unlock status for capsule #${capsuleId}...`);
      
      // Import ethers dynamically
      const { ethers } = await import('ethers');
      
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      
      const contractAbi = [
        "function getTimeCapsule(uint256 _capsuleId) external view returns (uint256 capsuleId, string memory encryptedBlobId, address owner, uint256 unlockTime, bool isUnlocked, string memory decryptionKey)",
        "function isReadyToUnlock(uint256 _capsuleId) external view returns (bool)",
        "function unlockTimeCapsule(uint256 _capsuleId, string memory _decryptionKey) external"
      ];
      
      const contract = new ethers.Contract('0x508bbc0cf873c11dbf9d72bfcea3dc1e69739c38', contractAbi, signer);
      
      // Check current status
      const capsuleData = await contract.getTimeCapsule(capsuleId);
      const isReady = await contract.isReadyToUnlock(capsuleId);
      
      const currentTime = new Date();
      const unlockTime = new Date(Number(capsuleData.unlockTime) * 1000);
      const timeLeft = unlockTime.getTime() - currentTime.getTime();
      
      console.log(`📊 Capsule #${capsuleId} Status:`, {
        isUnlocked: capsuleData.isUnlocked,
        isReady: isReady,
        unlockTime: unlockTime.toLocaleString(),
        timeLeft: timeLeft > 0 ? `${Math.ceil(timeLeft / 1000)}s` : 'Time expired'
      });
      
      if (capsuleData.isUnlocked) {
        alert(`🔓 Capsule #${capsuleId} is already unlocked!\nDecrypted content: ${capsuleData.decryptionKey}`);
      } else if (isReady && timeLeft <= 0) {
        // Time is up, try to unlock
        const shouldUnlock = confirm(`⏰ Time is up for capsule #${capsuleId}!\nUnlock time was: ${unlockTime.toLocaleString()}\n\nWould you like to unlock it now?`);
        
        if (shouldUnlock) {
          console.log(`🔓 Attempting to unlock capsule #${capsuleId}...`);
          const tx = await contract.unlockTimeCapsule(capsuleId, capsuleData.decryptionKey);
          console.log('📝 Unlock transaction sent:', tx.hash);
          
          alert(`🚀 Unlock transaction sent!\nTransaction: ${tx.hash}\n\nRefresh the page after confirmation to see decrypted content.`);
          
          // Wait for confirmation
          const receipt = await tx.wait();
          console.log('✅ Unlock confirmed:', receipt.transactionHash);
          
          // Refresh metadata to show updated status
          checkMetadata();
        }
      } else {
        // Still locked
        const timeLeftText = timeLeft > 0 ? 
          `${Math.floor(timeLeft / 60000)}m ${Math.ceil((timeLeft % 60000) / 1000)}s` : 
          'Should be unlockable now';
          
        alert(`🔒 Capsule #${capsuleId} is still locked\n\nUnlock time: ${unlockTime.toLocaleString()}\nTime left: ${timeLeftText}\nCurrent time: ${currentTime.toLocaleString()}`);
      }
      
    } catch (error: any) {
      console.error('Failed to check unlock status:', error);
      alert(`❌ Error checking capsule #${capsuleId}:\n${error.message}`);
    } finally {
      setUnlockingCapsule(null);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden">
      <Vortex
        backgroundColor="black"
        rangeY={800}
        particleCount={500}
        baseHue={120}
      >
        <div className="relative z-10">
          {/* Navigation */}
          <Navbar 
            isConnected={isConnected}
            walletAddress={walletAddress}
            handleConnectWallet={handleConnectWallet}
            onWalletRestore={handleWalletRestore}
            onWalletDisconnect={handleWalletDisconnect}
            isConnecting={isConnecting}
            formatAddress={formatAddress}
          />

          {/* Main Content */}
          <div className="container mx-auto px-6 py-12">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-white mb-4">🔍 NFT Metadata Checker</h1>
              <p className="text-gray-400 text-lg">
                Check individual NFT metadata and view blob ID type (encrypted or plaintext)
              </p>
            </div>

            {/* Input Section */}
            <div className="max-w-2xl mx-auto mb-8">
              <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-700">
                <h2 className="text-white font-medium mb-4">🔍 Check NFT Metadata</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-gray-300 text-sm font-medium mb-2">
                      Token ID
                    </label>
                    <input
                      type="number"
                      value={tokenId}
                      onChange={(e) => setTokenId(e.target.value)}
                      className="w-full px-4 py-2 bg-black/50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none"
                      placeholder="1"
                      min="1"
                    />
                  </div>
                  
                  <button
                    onClick={checkMetadata}
                    disabled={isFetching || !tokenId.trim()}
                    className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors duration-200"
                  >
                    {isFetching ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Checking...
                      </div>
                    ) : 'Check Metadata'}
                  </button>

                  {/* Contract Test Button */}
                  <button
                    onClick={() => {
                      testTimeCapsuleContract().then(result => {
                        if (result.success) {
                          console.log('✅ Contract test completed successfully!');
                        } else {
                          console.error('❌ Contract test failed:', result.error);
                        }
                      });
                    }}
                    className="w-full px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-colors duration-200"
                  >
                    🧪 Test Contract
                  </button>
                </div>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="max-w-2xl mx-auto mb-6">
                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
                  <div className="text-red-400 text-sm">{error}</div>
                </div>
              </div>
            )}

            {/* Results */}
            {metadata && metadata.nfts && (
              <div className="max-w-4xl mx-auto space-y-6">
                <h3 className="text-white font-medium text-lg text-center">📋 NFT Metadata</h3>
                
                <div className="grid gap-4">
                  {metadata.nfts.map((nft: any, index: number) => (
                    <div key={index} className={`rounded-lg p-6 border ${
                      nft.error 
                        ? 'bg-red-500/10 border-red-500/30' 
                        : nft.contractType.includes('Time-Locked')
                        ? 'bg-purple-500/10 border-purple-500/30'
                        : 'bg-green-500/10 border-green-500/30'
                    }`}>
                      {nft.error ? (
                        <div className="text-center">
                          <div className="text-lg font-medium text-red-400 mb-2">❌ {nft.contractType}</div>
                          <div className="text-red-300">{nft.error}</div>
                        </div>
                      ) : (
                        <div className="space-y-4">
                          {/* Header */}
                          <div className="text-center">
                            <div className="text-2xl font-bold text-white mb-2">{nft.name}</div>
                            <div className="text-gray-400">#{nft.tokenId} • {nft.contractType}</div>
                          </div>

                          {/* Status Badge */}
                          <div className="text-center">
                            <div className={`inline-block px-4 py-2 rounded-lg ${
                              nft.isUnlocked ? 'bg-green-500/20 text-green-300 border border-green-500/30' :
                              nft.unlockTime ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' :
                              'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                            }`}>
                              {nft.isUnlocked ? '🔓 Unlocked & Available' : 
                               nft.unlockTime ? '🔒 Time-Locked' : 
                               '📥 Immediately Available'}
                            </div>
                          </div>

                          {/* Description */}
                          <div className="text-center text-gray-300">{nft.description}</div>

                          {/* Blob Information */}
                          <div className="bg-black/40 rounded-lg p-4">
                            <div className="text-center mb-3">
                              <div className={`inline-block text-lg font-bold px-4 py-2 rounded-lg ${
                                nft.blobType.includes('Decrypted') 
                                  ? 'bg-green-500/20 text-green-300 border border-green-500/30'
                                  : nft.blobType.includes('Encrypted') 
                                  ? 'bg-orange-500/20 text-orange-300 border border-orange-500/30' 
                                  : 'bg-green-500/20 text-green-300 border border-green-500/30'
                              }`}>
                                {nft.blobType.includes('Decrypted') ? '🔓 DECRYPTED CONTENT' :
                                 nft.blobType.includes('Encrypted') ? '🔐 ENCRYPTED BLOB ID' : 
                                 '📁 PLAINTEXT BLOB ID'}
                              </div>
                            </div>
                            
                            <div className="bg-black/60 rounded p-3 text-center">
                              <div className="text-xs text-gray-400 mb-1">
                                {nft.actualContent ? 'Decrypted Content:' : 'Blob ID:'}
                              </div>
                              <div className={`font-mono text-sm break-all ${
                                nft.actualContent ? 'text-green-300' : 'text-white'
                              }`}>
                                {nft.blobId}
                              </div>
                            </div>
                            
                            {/* Show original encrypted blob if we have decrypted content */}
                            {nft.actualContent && (
                              <div className="mt-3 bg-black/30 rounded p-2">
                                <div className="text-xs text-gray-400 mb-1">Original Encrypted Blob:</div>
                                <div className="text-gray-500 font-mono text-xs break-all">
                                  {nft.blobId !== nft.actualContent ? 'Available in contract' : 'N/A'}
                                </div>
                              </div>
                            )}
                          </div>

                          {/* Additional Details */}
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                            <div className="text-center">
                              <div className="text-gray-400 mb-1">Owner:</div>
                              <div className="text-white font-mono">{formatAddress(nft.owner || 'Unknown')}</div>
                            </div>
                            {nft.unlockTime && (
                              <div className="text-center">
                                <div className="text-gray-400 mb-1">Unlock Time:</div>
                                <div className="text-white">{nft.unlockTime.toLocaleString()}</div>
                              </div>
                            )}
                          </div>

                          {/* Decryption Key */}
                          {nft.decryptionKey && (
                            <div className="bg-green-500/10 border border-green-500/30 rounded p-4">
                              <div className="text-center">
                                <div className="text-green-300 font-medium mb-2">🔑 Decryption Key Available</div>
                                <div className="text-green-300 font-mono text-xs break-all bg-black/30 rounded p-2">
                                  {nft.decryptionKey}
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* Console Note */}
                <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 text-center">
                  <div className="text-yellow-300 text-sm">
                    💡 Check your browser console for detailed metadata tables!
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </Vortex>
    </div>
  );
}