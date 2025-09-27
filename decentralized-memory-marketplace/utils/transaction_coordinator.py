"""
Transaction Coordination System
Coordinate complex multi-agent transactions, escrow management, and atomic swaps
"""
import os
import json
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

class TransactionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TransactionType(Enum):
    NFT_PURCHASE = "nft_purchase"
    NFT_LISTING = "nft_listing"
    NFT_TRANSFER = "nft_transfer"
    BATCH_OPERATION = "batch_operation"
    ESCROW_RELEASE = "escrow_release"

@dataclass
class TransactionStep:
    """Individual step in a transaction"""
    step_id: str
    agent_address: str
    action: str
    parameters: Dict[str, Any]
    status: TransactionStatus
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    timestamp: Optional[str] = None
    dependencies: List[str] = None  # Other step IDs this depends on
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass 
class Transaction:
    """Complete transaction with multiple coordinated steps"""
    transaction_id: str
    transaction_type: TransactionType
    initiator_address: str
    participants: List[str]  # All agent addresses involved
    steps: List[TransactionStep]
    status: TransactionStatus
    total_value: float
    fees: Dict[str, float]
    metadata: Dict[str, Any]
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None
    
    def get_next_pending_steps(self) -> List[TransactionStep]:
        """Get steps that are ready to execute"""
        ready_steps = []
        completed_step_ids = {step.step_id for step in self.steps if step.status == TransactionStatus.COMPLETED}
        
        for step in self.steps:
            if (step.status == TransactionStatus.PENDING and 
                all(dep_id in completed_step_ids for dep_id in step.dependencies)):
                ready_steps.append(step)
        
        return ready_steps

