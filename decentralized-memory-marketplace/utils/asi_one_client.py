"""
ASI:One Natural Language Interface Client
Integration with ASI:One LLM for human-agent interaction in the memory marketplace
"""
import os
import json
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import aiohttp
import requests
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ASIOneResponse:
    """Response from ASI:One LLM"""
    content: str
    confidence: float
    intent: str
    entities: Dict[str, Any]
    timestamp: str

class ASIOneClient:
    """Client for ASI:One natural language interface"""
    
    def __init__(self):
        self.api_key = os.getenv("ASI_ONE_API_KEY", "demo_key")
        self.base_url = "https://api.asi1.ai/v1"
        self.model = "asi1-mini"
        self.marketplace_context = {
            "domain": "memory_nft_marketplace",
            "capabilities": [
                "Memory valuation and pricing",
                "Portfolio analysis and management", 
                "Market trend analysis",
                "Collection worth calculation",
                "Transaction coordination",
                "NFT listing and trading"
            ],
            "supported_queries": [
                "What's my collection worth?",
                "How much is this memory worth?",
                "Show me market trends",
                "List my NFTs for sale",
                "Find similar memories",
                "Calculate portfolio value"
            ]
        }
    
    async def process_natural_language_query(self, query: str, user_context: Dict = None) -> ASIOneResponse:
        """
        Process natural language query through ASI:One with marketplace context
        """
        print(f"🤖 Processing ASI:One query: {query}")
        
        # Enhanced query analysis with marketplace context
        intent = await self._analyze_query_intent(query)
        entities = await self._extract_entities(query)
        
        if self.api_key == "demo_key":
            # Simulation mode for development
            return await self._simulate_asi_one_response(query, intent, entities, user_context)
        else:
            # Real ASI:One API integration
            return await self._call_asi_one_api(query, intent, entities, user_context)
    
    async def _analyze_query_intent(self, query: str) -> str:
        """Analyze the intent of user query"""
        query_lower = query.lower()
        
        intent_patterns = {
            "portfolio_value": ["collection worth", "portfolio value", "total value", "my nfts worth", "portfolio", "collection value"],
            "memory_valuation": ["worth", "value", "price", "how much", "valuation", "estimate"],
            "market_analysis": ["market", "trends", "analysis", "performance", "market data", "best performing"],
            "list_nft": ["sell", "list", "trade", "marketplace", "list my", "put up for sale"],
            "find_similar": ["similar", "find", "search", "like this", "compare"],
            "transaction": ["buy", "purchase", "transfer", "coordinate", "want to buy", "nft for"],
            "portfolio_optimization": ["optimize", "improve", "strategy", "recommendations", "portfolio advice"],
            "listing_status": ["how is", "status", "listing doing", "my listing", "nft doing"],
            "general_info": ["help", "info", "capabilities", "what can", "assistant"]
        }
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                return intent
        
        return "general_query"
    
    async def _extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities from user query"""
        entities = {}
        query_lower = query.lower()
        
        # Extract memory types
        memory_types = ["childhood", "first love", "achievement", "travel", "family"]
        for memory_type in memory_types:
            if memory_type in query_lower:
                entities["memory_type"] = memory_type
                break
        
        # Extract price ranges
        if "under" in query_lower and any(char.isdigit() for char in query):
            price_match = ''.join(filter(str.isdigit, query))
            if price_match:
                entities["max_price"] = int(price_match)
        
        # Extract time periods
        time_periods = ["week", "month", "year", "today", "recent"]
        for period in time_periods:
            if period in query_lower:
                entities["time_period"] = period
                break
        
        return entities
    
    async def _simulate_asi_one_response(self, query: str, intent: str, entities: Dict, user_context: Dict = None) -> ASIOneResponse:
        """Simulate ASI:One response for development"""
        
        response_templates = {
            "portfolio_value": {
                "content": f"📊 Your Memory NFT Collection Analysis:\n\n• Total Collection Value: $2,450.00\n• Number of NFTs: 8 memories\n• Average Value: $306.25\n• Top Memory: 'First Love at College' ($520)\n• Portfolio Growth: +12% this month\n\n💡 Your collection shows strong emotional value with high-demand childhood and romance memories. Consider listing 2-3 mid-tier memories to optimize your portfolio.",
                "confidence": 0.92,
                "entities": {"total_value": 2450.00, "nft_count": 8, "growth": 12}
            },
            "memory_valuation": {
                "content": f"💎 Memory Valuation Analysis:\n\n• Estimated Value: $185 - $220\n• Memory Type: {entities.get('memory_type', 'Personal Experience')}\n• Rarity Score: 7.2/10\n• Market Demand: High\n• Authenticity Score: 95%\n\n🎯 This memory shows strong market potential. Similar memories sold for $190-$215 in the past week.",
                "confidence": 0.88,
                "entities": {"value_range": [185, 220], "rarity": 7.2}
            },
            "market_analysis": {
                "content": "📈 Memory NFT Market Trends:\n\n• Overall Market: +8% growth this week\n• Hot Categories: Childhood (+15%), First Love (+12%)\n• Trading Volume: $45K daily average\n• Active Listings: 342 memories\n• Price Range: $50 - $1,200\n\n🔥 Peak trading hours: 7-9 PM EST\n💡 Best selling strategy: List emotional memories during evening hours",
                "confidence": 0.85,
                "entities": {"market_growth": 8, "volume": 45000}
            },
            "list_nft": {
                "content": "🏷️ NFT Listing Assistant:\n\n• I can help you list your memory NFT for sale!\n• First, let me value your memory for optimal pricing\n• Required info: Memory type, emotional significance, rarity\n• Listing fee: $5, plus 2.5% marketplace fee\n\n💡 Tip: Childhood and romance memories perform best in current market!",
                "confidence": 0.90,
                "entities": {"action": "listing_help"}
            },
            "transaction": {
                "content": f"💰 NFT Purchase Assistant:\n\n• Budget: ${entities.get('max_price', 200)}\n• Available memories in your range: 15-20 options\n• Recommended categories: Achievement, Travel (good ROI)\n• I can coordinate the entire purchase process\n\n🎯 Let me find the perfect memory NFT for your collection!",
                "confidence": 0.85,
                "entities": {"budget": entities.get('max_price', 200)}
            },
            "portfolio_optimization": {
                "content": "📊 Portfolio Optimization Strategy:\n\n• Diversify across 4-5 memory categories\n• Target 70% emotional memories, 30% achievement-based\n• Optimal portfolio size: 6-12 NFTs\n• Rebalance quarterly based on market trends\n\n💡 Current hot tip: Childhood memories up 15% this month!",
                "confidence": 0.88,
                "entities": {"strategy": "diversification"}
            },
            "listing_status": {
                "content": "📋 Your NFT Listing Status:\n\n• Active listings are performing well\n• Average time to sale: 3-5 days\n• Current market activity: High demand\n• Suggested action: Hold current pricing\n\n✨ Your memories are getting good visibility in the marketplace!",
                "confidence": 0.82,
                "entities": {"listing_performance": "good"}
            },
            "general_info": {
                "content": "🎯 Memory NFT Marketplace Assistant\n\nI can help you with:\n• 'What's my collection worth?' - Portfolio valuation\n• 'How much is this memory worth?' - Individual pricing\n• 'Show market trends' - Market analysis\n• 'List my NFT' - Create marketplace listings\n• 'Find similar memories' - Discovery and comparison\n• 'Buy an NFT for $X' - Purchase coordination\n\n💬 Just ask me naturally, like talking to a friend!",
                "confidence": 0.95,
                "entities": {}
            }
        }
        
        template = response_templates.get(intent, response_templates["general_info"])
        
        return ASIOneResponse(
            content=template["content"],
            confidence=template["confidence"],
            intent=intent,
            entities={**entities, **template["entities"]},
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    
    async def _call_asi_one_api(self, query: str, intent: str, entities: Dict, user_context: Dict = None) -> ASIOneResponse:
        """Call real ASI:One API using the official format"""
        
        # Build context-aware prompt for the memory NFT marketplace
        system_context = f"""You are an AI assistant for a Memory NFT Marketplace. You help users with:
