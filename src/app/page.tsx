'use client';
import { useState } from "react";

export default function Home() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    openDate: '',
    openTime: '',
    detailNote: '',
    mediaFiles: [] as File[],
  });
  
  const [logs, setLogs] = useState<string[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleInputChange = (field: string, value: string | File[]) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()} - ${message}`]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    setLogs([]);
    
    addLog('Initializing time capsule creation...');
    
    // Simulate the 6-step process
    setTimeout(() => addLog('Step 1: Uploading to Walrus...'), 500);
    setTimeout(() => addLog('Step 2: Creating JSON metadata...'), 1500);
    setTimeout(() => addLog('Step 3: Storing on Filecoin...'), 2500);
    setTimeout(() => addLog('Step 4: Minting NFT...'), 3500);
    setTimeout(() => addLog('Step 5: Encrypting with Hedera...'), 4500);
    setTimeout(() => {
      addLog('Step 6: Setting up scheduled decryption...');
      addLog('Time capsule created successfully!');
      setIsProcessing(false);
    }, 5500);
  };

  return (
    <div className="min-h-screen bg-black text-white font-quantico">
      {/* Logo */}
      <div className="text-center py-8 border-b border-white">
        <h1 className="text-4xl font-bold tracking-wider">&lt; Tempris &gt;</h1>
        <p className="text-sm mt-2 tracking-wide">DECENTRALIZED TIME-CAPSULE PLATFORM</p>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="space-y-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Title */}
              <div>
                <label className="block text-white mb-2 font-bold tracking-wide">TITLE</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  className="w-full p-3 bg-black border border-white text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                  placeholder="Enter capsule title..."
                  required
                />
              </div>

              {/* Description */}
              <div>
                <label className="block text-white mb-2 font-bold tracking-wide">DESCRIPTION</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  className="w-full p-3 bg-black border border-white text-white focus:outline-none focus:ring-2 focus:ring-white/50 h-24 resize-none"
                  placeholder="Brief description of your time capsule..."
                  required
                />
              </div>

              {/* Time to Open */}
              <div>
                <label className="block text-white mb-2 font-bold tracking-wide">TIME TO OPEN</label>
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="date"
                    value={formData.openDate}
                    onChange={(e) => handleInputChange('openDate', e.target.value)}
                    className="p-3 bg-black border border-white text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                    required
                  />
                  <input
                    type="time"
                    step="1"
                    value={formData.openTime}
                    onChange={(e) => handleInputChange('openTime', e.target.value)}
                    className="p-3 bg-black border border-white text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                    required
                  />
                </div>
              </div>

              {/* Detail Note */}
              <div>
                <label className="block text-white mb-2 font-bold tracking-wide">
                  DETAIL NOTE FOR FUTURE ({formData.detailNote.length}/20000)
                </label>
                <textarea
                  value={formData.detailNote}
                  onChange={(e) => handleInputChange('detailNote', e.target.value)}
                  className="w-full p-3 bg-black border border-white text-white focus:outline-none focus:ring-2 focus:ring-white/50 h-32 resize-none"
                  placeholder="Write your message to the future..."
                  maxLength={20000}
                  required
                />
              </div>

              {/* Upload Box */}
              <div>
                <label className="block text-white mb-2 font-bold tracking-wide">MULTIMEDIA FILES</label>
                <div className="border-2 border-dashed border-white p-8 text-center hover:border-white/70 transition-colors">
                  <input
                    type="file"
                    multiple
                    accept="image/*,video/*,audio/*,.pdf,.doc,.docx"
                    onChange={(e) => handleInputChange('mediaFiles', Array.from(e.target.files || []))}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <div className="text-white/70 mb-2">
                      {formData.mediaFiles.length > 0 
                        ? `${formData.mediaFiles.length} file(s) selected`
                        : 'DRAG & DROP OR CLICK TO UPLOAD'
                      }
                    </div>
                    <div className="text-sm text-white/50">
                      IMAGES • VIDEOS • AUDIO • DOCUMENTS
                    </div>
                  </label>
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isProcessing}
                className={`w-full py-4 font-bold text-xl tracking-wider transition-colors border-2 ${
                  isProcessing 
                    ? 'bg-black text-white/50 border-white/50 cursor-not-allowed'
                    : 'bg-white text-black border-white hover:bg-black hover:text-white'
                }`}
              >
                {isProcessing ? 'PROCESSING...' : 'CAPSULE IT'}
              </button>
            </form>
          </div>

          {/* Log Box Section */}
          <div className="space-y-6">
            <div>
              <h2 className="text-white mb-4 font-bold tracking-wide">CAPSULE CREATION LOG</h2>
              <div className="bg-black border border-white h-96 overflow-y-auto p-4">
                {logs.length === 0 ? (
                  <div className="text-white/50 text-center py-8">
                    Logs will appear here during capsule creation...
                  </div>
                ) : (
                  <div className="space-y-2">
                    {logs.map((log, index) => (
                      <div key={index} className="text-white/80 text-sm font-mono">
                        {log}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Process Indicator */}
            {isProcessing && (
              <div className="border border-white p-4">
                <h3 className="text-white mb-3 font-bold">MULTI-CHAIN WORKFLOW</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>WALRUS UPLOAD</span>
                    <span className="text-white/50">●●●</span>
                  </div>
                  <div className="flex justify-between">
                    <span>JSON METADATA</span>
                    <span className="text-white/50">●●●</span>
                  </div>
                  <div className="flex justify-between">
                    <span>FILECOIN STORAGE</span>
                    <span className="text-white/50">●●●</span>
                  </div>
                  <div className="flex justify-between">
                    <span>NFT MINTING</span>
                    <span className="text-white/50">●●●</span>
                  </div>
                  <div className="flex justify-between">
                    <span>HEDERA ENCRYPTION</span>
                    <span className="text-white/50">●●●</span>
                  </div>
                  <div className="flex justify-between">
                    <span>SCHEDULED DECRYPTION</span>
                    <span className="text-white/50">●●●</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
