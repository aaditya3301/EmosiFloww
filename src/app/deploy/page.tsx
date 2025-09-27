"use client";

import React, { useState, useEffect } from "react";
import { Vortex } from "@/components/ui/vortex";
import Navbar from "@/components/ui/navbar";
import { FileUpload } from "@/components/ui/file-upload";
import { SpinnerLoader } from "@/components/ui/loaders";
import { walrus, createTimeCapsule } from "@/store/functions";

interface UploadedFile {
  file: File;
  blobId?: string;
  fileUrl?: string;
  encryptedBlobId?: string;
  capsuleId?: string;
  nftTokenId?: number;
  nftTxHash?: string;
  status: 'pending' | 'uploading' | 'uploaded' | 'minting' | 'completed' | 'error';
  error?: string;
}

export default function VortexDemoSecond() {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [ethAmount, setEthAmount] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1800);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <SpinnerLoader />;
  }

  const handleFileUpload = async (files: File[]) => {
    const newFiles: UploadedFile[] = files.map(file => ({
      file,
      status: 'pending' as const
    }));
    
    setUploadedFiles(prev => [...prev, ...newFiles]);
    
    // Upload files to Walrus
    await uploadFilesToWalrus(newFiles);
  };

  const uploadFilesToWalrus = async (filesToUpload: UploadedFile[]) => {
    setIsUploading(true);
    
    for (let i = 0; i < filesToUpload.length; i++) {
      const fileObj = filesToUpload[i];
      
      // Update status to uploading
      setUploadedFiles(prev => 
        prev.map(f => 
          f.file === fileObj.file 
            ? { ...f, status: 'uploading' as const }
            : f
        )
      );
      
      try {
        console.log(`Creating time capsule ${i + 1}/${filesToUpload.length}: ${fileObj.file.name}`);
        
        // Create complete time capsule (Walrus + Encryption + NFT)
        const result = await createTimeCapsule(fileObj.file, 5);
        
        // Update with success
        setUploadedFiles(prev => 
          prev.map(f => 
            f.file === fileObj.file 
              ? { 
                  ...f, 
                  status: 'completed' as const,
                  blobId: result.blobId,
                  fileUrl: result.fileUrl,
                  encryptedBlobId: result.encryptedBlobId,
                  capsuleId: result.capsuleId,
                  nftTokenId: (result.nftResult as any).tokenId,
                  nftTxHash: (result.nftResult as any).txHash
                }
              : f
          )
        );
        
        console.log(`✅ Time capsule created: ${fileObj.file.name}`);
        console.log(`🎨 NFT Token ID: ${(result.nftResult as any).tokenId}`);
        console.log(`💎 Transaction: ${(result.nftResult as any).txHash}`);
        
      } catch (error) {
        console.error(`❌ Failed to create time capsule for ${fileObj.file.name}:`, error);
        
        // Update with error
        setUploadedFiles(prev => 
          prev.map(f => 
            f.file === fileObj.file 
              ? { 
                  ...f, 
                  status: 'error' as const,
                  error: error instanceof Error ? error.message : 'Time capsule creation failed'
                }
              : f
          )
        );
      }
    }
    
    setIsUploading(false);
  };

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
          className="flex items-center justify-center px-6 md:px-16 py-4 w-full h-full pt-20"
        >
          {/* Time Capsule Form */}
          <div className="w-full h-full flex gap-6">
            {/* Left Side - Form */}
            <div className="flex-1 bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10 overflow-y-auto max-h-[calc(100vh-120px)]">
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-white mb-2">
                  Create Time Capsule
                </h2>
                <p className="text-gray-400 text-sm mb-4">
                  Upload files to decentralized storage and mint as encrypted NFTs
                </p>
                
                {/* Requirements Notice */}
                {!isConnected && (
                  <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 mb-4 text-left">
                    <h3 className="text-blue-400 font-medium mb-2">📋 Requirements:</h3>
                    <ul className="text-gray-300 text-sm space-y-1">
                      <li>• MetaMask wallet installed</li>
                      <li>• Connected to Sepolia testnet</li>
                      <li>• Some Sepolia ETH for gas fees</li>
                    </ul>
                    <div className="mt-2 text-xs text-gray-400">
                      Get Sepolia ETH from: 
                      <a href="https://sepoliafaucet.com/" target="_blank" rel="noopener noreferrer" className="text-blue-400 ml-1 underline">
                        Sepolia Faucet
                      </a>
                    </div>
                  </div>
                )}
              </div>

              <div className="space-y-4">
                {/* Title */}
                <div>
                  <label className="block text-white text-sm font-medium mb-2">
                    Title
                  </label>
                  <input
                    type="text"
                    placeholder="Enter capsule title"
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none"
                  />
                </div>

                {/* Description */}
                <div>
                  <label className="block text-white text-sm font-medium mb-2">
                    Description
                  </label>
                  <input
                    type="text"
                    placeholder="Brief description"
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none"
                  />
                </div>

                {/* Time to Open & Created By - Same Line */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Time to Open
                    </label>
                    <input
                      type="datetime-local"
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white focus:border-white/40 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Created By
                    </label>
                    <input
                      type="text"
                      placeholder="Your name or identifier"
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Detailed Notes */}
                <div>
                  <label className="block text-white text-sm font-medium mb-2">
                    Detailed Notes
                  </label>
                  <textarea
                    rows={3}
                    placeholder="Write detailed notes for your future self..."
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none resize-none"
                  ></textarea>
                </div>

                {/* File Upload - More Space */}
                <div>
                  <label className="block text-white text-sm font-medium mb-2">
                    Upload Files
                  </label>
                  <div className="bg-white/5 border border-white/20 rounded-lg overflow-hidden min-h-[200px]">
                    <FileUpload onChange={handleFileUpload} />
                  </div>
                </div>

                {/* ETH Amount */}
                <div>
                  <label className="block text-white text-sm font-medium mb-2">
                    ETH Amount (optional)
                  </label>
                  <input
                    type="number"
                    step="0.001"
                    placeholder="0.0"
                    value={ethAmount}
                    onChange={(e) => setEthAmount(e.target.value)}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">Optional ETH to include with your capsule</p>
                </div>

                {/* Deploy Button */}
                <button className="w-full mt-4 px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/30 text-white font-medium rounded-lg transition-all">
                  Deploy Capsule
                </button>
              </div>
            </div>

            {/* Right Side - Logs & Assets */}
            <div className="w-72 bg-black/20 backdrop-blur-sm rounded-xl p-4 border border-white/10 flex flex-col max-h-[calc(100vh-120px)]">
              {/* System Logs - Compact */}
              <div className="mb-4">
                <div className="mb-2">
                  <h3 className="text-base font-medium text-white mb-1">
                    System Logs
                  </h3>
                  <p className="text-gray-500 text-xs">
                    Real-time status
                  </p>
                </div>

                {/* Log Container - More Compact */}
                <div className="h-24 bg-black/40 rounded-lg p-2 font-mono text-xs overflow-y-auto border border-white/10">
                  <div className="space-y-0.5">
                    <div className="text-green-400">[INFO] System ready</div>
                    <div className="text-gray-500">[SYSTEM] Waiting for input...</div>
                    <div className="text-blue-400">[NETWORK] Ethereum connected</div>
                    <div className="text-yellow-400">[STATUS] Ready to deploy</div>
                  </div>
                </div>
              </div>

              {/* Asset List - Takes Remaining Space */}
              <div className="flex-1 min-h-0">
                <div className="mb-2">
                  <h3 className="text-base font-medium text-white mb-1">
                    Assets
                  </h3>
                  <p className="text-gray-500 text-xs">
                    Files & ETH value
                  </p>
                </div>

                {/* Assets Container - Flexible Height */}
                <div className="h-full bg-black/40 rounded-lg p-3 overflow-y-auto">
                  {/* ETH Value */}
                  {ethAmount && (
                    <div className="mb-2 p-2 bg-yellow-500/10 border border-yellow-500/30 rounded text-xs">
                      <div className="flex justify-between items-center">
                        <span className="text-yellow-400 font-medium">ETH</span>
                        <span className="text-white">{ethAmount} ETH</span>
                      </div>
                    </div>
                  )}

                  {/* Uploaded Files */}
                  {uploadedFiles.length > 0 ? (
                    <div className="space-y-2">
                      {uploadedFiles.map((fileObj, index) => (
                        <div key={index} className="p-2 bg-blue-500/10 border border-blue-500/30 rounded text-xs">
                          <div className="flex items-center justify-between mb-1">
                            <div className="text-blue-400 font-medium truncate">
                              {fileObj.file.name}
                            </div>
                            <div className="flex items-center gap-1">
                              {fileObj.status === 'uploading' && (
                                <div className="w-3 h-3 border border-yellow-400 border-t-transparent rounded-full animate-spin"></div>
                              )}
                              {fileObj.status === 'minting' && (
                                <div className="w-3 h-3 border border-purple-400 border-t-transparent rounded-full animate-spin"></div>
                              )}
                              {fileObj.status === 'completed' && (
                                <div className="text-green-400">✨</div>
                              )}
                              {fileObj.status === 'error' && (
                                <div className="text-red-400">✗</div>
                              )}
                            </div>
                          </div>
                          <div className="flex justify-between text-gray-400 mb-1">
                            <span className="truncate">{fileObj.file.type || 'unknown'}</span>
                            <span className="ml-2 shrink-0">{(fileObj.file.size / 1024).toFixed(1)}KB</span>
                          </div>
                          {fileObj.status === 'completed' && (
                            <div className="text-green-400 text-xs space-y-1">
                              <div>🎯 Capsule ID: {fileObj.capsuleId}</div>
                              <div>🔗 Blob: {fileObj.blobId?.substring(0, 20)}...</div>
                              <div>🔐 Encrypted: {fileObj.encryptedBlobId?.substring(0, 20)}...</div>
                              <div>🎨 NFT Token: #{fileObj.nftTokenId} <span className="text-yellow-400">(DEMO)</span></div>
                              <div className="flex gap-2">
                                <a 
                                  href={fileObj.fileUrl} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="text-blue-400 hover:text-blue-300 underline"
                                >
                                  View File
                                </a>
                                <span className="text-gray-500 text-xs">
                                  NFT: Demo Mode
                                </span>
                              </div>
                            </div>
                          )}
                          {fileObj.status === 'error' && fileObj.error && (
                            <div className="text-red-400 text-xs">
                              Error: {fileObj.error}
                            </div>
                          )}
                        </div>
                      ))}
                      {isUploading && (
                        <div className="text-yellow-400 text-xs text-center py-2">
                          🚀 Creating time capsules (Walrus + NFT)...
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-gray-500 text-xs text-center py-6">
                      No files uploaded yet
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </Vortex>
      </div>
    </div>
  );
}