- Portfolio analysis and valuation
- Memory NFT pricing and market trends  
- Transaction coordination and trading
- Collection management advice

User's Query Intent: {intent}
Extracted Entities: {entities}
Marketplace Context: {json.dumps(self.marketplace_context, indent=2)}
"""
        
        if user_context:
            system_context += f"\nUser Context: {json.dumps(user_context, indent=2)}"

        # Create messages for ASI:One API
        messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": query}
        ]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    json=body,
                    headers=headers,
                    timeout=30
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract response using the ASI:One format you provided
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        
                        # Get additional ASI:One specific data
                        thought = data.get("thought", [""])[0] if data.get("thought") else ""
                        usage = data.get("usage", {})
                        
                        print(f"✅ ASI:One API Success - Tokens used: {usage.get('total_tokens', 'unknown')}")
                        
                        return ASIOneResponse(
                            content=content,
                            confidence=0.9,  # High confidence for real API responses
                            intent=intent,
                            entities={
                                **entities, 
                                "asi_one_thought": thought,
                                "token_usage": usage
                            },
                            timestamp=datetime.now(timezone.utc).isoformat()
                        )
                    else:
                        error_text = await response.text()
                        print(f"⚠️ ASI:One API error ({response.status}): {error_text}")
                        # Fallback to simulation
                        return await self._simulate_asi_one_response(query, intent, entities, user_context)
                        
        except Exception as e:
            print(f"❌ ASI:One API connection error: {e}, using simulation")
            return await self._simulate_asi_one_response(query, intent, entities, user_context)

# Global client instance
asi_one_client = ASIOneClient()

async def process_natural_language_query(query: str, user_context: Dict = None) -> ASIOneResponse:
    """Convenience function for natural language processing"""
    return await asi_one_client.process_natural_language_query(query, user_context)

if __name__ == "__main__":
    # Test the ASI:One client with both real API and simulation
    async def test_asi_one():
        client = ASIOneClient()
        
        print(f"🧪 Testing ASI:One Client")
        print(f"API Key: {'REAL' if client.api_key != 'demo_key' else 'DEMO'}")
        print(f"Base URL: {client.base_url}")
        
        test_queries = [
            "What's my collection worth?",
            "How much is my childhood memory worth?", 
            "Show me market trends for this week",
            "Help me list my first love memory for sale"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}/4: {query}")
            try:
                response = await client.process_natural_language_query(query)
                print(f"   Intent: {response.intent}")
                print(f"   Confidence: {response.confidence}")
                print(f"   Response Preview: {response.content[:100]}...")
                
                # Show if real ASI:One was used
                if "token_usage" in response.entities:
                    print(f"   🤖 Real ASI:One Used - Tokens: {response.entities['token_usage'].get('total_tokens', 'N/A')}")
                else:
                    print(f"   🎭 Simulation Mode Used")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 50)
    
    # Also test synchronous version like in your example
    def test_sync_asi_one():
        print(f"\n🧪 Testing Synchronous ASI:One API (like your example)")
        
        api_key = os.getenv('ASI_ONE_API_KEY')
        if api_key == "demo_key":
            print("⚠️ Using demo key, skipping sync test")
            return
            
        url = "https://api.asi1.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "asi1-mini",
            "messages": [{"role": "user", "content": "What's my NFT collection worth? I have 5 memory NFTs."}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=body)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                print(f"✅ Sync API Success!")
                print(f"Response: {content[:150]}...")
                print(f"Tokens: {usage.get('total_tokens', 'N/A')}")
            else:
                print(f"❌ Sync API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Sync API Exception: {e}")
    
    asyncio.run(test_asi_one())
    test_sync_asi_one()