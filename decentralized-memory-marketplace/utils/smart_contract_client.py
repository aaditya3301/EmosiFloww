import os
import json
from datetime import datetime, timezone
from typing import Dict, Optional, List
import hashlib

class SmartContractClient:
    def __init__(self):
        self.contract_address = "0x742d35Cc6642C53532A8E2c70B6A2E8a5c5c5c5c"
        self.network = "ethereum_testnet"
        self.nft_storage = {}
        self.transaction_history = []
        
    async def mint_memory_nft(self, memory_data: Dict) -> Dict:
        """Mint a new memory NFT"""
        
        memory_hash = hashlib.sha256(
            json.dumps(memory_data, sort_keys=True).encode()
        ).hexdigest()
        
        token_id = len(self.nft_storage) + 1
        
        nft_metadata = {
            "token_id": token_id,
            "creator": memory_data.get("creator_address"),
            "memory_hash": memory_hash,
            "unlock_timestamp": memory_data.get("unlock_timestamp"),
            "creation_timestamp": int(datetime.now(timezone.utc).timestamp()),
            "is_listed": False,
            "price": 0,
            "authenticity": "pending",
            "valuation_score": 0,
            "metadata_uri": f"ipfs://memory-capsule/{token_id}"
        }
        
        self.nft_storage[token_id] = nft_metadata
        
        transaction = {
            "tx_hash": f"0x{hashlib.sha256(str(token_id).encode()).hexdigest()}",
            "type": "mint",
            "token_id": token_id,
            "from_address": "0x0000000000000000000000000000000000000000",
            "to_address": memory_data.get("creator_address"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gas_used": 150000,
            "gas_price": "20000000000"
        }
        
        self.transaction_history.append(transaction)
        
        return {
            "success": True,
            "token_id": token_id,
            "transaction_hash": transaction["tx_hash"],
            "contract_address": self.contract_address,
            "metadata": nft_metadata
        }
    
    async def list_memory_for_sale(self, token_id: int, price: float, seller_address: str) -> Dict:
        """List memory NFT for sale"""
        
        if token_id not in self.nft_storage:
            return {"success": False, "error": "NFT not found"}
        
        nft = self.nft_storage[token_id]
        
        if nft["creator"] != seller_address:
            return {"success": False, "error": "Not the owner"}
        
        nft["is_listed"] = True
        nft["price"] = price
        
        transaction = {
            "tx_hash": f"0x{hashlib.sha256(f'list_{token_id}_{price}'.encode()).hexdigest()}",
            "type": "list",
            "token_id": token_id,
            "price": price,
            "seller": seller_address,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.transaction_history.append(transaction)
        
        return {
            "success": True,
            "transaction_hash": transaction["tx_hash"],
            "listing_id": f"listing_{token_id}",
            "price": price
        }
    
    async def purchase_memory_nft(self, token_id: int, buyer_address: str, payment_amount: float) -> Dict:
        """Purchase a listed memory NFT"""
        
        if token_id not in self.nft_storage:
            return {"success": False, "error": "NFT not found"}
        
        nft = self.nft_storage[token_id]
        
        if not nft["is_listed"]:
            return {"success": False, "error": "NFT not listed for sale"}
        
        if payment_amount < nft["price"]:
            return {"success": False, "error": "Insufficient payment"}
        
        seller = nft["creator"]
        platform_fee = nft["price"] * 0.025
        seller_amount = nft["price"] - platform_fee
        
        nft["creator"] = buyer_address
        nft["is_listed"] = False
        nft["price"] = 0
        
        transaction = {
            "tx_hash": f"0x{hashlib.sha256(f'purchase_{token_id}_{buyer_address}'.encode()).hexdigest()}",
            "type": "purchase",
            "token_id": token_id,
            "from_address": seller,
            "to_address": buyer_address,
            "price": nft["price"],
            "platform_fee": platform_fee,
            "seller_amount": seller_amount,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.transaction_history.append(transaction)
        
        return {
            "success": True,
            "transaction_hash": transaction["tx_hash"],
            "new_owner": buyer_address,
            "seller_received": seller_amount,
            "platform_fee": platform_fee
        }
    
    async def verify_authenticity(self, token_id: int, authenticity_data: Dict) -> Dict:
        """Update NFT with authenticity verification"""
        
        if token_id not in self.nft_storage:
            return {"success": False, "error": "NFT not found"}
        
        nft = self.nft_storage[token_id]
        nft["authenticity"] = authenticity_data.get("status", "verified")
        nft["valuation_score"] = authenticity_data.get("score", 0)
        nft["authenticity_details"] = authenticity_data
        
        transaction = {
            "tx_hash": f"0x{hashlib.sha256(f'verify_{token_id}'.encode()).hexdigest()}",
            "type": "authenticity_verification",
            "token_id": token_id,
            "authenticity_status": nft["authenticity"],
            "score": nft["valuation_score"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.transaction_history.append(transaction)
        
        return {
            "success": True,
            "transaction_hash": transaction["tx_hash"],
            "authenticity_status": nft["authenticity"],
            "verification_score": nft["valuation_score"]
        }
    
    async def get_nft_metadata(self, token_id: int) -> Optional[Dict]:
        """Get NFT metadata"""
        return self.nft_storage.get(token_id)
    
    async def get_listed_memories(self) -> List[Dict]:
        """Get all listed memories for sale"""
        listed = []
        for token_id, nft in self.nft_storage.items():
            if nft["is_listed"]:
                listed.append({
                    "token_id": token_id,
                    "price": nft["price"],
                    "creator": nft["creator"],
                    "authenticity": nft["authenticity"],
                    "valuation_score": nft["valuation_score"],
                    "unlock_timestamp": nft["unlock_timestamp"]
                })
        return listed
    
    async def get_user_collection(self, user_address: str) -> List[Dict]:
        """Get all NFTs owned by a user"""
        collection = []
        for token_id, nft in self.nft_storage.items():
            if nft["creator"] == user_address:
                collection.append({
                    "token_id": token_id,
                    "memory_hash": nft["memory_hash"],
                    "creation_timestamp": nft["creation_timestamp"],
                    "unlock_timestamp": nft["unlock_timestamp"],
                    "is_listed": nft["is_listed"],
                    "price": nft["price"],
                    "authenticity": nft["authenticity"],
                    "valuation_score": nft["valuation_score"]
                })
        return collection
    
    async def is_memory_unlocked(self, token_id: int) -> bool:
        """Check if memory is unlocked"""
        if token_id not in self.nft_storage:
            return False
        
        nft = self.nft_storage[token_id]
        current_time = int(datetime.now(timezone.utc).timestamp())
        return current_time >= nft["unlock_timestamp"]
    
    async def get_transaction_history(self, limit: int = 100) -> List[Dict]:
        """Get recent transaction history"""
        return self.transaction_history[-limit:] if len(self.transaction_history) > limit else self.transaction_history
    
    async def get_marketplace_stats(self) -> Dict:
        """Get marketplace statistics"""
        total_nfts = len(self.nft_storage)
        listed_count = sum(1 for nft in self.nft_storage.values() if nft["is_listed"])
        
        total_volume = sum(
            tx.get("price", 0) for tx in self.transaction_history 
            if tx["type"] == "purchase"
        )
        
        avg_price = 0
        purchase_txs = [tx for tx in self.transaction_history if tx["type"] == "purchase"]
        if purchase_txs:
            avg_price = sum(tx["price"] for tx in purchase_txs) / len(purchase_txs)
        
        return {
            "total_nfts_minted": total_nfts,
            "active_listings": listed_count,
            "total_trading_volume": total_volume,
            "average_price": avg_price,
            "total_transactions": len(self.transaction_history),
            "verified_authentic": sum(
                1 for nft in self.nft_storage.values() 
                if nft["authenticity"] == "verified"
            )
        }

smart_contract_client = SmartContractClient()