'use client'

import { useState } from 'react'
import { decodeNFTData, decryptBlobId } from '@/lib/nft-decoder'

export default function NFTDecoder() {
  const [tokenId, setTokenId] = useState('1')
  const [nftData, setNftData] = useState<any>(null)
  const [decryptedData, setDecryptedData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleDecode = async () => {
    setLoading(true)
    try {
      // Decode NFT data
      const data = await decodeNFTData(parseInt(tokenId))
      setNftData(data)
      
      // If we got encrypted blob ID, decrypt it
      if (data.encryptedBlobId) {
        const decrypted = await decryptBlobId(data.encryptedBlobId)
        setDecryptedData(decrypted)
      }
      
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">🔍 NFT Data Decoder</h1>
          <p className="text-xl text-gray-300">Decode your Time Capsule NFT metadata and encrypted content</p>
        </div>

        <div className="bg-black/20 backdrop-blur-lg rounded-2xl border border-white/10 p-8 mb-8">
          <div className="flex gap-4 mb-6">
            <div className="flex-1">
              <label className="block text-sm font-medium mb-2">Token ID</label>
              <input
                type="number"
                value={tokenId}
                onChange={(e) => setTokenId(e.target.value)}
                className="w-full px-4 py-2 bg-black/30 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-400"
                placeholder="Enter NFT Token ID"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={handleDecode}
                disabled={loading}
                className="px-6 py-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 transition-all"
              >
                {loading ? '🔍 Decoding...' : '🔍 Decode NFT'}
              </button>
            </div>
          </div>
        </div>

        {nftData && (
          <div className="space-y-6">
            {/* Basic NFT Info */}
            <div className="bg-black/20 backdrop-blur-lg rounded-2xl border border-white/10 p-6">
              <h2 className="text-2xl font-bold mb-4 text-purple-300">📋 NFT Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-300">Token ID</p>
                  <p className="font-mono text-green-300">{nftData.tokenId}</p>
                </div>
                <div>
                  <p className="text-gray-300">Owner</p>
                  <p className="font-mono text-green-300 break-all">{nftData.owner}</p>
                </div>
                <div>
                  <p className="text-gray-300">Creator</p>
                  <p className="font-mono text-green-300 break-all">{nftData.creator}</p>
                </div>
                <div>
                  <p className="text-gray-300">Contract</p>
                  <p className="font-mono text-green-300 break-all">0xfb42a2c4b5eb535cfe704ef64da416f1cf69bde3</p>
                </div>
              </div>
            </div>

            {/* Encrypted Data */}
            <div className="bg-black/20 backdrop-blur-lg rounded-2xl border border-white/10 p-6">
              <h2 className="text-2xl font-bold mb-4 text-red-300">🔐 Encrypted Content</h2>
              <div>
                <p className="text-gray-300 mb-2">Encrypted Blob ID (stored on blockchain)</p>
                <p className="font-mono text-red-300 break-all bg-black/30 p-3 rounded">{nftData.encryptedBlobId}</p>
              </div>
            </div>

            {/* Decrypted Data */}
            {decryptedData && !decryptedData.error && (
              <div className="bg-black/20 backdrop-blur-lg rounded-2xl border border-white/10 p-6">
                <h2 className="text-2xl font-bold mb-4 text-green-300">🔓 Decrypted Content</h2>
                <div className="space-y-4">
                  <div>https://aggregator.walrus-testnet.walrus.space/v1/TojzKFUlRp1Dklp2KBIiCQBSSYlricxrkzo0EvwIY9Y
                    <p className="text-gray-300 mb-2">Original Walrus Blob ID</p>
                    <p className="font-mono text-green-300 break-all bg-black/30 p-3 rounded">{decryptedData.originalBlobId}</p>
                  </div>
                  <div>
                    <p className="text-gray-300 mb-2">Walrus Download URL</p>
                    <a 
                      href={decryptedData.walrusUrl} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="font-mono text-blue-300 hover:text-blue-200 break-all bg-black/30 p-3 rounded block transition-colors"
                    >
                      {decryptedData.walrusUrl}
                    </a>
                  </div>
                </div>
              </div>
            )}

            {/* Metadata */}
            {nftData.metadata && (
              <div className="bg-black/20 backdrop-blur-lg rounded-2xl border border-white/10 p-6">
                <h2 className="text-2xl font-bold mb-4 text-purple-300">📋 Metadata</h2>
                <div className="space-y-3">
                  <div>
                    <p className="text-gray-300">Name</p>
                    <p className="text-white">{nftData.metadata.name}</p>
                  </div>
                  <div>
                    <p className="text-gray-300">Description</p>
                    <p className="text-white">{nftData.metadata.description}</p>
                  </div>
                  <div>
                    <p className="text-gray-300">Capsule ID</p>
                    <p className="font-mono text-yellow-300">{nftData.metadata.capsuleId}</p>
                  </div>
                  {nftData.metadata.attributes && (
                    <div>
                      <p className="text-gray-300 mb-2">Attributes</p>
                      <div className="space-y-2">
                        {nftData.metadata.attributes.map((attr: any, i: number) => (
                          <div key={i} className="bg-black/30 p-2 rounded">
                            <span className="text-gray-400">{attr.trait_type}:</span>{' '}
                            <span className="text-white">{attr.value}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="text-center mt-12 text-gray-400">
          <p>🔍 Use this tool to decode any Time Capsule NFT and access encrypted content</p>
        </div>
      </div>
    </div>
  )
}