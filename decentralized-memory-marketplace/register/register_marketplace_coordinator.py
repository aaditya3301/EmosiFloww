import os
from uagents_core.identity import Identity
from fetchai.registration import register_with_agentverse
from dotenv import load_dotenv

load_dotenv()

def register_marketplace_coordinator():
    
    agentverse_key = os.getenv("AGENTVERSE_API_KEY")
    agent_identity = Identity.from_seed(os.getenv("MARKETPLACE_COORDINATOR_SEED"), 0)
    
    name = "Memory NFT Marketplace Coordinator"
    readme = """<description>
Central coordinator for Memory NFT Marketplace. Handles valuation requests, market queries, and NFT listings using multi-agent collaboration and MeTTa reasoning.
</description>

<use_cases>
    <use_case>Request memory NFT valuations with AI-powered pricing</use_case>
    <use_case>Search marketplace for memory collections and rare items</use_case>
    <use_case>List memory NFTs with intelligent market positioning</use_case>
    <use_case>Get market analysis and investment recommendations</use_case>
</use_cases>

<payload_requirements>
<description>Send marketplace requests for memory trading and valuation</description>
<payload>
    <requirement>
        <parameter>type</parameter>
        <description>Request type: valuation_request, market_query, or list_nft</description>
    </requirement>
    <requirement>
        <parameter>data</parameter>
        <description>Request data containing memory details, search parameters, or NFT information</description>
    </requirement>
</payload>
</payload_requirements>"""
    
    webhook_url = "http://localhost:8000/submit"
    
    print(f"🚀 Registering Marketplace Coordinator...")
    print(f"Agent Address: {agent_identity.address}")
    
    success = register_with_agentverse(
        identity=agent_identity,
        url=webhook_url,
        agentverse_token=agentverse_key,
        agent_title=name,
        readme=readme,
        is_public=True,
    )
    
    if success:
        print("✅ Marketplace Coordinator registered!")
        print(f"Address: {agent_identity.address}")
    else:
        print("❌ Registration failed")
    
    return success

if __name__ == "__main__":
    register_marketplace_coordinator()