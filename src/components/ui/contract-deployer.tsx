"use client";

import React, { useState, useEffect } from "react";
import { deployTimeCapsuleContract, getDeploymentCost } from "@/lib/deploy-contract";
import { switchToSepolia } from "@/lib/nft";

export default function ContractDeployer({ onContractDeployed }: { onContractDeployed?: (address: string) => void }) {
  const [isDeploying, setIsDeploying] = useState(false);
  const [deployedContract, setDeployedContract] = useState<string | null>(null);
  const [deploymentTx, setDeploymentTx] = useState<string | null>(null);
  const [estimatedCost, setEstimatedCost] = useState<string>("Calculating...");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Get estimated deployment cost
    getDeploymentCost().then(cost => {
      setEstimatedCost(cost);
    });
  }, []);

  const handleDeploy = async () => {
    setIsDeploying(true);
    setError(null);
    
    try {
      // First ensure we're on Sepolia
      const switched = await switchToSepolia();
      if (!switched) {
        throw new Error("Please switch to Sepolia testnet manually");
      }

      const result = await deployTimeCapsuleContract("EmosiFloww Time Capsules", "EFLOW");
      
      if (result.success && result.contractAddress) {
        setDeployedContract(result.contractAddress);
        setDeploymentTx(result.txHash || null);
        
        // Notify parent component
        if (onContractDeployed) {
          onContractDeployed(result.contractAddress);
        }
        
        // Store in localStorage for future use
        localStorage.setItem('deployed-contract-address', result.contractAddress);
        
      } else {
        setError(result.error || "Deployment failed");
      }
      
    } catch (err: any) {
      setError(err.message || "Deployment failed");
    } finally {
      setIsDeploying(false);
    }
  };

  // Check if contract was previously deployed
  useEffect(() => {
    const storedAddress = localStorage.getItem('deployed-contract-address');
    if (storedAddress) {
      setDeployedContract(storedAddress);
    }
  }, []);

  return (
    <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-6 mb-6">
      <h3 className="text-purple-400 font-bold text-lg mb-4">🚀 Deploy Your NFT Contract</h3>
      
      {!deployedContract ? (
        <div className="space-y-4">
          <p className="text-gray-300 text-sm">
            Deploy your own ERC721 contract on Sepolia testnet to mint real NFTs for your time capsules.
          </p>
          
          <div className="bg-black/20 rounded-lg p-4 text-sm">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-gray-400">Contract Name:</span>
                <span className="text-white ml-2">EmosiFloww Time Capsules</span>
              </div>
              <div>
                <span className="text-gray-400">Symbol:</span>
                <span className="text-white ml-2">EFLOW</span>
              </div>
              <div>
                <span className="text-gray-400">Network:</span>
                <span className="text-blue-400 ml-2">Sepolia Testnet</span>
              </div>
              <div>
                <span className="text-gray-400">Est. Cost:</span>
                <span className="text-yellow-400 ml-2">~{estimatedCost} ETH</span>
              </div>
            </div>
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 text-red-400 text-sm">
              ❌ {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={handleDeploy}
              disabled={isDeploying}
              className="flex-1 bg-purple-600/20 hover:bg-purple-600/30 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-3 rounded-lg border border-purple-500/30 transition-all font-medium"
            >
              {isDeploying ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin"></div>
                  Deploying Contract...
                </div>
              ) : (
                "Deploy Contract"
              )}
            </button>
            
            <a
              href="https://sepoliafaucet.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 px-4 py-3 rounded-lg border border-blue-500/30 transition-all text-sm"
            >
              Get Sepolia ETH
            </a>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="text-center">
            <div className="text-green-400 text-2xl mb-2">✅</div>
            <h4 className="text-green-400 font-medium text-lg">Contract Deployed Successfully!</h4>
            <p className="text-gray-300 text-sm mt-1">Your time capsules will now mint real NFTs</p>
          </div>
          
          <div className="bg-black/20 rounded-lg p-4 text-sm space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Contract Address:</span>
              <span className="text-green-400 font-mono text-xs">{deployedContract}</span>
            </div>
            {deploymentTx && (
              <div className="flex justify-between">
                <span className="text-gray-400">Deploy Transaction:</span>
                <a 
                  href={`https://sepolia.etherscan.io/tx/${deploymentTx}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 underline font-mono text-xs"
                >
                  {deploymentTx.substring(0, 10)}...
                </a>
              </div>
            )}
          </div>

          <div className="flex gap-2 text-sm">
            <a
              href={`https://sepolia.etherscan.io/address/${deployedContract}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 px-3 py-2 rounded-lg border border-blue-500/30 transition-all text-center"
            >
              View on Etherscan
            </a>
            <button
              onClick={() => {
                localStorage.removeItem('deployed-contract-address');
                setDeployedContract(null);
                setDeploymentTx(null);
                setError(null);
              }}
              className="bg-gray-600/20 hover:bg-gray-600/30 text-gray-400 px-3 py-2 rounded-lg border border-gray-500/30 transition-all"
            >
              Deploy New
            </button>
          </div>
        </div>
      )}
    </div>
  );
}