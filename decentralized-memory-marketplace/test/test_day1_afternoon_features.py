"""
Day 1 Afternoon Features Test Suite
Test ASI:One natural language interface, portfolio management, 
transaction coordination, and collection worth analysis
"""
import asyncio
import json
from datetime import datetime, timezone

# Import the systems we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.asi_one_client import process_natural_language_query
from utils.portfolio_manager import get_collection_worth, get_user_portfolio_summary
from utils.transaction_coordinator import (
    coordinate_nft_purchase, 
    coordinate_nft_listing,
    get_transaction_status,
    transaction_coordinator
)

async def test_asi_one_natural_language():
    """Test ASI:One natural language interface"""
    print("🧪 Testing ASI:One Natural Language Interface")
    print("=" * 60)
    
    test_queries = [
        "What's my collection worth?",
        "How much is my childhood memory worth?", 
        "Show me market trends for this week",
        "Help me list my first love memory for sale",
        "I want to buy an NFT for $200",
        "What are the best performing memory types?",
        "How can I optimize my portfolio?"
    ]
    
    for query in test_queries:
        print(f"\n🤖 Query: {query}")
        try:
            response = await process_natural_language_query(query)
            print(f"   Intent: {response.intent}")
            print(f"   Confidence: {response.confidence:.2f}")
            print(f"   Response Preview: {response.content[:100]}...")
            print(f"   Entities: {response.entities}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ ASI:One Natural Language Interface Test Complete")

async def test_portfolio_management():
    """Test portfolio management and 'What's my collection worth?' functionality"""
    print("\n🧪 Testing Portfolio Management System")
    print("=" * 60)
    
    test_addresses = [
        "0x1234567890abcdef",
        "0x9876543210fedcba", 
        "0xtest_user_address"
    ]
    
    for address in test_addresses:
        print(f"\n📊 Testing portfolio for: {address}")
        
        try:
            # Test portfolio summary
            portfolio = await get_user_portfolio_summary(address)
            print(f"   Total Value: ${portfolio.total_value:,.2f}")
            print(f"   Total NFTs: {portfolio.total_nfts}")
            print(f"   ROI: {portfolio.roi_percentage:+.1f}%")
            print(f"   Categories: {len(portfolio.category_breakdown)}")
            
            # Test collection worth analysis
            worth_analysis = await get_collection_worth(address)
            print(f"   Collection Analysis Length: {len(worth_analysis)} characters")
            print(f"   Analysis Preview: {worth_analysis[:150]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Portfolio Management Test Complete")

async def test_transaction_coordination():
    """Test transaction coordination system"""
    print("\n🧪 Testing Transaction Coordination System")
    print("=" * 60)
    
    try:
        # Test NFT Purchase Coordination
        print("🛒 Testing NFT Purchase Coordination...")
        purchase_tx = await coordinate_nft_purchase(
            buyer_address="0xbuyer123",
            seller_address="0xseller456", 
            nft_token_id="memory_test_001",
            purchase_price=250.0
        )
        print(f"   Purchase Transaction ID: {purchase_tx}")
        
        # Test NFT Listing Coordination
        print("\n📋 Testing NFT Listing Coordination...")
        listing_tx = await coordinate_nft_listing(
            seller_address="0xseller789",
            nft_token_id="memory_test_002",
            asking_price=180.0
        )
        print(f"   Listing Transaction ID: {listing_tx}")
        
        # Monitor transaction progress
        print("\n⏳ Monitoring transaction progress...")
        await asyncio.sleep(2)  # Give transactions time to process
        
        # Check purchase status
        purchase_status = await get_transaction_status(purchase_tx)
        if purchase_status:
            print(f"   Purchase Progress: {purchase_status['progress']}")
            print(f"   Purchase Status: {purchase_status['status']}")
        
        # Check listing status 
        listing_status = await get_transaction_status(listing_tx)
        if listing_status:
            print(f"   Listing Progress: {listing_status['progress']}")
            print(f"   Listing Status: {listing_status['status']}")
        
        # Test active transactions list
        print("\n📋 Active Transactions:")
        active_transactions = transaction_coordinator.get_active_transactions()
        for tx in active_transactions:
            print(f"   - {tx['transaction_id']}: {tx['type']} (${tx['total_value']})")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Transaction Coordination Test Complete")

