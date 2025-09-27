"""
Enhanced Memory Marketplace Communication Test with Chat Protocol
Tests agent-to-agent communication using the new chat protocol features.
"""

import asyncio
import json
import time
from datetime import datetime, timezone
from fetchai.communication import send_message_to_agent
from uagents_core.identity import Identity
import os
from dotenv import load_dotenv

load_dotenv()

# Enhanced agent addresses with chat protocol (use current addresses)
AGENT_ADDRESSES = {
    "marketplace_coordinator": "agent1q2p0gyh95sc6jhlaclxtfj4f5h5huxjx6dggekh2d6hzyypdq5krswm65ay",
    "memory_appraiser": "agent1qfnvqg25udtmylkdca66hfymmymk39c7hmxpdld6q87v2cg83qenskjhcfk", 
    "authenticity_validator": "agent1qgmnuepkgp32s58lhn97ry4hudt886rfr7q46phhxuv2h9suzs5tclapg7a",
    "trading_legacy": "agent1qt37y2uv5gaujj90d3v0hf0dw2kvdeq9r6uauc244jc7d9uq5cw7xex2s38"
}

# Test identity
TESTER_IDENTITY = Identity.from_seed("test_marketplace_2024", 0)
print(f"🧪 Enhanced Tester Identity: {TESTER_IDENTITY.address}")

async def test_enhanced_agent_communication():
    """Test enhanced agent communication with chat protocol"""
    
    print("🚀 Starting Enhanced Memory Marketplace Communication Tests")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Enhanced Marketplace Coordinator
    print("\n📋 Test 1: Enhanced Marketplace Coordinator")
    result = await test_marketplace_coordinator_enhanced()
    test_results.append(("Enhanced Marketplace Coordinator", result))
    
    # Test 2: Enhanced Memory Appraiser
    print("\n📋 Test 2: Enhanced MeTTa Memory Appraiser") 
    result = await test_memory_appraiser_enhanced()
    test_results.append(("Enhanced Memory Appraiser", result))
    
    # Test 3: Enhanced Authenticity Validator
    print("\n📋 Test 3: Enhanced Multi-Agent Authenticity Validator")
    result = await test_authenticity_validator_enhanced()
    test_results.append(("Enhanced Authenticity Validator", result))
    
    # Test 4: Enhanced Trading & Legacy Agent
    print("\n📋 Test 4: Enhanced Trading & Legacy Agent")
    result = await test_trading_legacy_enhanced()
    test_results.append(("Enhanced Trading & Legacy", result))
    
    # Test 5: Chat Protocol Direct Communication
    print("\n📋 Test 5: Direct Chat Protocol Communication")
    result = await test_chat_protocol_direct()
    test_results.append(("Chat Protocol Direct", result))
    
    # Test 6: Multi-Agent Orchestration
    print("\n📋 Test 6: Enhanced Multi-Agent Orchestration")
    result = await test_multi_agent_orchestration()
    test_results.append(("Multi-Agent Orchestration", result))
    
    # Results Summary
    print("\n" + "=" * 60)
    print("🎯 ENHANCED COMMUNICATION TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Summary: {passed}/{len(test_results)} tests passed")
    print(f"🌟 Chat Protocol Success Rate: {(passed/len(test_results))*100:.1f}%")

