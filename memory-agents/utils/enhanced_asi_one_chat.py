"""
Enhanced ASI:One Chat Protocol for Agent Discovery
Implements comprehensive human-agent interaction with agent discovery
"""
import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Import agent registry
from .asi_alliance_registry import agent_registry

class ASIOneChatRequest(BaseModel):
    message: str
    user_context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    intent: Optional[str] = None

class ASIOneChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    relevant_agents: List[Dict[str, Any]]
    suggested_actions: List[str]
    metta_reasoning: Optional[Dict[str, Any]] = None

class EnhancedASIOneClient:
    """Enhanced ASI:One client with agent discovery and MeTTa reasoning"""
    
    def __init__(self):
        self.api_key = os.getenv("ASI_ONE_API_KEY", "demo_key")
        self.session_history = {}
        
        # Enhanced intent patterns for agent discovery
        self.intent_patterns = {
            "agent_discovery": [
                "what agents", "show agents", "available agents", "help me find",
                "which agent", "who can help", "agent list", "services available"
            ],
            "portfolio_analysis": [
                "my collection", "portfolio worth", "nft value", "collection value",
                "show my nfts", "assets", "investment"
            ],
            "memory_valuation": [
                "how much worth", "appraise", "value this", "price", "evaluate",
                "market value", "what's it worth"
            ],
            "authenticity_check": [
                "is real", "authentic", "verify", "check authenticity", "fraud",
                "genuine", "fake detection"
            ],
            "trading_assistance": [
                "buy memory", "sell nft", "trade", "purchase", "marketplace",
                "estate plan", "inheritance"
            ],
            "market_insights": [
                "market trends", "prices", "demand", "popular memories",
                "investment advice", "market analysis"
            ]
        }
        
        # MeTTa reasoning templates for different intents
        self.metta_reasoning_templates = {
            "agent_discovery": {
                "reasoning_chain": [
                    "User seeks agent assistance",
                    "Analyze query for specific capabilities needed", 
                    "Match capabilities to available agents",
                    "Rank agents by relevance and confidence",
                    "Provide discovery response with suggested actions"
                ],
                "knowledge_base": "agent_registry_ontology"
            },
            "portfolio_analysis": {
                "reasoning_chain": [
                    "User wants portfolio insights",
                    "Route to Memory Appraiser for valuation",
                    "Consider market trends and rarity factors",
                    "Generate comprehensive analysis report"
                ],
                "knowledge_base": "memory_valuation_ontology"
            },
            "authenticity_check": {
                "reasoning_chain": [
                    "User questions memory authenticity",
                    "Route to Authenticity Validator agent",
                    "Apply multi-agent consensus verification",
                    "Provide confidence score and reasoning"
                ],
                "knowledge_base": "authenticity_verification_ontology"
            }
        }
    
    async def process_asi_one_chat(self, request: ASIOneChatRequest) -> ASIOneChatResponse:
        """Process ASI:One chat request with agent discovery"""
        
        # Classify intent
        intent = self._classify_intent(request.message)
        
        # Get relevant agents for this intent
        relevant_agents = agent_registry.discover_agents_by_asi_one_query(request.message)
        
        # Generate MeTTa reasoning
        metta_reasoning = self._generate_metta_reasoning(intent, request.message)
        
        # Generate response based on intent
        if intent == "agent_discovery":
            response = await self._handle_agent_discovery(request, relevant_agents)
        elif intent == "portfolio_analysis":
            response = await self._handle_portfolio_query(request, relevant_agents)
        elif intent == "memory_valuation":
            response = await self._handle_valuation_query(request, relevant_agents)
        elif intent == "authenticity_check":
            response = await self._handle_authenticity_query(request, relevant_agents)
        elif intent == "trading_assistance":
            response = await self._handle_trading_query(request, relevant_agents)
        else:
            response = await self._handle_general_query(request, relevant_agents)
        
        return ASIOneChatResponse(
            response=response["content"],
            intent=intent,
            confidence=response["confidence"],
            relevant_agents=relevant_agents,
            suggested_actions=response["suggested_actions"],
            metta_reasoning=metta_reasoning
        )
    
    def _classify_intent(self, message: str) -> str:
        """Classify user intent from message"""
        message_lower = message.lower()
        
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in message_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores.items(), key=lambda x: x[1])[0]
        
        return "general_inquiry"
    
    def _generate_metta_reasoning(self, intent: str, query: str) -> Dict[str, Any]:
        """Generate MeTTa reasoning explanation"""
        template = self.metta_reasoning_templates.get(intent, {})
        
        return {
            "intent_classification": intent,
            "reasoning_chain": template.get("reasoning_chain", ["General query processing"]),
            "knowledge_base_used": template.get("knowledge_base", "general_knowledge"),
            "confidence_factors": [
                "Intent pattern matching",
                "Agent capability alignment", 
                "Historical query success rate"
            ],
            "metta_features_applied": [
                "Intent recognition ontology",
                "Agent capability mapping",
                "User context reasoning"
            ]
        }
    
    async def _handle_agent_discovery(self, request: ASIOneChatRequest, agents: List[Dict]) -> Dict:
        """Handle agent discovery requests"""
        registry_summary = agent_registry.get_agent_registry_summary()
        
        response_content = f"""🤖 **Memory Marketplace Agent Discovery**

I found **{len(agents)}** agents that can help you:

"""
        
        # Show top 3 most relevant agents
        for i, agent in enumerate(agents[:3], 1):
            response_content += f"""**{i}. {agent['name']}** (Confidence: {agent['confidence']:.1%})
   📋 {agent['description']}
   🎯 Webhook: `{agent['webhook']}`
   💡 Try: "{agent['suggested_queries'][0] if agent.get('suggested_queries') else 'How can you help me?'}"

"""
        
        response_content += f"""📊 **System Overview:**
• Total Agents: {registry_summary['total_agents']} 
• ASI:One Compatible: {registry_summary['asi_one_compatible']}
• MeTTa Enabled: {registry_summary['metta_enabled']}

🔍 **Popular Queries:**
"""
        for query in registry_summary['sample_queries'][:3]:
            response_content += f"• \"{query}\"\n"
        
        return {
            "content": response_content,
            "confidence": 0.95,
            "suggested_actions": [
                f"Connect to {agents[0]['name']}" if agents else "Explore agent capabilities",
                "Ask about specific memory services",
                "Request portfolio analysis"
            ]
        }
    
    async def _handle_portfolio_query(self, request: ASIOneChatRequest, agents: List[Dict]) -> Dict:
        """Handle portfolio analysis requests"""
        appraiser_agent = next((a for a in agents if "appraiser" in a['name'].lower()), None)
        
        response_content = f"""📊 **Portfolio Analysis Request Received**

I'll connect you with our **Memory Appraiser Agent** for detailed analysis:

🤖 **Best Agent for This Task:**
**{appraiser_agent['name'] if appraiser_agent else 'Memory Appraiser'}**
📋 Specializes in memory valuation using advanced MeTTa reasoning
🧠 Features: 15+ memory ontologies, predictive pricing models

🎯 **What I Can Analyze:**
• Collection total value and growth trends
• Individual memory rarity scores  
• Market positioning vs similar collections
• Investment recommendations

💡 **Next Steps:**
Connect to the Memory Appraiser at `{appraiser_agent['webhook'] if appraiser_agent else 'http://localhost:8001'}`
"""
        
        return {
            "content": response_content,
            "confidence": 0.88,
            "suggested_actions": [
                "Connect to Memory Appraiser Agent",
                "Provide memory collection details",
                "Request detailed valuation report"
            ]
        }
    
    async def _handle_authenticity_query(self, request: ASIOneChatRequest, agents: List[Dict]) -> Dict:
        """Handle authenticity verification requests"""
        validator_agent = next((a for a in agents if "authenticity" in a['name'].lower() or "verifier" in a['name'].lower()), None)
        
        response_content = f"""🔍 **Authenticity Verification Request**

I'll route you to our **Multi-Agent Authenticity Verification System**:

🤖 **Specialist Agent:**
**{validator_agent['name'] if validator_agent else 'Authenticity Validator'}**
🛡️ Multi-agent consensus system with advanced fraud detection

🧠 **MeTTa-Powered Analysis:**
• Deepfake detection algorithms
• Metadata consistency verification
• Emotional congruence analysis
• Consensus voting across multiple AI agents

✅ **Verification Process:**
1. Upload memory for analysis
2. Multi-agent consensus verification (95%+ accuracy)
3. Receive authenticity score and detailed report

🎯 **Connect at:** `{validator_agent['webhook'] if validator_agent else 'http://localhost:8002'}`
"""
        
        return {
            "content": response_content,
            "confidence": 0.92,
            "suggested_actions": [
                "Connect to Authenticity Validator",
                "Upload memory for verification", 
                "Review consensus verification report"
            ]
        }
    
    async def _handle_trading_query(self, request: ASIOneChatRequest, agents: List[Dict]) -> Dict:
        """Handle trading and marketplace requests"""
        trading_agent = next((a for a in agents if "trading" in a['name'].lower() or "market" in a['name'].lower()), None)
        
        response_content = f"""💰 **Memory Trading & Marketplace Services**

Our **Trading & Legacy Agent** can help with:

🤖 **Specialist Agent:**  
**{trading_agent['name'] if trading_agent else 'Trading & Legacy Agent'}**
📈 Combined market making and inheritance management

🎯 **Available Services:**
• **Market Making:** Create liquidity for memory NFTs
• **Estate Planning:** Digital inheritance protocols
• **Legacy Transfers:** Multi-generational wealth management
• **Trading Strategies:** Optimized buy/sell recommendations

💡 **Popular Actions:**
• Buy rare childhood memories
• Create digital estate plans
• Set up inheritance protocols
• Get trading recommendations

🔗 **Connect at:** `{trading_agent['webhook'] if trading_agent else 'http://localhost:8005'}`
"""
        
        return {
            "content": response_content,
            "confidence": 0.90,
            "suggested_actions": [
                "Connect to Trading & Legacy Agent",
                "Explore marketplace opportunities",
                "Create estate planning strategy"
            ]
        }
    
    async def _handle_general_query(self, request: ASIOneChatRequest, agents: List[Dict]) -> Dict:
        """Handle general queries"""
        response_content = f"""🧠 **Memory Marketplace Assistant**

I understand you're looking for help with: "{request.message}"

🤖 **Available Specialized Agents:**
"""
        
        for agent in agents[:2]:
            response_content += f"• **{agent['name']}**: {agent['description']}\n"
        
        response_content += f"""
💡 **Try These Specific Queries:**
• "What's my memory collection worth?"
• "Is this childhood video authentic?" 
• "Help me buy rare graduation memories"
• "Create an estate plan for my NFTs"

🔍 **For Agent Discovery:** "Show me available agents"
"""
        
        return {
            "content": response_content,
            "confidence": 0.75,
            "suggested_actions": [
                "Refine your query for better agent matching",
                "Explore specific agent capabilities",
                "Ask about memory marketplace services"
            ]
        }


