from datetime import datetime
from uuid import uuid4
import os
import asyncio
import logging
from dotenv import load_dotenv

from uagents import Context, Protocol, Agent, Bureau
from uagents.network import get_agent_address
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Import our 4 specialized agents
from agents.marketplace_coordinator import MarketplaceCoordinator
from agents.memory_appraiser import MemoryAppraiser  
from agents.authenticity_validator import AuthenticityValidator
from agents.trading_legacy_agent import TradingLegacyAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmosiFlowwAgentOrchestrator:
    
    def __init__(self):
        self.bureau = Bureau()
        self.agents = {}
        self.initialize_agents()
    
    def initialize_agents(self):
        
        logger.info("🚀 Initializing EmosiFloww ASI Alliance Agents...")
        
        try:
            marketplace_agent = MarketplaceCoordinator(
                name="EmosiFloww-Marketplace-Coordinator",
                seed=os.getenv("MARKETPLACE_COORDINATOR_SEED", "marketplace_coordinator_seed_123"),
                port=8001,
                mailbox=True
            )
            self.bureau.add(marketplace_agent.agent)
            self.agents['marketplace_coordinator'] = marketplace_agent
            logger.info("✅ Marketplace Coordinator initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Marketplace Coordinator: {e}")
        
        # Initialize Memory Appraiser
        try:
            memory_agent = MemoryAppraiser(
                name="EmosiFloww-Memory-Appraiser",
                seed=os.getenv("MEMORY_APPRAISER_SEED", "memory_appraiser_seed_456"),
                port=8002,
                mailbox=True
            )
            self.bureau.add(memory_agent.agent)
            self.agents['memory_appraiser'] = memory_agent
            logger.info("✅ Memory Appraiser initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Memory Appraiser: {e}")
        
        # Initialize Authenticity Validator
        try:
            auth_agent = AuthenticityValidator(
                name="EmosiFloww-Authenticity-Validator",
                seed=os.getenv("AUTHENTICITY_VALIDATOR_SEED", "authenticity_validator_seed_789"),
                port=8003,
                mailbox=True
            )
            self.bureau.add(auth_agent.agent)
            self.agents['authenticity_validator'] = auth_agent
            logger.info("✅ Authenticity Validator initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Authenticity Validator: {e}")
        
        # Initialize Trading Legacy Agent
        try:
            legacy_agent = TradingLegacyAgent(
                name="EmosiFloww-Trading-Legacy",
                seed=os.getenv("TRADING_LEGACY_SEED", "trading_legacy_seed_888"),
                port=8004,
                mailbox=True
            )
            self.bureau.add(legacy_agent.agent)
            self.agents['trading_legacy'] = legacy_agent
            logger.info("✅ Trading Legacy Agent initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Trading Legacy Agent: {e}")
        
        logger.info(f"🎯 Successfully initialized {len(self.agents)}/4 agents")
        
        # Print agent addresses for Agentverse discovery
        for agent_name, agent_obj in self.agents.items():
            logger.info(f"🔗 {agent_name}: {agent_obj.agent.address}")
    
    def run(self):
        logger.info("🔄 Starting EmosiFloww Agent Bureau...")
        logger.info("🏆 ASI Alliance Hackathon - Human-AI Interaction Excellence")
        logger.info("📍 All agents registered with mailbox=True for ASI:One discovery")
        
        if len(self.agents) == 0:
            logger.error("❌ No agents initialized! Check your environment configuration.")
            return
        
        # Run the bureau (this will start all agents concurrently)
        self.bureau.run()

# Create and run the orchestrator
if __name__ == "__main__":
    logger.info("🎯 EmosiFloww ASI Alliance Agents - Multi-Agent System")
    logger.info("🚀 Deploying to Agentverse via Render Background Worker")
    
    orchestrator = EmosiFlowwAgentOrchestrator()
    orchestrator.run()