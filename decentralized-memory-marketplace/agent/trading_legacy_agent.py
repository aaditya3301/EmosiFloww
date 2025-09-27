import os
from fastapi import FastAPI
from fetchai.communication import (
    parse_message_from_agent_message_dict,
    send_message_to_agent
)
from fetchai.schema import EncodedAgentMessage
from uagents_core.identity import Identity
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

AGENT_IDENTITY = Identity.from_seed("trading_legacy_agent_seed", 0)

print(f"Trading & Legacy Agent Address: {AGENT_IDENTITY.address}")
print(f"Webhook: http://localhost:8005")

@app.get("/")
async def healthcheck():
    return {"status": "Trading & Legacy Agent running!", "address": AGENT_IDENTITY.address}

@app.post("/submit")
async def webhook_handler(agent_message: EncodedAgentMessage):
    print("📨 Trading/Legacy request received")
    
    try:
        message = parse_message_from_agent_message_dict(
            agent_message.model_dump(by_alias=True)
        )
        
        request_type = message.payload.get("type", "unknown")
        data = message.payload.get("data", {})
        
        if request_type == "create_listing":
            response = await create_market_listing(data)
        elif request_type == "price_discovery":
            response = await perform_price_discovery(data)
        elif request_type == "estate_planning":
            response = await create_estate_plan(data)
        elif request_type == "inheritance_transfer":
            response = await process_inheritance(data)
        else:
            response = {"status": "I handle NFT trading, market making, and digital legacy management"}
        
        result = send_message_to_agent(
            sender=AGENT_IDENTITY,
            target=message.sender,
            payload=response
        )
        
        return {"status": "processed"}
        
    except Exception as e:
        return {"status": f"error: {e}"}

async def create_market_listing(data):
    memory_id = data.get("memory_id", "unknown")
    asking_price = data.get("asking_price", 100.0)
    
    listing_id = f"market_{memory_id}_{hash(memory_id) % 100000}"
    
    return {
        "type": "market_listing_created", 
        "listing_id": listing_id,
        "memory_id": memory_id,
        "asking_price": asking_price,
        "current_bid": asking_price * 0.85,
        "spread": {"bid": asking_price * 0.98, "ask": asking_price * 1.02},
        "liquidity_score": 0.75,
        "estimated_fill_time": "2-5 hours"
    }

async def perform_price_discovery(data):
    memory_type = data.get("memory_type", "generic")
    base_price = 150.0
    market_sentiment = 1.1
    
    discovered_price = base_price * market_sentiment * 0.8
    
    return {
        "type": "price_discovery_result",
        "memory_type": memory_type,
        "discovered_price": round(discovered_price, 2),
        "market_factors": {"sentiment": market_sentiment, "volatility": 0.15},
        "trading_volume_24h": 2500.0,
        "price_trend": "bullish"
    }

async def create_estate_plan(data):
    owner_id = data.get("owner_id", "unknown")
    collection_value = data.get("collection_value", 1000.0)
    beneficiaries = data.get("beneficiaries", [])
    
    estate_id = f"estate_{owner_id}_{hash(owner_id) % 10000}"
    
    per_beneficiary = collection_value / len(beneficiaries) if beneficiaries else 0
    
    return {
        "type": "estate_plan_created",
        "estate_id": estate_id,
        "owner_id": owner_id,
        "total_value": collection_value,
        "beneficiary_count": len(beneficiaries),
        "per_beneficiary_value": round(per_beneficiary, 2),
        "smart_contract_address": f"0x{hash(estate_id) % (10**40):040x}",
        "execution_conditions": {
            "time_lock": "upon_verification",
            "multi_sig_required": True
        }
    }

async def process_inheritance(data):
    estate_id = data.get("estate_id", "unknown")
    beneficiary_id = data.get("beneficiary_id", "unknown")
    
    transfer_id = f"transfer_{estate_id}_{beneficiary_id}"
    
    return {
        "type": "inheritance_processed",
        "transfer_id": transfer_id,
        "estate_id": estate_id,
        "beneficiary_id": beneficiary_id,
        "status": "approved",
        "transferred_assets": [
            {"type": "childhood_memories", "count": 15, "value": 750.0},
            {"type": "milestone_events", "count": 8, "value": 1200.0}
        ],
        "transfer_fee": 25.0,
        "blockchain_tx": f"0x{hash(transfer_id) % (10**64):064x}"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Trading & Legacy Agent...")
    print(f"Agent Address: {AGENT_IDENTITY.address}")
    uvicorn.run(app, host="0.0.0.0", port=8005)