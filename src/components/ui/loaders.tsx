"use client";

import React from "react";

// Dots Loader for Capsules page
export const DotsLoader = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-black">
      <div className="flex space-x-2">
        <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        <div className="w-3 h-3 bg-green-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce"></div>
      </div>
    </div>
  );
};

// Spinner Loader for Future page
export const SpinnerLoader = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-black">
      <div className="relative">
        <div className="w-12 h-12 border-4 border-gray-700 border-t-blue-500 rounded-full animate-spin"></div>
        <div className="absolute inset-0 w-12 h-12 border-4 border-transparent border-r-green-500 rounded-full animate-spin [animation-direction:reverse] [animation-duration:1.5s]"></div>
      </div>
    </div>
  );
};

// Pulse Loader for Docs page
export const PulseLoader = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-black">
      <div className="flex flex-col items-center space-y-4">
        <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg animate-pulse"></div>
        <div className="text-white text-sm animate-pulse">Loading Documentation...</div>
      </div>
    </div>
  );
};

// Wave Loader for any other pages
export const WaveLoader = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-black">
      <div className="flex space-x-1">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="w-2 h-8 bg-gradient-to-t from-blue-500 to-cyan-400 animate-pulse"
            style={{
              animationDelay: `${i * 0.1}s`,
              animationDuration: '1s',
            }}
          ></div>
        ))}
      </div>
    </div>
  );
};