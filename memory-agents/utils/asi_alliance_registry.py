"""
ASI Alliance Agent Registration & Discovery System
Makes all 4 agents easily discoverable through ASI:One Chat Protocol
"""
import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from uagents import Agent, Context, Bureau, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
from uagents.communication import send_wallet_connect_request, send_message
import logging

# Agent Discovery Protocol
class AgentRegistrationRequest(Model):
    agent_address: str
    agent_name: str
    capabilities: List[str]
    description: str
    asi_one_compatible: bool
    metta_enabled: bool

class AgentDiscoveryResponse(Model):
    available_agents: List[Dict[str, Any]]
    total_count: int
    categories: Dict[str, int]

class ASIAllianceAgentRegistry:
    """Central registry for ASI Alliance agent discovery"""
    
    def __init__(self):
        self.registered_agents = {}
        self.agent_capabilities = {
            "marketplace_coordinator": {
                "name": "Memory Marketplace Coordinator",
                "description": "Natural language interface for memory NFT marketplace operations",
                "capabilities": [
                    "Natural language query processing",
                    "Portfolio valuation and analysis", 
                    "Transaction coordination",
                    "Market trend analysis",
                    "User interaction management"
                ],
                "asi_one_endpoints": [
                    "/chat",
                    "/portfolio-analysis",
                    "/market-query",
                    "/transaction-status"
                ],
                "metta_features": [
                    "Memory valuation reasoning",
                    "Market sentiment analysis",
                    "User intent recognition"
                ],
                "port": 8000,
                "webhook": "http://localhost:8000",
                "status": "active"
            },
            "memory_appraiser": {
                "name": "Memory Valuation Specialist",
                "description": "AI-powered memory appraisal using advanced MeTTa reasoning",
                "capabilities": [
                    "Memory rarity assessment",
                    "Emotional value calculation",
                    "Market trend prediction",
                    "Comparative valuation analysis",
                    "Price discovery mechanisms"
                ],
                "asi_one_endpoints": [
                    "/appraise-memory",
                    "/market-analysis", 
                    "/price-prediction",
                    "/rarity-assessment"
                ],
                "metta_features": [
                    "15+ memory ontologies",
                    "Multi-dimensional scoring",
                    "Predictive pricing models",
                    "Self-learning valuation algorithms"
                ],
                "port": 8001,
                "webhook": "http://localhost:8001", 
                "status": "active"
            },
            "authenticity_validator": {
                "name": "Memory Authenticity Verifier",
                "description": "Multi-agent consensus system for memory authenticity verification",
                "capabilities": [
                    "Deepfake detection",
                    "Metadata verification",
                    "Emotional congruence analysis", 
                    "Multi-agent consensus voting",
                    "Fraud prevention"
                ],
                "asi_one_endpoints": [
                    "/verify-authenticity",
                    "/consensus-check",
                    "/fraud-analysis",
                    "/metadata-validation"
                ],
                "metta_features": [
                    "Authenticity reasoning chains",
                    "Consensus decision trees",
                    "Fraud pattern recognition",
                    "Evidence weighting algorithms"
                ],
                "port": 8002,
                "webhook": "http://localhost:8002",
                "status": "active"  
            },
            "trading_legacy_agent": {
                "name": "Market Maker & Legacy Broker",
                "description": "Combined trading and inheritance management for memory NFTs",
                "capabilities": [
                    "Market making and liquidity",
                    "Estate planning integration",
                    "Inheritance protocol execution",
                    "Bid/ask spread management",
                    "Legacy transfer coordination"
                ],
                "asi_one_endpoints": [
                    "/create-market",
                    "/estate-planning",
                    "/inheritance-setup",
                    "/legacy-transfer"
                ],
                "metta_features": [
                    "Market efficiency optimization",
                    "Estate risk assessment",
                    "Generational value modeling",
                    "Legal compliance reasoning"
                ],
                "port": 8005,
                "webhook": "http://localhost:8005",
                "status": "active"
            }
        }
        
        # ASI:One Chat Protocol Integration
        self.asi_one_queries = {
            "portfolio": ["What's my collection worth?", "Show my NFTs", "Portfolio analysis"],
            "valuation": ["How much is this memory worth?", "Appraise my memory", "Market value"],
            "authenticity": ["Is this memory real?", "Verify authenticity", "Check for fraud"],
            "trading": ["Buy memory NFT", "Sell my collection", "Create estate plan"],
            "discovery": ["Show available agents", "What agents are online?", "Agent capabilities"]
        }
    
    def register_agent(self, agent_address: str, agent_info: Dict) -> bool:
        """Register agent for ASI:One discovery"""
        try:
            self.registered_agents[agent_address] = {
                **agent_info,
                "registered_at": asyncio.get_event_loop().time(),
                "last_seen": asyncio.get_event_loop().time(),
                "message_count": 0,
                "success_rate": 1.0
            }
            
            logging.info(f"✅ Registered agent: {agent_info['name']} at {agent_address}")
            return True
        except Exception as e:
            logging.error(f"❌ Failed to register agent: {e}")
            return False
    
    def discover_agents_by_capability(self, capability: str) -> List[Dict]:
        """Discover agents by specific capability"""
        matching_agents = []
        
        for address, agent_info in self.registered_agents.items():
            if capability.lower() in [cap.lower() for cap in agent_info.get("capabilities", [])]:
                matching_agents.append({
                    "address": address,
                    "name": agent_info["name"],
                    "description": agent_info["description"],
                    "webhook": agent_info["webhook"],
                    "capabilities": agent_info["capabilities"],
                    "metta_features": agent_info.get("metta_features", [])
                })
        
        return matching_agents
    
    def discover_agents_by_asi_one_query(self, query: str) -> List[Dict]:
        """Discover agents based on ASI:One natural language query"""
        query_lower = query.lower()
        relevant_agents = []
        
        # Query intent classification
        intent_mapping = {
            "portfolio": ["portfolio", "collection", "worth", "value", "nfts", "assets"],
            "valuation": ["appraise", "value", "worth", "price", "evaluate"],
            "authenticity": ["authentic", "real", "verify", "fraud", "fake", "check"],
            "trading": ["buy", "sell", "trade", "market", "estate", "inheritance"],
            "discovery": ["agents", "available", "help", "capabilities", "services"]
        }
        
        for intent, keywords in intent_mapping.items():
            if any(keyword in query_lower for keyword in keywords):
                # Find agents that handle this intent
                for address, agent_info in self.registered_agents.items():
                    agent_name = agent_info["name"].lower()
                    if intent in agent_name or any(keyword in agent_info["description"].lower() for keyword in keywords):
                        relevant_agents.append({
                            "address": address,
                            "name": agent_info["name"],
                            "description": agent_info["description"],
                            "webhook": agent_info["webhook"],
                            "confidence": self._calculate_relevance_score(query, agent_info),
                            "asi_one_endpoints": agent_info.get("asi_one_endpoints", []),
                            "suggested_queries": self.asi_one_queries.get(intent, [])
                        })
        
        # Sort by confidence/relevance
        relevant_agents.sort(key=lambda x: x["confidence"], reverse=True)
        return relevant_agents
    
    def _calculate_relevance_score(self, query: str, agent_info: Dict) -> float:
        """Calculate how relevant an agent is to a query"""
        query_words = set(query.lower().split())
        
        # Check description relevance
        description_words = set(agent_info["description"].lower().split())
        description_overlap = len(query_words & description_words) / len(query_words)
        
        # Check capability relevance  
        capability_text = " ".join(agent_info.get("capabilities", [])).lower()
        capability_words = set(capability_text.split())
        capability_overlap = len(query_words & capability_words) / len(query_words)
        
        # Weighted score
        return (description_overlap * 0.6) + (capability_overlap * 0.4)
    
    def get_agent_registry_summary(self) -> Dict[str, Any]:
        """Get complete registry summary for ASI:One"""
        return {
            "total_agents": len(self.registered_agents),
            "active_agents": len([a for a in self.registered_agents.values() if a.get("status") == "active"]),
            "agent_categories": {
                "coordination": 1,
                "valuation": 1,
                "verification": 1, 
                "trading": 1
            },
            "asi_one_compatible": len(self.registered_agents),
            "metta_enabled": len([a for a in self.registered_agents.values() if a.get("metta_features")]),
            "available_capabilities": list(set(
                cap for agent in self.registered_agents.values() 
                for cap in agent.get("capabilities", [])
            )),
            "sample_queries": [
                "What's my memory collection worth?",
                "Is this childhood video authentic?", 
                "Help me create an estate plan",
                "Find rare graduation memories to buy"
            ]
        }
    
    def generate_asi_one_discovery_response(self, query: str) -> Dict[str, Any]:
        """Generate comprehensive discovery response for ASI:One"""
        relevant_agents = self.discover_agents_by_asi_one_query(query)
        registry_summary = self.get_agent_registry_summary()
        
        return {
            "query": query,
            "relevant_agents": relevant_agents,
            "total_agents_available": registry_summary["total_agents"],
            "registry_summary": registry_summary,
            "suggested_next_queries": [
                "Show me market trends for childhood memories",
                "Help me verify this family photo authenticity", 
                "What agents can help with estate planning?",
                "Create a trading strategy for memory NFTs"
            ],
            "asi_one_compatible": True,
            "response_timestamp": asyncio.get_event_loop().time()
        }


