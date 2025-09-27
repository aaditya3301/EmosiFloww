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

# Import Day 2 Morning advanced features
from utils.advanced_metta_valuation import calculate_advanced_memory_valuation

load_dotenv()

app = FastAPI()

AGENT_IDENTITY = Identity.from_seed(os.getenv("MEMORY_APPRAISER_SEED"), 0)

print(f"💎 Enhanced Memory Appraiser Started - Day 2 Morning Features")
print(f"📍 Address: {AGENT_IDENTITY.address}")
print(f"🔗 Webhook: http://localhost:8001")
print(f"✨ MeTTa AI + Chat Protocol: Enabled")
print(f"🧠 Advanced Rarity Assessment: Online")
print(f"💝 Emotional Value Calculation: Active")
print(f"📈 Market Trend Analysis: Ready")

@app.get("/")
async def healthcheck():
    return {
        "status": "Enhanced Memory Appraiser with Day 2 Morning Features", 
        "address": AGENT_IDENTITY.address,
        "features": [
            "Advanced MeTTa-powered valuation algorithms",
            "Comprehensive rarity assessment systems",
            "Emotional value calculation engine",
            "Real-time market trend analysis",
            "Multi-dimensional memory scoring"
        ],
        "version": "2.1"
    }

@app.post("/submit")
async def webhook_handler(agent_message: EncodedAgentMessage):
    print("🧠 Enhanced MeTTa valuation request received")
    
    try:
        message = parse_message_from_agent_message_dict(
            agent_message.model_dump(by_alias=True)
        )
        
        # Enhanced processing with chat protocol
        response = await process_enhanced_valuation(message)
        
        # Send response with metadata
        enhanced_response = create_metadata_message({
            "agent_type": "memory_appraiser",
            "response_timestamp": datetime.now(timezone.utc).isoformat(),
            "metta_version": "2.0",
            **response
        })
        
        result = send_message_to_agent(
            sender=AGENT_IDENTITY,
            target=message.sender,
            payload=response
        )
        
        print(f"✅ Enhanced MeTTa valuation sent to {message.sender}")
        return {"status": "metta_analysis_complete"}
        
    except Exception as e:
        print(f"❌ Error in MeTTa analysis: {e}")
        return {"status": f"error: {e}"}

