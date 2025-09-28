"use client";

import React, { useState, useEffect } from "react";
import { Vortex } from "@/components/ui/vortex";
import Navbar from "@/components/ui/navbar";
import { FileUpload } from "@/components/ui/file-upload";
import { LoaderFive } from "@/components/ui/loader";
import { walrus, createTimeCapsule, createScheduledTimeCapsule } from "@/store/functions";

interface UploadedFile {
  file: File;
  blobId?: string;
  fileUrl?: string;
  encryptedBlobId?: string;
  capsuleId?: string;
  nftTokenId?: number;
  nftTxHash?: string;
  status: 'pending' | 'uploading' | 'uploaded' | 'minting' | 'scheduling' | 'completed' | 'error';
  error?: string;
  // Hedera scheduled fields
  hederaCapsuleId?: number;
  scheduleId?: string;
  unlockTime?: number;
  isScheduled?: boolean;
}

export default function VortexDemoSecond() {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [ethAmount, setEthAmount] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  
  // New state for Hedera time-locking
  const [capsuleType, setCapsuleType] = useState<'immediate' | 'scheduled'>('immediate');
  const [unlockDateTime, setUnlockDateTime] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [createdBy, setCreatedBy] = useState('');
  const [detailedNotes, setDetailedNotes] = useState('');

  // ETH Price state
  const [ethPriceUSD, setEthPriceUSD] = useState<number | null>(null);
  const [isPriceLoading, setIsPriceLoading] = useState(true);
  const [priceError, setPriceError] = useState<string | null>(null);

  useEffect(() => {
    // Simulate loading time and fetch ETH price
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1800);

    // Fetch ETH price from CoinGecko
    fetchEthPrice();

    // Set up interval to refresh price every 60 seconds
    const priceInterval = setInterval(fetchEthPrice, 60000);

    return () => {
      clearTimeout(timer);
      clearInterval(priceInterval);
    };
  }, []);

  const fetchEthPrice = async () => {
    try {
      setIsPriceLoading(true);
      setPriceError(null);
      
      const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd');
      
      if (!response.ok) {
        throw new Error('Failed to fetch ETH price');
      }
      
      const data = await response.json();
      setEthPriceUSD(data.ethereum.usd);
    } catch (error) {
      console.error('Error fetching ETH price:', error);
      setPriceError('Failed to fetch price');
    } finally {
      setIsPriceLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center w-full h-screen">
        <LoaderFive text="Loading Deployment Environment..." />
      </div>
    );
  }

  const handleFileUpload = async (files: File[]) => {
    const newFiles: UploadedFile[] = files.map(file => ({
      file,
      status: 'pending' as const
    }));
    
    setUploadedFiles(prev => [...prev, ...newFiles]);
    
    // Don't upload files to Walrus immediately - wait for user to click Deploy
    // await uploadFilesToWalrus(newFiles);
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
        
        const metadata = {
          title: title || fileObj.file.name,
          description: description || 'Time capsule created with Tempris',
          createdBy: createdBy || 'Anonymous',
          detailedNotes: detailedNotes || '',
          ethAmount: ethAmount || '0'
        };

        if (capsuleType === 'scheduled' && unlockDateTime) {
          // Update status to scheduling
          setUploadedFiles(prev => 
            prev.map(f => 
              f.file === fileObj.file 
                ? { ...f, status: 'scheduling' as const }
                : f
            )
          );

          // Convert datetime-local to Unix timestamp
          const unlockTime = Math.floor(new Date(unlockDateTime).getTime() / 1000);
          
          // Create scheduled time capsule with Hedera
          const result = await createScheduledTimeCapsule(
            fileObj.file, 
            unlockTime, 
            walletAddress, 
            10, // 10 epochs for long-term storage
            metadata
          ) as any;
          
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
                    nftTxHash: (result.nftResult as any).txHash,
                    hederaCapsuleId: result.hederaCapsuleId,
                    scheduleId: result.scheduleId,
                    unlockTime: unlockTime,
                    isScheduled: true
                  }
                : f
            )
          );
          
          console.log(`✅ Scheduled time capsule created: ${fileObj.file.name}`);
          console.log(`⏰ Hedera Capsule ID: ${result.hederaCapsuleId}`);
          console.log(`📅 Schedule ID: ${result.scheduleId}`);
          console.log(`🔓 Unlocks at: ${new Date(unlockTime * 1000).toLocaleString()}`);
          
        } else {
          // Create immediate time capsule (original functionality)
          const result = await createTimeCapsule(fileObj.file, 5, metadata) as any;
          
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
                    nftTxHash: (result.nftResult as any).txHash,
                    isScheduled: false
                  }
                : f
            )
          );
          
          console.log(`✅ Time capsule created: ${fileObj.file.name}`);
          console.log(`🎨 NFT Token ID: ${(result.nftResult as any).tokenId}`);
          console.log(`💎 Transaction: ${(result.nftResult as any).txHash}`);
        }
        
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
                {/* Capsule Type Selection */}
                <div>
                  <label className="block text-white text-sm font-medium mb-2">
                    Capsule Type
                  </label>
                  <div className="flex gap-3">
                    <button
                      type="button"
                      onClick={() => setCapsuleType('immediate')}
                      className={`flex-1 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                        capsuleType === 'immediate'
                          ? 'bg-blue-500/20 border border-blue-500/50 text-blue-300'
                          : 'bg-white/5 border border-white/20 text-gray-400 hover:bg-white/10'
                      }`}
                    >
                      Immediate Access
                    </button>
                    <button
                      type="button"
                      onClick={() => setCapsuleType('scheduled')}
                      className={`flex-1 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                        capsuleType === 'scheduled'
                          ? 'bg-purple-500/20 border border-purple-500/50 text-purple-300'
                          : 'bg-white/5 border border-white/20 text-gray-400 hover:bg-white/10'
                      }`}
                    >
                      Time-Locked
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {capsuleType === 'immediate' 
                      ? 'Content is immediately accessible after creation'
                      : 'Content is locked until specified unlock time using Hedera scheduling'
                    }
                  </p>
                </div>

                {/* Title */}
                <div>
                  <label className="block text-white text-sm font-medium mb-2">
                    Title
                  </label>
                  <input
                    type="text"
                    placeholder="Enter capsule title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
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
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none"
                  />
                </div>

                {/* Time to Open & Created By - Same Line */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      {capsuleType === 'scheduled' ? 'Unlock Time' : 'Time to Open'}
                    </label>
                    <input
                      type="datetime-local"
                      value={unlockDateTime}
                      onChange={(e) => setUnlockDateTime(e.target.value)}
                      min={new Date().toISOString().slice(0, 16)} // Prevent past dates
                      className={`w-full px-4 py-2.5 border rounded-lg text-white focus:outline-none ${
                        capsuleType === 'scheduled'
                          ? 'bg-purple-500/10 border-purple-500/30 focus:border-purple-400'
                          : 'bg-white/5 border-white/20 focus:border-white/40'
                      }`}
                    />
                    {capsuleType === 'scheduled' && (
                      <p className="text-xs text-purple-400 mt-1">
                        ⚠️ Cannot be changed once created
                      </p>
                    )}
                  </div>
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Created By
                    </label>
                    <input
                      type="text"
                      placeholder="Your name or identifier"
                      value={createdBy}
                      onChange={(e) => setCreatedBy(e.target.value)}
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
                    value={detailedNotes}
                    onChange={(e) => setDetailedNotes(e.target.value)}
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
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-white text-sm font-medium">
                      ETH Amount (optional)
                    </label>
                    {/* Live ETH Price Display */}
                    <div className="flex items-center gap-2 text-xs">
                      {isPriceLoading ? (
                        <div className="flex items-center gap-1 text-gray-400">
                          <div className="w-3 h-3">
                            <LoaderFive text="..." />
                          </div>
                          <span>Loading price...</span>
                        </div>
                      ) : priceError ? (
                        <span className="text-red-400">Price unavailable</span>
                      ) : (
                        <div className="flex items-center gap-1 text-green-400">
                          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                          <span className="font-mono">${ethPriceUSD?.toLocaleString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="relative">
                    <input
                      type="number"
                      step="0.001"
                      placeholder="0.0"
                      value={ethAmount}
                      onChange={(e) => setEthAmount(e.target.value)}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:border-white/40 focus:outline-none pr-24"
                    />
                    <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm">
                      ETH
                    </div>
                  </div>
                  
                  {/* USD Equivalent */}
                  {ethAmount && ethPriceUSD && !isNaN(parseFloat(ethAmount)) && (
                    <div className="mt-2 p-2 bg-green-500/10 border border-green-500/30 rounded-lg">
                      <div className="flex justify-between items-center text-xs">
                        <span className="text-green-400">USD Equivalent:</span>
                        <span className="text-white font-mono">
                          ${(parseFloat(ethAmount) * ethPriceUSD).toLocaleString(undefined, {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                          })}
                        </span>
                      </div>
                    </div>
                  )}
                  
                  <p className="text-xs text-gray-500 mt-1">
                    Optional ETH to include with your capsule
                    {ethPriceUSD && (
                      <span className="ml-1 text-green-400">
                        • Live price from CoinGecko
                      </span>
                    )}
                  </p>
                </div>

                {/* Deploy Button */}
                <button 
                  onClick={() => {
                    if (uploadedFiles.length === 0) {
                      alert('Please upload at least one file');
                      return;
                    }
                    if (capsuleType === 'scheduled' && !unlockDateTime) {
                      alert('Please set an unlock time for scheduled time capsules');
                      return;
                    }
                    if (capsuleType === 'scheduled' && new Date(unlockDateTime).getTime() <= Date.now()) {
                      alert('Unlock time must be in the future');
                      return;
                    }
                    if (!isConnected) {
                      alert('Please connect your wallet first');
                      return;
                    }
                    
                    // Start upload process for all pending files
                    const pendingFiles = uploadedFiles.filter(f => f.status === 'pending');
                    if (pendingFiles.length > 0) {
                      uploadFilesToWalrus(pendingFiles);
                    } else {
                      alert('All files have already been processed');
                    }
                  }}
                  disabled={isUploading || uploadedFiles.length === 0 || !isConnected || uploadedFiles.filter(f => f.status === 'pending').length === 0}
                  className={`w-full mt-4 px-6 py-3 font-medium rounded-lg transition-all ${
                    isUploading || uploadedFiles.length === 0 || !isConnected || uploadedFiles.filter(f => f.status === 'pending').length === 0
                      ? 'bg-gray-600/20 border border-gray-600/30 text-gray-500 cursor-not-allowed'
                      : capsuleType === 'scheduled'
                      ? 'bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-purple-300'
                      : 'bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 text-blue-300'
                  }`}
                >
                  {isUploading ? (
                    <span className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border border-current border-t-transparent rounded-full animate-spin"></div>
                      Creating {capsuleType === 'scheduled' ? 'Scheduled' : 'Immediate'} Capsules...
                    </span>
                  ) : (
                    `Deploy ${capsuleType === 'scheduled' ? 'Time-Locked' : 'Immediate'} Capsule${uploadedFiles.filter(f => f.status === 'pending').length > 1 ? 's' : ''} (${uploadedFiles.filter(f => f.status === 'pending').length})`
                  )}
                </button>
                
                {/* Validation Messages */}
                {capsuleType === 'scheduled' && (
                  <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-3 mt-2 text-left">
                    <h3 className="text-purple-400 font-medium mb-1">⏰ Scheduled Time Capsule:</h3>
                    <ul className="text-gray-300 text-xs space-y-1">
                      <li>• Uses Hedera network for true time-locking</li>
                      <li>• Content cannot be accessed before unlock time</li>
                      <li>• Requires additional Hedera transaction fees</li>
                      <li>• Once created, unlock time cannot be changed</li>
                    </ul>
                  </div>
                )}
              </div>
            </div>

            {/* Right Side - Logs & Assets */}
            <div className="w-72 bg-black/20 backdrop-blur-sm rounded-xl p-4 border border-white/10 flex flex-col max-h-[calc(100vh-120px)]">
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
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-yellow-400 font-medium">ETH</span>
                        <span className="text-white font-mono">{ethAmount} ETH</span>
                      </div>
                      {ethPriceUSD && !isNaN(parseFloat(ethAmount)) && (
                        <div className="flex justify-between items-center text-gray-400">
                          <span>USD Value:</span>
                          <span className="font-mono">
                            ${(parseFloat(ethAmount) * ethPriceUSD).toLocaleString(undefined, {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 2
                            })}
                          </span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Uploaded Files */}
                  {uploadedFiles.length > 0 ? (
                    <div className="space-y-2">
                      {uploadedFiles.map((fileObj, index) => (
                        <div key={index} className="p-2 bg-blue-500/10 border border-blue-500/30 rounded text-xs">
                          <div className="flex items-center justify-between mb-1">
                            <div className="text-blue-400 font-medium truncate flex items-center gap-1">
                              {fileObj.isScheduled && <span>⏰</span>}
                              {fileObj.file.name}
                            </div>
                            <div className="flex items-center gap-1">
                              {fileObj.status === 'uploading' && (
                                <div className="w-3 h-3 border border-yellow-400 border-t-transparent rounded-full animate-spin"></div>
                              )}
                              {fileObj.status === 'scheduling' && (
                                <div className="w-3 h-3 border border-purple-400 border-t-transparent rounded-full animate-spin"></div>
                              )}
                              {fileObj.status === 'minting' && (
                                <div className="w-3 h-3 border border-purple-400 border-t-transparent rounded-full animate-spin"></div>
                              )}
                              {fileObj.status === 'completed' && (
                                <div className={fileObj.isScheduled ? "text-purple-400" : "text-green-400"}> </div>
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
                            <div className={`text-xs ${fileObj.isScheduled ? 'text-purple-400' : 'text-green-400'}`}>
                              <div className="flex items-center justify-center gap-2 py-1">
                                <span className="font-medium">NFT Minted</span>
                                {fileObj.isScheduled ? 
                                  <span className="text-purple-300 text-xs">(SCHEDULED)</span> : 
                                  <span className="text-yellow-400 text-xs">(IMMEDIATE)</span>
                                }
                              </div>
                              {fileObj.isScheduled && (
                                <div className="flex justify-center mt-1">
                                  <span className="text-purple-400 text-xs">
                                    Locked until unlock
                                  </span>
                                </div>
                              )}
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
                          Creating time capsules...
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
