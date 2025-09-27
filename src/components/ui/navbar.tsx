     
"use client";

import React, { useState } from "react";

interface NavbarProps {
  isConnected: boolean;
  walletAddress: string;
  isConnecting: boolean;
  handleConnectWallet: () => void;
  formatAddress: (address: string) => string;
}

export default function Navbar({
  isConnected,
  walletAddress,
  isConnecting,
  handleConnectWallet,
  formatAddress,
}: NavbarProps) {
  return (
    <nav className="absolute top-0 left-0 right-0 z-20 flex items-center justify-between px-6 py-4 bg-transparent">
      {/* Brand Name */}
      <div className="text-white text-xl font-bold">
        <a href="/" >
        &lt;EmosiFloww&gt;
        </a>
      </div>
      
      {/* Right Side */}
      <div className="flex items-center gap-6">
        {/* Docs Link */}

        <a href="/deploy" className="text-white hover:text-gray-300 transition-colors">
          Deploy Capsules
        </a>
        <a href="/capsules" className="text-white hover:text-gray-300 transition-colors">
          Your Capsules
        </a>

        <a href="/docs" className="text-white hover:text-gray-300 transition-colors">
          Docs
        </a>
        
        {/* GitHub Icon with count */}
        <div className="flex items-center gap-2 text-white">
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          <span className="text-sm">2.1k</span>
        </div>

        {/* Wallet Connection */}
        {isConnected ? (
          <div className="flex items-center gap-2 text-white bg-green-600/20 px-3 py-1 rounded-lg border border-green-500/30">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span className="text-sm font-mono">{formatAddress(walletAddress)}</span>
          </div>
        ) : (
          <button
            onClick={handleConnectWallet}
            disabled={isConnecting}
            className="text-white bg-blue-600/20 hover:bg-blue-600/30 px-3 py-1 rounded-lg border border-blue-500/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isConnecting ? "Connecting..." : "Connect Wallet"}
          </button>
        )}
        
      </div>
    </nav>
  );
}
