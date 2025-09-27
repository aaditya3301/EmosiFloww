"use client";

import React, { useState, useEffect } from "react";
import { Vortex } from "@/components/ui/vortex";
import Navbar from "@/components/ui/navbar";
import { LoaderFive } from "@/components/ui/loader";
import { checkTimeCapsuleStatus, unlockScheduledTimeCapsule } from "@/store/functions";

interface TimeCapsuleStatus {
  capsuleId: number;
  encryptedBlobId: string;
  owner: string;
  unlockTime: number;
  isUnlocked: boolean;
  isReady: boolean;
  timeUntilUnlock: number;
  decryptionKey?: string;
}

export default function TimeCapsuleStatus() {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [capsuleId, setCapsuleId] = useState('');
  const [capsuleStatus, setCapsuleStatus] = useState<TimeCapsuleStatus | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [isUnlocking, setIsUnlocking] = useState(false);
  const [error, setError] = useState('');
  const [decryptionKey, setDecryptionKey] = useState('');

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center w-full h-screen">
        <LoaderFive text="Loading Status..." />
      </div>
    );
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

  const checkStatus = async () => {
    if (!capsuleId) {
      setError('Please enter a Hedera capsule ID');
      return;
    }

    setIsChecking(true);
    setError('');
    setCapsuleStatus(null);

    try {
      const status = await checkTimeCapsuleStatus(parseInt(capsuleId)) as any;
      setCapsuleStatus(status);
      console.log('Capsule status:', status);
    } catch (error) {
      console.error('Failed to check capsule status:', error);
      setError(error instanceof Error ? error.message : 'Failed to check capsule status');
    } finally {
      setIsChecking(false);
    }
  };

  const unlockCapsule = async () => {
    if (!capsuleStatus || !decryptionKey) {
      setError('Please provide the decryption key');
      return;
    }

    if (!capsuleStatus.isReady) {
      setError('Time capsule is not ready to unlock yet');
      return;
    }

    setIsUnlocking(true);
    setError('');

    try {
      const result = await unlockScheduledTimeCapsule(capsuleStatus.capsuleId, decryptionKey) as any;
      
      if (result.success) {
        alert('Time capsule unlocked successfully!');
        // Refresh status
        await checkStatus();
      } else {
        setError('Failed to unlock time capsule');
      }
    } catch (error) {
      console.error('Failed to unlock capsule:', error);
      setError(error instanceof Error ? error.message : 'Failed to unlock capsule');
    } finally {
      setIsUnlocking(false);
    }
  };

  const formatTimeRemaining = (seconds: number) => {
    if (seconds <= 0) return 'Ready to unlock!';
    
    const days = Math.floor(seconds / (24 * 60 * 60));
    const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));
    const minutes = Math.floor((seconds % (60 * 60)) / 60);
    
    if (days > 0) return `${days}d ${hours}h ${minutes}m remaining`;
    if (hours > 0) return `${hours}h ${minutes}m remaining`;
    return `${minutes}m remaining`;
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
      
      <div className="w-full h-full">
        <Vortex
          backgroundColor="black"
          rangeY={800}
          particleCount={500}
          baseHue={280} // Purple theme for status page
          className="flex items-center justify-center px-6 md:px-16 py-4 w-full h-full pt-20"
        >
          <div className="w-full max-w-2xl bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold text-white mb-2">
                Time Capsule Status
              </h2>
              <p className="text-gray-400 text-sm">
                Check and unlock your scheduled time capsules
              </p>
            </div>

            <div className="space-y-4">
              {/* Capsule ID Input */}
              <div>
                <label className="block text-white text-sm font-medium mb-2">
                  Hedera Capsule ID
                </label>
                <div className="flex gap-2">
                  <input
                    type="number"
                    placeholder="Enter Hedera capsule ID (e.g. 1, 2, 3...)"
                    value={capsuleId}
                    onChange={(e) => setCapsuleId(e.target.value)}
                    className="flex-1 px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none"
                  />
                  <button
                    onClick={checkStatus}
                    disabled={isChecking || !capsuleId}
                    className="px-6 py-2.5 bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-purple-300 font-medium rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isChecking ? (
                      <span className="flex items-center gap-2">
                        <div className="w-4 h-4 border border-current border-t-transparent rounded-full animate-spin"></div>
                        Checking...
                      </span>
                    ) : 'Check Status'}
                  </button>
                </div>
              </div>

              {/* Error Display */}
              {error && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                  <div className="text-red-400 text-sm">{error}</div>
                </div>
              )}

              {/* Capsule Status Display */}
              {capsuleStatus && (
                <div className="space-y-4">
                  <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                    <h3 className="text-purple-300 font-medium mb-3">Capsule Information</h3>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-400">Capsule ID:</span>
                        <div className="text-white font-mono">#{capsuleStatus.capsuleId}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Owner:</span>
                        <div className="text-white font-mono">{formatAddress(capsuleStatus.owner)}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Unlock Time:</span>
                        <div className="text-white">
                          {new Date(capsuleStatus.unlockTime * 1000).toLocaleString()}
                        </div>
                      </div>
                      <div>
                        <span className="text-gray-400">Status:</span>
                        <div className={`font-medium ${
                          capsuleStatus.isUnlocked 
                            ? 'text-green-400' 
                            : capsuleStatus.isReady 
                            ? 'text-yellow-400' 
                            : 'text-purple-400'
                        }`}>
                          {capsuleStatus.isUnlocked 
                            ? '🔓 Unlocked' 
                            : capsuleStatus.isReady 
                            ? '⏰ Ready to unlock' 
                            : '🔒 Locked'
                          }
                        </div>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-purple-500/30">
                      <span className="text-gray-400 text-sm">Encrypted Blob ID:</span>
                      <div className="text-white font-mono text-xs bg-black/30 rounded p-2 mt-1 break-all">
                        {capsuleStatus.encryptedBlobId}
                      </div>
                    </div>

                    {!capsuleStatus.isUnlocked && (
                      <div className="mt-4 pt-4 border-t border-purple-500/30">
                        <div className={`text-center py-3 rounded-lg ${
                          capsuleStatus.isReady 
                            ? 'bg-yellow-500/10 border border-yellow-500/30 text-yellow-300'
                            : 'bg-purple-500/10 border border-purple-500/30 text-purple-300'
                        }`}>
                          {capsuleStatus.isReady ? (
                            <div>
                              <div className="text-lg font-medium mb-1">🎉 Ready to Unlock!</div>
                              <div className="text-sm">You can now unlock this time capsule</div>
                            </div>
                          ) : (
                            <div>
                              <div className="text-lg font-medium mb-1">⏳ Time Remaining</div>
                              <div className="text-sm">{formatTimeRemaining(capsuleStatus.timeUntilUnlock)}</div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {capsuleStatus.isUnlocked && capsuleStatus.decryptionKey && (
                      <div className="mt-4 pt-4 border-t border-green-500/30">
                        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3">
                          <h4 className="text-green-300 font-medium mb-2">🔓 Unlocked Successfully!</h4>
                          <span className="text-gray-400 text-sm">Decryption Key:</span>
                          <div className="text-green-300 font-mono text-xs bg-black/30 rounded p-2 mt-1 break-all">
                            {capsuleStatus.decryptionKey}
                          </div>
                          <div className="text-xs text-gray-400 mt-2">
                            Use this key to decrypt your time capsule content
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Unlock Section */}
                  {capsuleStatus.isReady && !capsuleStatus.isUnlocked && (
                    <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
                      <h3 className="text-yellow-300 font-medium mb-3">Unlock Time Capsule</h3>
                      
                      <div className="space-y-3">
                        <div>
                          <label className="block text-white text-sm font-medium mb-2">
                            Decryption Key
                          </label>
                          <input
                            type="text"
                            placeholder="Enter your decryption key"
                            value={decryptionKey}
                            onChange={(e) => setDecryptionKey(e.target.value)}
                            className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none font-mono text-sm"
                          />
                          <p className="text-xs text-gray-400 mt-1">
                            This is the key you received when creating the time capsule
                          </p>
                        </div>

                        <button
                          onClick={unlockCapsule}
                          disabled={isUnlocking || !decryptionKey || !isConnected}
                          className="w-full px-6 py-3 bg-yellow-500/20 hover:bg-yellow-500/30 border border-yellow-500/50 text-yellow-300 font-medium rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {isUnlocking ? (
                            <span className="flex items-center justify-center gap-2">
                              <div className="w-4 h-4 border border-current border-t-transparent rounded-full animate-spin"></div>
                              Unlocking...
                            </span>
                          ) : '🔓 Unlock Time Capsule'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Information Panel */}
              <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 text-left">
                <h3 className="text-blue-400 font-medium mb-2">ℹ️ How it works:</h3>
                <ul className="text-gray-300 text-sm space-y-1">
                  <li>• Enter your Hedera capsule ID to check status</li>
                  <li>• Time capsules are locked until their specified unlock time</li>
                  <li>• Once ready, provide your decryption key to unlock</li>
                  <li>• Unlocked capsules reveal their decryption keys</li>
                </ul>
              </div>
            </div>
          </div>
        </Vortex>
      </div>
    </div>
  );
}