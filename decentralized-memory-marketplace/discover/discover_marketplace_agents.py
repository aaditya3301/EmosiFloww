from fetchai import fetch

def discover_marketplace_agents():
    
    print("🔍 Searching for Memory NFT Marketplace Agents")
    print("=" * 50)
    
    search_queries = [
        "memory nft marketplace",
        "memory appraiser",
        "memory valuation",
        "nft marketplace coordinator",
        "metta reasoning"
    ]
    
    found_agents = []
    
    for query in search_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 30)
        
        try:
            result = fetch.ai(query, limit=5)
            agents = result.get('ais', [])
            
            if agents:
                print(f"Found {len(agents)} agents:")
                
                for i, agent in enumerate(agents, 1):
                    name = agent.get('name', 'Unknown')
                    address = agent.get('address', 'N/A')
                    
                    if any(keyword in name.lower() for keyword in ['memory', 'marketplace', 'appraiser']):
                        found_agents.append({
                            'name': name,
                            'address': address,
                            'query': query
                        })
                        print(f"🎯 FOUND: {name}")
                        print(f"   Address: {address}")
                    else:
                        print(f"   {i}. {name} ({address[:20]}...)")
            else:
                print("No agents found")
                
        except Exception as e:
            print(f"❌ Search error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 MARKETPLACE AGENTS DISCOVERED:")
    
    if found_agents:
        for agent in found_agents:
            print(f"✅ {agent['name']} - {agent['address']}")
    else:
        print("❌ No marketplace agents found yet")
        print("💡 Agents may need time to propagate in search")

if __name__ == "__main__":
    discover_marketplace_agents()