async def test_marketplace_coordinator_enhanced():
    """Test enhanced marketplace coordinator with chat protocol"""
    try:
        print("  💬 Testing enhanced marketplace query...")
        
        payload = {
            "type": "chat_message",
            "data": {
                "message": "hello",
                "protocol_version": "2.0",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        result = send_message_to_agent(
            sender=TESTER_IDENTITY,
            target=AGENT_ADDRESSES["marketplace_coordinator"],
            payload=payload
        )
        
        print(f"  📤 Enhanced message sent: {result.status}")
        await asyncio.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Enhanced coordinator test failed: {e}")
        return False

async def test_memory_appraiser_enhanced():
    """Test enhanced memory appraiser with MeTTa AI"""
    try:
        print("  🧠 Testing enhanced MeTTa valuation...")
        
        payload = {
            "memory_content": "My first day of school - I was nervous but excited to meet new friends",
            "memory_type": "childhood_experience",
            "emotional_intensity": 8,
            "protocol_version": "2.0",
            "enhancement_features": ["metta_reasoning", "emotional_analysis", "rarity_scoring"]
        }
        
        result = send_message_to_agent(
            sender=TESTER_IDENTITY,
            target=AGENT_ADDRESSES["memory_appraiser"],
            payload=payload
        )
        
        print(f"  📤 Enhanced MeTTa analysis sent: {result.status}")
        await asyncio.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Enhanced appraiser test failed: {e}")
        return False

async def test_authenticity_validator_enhanced():
    """Test enhanced authenticity validator with multi-agent consensus"""
    try:
        print("  🔐 Testing enhanced multi-agent authenticity validation...")
        
        payload = {
            "memory_content": "The day I graduated from university - walking across the stage with my family watching proudly",
            "memory_id": "test_memory_graduation_001",
            "validation_type": "premium",
            "consensus_requirements": {
                "minimum_validators": 4,
                "consensus_threshold": 0.75,
                "protocol_version": "2.0"
            }
        }
        
        result = send_message_to_agent(
            sender=TESTER_IDENTITY,
            target=AGENT_ADDRESSES["authenticity_validator"],
            payload=payload
        )
        
        print(f"  📤 Enhanced multi-agent validation sent: {result.status}")
        await asyncio.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Enhanced validator test failed: {e}")
        return False

async def test_trading_legacy_enhanced():
    """Test enhanced trading & legacy agent"""
    try:
        print("  💼 Testing enhanced trading operations...")
        
        payload = {
            "action": "create_market_listing",
            "memory_details": {
                "content": "Summer vacation at the beach with family",
                "asking_price": 250.0,
                "memory_type": "family_moment"
            },
            "enhanced_features": {
                "smart_pricing": True,
                "auto_promotion": True,
                "protocol_version": "2.0"
            }
        }
        
        result = send_message_to_agent(
            sender=TESTER_IDENTITY,
            target=AGENT_ADDRESSES["trading_legacy"],
            payload=payload
        )
        
        print(f"  📤 Enhanced trading request sent: {result.status}")
        await asyncio.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Enhanced trading test failed: {e}")
        return False

async def test_chat_protocol_direct():
    """Test direct chat protocol communication"""
    try:
        print("  💭 Testing direct chat protocol features...")
        
        # Test with marketplace coordinator
        chat_payload = {
            "type": "chat_message",
            "data": {
                "message": "status",
                "chat_protocol": {
                    "version": "2.0",
                    "features": ["acknowledgments", "metadata", "sessions"],
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        }
        
        result = send_message_to_agent(
            sender=TESTER_IDENTITY,
            target=AGENT_ADDRESSES["marketplace_coordinator"],
            payload=chat_payload
        )
        
        print(f"  📤 Chat protocol message sent: {result.status}")
        await asyncio.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Chat protocol test failed: {e}")
        return False

async def test_multi_agent_orchestration():
    """Test multi-agent orchestration with chat protocol"""
    try:
        print("  🎭 Testing enhanced multi-agent orchestration...")
        
        # Simulate a complex workflow involving multiple agents
        workflow_payload = {
            "workflow_type": "complete_nft_creation",
            "memory_data": {
                "content": "The moment I held my first child",
                "type": "family_moment",
                "emotional_intensity": 10
            },
            "orchestration": {
                "steps": ["valuation", "authenticity", "listing"],
                "protocol_version": "2.0",
                "enhanced_features": True
            }
        }
        
        # Send to coordinator for orchestration
        result = send_message_to_agent(
            sender=TESTER_IDENTITY,
            target=AGENT_ADDRESSES["marketplace_coordinator"],
            payload=workflow_payload
        )
        
        print(f"  📤 Multi-agent orchestration sent: {result.status}")
        await asyncio.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Multi-agent orchestration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🌟 Enhanced Memory NFT Marketplace - Chat Protocol Tests")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    asyncio.run(test_enhanced_agent_communication())
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Enhanced communication testing complete!")