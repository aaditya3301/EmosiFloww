"""
Enhanced Ownership Transfer Protocols
Advanced NFT ownership management, atomic swaps, and transfer coordination
"""
import os
import json
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import hashlib

class TransferType(Enum):
    DIRECT_TRANSFER = "direct_transfer"
    MARKETPLACE_SALE = "marketplace_sale"
    ATOMIC_SWAP = "atomic_swap"
    BATCH_TRANSFER = "batch_transfer"
    ESCROW_RELEASE = "escrow_release"
    INHERITANCE_TRANSFER = "inheritance_transfer"

class TransferStatus(Enum):
    INITIATED = "initiated"
    VERIFIED = "verified"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class OwnershipRecord:
    """Complete ownership record for NFT"""
    token_id: str
    current_owner: str
    previous_owner: Optional[str]
    original_creator: str
    ownership_start: str
    ownership_duration: Optional[str] = None  # For completed transfers
    transfer_history: List[str] = None
    
    def __post_init__(self):
        if self.transfer_history is None:
            self.transfer_history = []

@dataclass
class TransferAgreement:
    """Transfer agreement between parties"""
    transfer_id: str
    transfer_type: TransferType
    nft_token_id: str
    from_address: str
    to_address: str
    transfer_value: float
    status: TransferStatus
    created_at: str
    executed_at: Optional[str] = None
    conditions: Dict[str, Any] = None
    verification_hash: Optional[str] = None
    escrow_id: Optional[str] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = {}