# Global registry instance
agent_registry = ASIAllianceAgentRegistry()

# Auto-register all agents
def initialize_agent_registry():
    """Initialize and register all marketplace agents"""
    for agent_name, agent_info in agent_registry.agent_capabilities.items():
        # Generate agent address (in real implementation, this would be actual addresses)
        agent_address = f"agent1{hash(agent_name) % 1000000:06d}..."
        
        agent_registry.register_agent(agent_address, agent_info)
    
    print("🎯 ASI Alliance Agent Registry Initialized")
    print(f"✅ {len(agent_registry.registered_agents)} agents registered for discovery")
    print(f"🤖 ASI:One Chat Protocol: ENABLED")
    print(f"🧠 MeTTa Reasoning: ENABLED for all agents")

# Test function
async def test_agent_discovery():
    """Test agent discovery functionality"""
    initialize_agent_registry()
    
    # Test queries
    test_queries = [
        "What's my collection worth?",
        "Is this memory authentic?",
        "Help me buy rare memories",
        "Show available agents"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        response = agent_registry.generate_asi_one_discovery_response(query)
        print(f"📊 Found {len(response['relevant_agents'])} relevant agents")
        
        for agent in response['relevant_agents'][:2]:  # Show top 2
            print(f"   ✅ {agent['name']} (confidence: {agent['confidence']:.2f})")

if __name__ == "__main__":
    asyncio.run(test_agent_discovery())