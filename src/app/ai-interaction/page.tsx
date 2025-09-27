'use client';

import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";

interface Agent {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'busy';
  specialization: string;
  lastResponse: string;
  confidence: number;
  address: string;
}

interface ChatMessage {
  id: string;
  sender: 'user' | string; // string for agent names
  message: string;
  timestamp: Date;
  agentResponse?: {
    confidence: number;
    analysis: string;
    recommendation?: string;
  };
}

interface CapsuleAnalysis {
  capsuleId: string;
  title: string;
  marketValue: string;
  sentiment: string;
  rarity: number;
  tradingRecommendation: 'buy' | 'hold' | 'sell';
  reasonsAnalysis: string[];
}

export default function AIInteractionPage() {
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: 'marketplace_coordinator',
      name: 'Marketplace Coordinator',
      status: 'online',
      specialization: 'Trading Strategy & Market Analysis',
      lastResponse: 'Analyzing market conditions...',
      confidence: 0.92,
      address: 'agent1qs2q6hqrvwlzh5lvkl29qvfh5cj3jjg3f5d4qnqrb8j5qe4'
    },
    {
      id: 'memory_appraiser',
      name: 'Memory Appraiser',
      status: 'online',
      specialization: 'Emotional Value & Authenticity Assessment',
      lastResponse: 'Evaluating memory significance...',
      confidence: 0.88,
      address: 'agent1qg8k6hqrvwlzh5lvkl29qvfh5cj3jjg3f5d4qnqrb8j5qe4'
    },
    {
      id: 'authenticity_validator',
      name: 'Authenticity Validator',
      status: 'busy',
      specialization: 'Fraud Detection & Verification',
      lastResponse: 'Running authenticity checks...',
      confidence: 0.95,
      address: 'agent1qh7k6hqrvwlzh5lvkl29qvfh5cj3jjg3f5d4qnqrb8j5qe4'
    },
    {
      id: 'trading_legacy',
      name: 'Trading Legacy Agent',
      status: 'online',
      specialization: 'Legacy Value & Historical Context',
      lastResponse: 'Assessing historical significance...',
      confidence: 0.84,
      address: 'agent1qi8k6hqrvwlzh5lvkl29qvfh5cj3jjg3f5d4qnqrb8j5qe4'
    }
  ]);

  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'user',
      message: 'Hello AI agents! Can you analyze my time capsule portfolio?',
      timestamp: new Date()
    },
    {
      id: '2',
      sender: 'Marketplace Coordinator',
      message: 'Hello! I\'m analyzing your portfolio. I see 4 capsules with strong market potential. The "Travel Adventures" capsule shows exceptional trading potential.',
      timestamp: new Date(),
      agentResponse: {
        confidence: 0.92,
        analysis: 'Strong bullish indicators in travel memory segment',
        recommendation: 'Consider early unlock premium for optimal trading window'
      }
    }
  ]);

  const [currentMessage, setCurrentMessage] = useState('');
  const [selectedCapsule, setSelectedCapsule] = useState<string>('');
  const [analysisResults, setAnalysisResults] = useState<CapsuleAnalysis[]>([
    {
      capsuleId: 'capsule_003',
      title: 'Travel Adventures',
      marketValue: '$4,200',
      sentiment: 'Very Bullish',
      rarity: 0.87,
      tradingRecommendation: 'buy',
      reasonsAnalysis: [
        'Travel memories show 22% price increase in last 30 days',
        'High emotional engagement scores from similar capsules',
        'Rare content combination (12 files, mixed media)',
        'Optimal unlock timing approaching peak travel season'
      ]
    },
    {
      capsuleId: 'capsule_001',
      title: 'My First Capsule',
      marketValue: '$2,500',
      sentiment: 'Bullish',
      rarity: 0.73,
      tradingRecommendation: 'hold',
      reasonsAnalysis: [
        'Strong nostalgic value premium detected',
        'Family-themed capsules trending upward',
        'Long unlock period creates scarcity value',
        'Sentiment analysis shows high emotional attachment'
      ]
    }
  ]);

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const sendMessage = () => {
    if (!currentMessage.trim()) return;

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      message: currentMessage,
      timestamp: new Date()
    };

    setChatMessages(prev => [...prev, newMessage]);
    setCurrentMessage('');

    // Simulate agent responses
    setTimeout(() => {
      const randomAgent = agents[Math.floor(Math.random() * agents.length)];
      const responses = [
        'Based on my analysis, this capsule shows strong market potential.',
        'I\'m detecting high authenticity scores and emotional value.',
        'Market conditions suggest this is an optimal trading opportunity.',
        'The memory significance algorithms indicate premium value.',
        'Cross-referencing with market data shows bullish sentiment.'
      ];

      const agentResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: randomAgent.name,
        message: responses[Math.floor(Math.random() * responses.length)],
        timestamp: new Date(),
        agentResponse: {
          confidence: Math.random() * 0.3 + 0.7,
          analysis: 'Multi-factor analysis shows positive indicators',
          recommendation: 'Recommend monitoring for 24-48 hours'
        }
      };

      setChatMessages(prev => [...prev, agentResponse]);
    }, 1500);
  };

  const triggerCollaborativeAnalysis = () => {
    const collaborativeMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      message: 'Run collaborative analysis on all my capsules',
      timestamp: new Date()
    };

    setChatMessages(prev => [...prev, collaborativeMessage]);

    // Simulate multiple agents collaborating
    const agentResponses = [
      { agent: 'Memory Appraiser', delay: 1000, message: 'Starting emotional value assessment across all capsules...' },
      { agent: 'Authenticity Validator', delay: 2000, message: 'Verifying authenticity scores and metadata consistency...' },
      { agent: 'Marketplace Coordinator', delay: 3000, message: 'Analyzing market conditions and trading opportunities...' },
      { agent: 'Trading Legacy Agent', delay: 4000, message: 'Collaborative analysis complete! Here are my unified recommendations...' }
    ];

    agentResponses.forEach(({ agent, delay, message }) => {
      setTimeout(() => {
        const agentMessage: ChatMessage = {
          id: (Date.now() + delay).toString(),
          sender: agent,
          message,
          timestamp: new Date(),
          agentResponse: {
            confidence: Math.random() * 0.2 + 0.8,
            analysis: 'Multi-agent collaborative assessment',
            recommendation: delay === 4000 ? 'Portfolio shows strong diversification and growth potential' : undefined
          }
        };
        setChatMessages(prev => [...prev, agentMessage]);
      }, delay);
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            🤖 Human-AI Collaboration Hub
          </h1>
          <p className="text-xl text-blue-200 mb-2">
            Interact with ASI Alliance agents to analyze and trade your time capsules
          </p>
          <Badge variant="secondary" className="text-sm">
            ASI Alliance Compatible • Multi-Agent System • Real-time Analysis
          </Badge>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Agent Status Panel */}
          <div className="lg:col-span-1">
            <Card className="bg-black/20 border-blue-500/30 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  🎯 Active AI Agents
                  <Badge variant="outline" className="ml-auto">
                    {agents.filter(a => a.status === 'online').length} Online
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {agents.map((agent) => (
                  <div key={agent.id} className="p-3 rounded-lg bg-white/5 border border-blue-400/20">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-white font-semibold text-sm">{agent.name}</h4>
                      <Badge 
                        variant={agent.status === 'online' ? 'default' : agent.status === 'busy' ? 'destructive' : 'secondary'}
                        className="text-xs"
                      >
                        {agent.status}
                      </Badge>
                    </div>
                    <p className="text-blue-200 text-xs mb-2">{agent.specialization}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-green-400 text-xs">
                        Confidence: {(agent.confidence * 100).toFixed(0)}%
                      </span>
                      <span className="text-gray-400 text-xs">
                        {agent.address.slice(0, 12)}...
                      </span>
                    </div>
                    <p className="text-gray-300 text-xs mt-1 italic">{agent.lastResponse}</p>
                  </div>
                ))}
                
                <Button 
                  onClick={triggerCollaborativeAnalysis}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                >
                  🚀 Trigger Collaborative Analysis
                </Button>
              </CardContent>
            </Card>

            {/* Analysis Results */}
            <Card className="bg-black/20 border-green-500/30 backdrop-blur-sm mt-4">
              <CardHeader>
                <CardTitle className="text-white">📊 Live Analysis Results</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {analysisResults.map((result) => (
                  <div key={result.capsuleId} className="p-3 rounded-lg bg-white/5 border border-green-400/20">
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="text-white font-semibold text-sm">{result.title}</h5>
                      <Badge 
                        variant={result.tradingRecommendation === 'buy' ? 'default' : 'secondary'}
                        className="text-xs"
                      >
                        {result.tradingRecommendation.toUpperCase()}
                      </Badge>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <span className="text-green-400">Value: {result.marketValue}</span>
                      <span className="text-blue-400">Rarity: {(result.rarity * 100).toFixed(0)}%</span>
                    </div>
                    <p className="text-yellow-400 text-xs mt-1">{result.sentiment}</p>
                    <div className="mt-2 space-y-1">
                      {result.reasonsAnalysis.slice(0, 2).map((reason, idx) => (
                        <p key={idx} className="text-gray-300 text-xs">• {reason}</p>
                      ))}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <Card className="bg-black/20 border-purple-500/30 backdrop-blur-sm h-[600px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  💬 Multi-Agent Chat Interface
                  <Badge variant="outline" className="ml-auto">
                    ASI:One Protocol
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="flex-1 flex flex-col">
                {/* Chat Messages */}
                <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-2">
                  {chatMessages.map((msg) => (
                    <div 
                      key={msg.id} 
                      className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-[80%] p-3 rounded-lg ${
                        msg.sender === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-purple-600/80 text-white'
                      }`}>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-semibold text-sm">
                            {msg.sender === 'user' ? '👤 You' : `🤖 ${msg.sender}`}
                          </span>
                          <span className="text-xs opacity-70">
                            {msg.timestamp.toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-sm">{msg.message}</p>
                        {msg.agentResponse && (
                          <div className="mt-2 p-2 rounded bg-black/20 border border-white/10">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-green-400">
                                Confidence: {(msg.agentResponse.confidence * 100).toFixed(0)}%
                              </span>
                            </div>
                            <p className="text-xs text-blue-200">{msg.agentResponse.analysis}</p>
                            {msg.agentResponse.recommendation && (
                              <p className="text-xs text-yellow-300 mt-1">
                                💡 {msg.agentResponse.recommendation}
                              </p>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>

                {/* Chat Input */}
                <div className="flex gap-2">
                  <Input
                    value={currentMessage}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setCurrentMessage(e.target.value)}
                    placeholder="Ask the AI agents about your time capsules..."
                    className="flex-1 bg-white/10 border-white/20 text-white placeholder-gray-400"
                    onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && sendMessage()}
                  />
                  <Button 
                    onClick={sendMessage}
                    disabled={!currentMessage.trim()}
                    className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                  >
                    Send
                  </Button>
                </div>

                {/* Quick Actions */}
                <div className="flex gap-2 mt-2">
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => setCurrentMessage('What is the market sentiment for family memory capsules?')}
                    className="text-xs border-blue-400/30 text-blue-300 hover:bg-blue-600/20"
                  >
                    Market Sentiment
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => setCurrentMessage('Check authenticity of my travel capsule')}
                    className="text-xs border-green-400/30 text-green-300 hover:bg-green-600/20"
                  >
                    Authenticity Check
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => setCurrentMessage('Should I unlock my capsule early for trading?')}
                    className="text-xs border-purple-400/30 text-purple-300 hover:bg-purple-600/20"
                  >
                    Trading Advice
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Demo Information */}
        <Card className="mt-6 bg-black/20 border-yellow-500/30 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              🏆 ASI Alliance Hackathon Demo Features
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div className="text-center p-4 rounded-lg bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-blue-400/30">
                <h4 className="text-white font-semibold mb-2">🎯 ASI:One Integration</h4>
                <p className="text-blue-200">All agents registered on ASI:One protocol with mailbox discovery</p>
              </div>
              <div className="text-center p-4 rounded-lg bg-gradient-to-br from-green-600/20 to-blue-600/20 border border-green-400/30">
                <h4 className="text-white font-semibold mb-2">🤝 Multi-Agent Collaboration</h4>
                <p className="text-green-200">Coordinated analysis across 4 specialized AI agents</p>
              </div>
              <div className="text-center p-4 rounded-lg bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-400/30">
                <h4 className="text-white font-semibold mb-2">💎 Human-AI Excellence</h4>
                <p className="text-purple-200">Intuitive interface for complex memory trading decisions</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}