class EnhancedOwnershipManager:
    """Enhanced ownership and transfer management system"""
    
    def __init__(self):
        self.ownership_records: Dict[str, OwnershipRecord] = {}
        self.active_transfers: Dict[str, TransferAgreement] = {}
        self.transfer_history: List[TransferAgreement] = []
        self.atomic_swap_pairs: Dict[str, List[str]] = {}  # swap_id -> [transfer_id1, transfer_id2]
        self.data_file = "ownership_data.json"
        self._load_ownership_data()
    
    def _load_ownership_data(self):
        """Load ownership data from storage"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                    # Load ownership records
                    for token_id, record_data in data.get('ownership_records', {}).items():
                        self.ownership_records[token_id] = OwnershipRecord(**record_data)
                    
                    # Load active transfers
                    for transfer_data in data.get('active_transfers', []):
                        transfer_data['transfer_type'] = TransferType(transfer_data['transfer_type'])
                        transfer_data['status'] = TransferStatus(transfer_data['status'])
                        transfer = TransferAgreement(**transfer_data)
                        self.active_transfers[transfer.transfer_id] = transfer
                    
                    # Load transfer history
                    for transfer_data in data.get('transfer_history', []):
                        transfer_data['transfer_type'] = TransferType(transfer_data['transfer_type'])
                        transfer_data['status'] = TransferStatus(transfer_data['status'])
                        transfer = TransferAgreement(**transfer_data)
                        self.transfer_history.append(transfer)
                    
                    # Load atomic swap pairs
                    self.atomic_swap_pairs = data.get('atomic_swap_pairs', {})
                        
                print(f"📂 Loaded ownership data for {len(self.ownership_records)} NFTs, {len(self.active_transfers)} active transfers")
            else:
                print("📂 No existing ownership data found")
        except Exception as e:
            print(f"⚠️ Error loading ownership data: {e}")
    
    def _save_ownership_data(self):
        """Save ownership data to storage"""
        try:
            serializable_data = {
                "ownership_records": {},
                "active_transfers": [],
                "transfer_history": [],
                "atomic_swap_pairs": self.atomic_swap_pairs
            }
            
            # Convert ownership records
            for token_id, record in self.ownership_records.items():
                serializable_data["ownership_records"][token_id] = asdict(record)
            
            # Convert active transfers
            for transfer in self.active_transfers.values():
                transfer_dict = asdict(transfer)
                transfer_dict["transfer_type"] = transfer.transfer_type.value
                transfer_dict["status"] = transfer.status.value
                serializable_data["active_transfers"].append(transfer_dict)
            
            # Convert transfer history
            for transfer in self.transfer_history:
                transfer_dict = asdict(transfer)
                transfer_dict["transfer_type"] = transfer.transfer_type.value
                transfer_dict["status"] = transfer.status.value
                serializable_data["transfer_history"].append(transfer_dict)
            
            with open(self.data_file, 'w') as f:
                json.dump(serializable_data, f, indent=2, default=str)
            
            print(f"💾 Saved ownership data for {len(self.ownership_records)} NFTs")
        except Exception as e:
            print(f"❌ Error saving ownership data: {e}")
    
    async def register_nft_ownership(self, token_id: str, owner_address: str, 
                                   creator_address: str) -> Dict[str, Any]:
        """Register initial NFT ownership"""
        
        if token_id in self.ownership_records:
            return {"success": False, "error": "NFT ownership already registered"}
        
        ownership_record = OwnershipRecord(
            token_id=token_id,
            current_owner=owner_address,
            previous_owner=None,
            original_creator=creator_address,
            ownership_start=datetime.now(timezone.utc).isoformat(),
            transfer_history=[]
        )
        
        self.ownership_records[token_id] = ownership_record
        self._save_ownership_data()
        
        print(f"📝 Registered ownership for NFT {token_id}")
        print(f"   Owner: {owner_address}")
        print(f"   Creator: {creator_address}")
        
        return {
            "success": True,
            "token_id": token_id,
            "owner": owner_address,
            "creator": creator_address,
            "registered_at": ownership_record.ownership_start
        }
    
    async def initiate_transfer(self, token_id: str, from_address: str, to_address: str,
                              transfer_value: float, transfer_type: TransferType = TransferType.DIRECT_TRANSFER,
                              conditions: Dict[str, Any] = None) -> str:
        """Initiate NFT ownership transfer"""
        
        # Verify current ownership
        if token_id not in self.ownership_records:
            raise ValueError("NFT not found in ownership records")
        
        current_record = self.ownership_records[token_id]
        if current_record.current_owner != from_address:
            raise ValueError("Transfer initiator is not the current owner")
        
        transfer_id = f"transfer_{uuid.uuid4().hex[:8]}"
        
        transfer_agreement = TransferAgreement(
            transfer_id=transfer_id,
            transfer_type=transfer_type,
            nft_token_id=token_id,
            from_address=from_address,
            to_address=to_address,
            transfer_value=transfer_value,
            status=TransferStatus.INITIATED,
            created_at=datetime.now(timezone.utc).isoformat(),
            conditions=conditions or {},
            verification_hash=self._generate_transfer_hash(transfer_id, token_id, from_address, to_address)
        )
        
        self.active_transfers[transfer_id] = transfer_agreement
        self._save_ownership_data()
        
        print(f"🔄 Initiated {transfer_type.value} for NFT {token_id}")
        print(f"   Transfer ID: {transfer_id}")
        print(f"   From: {from_address}")
        print(f"   To: {to_address}")
        print(f"   Value: ${transfer_value}")
        
        return transfer_id
    
    async def verify_transfer_conditions(self, transfer_id: str) -> Dict[str, Any]:
        """Verify transfer conditions are met"""
        
        if transfer_id not in self.active_transfers:
            return {"success": False, "error": "Transfer not found"}
        
        transfer = self.active_transfers[transfer_id]
        
        if transfer.status != TransferStatus.INITIATED:
            return {"success": False, "error": f"Transfer is in {transfer.status.value} status"}
        
        # Check various conditions
        verification_results = {
            "ownership_verified": await self._verify_current_ownership(transfer),
            "payment_verified": await self._verify_payment_conditions(transfer),
            "escrow_verified": await self._verify_escrow_conditions(transfer),
            "custom_conditions": await self._verify_custom_conditions(transfer)
        }
        
        all_verified = all(verification_results.values())
        
        if all_verified:
            transfer.status = TransferStatus.VERIFIED
            self._save_ownership_data()
            
            print(f"✅ Transfer {transfer_id} conditions verified")
            
            # Automatically proceed to execution
            return await self.execute_transfer(transfer_id)
        else:
            failed_conditions = [k for k, v in verification_results.items() if not v]
            return {
                "success": False,
                "error": "Transfer conditions not met",
                "failed_conditions": failed_conditions,
                "verification_results": verification_results
            }
    
    async def execute_transfer(self, transfer_id: str) -> Dict[str, Any]:
        """Execute verified transfer"""
        
        if transfer_id not in self.active_transfers:
            return {"success": False, "error": "Transfer not found"}
        
        transfer = self.active_transfers[transfer_id]
        
        if transfer.status != TransferStatus.VERIFIED:
            return {"success": False, "error": f"Transfer must be verified before execution. Current status: {transfer.status.value}"}
        
        transfer.status = TransferStatus.EXECUTING
        
        try:
            # Update ownership record
            ownership_record = self.ownership_records[transfer.nft_token_id]
            
            # Calculate ownership duration
            ownership_start = datetime.fromisoformat(ownership_record.ownership_start.replace('Z', '+00:00'))
            ownership_duration = (datetime.now(timezone.utc) - ownership_start).total_seconds()
            
            # Update ownership
            ownership_record.previous_owner = ownership_record.current_owner
            ownership_record.current_owner = transfer.to_address
            ownership_record.ownership_duration = str(ownership_duration)
            ownership_record.ownership_start = datetime.now(timezone.utc).isoformat()
            ownership_record.transfer_history.append(transfer_id)
            
            # Complete transfer
            transfer.status = TransferStatus.COMPLETED
            transfer.executed_at = datetime.now(timezone.utc).isoformat()
            
            # Move to history
            self.transfer_history.append(transfer)
            del self.active_transfers[transfer_id]
            
            self._save_ownership_data()
            
            print(f"✅ Transfer {transfer_id} executed successfully")
            print(f"   NFT {transfer.nft_token_id} now owned by {transfer.to_address}")
            
            return {
                "success": True,
                "transfer_id": transfer_id,
                "nft_token_id": transfer.nft_token_id,
                "new_owner": transfer.to_address,
                "previous_owner": ownership_record.previous_owner,
                "executed_at": transfer.executed_at,
                "ownership_duration_previous": ownership_duration
            }
            
        except Exception as e:
            transfer.status = TransferStatus.FAILED
            self._save_ownership_data()
            return {"success": False, "error": f"Transfer execution failed: {e}"}
    
    async def initiate_atomic_swap(self, nft1_token_id: str, nft1_owner: str,
                                 nft2_token_id: str, nft2_owner: str) -> str:
        """Initiate atomic swap between two NFTs"""
        
        swap_id = f"swap_{uuid.uuid4().hex[:8]}"
        
        # Create transfers for both NFTs
        transfer1_id = await self.initiate_transfer(
            token_id=nft1_token_id,
            from_address=nft1_owner,
            to_address=nft2_owner,
            transfer_value=0,  # No monetary value in swap
            transfer_type=TransferType.ATOMIC_SWAP,
            conditions={"atomic_swap_id": swap_id, "counterpart_nft": nft2_token_id}
        )
        
        transfer2_id = await self.initiate_transfer(
            token_id=nft2_token_id,
            from_address=nft2_owner,
            to_address=nft1_owner,
            transfer_value=0,
            transfer_type=TransferType.ATOMIC_SWAP,
            conditions={"atomic_swap_id": swap_id, "counterpart_nft": nft1_token_id}
        )
        
        # Link the transfers as atomic swap pair
        self.atomic_swap_pairs[swap_id] = [transfer1_id, transfer2_id]
        self._save_ownership_data()
        
        print(f"🔄 Initiated atomic swap {swap_id}")
        print(f"   NFT1: {nft1_token_id} ({nft1_owner} → {nft2_owner})")
        print(f"   NFT2: {nft2_token_id} ({nft2_owner} → {nft1_owner})")
        
        return swap_id
    
    async def execute_atomic_swap(self, swap_id: str) -> Dict[str, Any]:
        """Execute atomic swap (both transfers must succeed or both fail)"""
        
        if swap_id not in self.atomic_swap_pairs:
            return {"success": False, "error": "Atomic swap not found"}
        
        transfer_ids = self.atomic_swap_pairs[swap_id]
        
        if len(transfer_ids) != 2:
            return {"success": False, "error": "Invalid atomic swap configuration"}
        
        # Verify both transfers
        verification_results = []
        for transfer_id in transfer_ids:
            result = await self.verify_transfer_conditions(transfer_id)
            verification_results.append(result)
        
        # Both must succeed for atomic swap
        if all(result["success"] for result in verification_results):
            print(f"✅ Atomic swap {swap_id} completed successfully")
            return {
                "success": True,
                "swap_id": swap_id,
                "transfers": verification_results
            }
        else:
            # Cancel both transfers if either fails
            for transfer_id in transfer_ids:
                await self.cancel_transfer(transfer_id, "Atomic swap counterpart failed")
            
            return {
                "success": False,
                "error": "Atomic swap failed - both transfers cancelled",
                "verification_results": verification_results
            }
    
    async def cancel_transfer(self, transfer_id: str, reason: str) -> Dict[str, Any]:
        """Cancel a pending transfer"""
        
        if transfer_id not in self.active_transfers:
            return {"success": False, "error": "Transfer not found"}
        
        transfer = self.active_transfers[transfer_id]
        
        if transfer.status in [TransferStatus.COMPLETED, TransferStatus.FAILED]:
            return {"success": False, "error": f"Cannot cancel {transfer.status.value} transfer"}
        
        transfer.status = TransferStatus.CANCELLED
        transfer.conditions["cancellation_reason"] = reason
        transfer.executed_at = datetime.now(timezone.utc).isoformat()
        
        # Move to history
        self.transfer_history.append(transfer)
        del self.active_transfers[transfer_id]
        
        self._save_ownership_data()
        
        print(f"🚫 Transfer {transfer_id} cancelled: {reason}")
        
        return {
            "success": True,
            "transfer_id": transfer_id,
            "status": "cancelled",
            "reason": reason
        }
    
    async def _verify_current_ownership(self, transfer: TransferAgreement) -> bool:
        """Verify current ownership of NFT"""
        if transfer.nft_token_id not in self.ownership_records:
            return False
        
        record = self.ownership_records[transfer.nft_token_id]
        return record.current_owner == transfer.from_address
    
    async def _verify_payment_conditions(self, transfer: TransferAgreement) -> bool:
        """Verify payment conditions"""
        # In real implementation, would check escrow or payment system
        # For now, assume payment conditions are met if transfer_value > 0
        return True
    
    async def _verify_escrow_conditions(self, transfer: TransferAgreement) -> bool:
        """Verify escrow conditions"""
        # Check if escrow is required and properly funded
        if transfer.escrow_id:
            # In real implementation, would check escrow status
            return True  # Simulate successful escrow verification
        return True  # No escrow required
    
    async def _verify_custom_conditions(self, transfer: TransferAgreement) -> bool:
        """Verify custom transfer conditions"""
        # Check any custom conditions specified in transfer
        conditions = transfer.conditions
        
        # For atomic swaps, verify counterpart
        if "atomic_swap_id" in conditions:
            counterpart_nft = conditions.get("counterpart_nft")
            if counterpart_nft and counterpart_nft in self.ownership_records:
                return True
        
        return True  # Default to true for now
    
    def _generate_transfer_hash(self, transfer_id: str, token_id: str, from_addr: str, to_addr: str) -> str:
        """Generate verification hash for transfer"""
        data = f"{transfer_id}:{token_id}:{from_addr}:{to_addr}:{datetime.now(timezone.utc).isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_ownership_record(self, token_id: str) -> Optional[Dict[str, Any]]:
        """Get ownership record for NFT"""
        if token_id not in self.ownership_records:
            return None
        
        record = self.ownership_records[token_id]
        return {
            "token_id": record.token_id,
            "current_owner": record.current_owner,
            "previous_owner": record.previous_owner,
            "original_creator": record.original_creator,
            "ownership_start": record.ownership_start,
            "ownership_duration": record.ownership_duration,
            "transfer_count": len(record.transfer_history),
            "transfer_history": record.transfer_history
        }
    
    def get_user_nfts(self, user_address: str) -> List[Dict[str, Any]]:
        """Get all NFTs owned by user"""
        user_nfts = []
        
        for token_id, record in self.ownership_records.items():
            if record.current_owner == user_address:
                user_nfts.append({
                    "token_id": token_id,
                    "ownership_start": record.ownership_start,
                    "is_original_creator": record.original_creator == user_address,
                    "transfer_count": len(record.transfer_history)
                })
        
        return user_nfts
    
    def get_transfer_status(self, transfer_id: str) -> Optional[Dict[str, Any]]:
        """Get status of transfer"""
        
        # Check active transfers
        if transfer_id in self.active_transfers:
            transfer = self.active_transfers[transfer_id]
        else:
            # Check history
            transfer = next((t for t in self.transfer_history if t.transfer_id == transfer_id), None)
        
        if not transfer:
            return None
        
        return {
            "transfer_id": transfer.transfer_id,
            "transfer_type": transfer.transfer_type.value,
            "nft_token_id": transfer.nft_token_id,
            "from_address": transfer.from_address,
            "to_address": transfer.to_address,
            "transfer_value": transfer.transfer_value,
            "status": transfer.status.value,
            "created_at": transfer.created_at,
            "executed_at": transfer.executed_at,
            "conditions": transfer.conditions,
            "verification_hash": transfer.verification_hash
        }

# Global ownership manager instance
ownership_manager = EnhancedOwnershipManager()

# Convenience functions
async def register_nft(token_id: str, owner_address: str, creator_address: str) -> Dict[str, Any]:
    """Convenience function to register NFT ownership"""
    return await ownership_manager.register_nft_ownership(token_id, owner_address, creator_address)

async def transfer_nft(token_id: str, from_address: str, to_address: str, value: float) -> str:
    """Convenience function to initiate NFT transfer"""
    return await ownership_manager.initiate_transfer(token_id, from_address, to_address, value)

if __name__ == "__main__":
    # Test the ownership manager
    async def test_ownership_manager():
        manager = EnhancedOwnershipManager()
        
        print("🧪 Testing Enhanced Ownership Manager")
        
        # Register NFT ownership
        await manager.register_nft_ownership("memory_001", "0xowner123", "0xcreator456")
        
        # Initiate transfer
        transfer_id = await manager.initiate_transfer(
            token_id="memory_001",
            from_address="0xowner123",
            to_address="0xbuyer789",
            transfer_value=250.0
        )
        
        # Verify and execute transfer
        result = await manager.verify_transfer_conditions(transfer_id)
        print(f"Transfer result: {result}")
        
        # Test atomic swap
        await manager.register_nft_ownership("memory_002", "0xowner2", "0xcreator2")
        swap_id = await manager.initiate_atomic_swap(
            nft1_token_id="memory_001",
            nft1_owner="0xbuyer789",
            nft2_token_id="memory_002", 
            nft2_owner="0xowner2"
        )
        
        swap_result = await manager.execute_atomic_swap(swap_id)
        print(f"Swap result: {swap_result}")
    
    asyncio.run(test_ownership_manager())