class TransactionCoordinator:
    """Coordinate complex multi-agent transactions"""
    
    def __init__(self):
        self.active_transactions: Dict[str, Transaction] = {}
        self.transaction_history: List[Transaction] = []
        self.agent_capabilities = {
            "marketplace_coordinator": ["nft_listing", "market_analysis", "coordination"],
            "memory_appraiser": ["valuation", "price_verification", "market_pricing"],
            "authenticity_validator": ["authenticity_check", "fraud_detection", "verification"],
            "trading_legacy_agent": ["trade_execution", "legacy_support", "transaction_processing"]
        }
        self.data_file = "transaction_data.json"
        self._load_transaction_data()
    
    def _load_transaction_data(self):
        """Load transaction history from storage"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Reconstruct transactions from saved data
                    for tx_data in data.get('transactions', []):
                        # Convert string enums back to enum objects
                        tx_data['transaction_type'] = TransactionType(tx_data['transaction_type'])
                        tx_data['status'] = TransactionStatus(tx_data['status'])
                        
                        # Convert step data back to TransactionStep objects with enum conversion
                        steps = []
                        for step_data in tx_data['steps']:
                            step_data['status'] = TransactionStatus(step_data['status'])
                            steps.append(TransactionStep(**step_data))
                        tx_data['steps'] = steps
                        
                        tx = Transaction(**tx_data)
                        if tx.status in [TransactionStatus.PENDING, TransactionStatus.EXECUTING]:
                            self.active_transactions[tx.transaction_id] = tx
                        else:
                            self.transaction_history.append(tx)
                print(f"📂 Loaded {len(self.active_transactions)} active and {len(self.transaction_history)} completed transactions")
            else:
                print("📂 No existing transaction data found")
        except Exception as e:
            print(f"⚠️ Error loading transaction data: {e}")
            # Continue with empty data to avoid blocking startup
    
    def _save_transaction_data(self):
        """Save transaction data to storage"""
        try:
            all_transactions = list(self.active_transactions.values()) + self.transaction_history
            serializable_data = {
                "transactions": []
            }
            
            # Convert transactions to serializable format
            for tx in all_transactions:
                tx_dict = asdict(tx)
                # Convert enums to strings for JSON serialization
                tx_dict["transaction_type"] = tx.transaction_type.value
                tx_dict["status"] = tx.status.value
                
                # Convert step enums to strings
                for step_dict in tx_dict["steps"]:
                    step_dict["status"] = step_dict["status"].value
                
                serializable_data["transactions"].append(tx_dict)
            
            with open(self.data_file, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            print(f"💾 Saved {len(all_transactions)} transactions")
        except Exception as e:
            print(f"❌ Error saving transaction data: {e}")
            # Continue without saving to avoid blocking operations
    
    async def initiate_nft_purchase(self, buyer_address: str, seller_address: str, 
                                   nft_token_id: str, purchase_price: float,
                                   metadata: Dict[str, Any] = None) -> str:
        """Initiate a coordinated NFT purchase transaction"""
        
        transaction_id = f"tx_{uuid.uuid4().hex[:8]}"
        current_time = datetime.now(timezone.utc).isoformat()
        
        # Define transaction steps in order
        steps = [
            TransactionStep(
                step_id=f"{transaction_id}_step_1",
                agent_address="memory_appraiser",
                action="verify_valuation",
                parameters={
                    "nft_token_id": nft_token_id,
                    "offered_price": purchase_price,
                    "market_validation": True
                },
                status=TransactionStatus.PENDING,
                dependencies=[]
            ),
            TransactionStep(
                step_id=f"{transaction_id}_step_2", 
                agent_address="authenticity_validator",
                action="verify_authenticity",
                parameters={
                    "nft_token_id": nft_token_id,
                    "seller_address": seller_address,
                    "comprehensive_check": True
                },
                status=TransactionStatus.PENDING,
                dependencies=[]
            ),
            TransactionStep(
                step_id=f"{transaction_id}_step_3",
                agent_address="trading_legacy_agent", 
                action="setup_escrow",
                parameters={
                    "buyer_address": buyer_address,
                    "seller_address": seller_address,
                    "amount": purchase_price,
                    "nft_token_id": nft_token_id
                },
                status=TransactionStatus.PENDING,
                dependencies=[f"{transaction_id}_step_1", f"{transaction_id}_step_2"]
            ),
            TransactionStep(
                step_id=f"{transaction_id}_step_4",
                agent_address="trading_legacy_agent",
                action="execute_transfer",
                parameters={
                    "from_address": seller_address,
                    "to_address": buyer_address,
                    "nft_token_id": nft_token_id,
                    "payment_amount": purchase_price
                },
                status=TransactionStatus.PENDING,
                dependencies=[f"{transaction_id}_step_3"]
            ),
            TransactionStep(
                step_id=f"{transaction_id}_step_5",
                agent_address="marketplace_coordinator",
                action="finalize_transaction",
                parameters={
                    "transaction_id": transaction_id,
                    "update_market_data": True,
                    "notify_participants": True
                },
                status=TransactionStatus.PENDING,
                dependencies=[f"{transaction_id}_step_4"]
            )
        ]
        
        # Calculate fees
        fees = {
            "marketplace_fee": purchase_price * 0.025,  # 2.5%
            "gas_fee": 15.0,  # Estimated blockchain fees
            "validation_fee": 5.0   # Authenticity + valuation
        }
        
        transaction = Transaction(
            transaction_id=transaction_id,
            transaction_type=TransactionType.NFT_PURCHASE,
            initiator_address=buyer_address,
            participants=[buyer_address, seller_address, "memory_appraiser", 
                         "authenticity_validator", "trading_legacy_agent", "marketplace_coordinator"],
            steps=steps,
            status=TransactionStatus.PENDING,
            total_value=purchase_price,
            fees=fees,
            metadata=metadata or {},
            created_at=current_time,
            updated_at=current_time
        )
        
        self.active_transactions[transaction_id] = transaction
        self._save_transaction_data()
        
        print(f"🚀 Initiated NFT purchase transaction: {transaction_id}")
        print(f"   Buyer: {buyer_address}")
        print(f"   NFT: {nft_token_id}")
        print(f"   Price: ${purchase_price}")
        print(f"   Steps: {len(steps)}")
        
        # Start processing transaction
        asyncio.create_task(self.process_transaction(transaction_id))
        
        return transaction_id
    
    async def initiate_nft_listing(self, seller_address: str, nft_token_id: str, 
                                  asking_price: float, metadata: Dict[str, Any] = None) -> str:
        """Initiate a coordinated NFT listing transaction"""
        
        transaction_id = f"tx_{uuid.uuid4().hex[:8]}"
        current_time = datetime.now(timezone.utc).isoformat()
        
        steps = [
            TransactionStep(
                step_id=f"{transaction_id}_step_1",
                agent_address="authenticity_validator",
                action="verify_ownership",
                parameters={
                    "nft_token_id": nft_token_id,
                    "claimed_owner": seller_address
                },
                status=TransactionStatus.PENDING
            ),
            TransactionStep(
                step_id=f"{transaction_id}_step_2",
                agent_address="memory_appraiser", 
                action="market_valuation",
                parameters={
                    "nft_token_id": nft_token_id,
                    "asking_price": asking_price,
                    "provide_pricing_recommendation": True
                },
                status=TransactionStatus.PENDING
            ),
            TransactionStep(
                step_id=f"{transaction_id}_step_3",
                agent_address="marketplace_coordinator",
                action="create_listing",
                parameters={
                    "seller_address": seller_address,
                    "nft_token_id": nft_token_id,
                    "asking_price": asking_price,
                    "metadata": metadata
                },
                status=TransactionStatus.PENDING,
                dependencies=[f"{transaction_id}_step_1", f"{transaction_id}_step_2"]
            )
        ]
        
        fees = {
            "listing_fee": 5.0,
            "validation_fee": 3.0
        }
        
        transaction = Transaction(
            transaction_id=transaction_id,
            transaction_type=TransactionType.NFT_LISTING,
            initiator_address=seller_address,
            participants=[seller_address, "authenticity_validator", "memory_appraiser", "marketplace_coordinator"],
            steps=steps,
            status=TransactionStatus.PENDING,
            total_value=asking_price,
            fees=fees,
            metadata=metadata or {},
            created_at=current_time,
            updated_at=current_time
        )
        
        self.active_transactions[transaction_id] = transaction
        self._save_transaction_data()
        
        print(f"📋 Initiated NFT listing transaction: {transaction_id}")
        print(f"   Seller: {seller_address}")
        print(f"   NFT: {nft_token_id}")
        print(f"   Asking Price: ${asking_price}")
        
        asyncio.create_task(self.process_transaction(transaction_id))
        return transaction_id
    
    async def process_transaction(self, transaction_id: str):
        """Process transaction steps in coordination with agents"""
        
        if transaction_id not in self.active_transactions:
            print(f"❌ Transaction {transaction_id} not found")
            return
        
        transaction = self.active_transactions[transaction_id]
        transaction.status = TransactionStatus.EXECUTING
        transaction.updated_at = datetime.now(timezone.utc).isoformat()
        
        print(f"⚡ Processing transaction: {transaction_id}")
        
        try:
            while transaction.status == TransactionStatus.EXECUTING:
                # Get next steps ready to execute
                ready_steps = transaction.get_next_pending_steps()
                
                if not ready_steps:
                    # Check if all steps are completed
                    completed_steps = [s for s in transaction.steps if s.status == TransactionStatus.COMPLETED]
                    failed_steps = [s for s in transaction.steps if s.status == TransactionStatus.FAILED]
                    
                    if failed_steps:
                        transaction.status = TransactionStatus.FAILED
                        print(f"❌ Transaction {transaction_id} failed at step: {failed_steps[0].step_id}")
                        break
                    elif len(completed_steps) == len(transaction.steps):
                        transaction.status = TransactionStatus.COMPLETED
                        transaction.completed_at = datetime.now(timezone.utc).isoformat()
                        print(f"✅ Transaction {transaction_id} completed successfully")
                        break
                    else:
                        # Wait for more steps to become ready
                        await asyncio.sleep(1)
                        continue
                
                # Execute ready steps (can be parallel if independent)
                await self.execute_transaction_steps(transaction, ready_steps)
                
                transaction.updated_at = datetime.now(timezone.utc).isoformat()
                self._save_transaction_data()
                
                await asyncio.sleep(0.5)  # Brief pause between step groups
            
            # Move completed transaction to history
            if transaction.status in [TransactionStatus.COMPLETED, TransactionStatus.FAILED]:
                self.transaction_history.append(transaction)
                del self.active_transactions[transaction_id]
                self._save_transaction_data()
        
        except Exception as e:
            print(f"❌ Error processing transaction {transaction_id}: {e}")
            transaction.status = TransactionStatus.FAILED
            transaction.updated_at = datetime.now(timezone.utc).isoformat()
    
    async def execute_transaction_steps(self, transaction: Transaction, steps: List[TransactionStep]):
        """Execute a batch of transaction steps"""
        
        # Execute steps (simulated for demo - in real implementation would call actual agents)
        tasks = []
        for step in steps:
            task = asyncio.create_task(self.simulate_step_execution(step))
            tasks.append(task)
        
        # Wait for all steps to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Update step statuses based on results
        for step, result in zip(steps, results):
            if isinstance(result, Exception):
                step.status = TransactionStatus.FAILED
                step.error_message = str(result)
                print(f"❌ Step {step.step_id} failed: {result}")
            else:
                step.status = TransactionStatus.COMPLETED
                step.result = result
                step.timestamp = datetime.now(timezone.utc).isoformat()
                print(f"✅ Step {step.step_id} completed: {step.action}")
    
    async def simulate_step_execution(self, step: TransactionStep) -> Dict[str, Any]:
        """Simulate step execution (replace with real agent communication)"""
        
        # Simulate processing time
        await asyncio.sleep(0.5 + (hash(step.step_id) % 10) / 10)
        
        # Simulate step results based on action type
        action_results = {
            "verify_valuation": {
                "valuation_confirmed": True,
                "market_price": step.parameters.get("offered_price", 0) * 0.95,
                "confidence": 0.88
            },
            "verify_authenticity": {
                "authenticity_confirmed": True,
                "authenticity_score": 0.92,
                "fraud_risk": "low"
            },
            "setup_escrow": {
                "escrow_address": f"0xescrow_{uuid.uuid4().hex[:8]}",
                "amount_locked": step.parameters.get("amount", 0),
                "status": "locked"
            },
            "execute_transfer": {
                "transaction_hash": f"0x{uuid.uuid4().hex}",
                "nft_transferred": True,
                "payment_transferred": True
            },
            "finalize_transaction": {
                "market_data_updated": True,
                "participants_notified": True,
                "transaction_recorded": True
            },
            "verify_ownership": {
                "ownership_confirmed": True,
                "owner_address": step.parameters.get("claimed_owner"),
                "verification_method": "blockchain_query"
            },
            "market_valuation": {
                "estimated_value": step.parameters.get("asking_price", 0) * 0.92,
                "market_demand": "moderate",
                "pricing_recommendation": "competitive"
            },
            "create_listing": {
                "listing_id": f"listing_{uuid.uuid4().hex[:8]}",
                "listing_created": True,
                "visible_on_marketplace": True
            }
        }
        
        return action_results.get(step.action, {"status": "completed"})
    
    async def get_transaction_status(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a transaction"""
        
        # Check active transactions
        if transaction_id in self.active_transactions:
            tx = self.active_transactions[transaction_id]
        else:
            # Check transaction history
            tx = next((t for t in self.transaction_history if t.transaction_id == transaction_id), None)
        
        if not tx:
            return None
        
        completed_steps = len([s for s in tx.steps if s.status == TransactionStatus.COMPLETED])
        total_steps = len(tx.steps)
        
        return {
            "transaction_id": tx.transaction_id,
            "type": tx.transaction_type.value,
            "status": tx.status.value,
            "progress": f"{completed_steps}/{total_steps}",
            "progress_percentage": (completed_steps / total_steps) * 100,
            "participants": tx.participants,
            "total_value": tx.total_value,
            "fees": tx.fees,
            "created_at": tx.created_at,
            "updated_at": tx.updated_at,
            "completed_at": tx.completed_at,
            "next_steps": [
                {
                    "step_id": step.step_id,
                    "agent": step.agent_address,
                    "action": step.action,
                    "status": step.status.value
                }
                for step in tx.get_next_pending_steps()
            ]
        }
    
    async def cancel_transaction(self, transaction_id: str, reason: str = "User cancelled") -> bool:
        """Cancel a pending transaction"""
        
        if transaction_id not in self.active_transactions:
            return False
        
        transaction = self.active_transactions[transaction_id]
        
        if transaction.status in [TransactionStatus.COMPLETED, TransactionStatus.FAILED]:
            return False  # Cannot cancel completed/failed transactions
        
        transaction.status = TransactionStatus.CANCELLED
        transaction.updated_at = datetime.now(timezone.utc).isoformat()
        transaction.metadata["cancellation_reason"] = reason
        
        # Move to history
        self.transaction_history.append(transaction)
        del self.active_transactions[transaction_id]
        self._save_transaction_data()
        
        print(f"🚫 Transaction {transaction_id} cancelled: {reason}")
        return True
    
    def get_active_transactions(self) -> List[Dict[str, Any]]:
        """Get all active transactions summary"""
        return [
            {
                "transaction_id": tx.transaction_id,
                "type": tx.transaction_type.value,
                "status": tx.status.value,
                "total_value": tx.total_value,
                "created_at": tx.created_at,
                "participants": len(tx.participants)
            }
            for tx in self.active_transactions.values()
        ]

