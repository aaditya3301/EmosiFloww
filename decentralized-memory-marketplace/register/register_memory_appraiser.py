import os
from uagents_core.identity import Identity
from fetchai.registration import register_with_agentverse
from dotenv import load_dotenv

load_dotenv()

def register_memory_appraiser():
    
    agentverse_key = os.getenv("AGENTVERSE_API_KEY")
    agent_identity = Identity.from_seed(os.getenv("MEMORY_APPRAISER_SEED"), 0)
    
    name = "Memory NFT Appraiser - MeTTa Powered"
    readme = """<description>
AI-powered memory valuation specialist using MeTTa reasoning for intelligent NFT pricing. Analyzes rarity, emotional value, and market demand for memory collections.
</description>

<use_cases>
    <use_case>Get precise memory NFT valuations using MeTTa AI reasoning</use_case>
    <use_case>Analyze rarity and emotional impact of digital memories</use_case>
    <use_case>Assess market demand for specific memory types</use_case>
    <use_case>Generate detailed valuation reports with confidence scores</use_case>
</use_cases>

<payload_requirements>
<description>Send memory valuation requests with content details</description>
<payload>
    <requirement>
        <parameter>type</parameter>
        <description>Request type: memory_valuation</description>
    </requirement>
    <requirement>
        <parameter>data</parameter>
        <description>Memory data including ID, content type, quality metrics, and metadata</description>
    </requirement>
</payload>
</payload_requirements>"""
    
    webhook_url = "http://localhost:8001/submit"
    
    print(f"🚀 Registering Memory Appraiser...")
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
        print("✅ Memory Appraiser registered!")
        print(f"Address: {agent_identity.address}")
    else:
        print("❌ Registration failed")
    
    return success

if __name__ == "__main__":
    register_memory_appraiser()