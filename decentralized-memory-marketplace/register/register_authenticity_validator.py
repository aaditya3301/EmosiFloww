import os
from uagents_core.identity import Identity
from fetchai.registration import register_with_agentverse
from dotenv import load_dotenv

load_dotenv()

def register_authenticity_validator():
    
    agentverse_key = os.getenv("AGENTVERSE_API_KEY")
    agent_identity = Identity.from_seed(os.getenv("AUTHENTICITY_VALIDATOR_SEED"), 0)
    
    name = "Memory NFT Authenticity Validator"
    readme = """<description>
AI-powered authenticity verification specialist for memory NFTs. Uses multi-agent consensus to detect synthetic content and verify genuine memories with high accuracy.
</description>

<use_cases>
    <use_case>Verify authenticity of memory NFTs using multi-agent consensus</use_case>
    <use_case>Detect deepfake and synthetic memory content</use_case>
    <use_case>Analyze metadata consistency for fraud prevention</use_case>
    <use_case>Generate confidence scores for memory authenticity</use_case>
</use_cases>

<payload_requirements>
<description>Send authenticity verification requests with memory data</description>
<payload>
    <requirement>
        <parameter>type</parameter>
        <description>Request type: authenticity_check</description>
    </requirement>
    <requirement>
        <parameter>data</parameter>
        <description>Memory data including ID, metadata, and quality metrics for verification</description>
    </requirement>
</payload>
</payload_requirements>"""
    
    webhook_url = "http://localhost:8002/submit"
    
    print(f"🚀 Registering Authenticity Validator...")
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
        print("✅ Authenticity Validator registered!")
        print(f"Address: {agent_identity.address}")
    else:
        print("❌ Registration failed")
    
    return success

if __name__ == "__main__":
    register_authenticity_validator()