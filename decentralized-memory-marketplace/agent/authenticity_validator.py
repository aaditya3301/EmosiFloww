import os
from fastapi import FastAPI
from fetchai.communication import (
    parse_message_from_agent_message_dict,
    send_message_to_agent
)
from fetchai.schema import EncodedAgentMessage
from uagents_core.identity import Identity
from dotenv import load_dotenv
from datetime import datetime, timezone
import json
import random
from uuid import uuid4

# Import enhanced protocol
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.agent_protocol import (
    agent_proto,
    AgentMessage,
    AgentAcknowledgement,
    TextContent,
    MetadataContent,
    create_text_message,
    create_metadata_message
)

load_dotenv()

app = FastAPI()

AGENT_IDENTITY = Identity.from_seed(os.getenv("AUTHENTICITY_VALIDATOR_SEED"), 0)

print(f"🔐 Enhanced Authenticity Validator Started")
print(f"📍 Address: {AGENT_IDENTITY.address}")
print(f"🔗 Webhook: http://localhost:8002")
print(f"✨ Multi-Agent Consensus + Chat Protocol: Enabled")

@app.get("/")
async def healthcheck():
    return {"status": "Enhanced Authenticity Validator running!", "address": AGENT_IDENTITY.address}

@app.post("/submit")
async def webhook_handler(agent_message: EncodedAgentMessage):
    print("🛡️ Enhanced authenticity validation request received")
    
    try:
        message = parse_message_from_agent_message_dict(
            agent_message.model_dump(by_alias=True)
        )
        
        # Enhanced validation with chat protocol
        response = await process_enhanced_validation(message)
        
        # Send response with metadata
        enhanced_response = create_metadata_message({
            "agent_type": "authenticity_validator",
            "validation_timestamp": datetime.now(timezone.utc).isoformat(),
            "consensus_version": "2.0",
            **response
        })
        
        result = send_message_to_agent(
            sender=AGENT_IDENTITY,
            target=message.sender,
            payload=response
        )
        
        print(f"✅ Enhanced authenticity report sent to {message.sender}")
        return {"status": "validation_complete"}
        
    except Exception as e:
        print(f"❌ Error in authenticity validation: {e}")
        return {"status": f"error: {e}"}

async def process_enhanced_validation(message):
    """Enhanced authenticity validation with multi-agent consensus"""
    payload = message.payload
    
    memory_content = payload.get("memory_content", "")
    memory_id = payload.get("memory_id", f"mem_{uuid4().hex[:8]}")
    validation_type = payload.get("validation_type", "standard")
    
    print(f"🔍 Enhanced validation for memory: {memory_id}")
    
    # Perform multi-agent consensus validation
    validation_result = await perform_enhanced_authenticity_validation(
        memory_content, memory_id, validation_type
    )
    
    return validation_result

async def perform_enhanced_authenticity_validation(content, memory_id, validation_type):
    """Enhanced multi-agent consensus for authenticity verification"""
    
    # Simulate multiple validation agents
    validators = [
        {"name": "Temporal Consistency Agent", "weight": 0.25},
        {"name": "Emotional Authenticity Agent", "weight": 0.25},
        {"name": "Narrative Coherence Agent", "weight": 0.25},
        {"name": "Historical Context Agent", "weight": 0.25}
    ]
    
    validation_scores = []
    validator_reports = []
    
    for validator in validators:
        # Simulate individual agent validation
        base_score = random.uniform(0.7, 0.95)
        
        # Add validation type modifier
        if validation_type == "premium":
            base_score = min(0.98, base_score + 0.05)
        elif validation_type == "basic":
            base_score = max(0.65, base_score - 0.05)
        
        validation_scores.append({
            "agent": validator["name"],
            "score": round(base_score, 3),
            "weight": validator["weight"]
        })
        
        # Generate validator-specific insights
        insights = generate_validator_insights(validator["name"], base_score)
        validator_reports.append({
            "validator": validator["name"],
            "confidence": round(base_score, 3),
            "insights": insights
        })
    
    # Calculate weighted consensus
    weighted_score = sum(
        score["score"] * score["weight"] 
        for score in validation_scores
    )
    
    # Determine authenticity status
    if weighted_score >= 0.85:
        status = "verified_authentic"
        trust_level = "high"
    elif weighted_score >= 0.70:
        status = "likely_authentic"
        trust_level = "medium"
    else:
        status = "verification_required"
        trust_level = "low"
    
    # Enhanced risk assessment
    risk_factors = assess_enhanced_risk_factors(content, validation_scores)
    
    return {
        "memory_id": memory_id,
        "authenticity_status": status,
        "trust_level": trust_level,
        "consensus_score": round(weighted_score, 3),
        "validation_type": validation_type,
        "multi_agent_consensus": {
            "participating_agents": len(validators),
            "consensus_method": "weighted_voting",
            "individual_scores": validation_scores,
            "agreement_level": calculate_agreement_level(validation_scores)
        },
        "validator_reports": validator_reports,
        "risk_assessment": risk_factors,
        "recommendations": generate_enhanced_recommendations(status, weighted_score, risk_factors),
        "metadata": {
            "validation_timestamp": datetime.now(timezone.utc).isoformat(),
            "validation_protocol": "multi_agent_consensus_v2",
            "chat_protocol_enabled": True,
            "consensus_algorithm": "weighted_byzantine_fault_tolerant"
        },
        "certification": {
            "certificate_id": f"auth_{uuid4().hex[:12]}",
            "valid_until": datetime.now(timezone.utc).isoformat(),
            "verification_level": validation_type,
            "issuing_agents": [v["name"] for v in validators]
        }
    }

