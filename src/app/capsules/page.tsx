"use client";

import React, { useState, useEffect } from "react";
import { Vortex } from "@/components/ui/vortex";
import Navbar from "@/components/ui/navbar";
import { CanvasRevealEffect } from "@/components/ui/canvas-reveal-effect";
import { AnimatePresence, motion } from "motion/react";
import { DotsLoader } from "@/components/ui/loaders";


export default function CapsulesPage() {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <DotsLoader />;
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
                View and manage your stored memories
              </p>
            </div>

            {/* Capsules Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl w-full">
              
              {/* Capsule Card 1 */}
              <CapsuleCard
                title="My First Capsule"
                description="A collection of memories from 2025"
                status="Locked"
                openDate="Opens: Dec 25, 2026"
                fileCount="3 files"
                canvasEffect={
                  <CanvasRevealEffect
                    animationSpeed={0.3}
                    containerClassName="bg-emerald-900"
                    colors={[[59, 130, 246]]}
                    dotSize={2}
                  />
                }
              />

              {/* Capsule Card 2 */}
              <CapsuleCard
                title="Birthday Memories"
                description="Special moments from my birthday"
                status="Unlocked"
                openDate="Opened: Jan 15, 2025"
                fileCount="5 files"
                canvasEffect={
                  <>
                    <CanvasRevealEffect
                      animationSpeed={3}
                      containerClassName="bg-black"
                      colors={[
                        [34, 197, 94],
                        [22, 163, 74],
                      ]}
                      dotSize={2}
                    />
                    <div className="absolute inset-0 [mask-image:radial-gradient(400px_at_center,white,transparent)] bg-black/50" />
                  </>
                }
              />

              {/* Capsule Card 3 */}
              <CapsuleCard
                title="Travel Adventures"
                description="Photos and videos from Europe trip"
                status="Locked"
                openDate="Opens: Jun 10, 2026"
                fileCount="12 files"
                canvasEffect={
                  <CanvasRevealEffect
                    animationSpeed={3}
                    containerClassName="bg-purple-900"
                    colors={[[168, 85, 247]]}
                    dotSize={2.5}
                  />
                }
              />

              {/* Create New Capsule Card */}
              <CreateCapsuleCard />

            </div>
          </div>
        </Vortex>
      </div>
    </div>
  );
}

// Capsule Card Component
const CapsuleCard = ({
  title,
  description,
  status,
  openDate,
  fileCount,
  canvasEffect,
}: {
  title: string;
  description: string;
  status: string;
  openDate: string;
  fileCount: string;
  canvasEffect: React.ReactNode;
}) => {
  const [hovered, setHovered] = React.useState(false);
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
            {canvasEffect}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="relative z-20 w-full h-full flex flex-col justify-between">
        <div className="flex justify-between items-start group-hover/canvas-card:opacity-0 transition duration-200">
          <h3 className="text-white font-medium text-sm">{title}</h3>
          <span className={`text-xs px-2 py-1 rounded ${
            status === "Unlocked" 
              ? "text-green-400 bg-green-500/20" 
              : "text-yellow-400 bg-yellow-500/20"
          }`}>
            {status}
          </span>
        </div>
        
        <div className="group-hover/canvas-card:opacity-0 transition duration-200">
          <p className="text-gray-400 text-xs mb-3">{description}</p>
          <div className="flex justify-between text-xs text-gray-400">
            <span>{openDate}</span>
            <span>{fileCount}</span>
          </div>
        </div>

        {/* Hover content */}
        <div className="absolute inset-0 flex flex-col justify-center items-center opacity-0 group-hover/canvas-card:opacity-100 transition duration-200">
          <h2 className="text-white text-lg font-bold mb-2 text-center group-hover/canvas-card:-translate-y-2 transition duration-200">
            {title}
          </h2>
          <p className="text-gray-300 text-sm text-center">{description}</p>
        </div>
      </div>
    </div>
  );
};

// Create Capsule Card Component
const CreateCapsuleCard = () => {
  const [hovered, setHovered] = React.useState(false);
  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
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
