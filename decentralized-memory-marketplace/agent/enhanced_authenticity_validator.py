"""
Day 2 Afternoon Enhanced Authenticity Validator Agent
Multi-agent consensus system, Deepfake detection, Metadata verification, Emotional congruence analysis
"""
import asyncio
import logging
from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
from typing import Dict, Any, Optional, List
import json
from datetime import datetime, timezone
from dataclasses import asdict

# Import our custom models and utilities
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.message_models import (
    AgentMessage, 
    AgentAcknowledgement,
    AuthenticityRequest,
    AuthenticityResult
)
from utils.asi_one_client import ASIOneClient
from utils.authenticity_verification import (
    perform_comprehensive_authenticity_check,
    AuthenticityLevel,
    ConsensusDecision
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedAuthenticityAnalysis:
    """Day 2 Afternoon Enhanced Authenticity Analysis"""
    
    def __init__(self):
        self.asi_client = ASIOneClient()
        
    async def perform_comprehensive_authenticity_analysis(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive Day 2 Afternoon authenticity analysis"""
        try:
            logger.info("🔍 Starting comprehensive authenticity analysis")
            
            # Perform comprehensive authenticity check
            assessment = await perform_comprehensive_authenticity_check(memory_data)
            
            # Use ASI:One for natural language explanation
            explanation_prompt = f"""
            Analyze this memory authenticity assessment and provide a clear explanation:
            
            Memory: {memory_data.get('content', '')[:200]}...
            Authenticity Level: {assessment.authenticity_level.value}
            Overall Confidence: {assessment.overall_confidence:.2f}
            
            Deepfake Analysis:
            - AI Generated Probability: {assessment.deepfake_analysis.ai_generated_probability:.2f}
            - Suspicious Patterns: {', '.join(assessment.deepfake_analysis.suspicious_patterns)}
            
            Multi-Agent Consensus:
            - Decision: {assessment.consensus_result.consensus_decision.value}
            - Agreement: {assessment.consensus_result.agreement_percentage:.1f}%
            
            Risk Factors: {', '.join(assessment.risk_factors)}
            
            Provide a clear, professional explanation of the authenticity assessment.
            """
            
            asi_response = await self.asi_client.analyze_with_context(explanation_prompt)
            
            # Compile comprehensive results
            analysis_result = {
                "authenticity_assessment": {
                    "authenticity_level": assessment.authenticity_level.value,
                    "overall_confidence": assessment.overall_confidence,
                    "verification_timestamp": assessment.verification_timestamp.isoformat()
                },
                "deepfake_detection": {
                    "is_deepfake": assessment.deepfake_analysis.is_deepfake,
                    "ai_generated_probability": assessment.deepfake_analysis.ai_generated_probability,
                    "confidence_score": assessment.deepfake_analysis.confidence_score,
                    "detection_method": assessment.deepfake_analysis.detection_method,
                    "suspicious_patterns": assessment.deepfake_analysis.suspicious_patterns,
                    "technical_indicators": assessment.deepfake_analysis.technical_indicators
                },
                "metadata_verification": {
                    "timestamp_authentic": assessment.metadata_verification.timestamp_authentic,
                    "location_consistent": assessment.metadata_verification.location_consistent,
                    "device_fingerprint_valid": assessment.metadata_verification.device_fingerprint_valid,
                    "metadata_tampering_detected": assessment.metadata_verification.metadata_tampering_detected,
                    "file_integrity_score": assessment.metadata_verification.file_integrity_score,
                    "verification_details": assessment.metadata_verification.verification_details
                },
                "emotional_congruence": {
                    "overall_congruence": assessment.emotional_congruence.overall_congruence,
                    "emotional_consistency": assessment.emotional_congruence.emotional_consistency,
                    "sentiment_alignment": assessment.emotional_congruence.sentiment_alignment,
                    "contextual_appropriateness": assessment.emotional_congruence.contextual_appropriateness,
                    "psychological_plausibility": assessment.emotional_congruence.psychological_plausibility,
                    "narrative_coherence": assessment.emotional_congruence.narrative_coherence,
                    "temporal_consistency": assessment.emotional_congruence.temporal_consistency
                },
                "multi_agent_consensus": {
                    "consensus_decision": assessment.consensus_result.consensus_decision.value,
                    "confidence_level": assessment.consensus_result.confidence_level,
                    "participating_agents": assessment.consensus_result.participating_agents,
                    "individual_scores": assessment.consensus_result.individual_scores,
                    "agreement_percentage": assessment.consensus_result.agreement_percentage,
                    "outlier_agents": assessment.consensus_result.outlier_agents,
                    "consensus_reasoning": assessment.consensus_result.consensus_reasoning
                },
                "risk_assessment": {
                    "risk_factors": assessment.risk_factors,
                    "recommendations": assessment.recommendations,
                    "requires_human_review": len(assessment.risk_factors) > 2 or assessment.overall_confidence < 0.6
                },
                "asi_explanation": {
                    "natural_language_summary": asi_response.get("content", "Analysis complete"),
                    "token_usage": asi_response.get("token_usage", 0)
                }
            }
            
            logger.info(f"✅ Comprehensive authenticity analysis complete: {assessment.authenticity_level.value}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Error in authenticity analysis: {str(e)}")
            return {
                "error": str(e),
                "authenticity_level": "error",
                "confidence": 0.0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

# Create the Authenticity Validator Agent
authenticity_validator = Agent(
    name="authenticity_validator",
    seed="authenticity_validator_day2_afternoon_seed_12345",
    port=8004,
    endpoint=["http://localhost:8004/submit"]
)

# Fund the agent
fund_agent_if_low(authenticity_validator.wallet.address())

# Initialize the enhanced analysis system
authenticity_analysis = AdvancedAuthenticityAnalysis()

# Create the enhanced chat protocol
authenticity_protocol = Protocol("Day2Afternoon-AuthenticityValidator-v2.0")

@authenticity_protocol.on_message(model=AgentMessage)
async def handle_authenticity_request(ctx: Context, sender: str, msg: AgentMessage):
    """Handle authenticity validation requests with Day 2 Afternoon features"""
    logger.info(f"🛡️ Day 2 Afternoon Authenticity request from {sender}")
    logger.info(f"📝 Request type: {msg.message_type}")
    
    try:
        if msg.message_type == "authenticity_request":
            # Extract memory data from the message
            memory_data = msg.content
            
            logger.info(f"🔍 Analyzing memory: {memory_data.get('memory_id', 'unknown')}")
            logger.info(f"📊 Features: Multi-agent consensus, Deepfake detection, Metadata verification, Emotional congruence")
            
            # Perform comprehensive authenticity analysis
            analysis_result = await authenticity_analysis.perform_comprehensive_authenticity_analysis(memory_data)
            
            # Create comprehensive response
            response = AgentMessage(
                message_type="authenticity_result",
                sender_id=ctx.agent.address,
                receiver_id=sender,
                content={
                    "memory_id": memory_data.get("memory_id"),
                    "authenticity_analysis": analysis_result,
                    "day2_afternoon_features": {
                        "multi_agent_consensus": "✅ Active",
                        "deepfake_detection": "✅ Active", 
                        "metadata_verification": "✅ Active",
                        "emotional_congruence_analysis": "✅ Active"
                    },
                    "processing_summary": {
                        "authenticity_level": analysis_result.get("authenticity_assessment", {}).get("authenticity_level", "unknown"),
                        "confidence": analysis_result.get("authenticity_assessment", {}).get("overall_confidence", 0.0),
                        "deepfake_detected": analysis_result.get("deepfake_detection", {}).get("is_deepfake", False),
                        "consensus_decision": analysis_result.get("multi_agent_consensus", {}).get("consensus_decision", "unknown"),
                        "risk_factors_count": len(analysis_result.get("risk_assessment", {}).get("risk_factors", [])),
                        "requires_human_review": analysis_result.get("risk_assessment", {}).get("requires_human_review", False)
                    }
                },
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
            await ctx.send(sender, response)
            
            # Log comprehensive results
            logger.info(f"🎯 Analysis Results:")
            logger.info(f"   🛡️ Authenticity: {analysis_result.get('authenticity_assessment', {}).get('authenticity_level', 'unknown')}")
            logger.info(f"   🎰 Confidence: {analysis_result.get('authenticity_assessment', {}).get('overall_confidence', 0.0):.3f}")
            logger.info(f"   🤖 AI Generated: {analysis_result.get('deepfake_detection', {}).get('ai_generated_probability', 0.0):.3f}")
            logger.info(f"   🗳️ Consensus: {analysis_result.get('multi_agent_consensus', {}).get('consensus_decision', 'unknown')}")
            logger.info(f"   📊 Agreement: {analysis_result.get('multi_agent_consensus', {}).get('agreement_percentage', 0.0):.1f}%")
            logger.info(f"   ⚠️ Risk Factors: {len(analysis_result.get('risk_assessment', {}).get('risk_factors', []))}")
            logger.info(f"   👤 Human Review: {analysis_result.get('risk_assessment', {}).get('requires_human_review', False)}")
            
        else:
            # Send acknowledgment for other message types
            ack = AgentAcknowledgement(
                message_id=msg.timestamp,
                sender_id=ctx.agent.address,
                receiver_id=sender,
                status="received",
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            await ctx.send(sender, ack)
            logger.info(f"📨 Sent acknowledgment for {msg.message_type}")
            
    except Exception as e:
        logger.error(f"❌ Error processing authenticity request: {str(e)}")
        
        # Send error response
        error_response = AgentMessage(
            message_type="authenticity_error",
            sender_id=ctx.agent.address,
            receiver_id=sender,
            content={
                "error": str(e),
                "memory_id": msg.content.get("memory_id") if hasattr(msg.content, 'get') else "unknown",
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        await ctx.send(sender, error_response)

# Include the protocol
authenticity_validator.include(authenticity_protocol)

@authenticity_validator.on_event("startup")
async def startup_event(ctx: Context):
    """Startup event handler"""
    logger.info("🚀 Day 2 Afternoon Enhanced Authenticity Validator Agent Started!")
    logger.info(f"🔗 Agent Address: {ctx.agent.address}")
    logger.info("🛡️ Advanced Features Enabled:")
    logger.info("   ✅ Multi-agent consensus system")
    logger.info("   ✅ Deepfake detection integration") 
    logger.info("   ✅ Metadata verification")
    logger.info("   ✅ Emotional congruence analysis")
    logger.info("   ✅ ASI:One natural language processing")
    logger.info("   ✅ Risk assessment and recommendations")

@authenticity_validator.on_event("shutdown")
async def shutdown_event(ctx: Context):
    """Shutdown event handler"""
    logger.info("🔒 Day 2 Afternoon Authenticity Validator Agent shutting down...")

if __name__ == "__main__":
    logger.info("🎯 Starting Day 2 Afternoon Enhanced Authenticity Validator Agent...")
    authenticity_validator.run()