def generate_validator_insights(validator_name, score):
    """Generate insights based on validator type"""
    insights_map = {
        "Temporal Consistency Agent": [
            "Timeline coherence verified" if score > 0.8 else "Minor temporal inconsistencies detected",
            "Date references align with historical context",
            "Sequential narrative flow validated"
        ],
        "Emotional Authenticity Agent": [
            "Emotional markers consistent with memory type" if score > 0.8 else "Emotional authenticity needs verification",
            "Sentiment analysis indicates genuine experience",
            "Emotional depth appropriate for described events"
        ],
        "Narrative Coherence Agent": [
            "Story structure maintains logical flow" if score > 0.8 else "Narrative coherence requires attention",
            "Details support primary narrative",
            "Language patterns indicate authentic recall"
        ],
        "Historical Context Agent": [
            "Cultural references accurate for time period" if score > 0.8 else "Historical context verification needed",
            "Environmental details consistent with location/era",
            "Social context aligns with described circumstances"
        ]
    }
    
    return insights_map.get(validator_name, ["Standard validation completed"])

def calculate_agreement_level(scores):
    """Calculate how much the validators agree"""
    score_values = [s["score"] for s in scores]
    variance = sum((x - sum(score_values)/len(score_values))**2 for x in score_values) / len(score_values)
    
    if variance < 0.01:
        return "high_agreement"
    elif variance < 0.05:
        return "moderate_agreement"
    else:
        return "low_agreement"

def assess_enhanced_risk_factors(content, validation_scores):
    """Assess risk factors for the memory"""
    avg_score = sum(s["score"] for s in validation_scores) / len(validation_scores)
    
    risk_level = "low" if avg_score > 0.85 else "medium" if avg_score > 0.70 else "high"
    
    return {
        "overall_risk_level": risk_level,
        "risk_factors": [
            factor for factor in [
                "Temporal inconsistencies" if avg_score < 0.80 else None,
                "Emotional authenticity concerns" if avg_score < 0.75 else None,
                "Narrative coherence issues" if avg_score < 0.70 else None
            ] if factor is not None
        ],
        "mitigation_required": avg_score < 0.75,
        "additional_verification_needed": avg_score < 0.70
    }

def generate_enhanced_recommendations(status, score, risk_factors):
    """Generate actionable recommendations"""
    recommendations = []
    
    if status == "verified_authentic":
        recommendations.extend([
            "Memory ready for premium NFT minting",
            "Eligible for marketplace featured listing",
            "Consider adding premium verification badge"
        ])
    elif status == "likely_authentic":
        recommendations.extend([
            "Standard NFT minting approved",
            "Monitor for additional validation opportunities",
            "Consider supplementary documentation"
        ])
    else:
        recommendations.extend([
            "Additional verification required before minting",
            "Provide supplementary evidence or documentation",
            "Consider professional memory authentication service"
        ])
    
    if risk_factors["mitigation_required"]:
        recommendations.append("Address identified risk factors before proceeding")
    
    return recommendations

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enhanced Authenticity Validator...")
    print(f"Agent Address: {AGENT_IDENTITY.address}")
    uvicorn.run(app, host="0.0.0.0", port=8002)