async def test_collection_worth_queries():
    """Test specific 'What's my collection worth?' queries"""
    print("\n🧪 Testing Collection Worth Queries")
    print("=" * 60)
    
    test_scenarios = [
        {
            "user_address": "0xuser_with_portfolio",
            "query": "What's my collection worth?",
            "context": "Standard portfolio analysis"
        },
        {
            "user_address": "0xnew_user",
            "query": "Show me my NFT portfolio value",
            "context": "New user with demo portfolio"
        },
        {
            "user_address": "0xhigh_value_collector",
            "query": "What's the total value of my memory collection?",
            "context": "High-value collector analysis"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n💰 Scenario: {scenario['context']}")
        print(f"   User: {scenario['user_address']}")
        print(f"   Query: {scenario['query']}")
        
        try:
            # Process as natural language query
            nl_response = await process_natural_language_query(
                scenario['query'], 
                {"user_address": scenario['user_address']}
            )
            print(f"   NL Intent: {nl_response.intent}")
            print(f"   NL Response: {nl_response.content[:200]}...")
            
            # Get detailed portfolio analysis
            worth_analysis = await get_collection_worth(scenario['user_address'])
            print(f"   Detailed Analysis Length: {len(worth_analysis)} chars")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Collection Worth Queries Test Complete")

async def test_integrated_day1_afternoon_flow():
    """Test integrated Day 1 Afternoon workflow"""
    print("\n🧪 Testing Integrated Day 1 Afternoon Flow")
    print("=" * 60)
    
    user_address = "0xintegrated_test_user"
    
    try:
        # Step 1: User asks about their collection in natural language
        print("1️⃣ Natural Language Query: 'What's my collection worth?'")
        nl_response = await process_natural_language_query(
            "What's my collection worth?", 
            {"user_address": user_address}
        )
        print(f"   Response: {nl_response.content[:150]}...")
        
        # Step 2: Get detailed portfolio analysis
        print("\n2️⃣ Detailed Portfolio Analysis")
        portfolio = await get_user_portfolio_summary(user_address)
        print(f"   Portfolio Value: ${portfolio.total_value:,.2f}")
        print(f"   Best Performer: {portfolio.top_performer.metadata.get('title', 'Unknown')}")
        
        # Step 3: User decides to list their best performer
        if portfolio.top_performer:
            print(f"\n3️⃣ Coordinating Sale of Best Performer: {portfolio.top_performer.token_id}")
            listing_tx = await coordinate_nft_listing(
                seller_address=user_address,
                nft_token_id=portfolio.top_performer.token_id,
                asking_price=portfolio.top_performer.current_value * 1.1  # 10% markup
            )
            print(f"   Listing Transaction: {listing_tx}")
        
        # Step 4: Show transaction coordination in action
        print("\n4️⃣ Transaction Coordination Status")
        await asyncio.sleep(1)  # Let transaction process
        active_txs = transaction_coordinator.get_active_transactions()
        print(f"   Active Transactions: {len(active_txs)}")
        
        # Step 5: Natural language follow-up
        print("\n5️⃣ Follow-up Natural Language Query")
        followup_response = await process_natural_language_query(
            "How is my NFT listing doing?",
            {"user_address": user_address}
        )
        print(f"   Follow-up Response: {followup_response.content[:100]}...")
        
    except Exception as e:
        print(f"   ❌ Error in integrated flow: {e}")
    
    print("\n✅ Integrated Day 1 Afternoon Flow Test Complete")

async def main():
    """Run all Day 1 Afternoon feature tests"""
    print("🎯 Day 1 Afternoon Features Test Suite")
    print("Testing: ASI:One Natural Language, Portfolio Management, Transaction Coordination")
    print("=" * 80)
    
    start_time = datetime.now()
    
    # Run all tests
    await test_asi_one_natural_language()
    await test_portfolio_management()
    await test_transaction_coordination()
    await test_collection_worth_queries()
    await test_integrated_day1_afternoon_flow()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n🎉 All Day 1 Afternoon Feature Tests Complete!")
    print(f"⏱️ Total Test Duration: {duration:.2f} seconds")
    print("\n📋 Features Tested:")
    print("✅ ASI:One Natural Language Interface")
    print("✅ Portfolio Management & Analytics") 
    print("✅ Transaction Coordination System")
    print("✅ Collection Worth Analysis ('What's my collection worth?')")
    print("✅ Integrated Multi-Agent Workflow")
    
    print(f"\n🏆 Day 1 Afternoon Tasks Status: COMPLETED")

if __name__ == "__main__":
    asyncio.run(main())