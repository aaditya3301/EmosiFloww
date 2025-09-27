import os
from uagents_core.identity import Identity
from fetchai.registration import register_with_agentverse
from dotenv import load_dotenv

load_dotenv()

def register_trading_legacy_agent():
    
    agentverse_key = os.getenv("AGENTVERSE_API_KEY")
    agent_identity = Identity.from_seed("trading_legacy_agent_seed", 0)
    
    name = "Memory NFT Trading & Legacy Manager"
    readme = """<description>
Combined trading and estate management agent for Memory NFTs. Provides market making, liquidity, price discovery, and digital inheritance services in one powerful agent.
</description>

<use_cases>
    <use_case>Create and manage Memory NFT trading listings with optimal pricing</use_case>
    <use_case>Provide market liquidity and automated price discovery</use_case>
    <use_case>Plan digital memory estates with smart contract execution</use_case>
    <use_case>Process inheritance transfers and beneficiary management</use_case>
    <use_case>Generate market analysis and legacy planning insights</use_case>
</use_cases>

<payload_requirements>
<description>Send trading or legacy management requests</description>
<payload>
    <requirement>
        <parameter>type</parameter>
        <description>Request type: create_listing, price_discovery, estate_planning, or inheritance_transfer</description>
    </requirement>
    <requirement>
        <parameter>data</parameter>
        <description>Request data including memory details, trading parameters, or estate information</description>
    </requirement>
</payload>
</payload_requirements>"""
    
    webhook_url = "http://localhost:8005/submit"
    
    print(f"🚀 Registering Trading & Legacy Agent...")
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
        print("✅ Trading & Legacy Agent registered!")
        print(f"Address: {agent_identity.address}")
    else:
        print("❌ Registration failed")
    
    return success

if __name__ == "__main__":
    register_trading_legacy_agent()