async def process_enhanced_valuation(message):
    """Enhanced MeTTa-powered memory valuation with Day 2 Morning features"""
    payload = message.payload
    
    # Extract comprehensive memory data
    memory_data = {
        "memory_id": payload.get("memory_id", f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
        "memory_type": payload.get("memory_type", "generic"),
        "content": payload.get("memory_content", payload.get("content", "")),
        "metadata": {
            "emotional_intensity": payload.get("emotional_intensity", 5),
            "year": payload.get("year", 2020),
            "location": payload.get("location", ""),
            "participants": payload.get("participants", []),
            "context": payload.get("context", ""),
            "life_changing": payload.get("life_changing", False),
            "significance": payload.get("significance", "medium")
        }
    }
    
    print(f"🔬 Day 2 Morning: Advanced MeTTa analyzing: {memory_data['memory_type']}")
    
    # Use advanced MeTTa valuation engine
    advanced_valuation = await calculate_advanced_memory_valuation(memory_data)
    
    # Convert to response format
    response = {
        "memory_id": advanced_valuation.memory_id,
        "memory_type": advanced_valuation.rarity_assessment.memory_type,
        "final_valuation": advanced_valuation.final_valuation,
        "confidence_score": advanced_valuation.confidence_score,
        
        # Day 2 Morning Feature: Rarity Assessment
        "rarity_assessment": {
            "rarity_score": advanced_valuation.rarity_assessment.rarity_score,
            "rarity_category": advanced_valuation.rarity_assessment.rarity_category,
            "temporal_significance": advanced_valuation.rarity_assessment.temporal_significance,
            "cultural_context": advanced_valuation.rarity_assessment.cultural_context,
            "personal_significance": advanced_valuation.rarity_assessment.personal_significance,
            "market_rarity": advanced_valuation.rarity_assessment.market_rarity,
            "uniqueness_factors": advanced_valuation.rarity_assessment.uniqueness_factors
        },
        
        # Day 2 Morning Feature: Emotional Value Calculation
        "emotional_analysis": {
            "emotional_intensity": advanced_valuation.emotional_analysis.emotional_intensity,
            "psychological_impact": advanced_valuation.emotional_analysis.psychological_impact,
            "nostalgic_value": advanced_valuation.emotional_analysis.nostalgic_value,
            "therapeutic_value": advanced_valuation.emotional_analysis.therapeutic_value,
            "social_connection": advanced_valuation.emotional_analysis.social_connection,
            "life_significance": advanced_valuation.emotional_analysis.life_significance,
            "total_emotional_score": advanced_valuation.emotional_analysis.total_emotional_score
        },
        
        # Day 2 Morning Feature: Market Trend Analysis
        "market_analysis": {
            "current_demand": advanced_valuation.market_analysis.current_demand,
            "price_trend": advanced_valuation.market_analysis.price_trend,
            "volume_trend": advanced_valuation.market_analysis.volume_trend,
            "market_sentiment": advanced_valuation.market_analysis.market_sentiment,
            "predicted_growth": advanced_valuation.market_analysis.predicted_growth,
            "seasonal_factors": advanced_valuation.market_analysis.seasonal_factors,
            "demographic_preferences": advanced_valuation.market_analysis.demographic_preferences
        },
        
        # Comprehensive valuation breakdown
        "valuation_breakdown": advanced_valuation.valuation_breakdown,
        "recommendations": advanced_valuation.recommendations,
        
        # Enhanced metadata
        "day2_morning_features": {
            "advanced_rarity_assessment": True,
            "emotional_value_calculation": True,
            "market_trend_analysis": True,
            "metta_powered_algorithms": True
        },
        
        "analysis_timestamp": advanced_valuation.timestamp,
        "metta_version": "2.1-day2-morning",
        "chat_protocol_enabled": True
    }
    
    return response

async def perform_enhanced_metta_valuation(content, memory_type, intensity):
    """Enhanced MeTTa reasoning for memory valuation"""
    
    # Enhanced emotional impact analysis
    emotional_factors = {
        "childhood_experience": {"base": 180, "multiplier": 1.8},
        "first_love": {"base": 220, "multiplier": 2.2},
        "achievement": {"base": 150, "multiplier": 1.5},
        "loss_grief": {"base": 200, "multiplier": 2.0},
        "family_moment": {"base": 160, "multiplier": 1.6},
        "travel_experience": {"base": 130, "multiplier": 1.3},
        "career_milestone": {"base": 140, "multiplier": 1.4},
        "friendship": {"base": 120, "multiplier": 1.2},
        "generic": {"base": 100, "multiplier": 1.0}
    }
    
    # Get memory type factors
    factors = emotional_factors.get(memory_type, emotional_factors["generic"])
    base_value = factors["base"]
    multiplier = factors["multiplier"]
    
    # Enhanced intensity scaling (1-10)
    intensity_modifier = 0.8 + (intensity / 10) * 0.4  # 0.8 to 1.2 range
    
    # MeTTa rarity analysis
    rarity_score = random.uniform(0.6, 1.0)  # Simulated uniqueness
    
    # Market conditions
    market_modifier = random.uniform(0.9, 1.1)
    
    # Final enhanced valuation
    final_value = base_value * multiplier * intensity_modifier * rarity_score * market_modifier
    
    # Enhanced confidence calculation
    confidence = min(0.95, 0.7 + (intensity / 10) * 0.25)
    
    # MeTTa reasoning breakdown
    metta_reasoning = {
        "emotional_resonance": intensity * 0.1,
        "memory_uniqueness": rarity_score,
        "temporal_significance": random.uniform(0.7, 1.0),
        "cultural_relevance": random.uniform(0.6, 0.9),
        "preservation_value": random.uniform(0.8, 1.0)
    }
    
    return {
        "memory_type": memory_type,
        "metta_valuation": round(final_value, 2),
        "confidence_score": round(confidence, 3),
        "emotional_intensity": intensity,
        "rarity_score": round(rarity_score, 3),
        "market_conditions": "favorable" if market_modifier > 1.0 else "stable",
        "metta_reasoning": metta_reasoning,
        "valuation_factors": {
            "base_value": base_value,
            "type_multiplier": multiplier,
            "intensity_modifier": round(intensity_modifier, 3),
            "rarity_impact": round(rarity_score, 3),
            "market_impact": round(market_modifier, 3)
        },
        "recommendations": {
            "listing_price_range": {
                "min": round(final_value * 0.85, 2),
                "max": round(final_value * 1.15, 2)
            },
            "optimal_timing": "immediate" if market_modifier > 1.05 else "monitor_market",
            "enhancement_suggestions": [
                "Add contextual metadata",
                "Include verification documents",
                "Provide emotional narrative"
            ]
        },
        "metta_version": "2.0-enhanced",
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        "chat_protocol_enabled": True
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enhanced Memory Appraiser with Day 2 Morning Features...")
    print(f"Agent Address: {AGENT_IDENTITY.address}")
    print("🧠 Advanced MeTTa Valuation Algorithms: Ready")
    print("🔍 Rarity Assessment Systems: Online") 
    print("💝 Emotional Value Calculation: Active")
    print("📈 Market Trend Analysis: Monitoring")
    uvicorn.run(app, host="0.0.0.0", port=8001)