# Global transaction coordinator instance
transaction_coordinator = TransactionCoordinator()

# Convenience functions
async def coordinate_nft_purchase(buyer_address: str, seller_address: str, 
                                nft_token_id: str, purchase_price: float) -> str:
    """Convenience function for NFT purchase coordination"""
    return await transaction_coordinator.initiate_nft_purchase(
        buyer_address, seller_address, nft_token_id, purchase_price
    )

async def coordinate_nft_listing(seller_address: str, nft_token_id: str, asking_price: float) -> str:
    """Convenience function for NFT listing coordination"""
    return await transaction_coordinator.initiate_nft_listing(
        seller_address, nft_token_id, asking_price
    )

async def get_transaction_status(transaction_id: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get transaction status"""
    return await transaction_coordinator.get_transaction_status(transaction_id)

if __name__ == "__main__":
    # Test the transaction coordinator
    async def test_transaction_coordinator():
        coordinator = TransactionCoordinator()
        
        print("🧪 Testing NFT purchase coordination...")
        
        tx_id = await coordinator.initiate_nft_purchase(
            buyer_address="0xbuyer123",
            seller_address="0xseller456",
            nft_token_id="memory_001",
            purchase_price=250.0
        )
        
        print(f"Transaction ID: {tx_id}")
        
        # Monitor transaction progress
        for i in range(10):
            status = await coordinator.get_transaction_status(tx_id)
            if status:
                print(f"Progress: {status['progress']} - Status: {status['status']}")
                if status['status'] in ['completed', 'failed']:
                    break
            await asyncio.sleep(1)
        
        print("🧪 Testing NFT listing coordination...")
        listing_tx = await coordinator.initiate_nft_listing(
            seller_address="0xseller789",
            nft_token_id="memory_002", 
            asking_price=180.0
        )
        
        print(f"Listing Transaction ID: {listing_tx}")
    
    asyncio.run(test_transaction_coordinator())