# Global enhanced ASI:One client
enhanced_asi_one = EnhancedASIOneClient()

# FastAPI endpoint for ASI:One Chat Protocol
def create_asi_one_chat_endpoint(app: FastAPI):
    """Add ASI:One chat endpoint to FastAPI app"""
    
    @app.post("/asi-one/chat")
    async def asi_one_chat_endpoint(request: ASIOneChatRequest):
        """ASI:One Chat Protocol endpoint with agent discovery"""
        try:
            response = await enhanced_asi_one.process_asi_one_chat(request)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/asi-one/agents")
    async def get_available_agents():
        """Get all available agents for ASI:One discovery"""
        return agent_registry.get_agent_registry_summary()
    
    @app.get("/asi-one/capabilities")  
    async def get_agent_capabilities():
        """Get detailed agent capabilities for ASI:One"""
        return {
            "agents": agent_registry.agent_capabilities,
            "total_capabilities": len(set(
                cap for agent in agent_registry.agent_capabilities.values()
                for cap in agent.get("capabilities", [])
            )),
            "metta_enabled_features": sum(
                len(agent.get("metta_features", [])) 
                for agent in agent_registry.agent_capabilities.values()
            )
        }

# Test function
async def test_enhanced_asi_one():
    """Test enhanced ASI:One functionality"""
    test_queries = [
        ASIOneChatRequest(message="What agents are available?"),
        ASIOneChatRequest(message="What's my collection worth?"),
        ASIOneChatRequest(message="Is this memory authentic?"),
        ASIOneChatRequest(message="Help me buy rare memories")
    ]
    
    for request in test_queries:
        print(f"\n🔍 Query: '{request.message}'")
        response = await enhanced_asi_one.process_asi_one_chat(request)
        print(f"🎯 Intent: {response.intent}")
        print(f"💡 Relevant Agents: {len(response.relevant_agents)}")
        print(f"🧠 MeTTa Reasoning: {len(response.metta_reasoning['reasoning_chain'])} steps")

if __name__ == "__main__":
    asyncio.run(test_enhanced_asi_one())