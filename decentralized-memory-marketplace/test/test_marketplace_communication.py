import os
import asyncio
from uagents_core.identity import Identity
from fetchai.communication import send_message_to_agent
from dotenv import load_dotenv

load_dotenv()

MARKETPLACE_ADDRESS = "agent1q2p0gyh95sc6jhlaclxtfj4f5h5huxjx6dggekh2d6hzyypdq5krswm65ay"
APPRAISER_ADDRESS = "agent1qfnvqg25udtmylkdca66hfymmymk39c7hmxpdld6q87v2cg83qenskjhcfk"
AUTHENTICITY_ADDRESS = "agent1qgmnuepkgp32s58lhn97ry4hudt886rfr7q46phhxuv2h9suzs5tclapg7a"
TRADING_LEGACY_ADDRESS = "agent1qt37y2uv5gaujj90d3v0hf0dw2kvdeq9r6uauc244jc7d9uq5cw7xex2s38"

CLIENT_IDENTITY = Identity.from_seed("test_client_seed", 0)

async def test_marketplace_communication():
    
    print(f"🧪 Testing Memory Marketplace Communication")
    print(f"Client Address: {CLIENT_IDENTITY.address}")
    print("-" * 50)
    
    test_scenarios = [
        {
            "name": "Memory Valuation Request",
            "target": MARKETPLACE_ADDRESS,
            "payload": {
                "type": "valuation_request",
                "data": {
                    "memory_id": "childhood_summer_001",
                    "content_type": "childhood_experience",
                    "quality_metrics": {
                        "clarity": 0.95,
                        "emotional_impact": 0.9,
                        "uniqueness": 0.85
                    },
                    "metadata": {
                        "title": "First Beach Trip",
                        "year": "1995"
                    }
                }
            }
        },
        {
            "name": "Market Search Query",
            "target": MARKETPLACE_ADDRESS,
            "payload": {
                "type": "market_query",
                "data": {
                    "query_type": "search",
                    "parameters": {
                        "term": "graduation memories",
                        "price_range": [100, 400]
                    }
                }
            }
        },
        {
            "name": "NFT Listing Request",
            "target": MARKETPLACE_ADDRESS,
            "payload": {
                "type": "list_nft",
                "data": {
                    "memory_id": "graduation_ceremony_001",
                    "requested_price": 350.0,
                    "metadata": {
                        "title": "College Graduation",
                        "category": "milestone"
                    }
                }
            }
        },
        {
            "name": "Direct Authenticity Check",
            "target": AUTHENTICITY_ADDRESS,
            "payload": {
                "type": "authenticity_check",
                "data": {
                    "memory_id": "wedding_video_001",
                    "metadata": {"title": "Wedding Ceremony", "year": "2020"},
                    "quality_metrics": {"clarity": 0.9, "emotional_impact": 0.95}
                }
            }
        },
        {
            "name": "Market Making Request",
            "target": TRADING_LEGACY_ADDRESS,
            "payload": {
                "type": "create_listing",
                "data": {
                    "memory_id": "family_reunion_001",
                    "asking_price": 200.0,
                    "metadata": {"title": "Family Reunion 2023"}
                }
            }
        },
        {
            "name": "Legacy Planning Request", 
            "target": TRADING_LEGACY_ADDRESS,
            "payload": {
                "type": "estate_planning",
                "data": {
                    "owner_id": "family_patriarch_001",
                    "collection_value": 5000.0,
                    "beneficiaries": ["child1", "child2", "grandchild1"]
                }
            }
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📤 Test {i}: {scenario['name']}")
        
        try:
            result = send_message_to_agent(
                sender=CLIENT_IDENTITY,
                target=scenario["target"],
                payload=scenario["payload"]
            )
            
            print(f"✅ Message sent: {result.status}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        await asyncio.sleep(2)

if __name__ == "__main__":
    print("🌟 Memory NFT Marketplace - Communication Test")
    print("=" * 60)
    print("⚠️  Update agent addresses after running the agents!")
    
    asyncio.run(test_marketplace_communication())