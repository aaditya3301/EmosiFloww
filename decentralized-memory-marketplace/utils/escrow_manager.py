"""
Advanced Escrow Manager
Handles secure transactions, atomic swaps, and escrow releases for the memory marketplace
"""
import os
import json
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import hashlib

class EscrowStatus(Enum):
    CREATED = "created"
    FUNDED = "funded"
    VERIFIED = "verified"
    RELEASED = "released"
    REFUNDED = "refunded"
    DISPUTED = "disputed"
    EXPIRED = "expired"

@dataclass
class EscrowAgreement:
    """Escrow agreement between buyer and seller"""
    escrow_id: str
    buyer_address: str
    seller_address: str
    nft_token_id: str
    escrow_amount: float
    platform_fee: float
    seller_fee: float
    status: EscrowStatus
    created_at: str
    expires_at: str
    funded_amount: float = 0.0
    verification_hash: Optional[str] = None
    dispute_reason: Optional[str] = None
    released_at: Optional[str] = None
    transaction_hash: Optional[str] = None

class AdvancedEscrowManager:
    """Advanced escrow management for secure NFT transactions"""
    
    def __init__(self):
        self.active_escrows: Dict[str, EscrowAgreement] = {}
        self.escrow_history: List[EscrowAgreement] = []
        self.platform_fee_rate = 0.025  # 2.5%
        self.seller_fee_rate = 0.005    # 0.5% 
        self.escrow_duration_hours = 24  # 24 hour default
        self.data_file = "escrow_data.json"
        self._load_escrow_data()
    
    def _load_escrow_data(self):
        """Load escrow data from storage"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                    for escrow_data in data.get('active_escrows', []):
                        escrow_data['status'] = EscrowStatus(escrow_data['status'])
                        escrow = EscrowAgreement(**escrow_data)
                        self.active_escrows[escrow.escrow_id] = escrow
                    
                    for escrow_data in data.get('escrow_history', []):
                        escrow_data['status'] = EscrowStatus(escrow_data['status'])
                        escrow = EscrowAgreement(**escrow_data)
                        self.escrow_history.append(escrow)
                        
                print(f"📂 Loaded {len(self.active_escrows)} active and {len(self.escrow_history)} completed escrows")
            else:
                print("📂 No existing escrow data found")
        except Exception as e:
            print(f"⚠️ Error loading escrow data: {e}")
    
    def _save_escrow_data(self):
        """Save escrow data to storage"""
        try:
            serializable_data = {
                "active_escrows": [],
                "escrow_history": []
            }
            
            # Convert active escrows
            for escrow in self.active_escrows.values():
                escrow_dict = asdict(escrow)
                escrow_dict["status"] = escrow.status.value
                serializable_data["active_escrows"].append(escrow_dict)
            
            # Convert escrow history
            for escrow in self.escrow_history:
                escrow_dict = asdict(escrow)
                escrow_dict["status"] = escrow.status.value
                serializable_data["escrow_history"].append(escrow_dict)
            
            with open(self.data_file, 'w') as f:
                json.dump(serializable_data, f, indent=2, default=str)
            
            print(f"💾 Saved {len(self.active_escrows)} active escrows and {len(self.escrow_history)} completed")
        except Exception as e:
            print(f"❌ Error saving escrow data: {e}")
    
    async def create_escrow_agreement(self, buyer_address: str, seller_address: str, 
                                    nft_token_id: str, purchase_price: float) -> str:
        """Create a new escrow agreement"""
        
        escrow_id = f"escrow_{uuid.uuid4().hex[:8]}"
        current_time = datetime.now(timezone.utc)
        expires_at = current_time + timedelta(hours=self.escrow_duration_hours)
        
        # Calculate fees
        platform_fee = purchase_price * self.platform_fee_rate
        seller_fee = purchase_price * self.seller_fee_rate
        total_escrow_amount = purchase_price + platform_fee + seller_fee
        
        escrow = EscrowAgreement(
            escrow_id=escrow_id,
            buyer_address=buyer_address,
            seller_address=seller_address,
            nft_token_id=nft_token_id,
            escrow_amount=total_escrow_amount,
            platform_fee=platform_fee,
            seller_fee=seller_fee,
            status=EscrowStatus.CREATED,
            created_at=current_time.isoformat(),
            expires_at=expires_at.isoformat(),
            verification_hash=self._generate_verification_hash(escrow_id, buyer_address, seller_address, nft_token_id)
        )
        
        self.active_escrows[escrow_id] = escrow
        self._save_escrow_data()
        
        print(f"🔐 Created escrow agreement: {escrow_id}")
        print(f"   Buyer: {buyer_address}")
        print(f"   Seller: {seller_address}")
        print(f"   NFT: {nft_token_id}")
        print(f"   Amount: ${total_escrow_amount:.2f} (including fees)")
        
        return escrow_id
    
    async def fund_escrow(self, escrow_id: str, funding_amount: float, funder_address: str) -> Dict[str, Any]:
        """Fund an escrow agreement"""
        
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow agreement not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        if escrow.status != EscrowStatus.CREATED:
            return {"success": False, "error": f"Escrow is in {escrow.status.value} status, cannot fund"}
        
        if funder_address != escrow.buyer_address:
            return {"success": False, "error": "Only the buyer can fund the escrow"}
        
        if funding_amount < escrow.escrow_amount:
            return {"success": False, "error": f"Insufficient funding. Required: ${escrow.escrow_amount:.2f}"}
        
        # Update escrow status and funding
        escrow.funded_amount = funding_amount
        escrow.status = EscrowStatus.FUNDED
        escrow.transaction_hash = f"0x{hashlib.sha256(f'{escrow_id}_funding'.encode()).hexdigest()}"
        
        self._save_escrow_data()
        
        print(f"💰 Escrow {escrow_id} funded with ${funding_amount:.2f}")
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "funded_amount": funding_amount,
            "transaction_hash": escrow.transaction_hash,
            "status": escrow.status.value
        }
    
    async def verify_nft_transfer(self, escrow_id: str, nft_transfer_hash: str) -> Dict[str, Any]:
        """Verify that NFT has been transferred to buyer"""
        
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow agreement not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        if escrow.status != EscrowStatus.FUNDED:
            return {"success": False, "error": f"Escrow must be funded before verification. Current status: {escrow.status.value}"}
        
        # In real implementation, would verify on blockchain
        # For now, simulate verification
        if nft_transfer_hash and len(nft_transfer_hash) > 10:
            escrow.status = EscrowStatus.VERIFIED
            escrow.verification_hash = nft_transfer_hash
            self._save_escrow_data()
            
            print(f"✅ NFT transfer verified for escrow {escrow_id}")
            
            # Automatically release escrow after verification
            return await self.release_escrow(escrow_id)
        else:
            return {"success": False, "error": "Invalid NFT transfer hash"}
    
    async def release_escrow(self, escrow_id: str) -> Dict[str, Any]:
        """Release escrow funds to seller and platform"""
        
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow agreement not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        if escrow.status != EscrowStatus.VERIFIED:
            return {"success": False, "error": f"Escrow must be verified before release. Current status: {escrow.status.value}"}
        
        # Calculate distributions
        seller_amount = escrow.escrow_amount - escrow.platform_fee - escrow.seller_fee
        platform_amount = escrow.platform_fee
        network_fee = escrow.seller_fee
        
        # Update escrow status
        escrow.status = EscrowStatus.RELEASED
        escrow.released_at = datetime.now(timezone.utc).isoformat()
        
        # Move to history
        self.escrow_history.append(escrow)
        del self.active_escrows[escrow_id]
        self._save_escrow_data()
        
        print(f"🎉 Escrow {escrow_id} released successfully")
        print(f"   Seller receives: ${seller_amount:.2f}")
        print(f"   Platform fee: ${platform_amount:.2f}")
        print(f"   Network fee: ${network_fee:.2f}")
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "distributions": {
                "seller_address": escrow.seller_address,
                "seller_amount": seller_amount,
                "platform_amount": platform_amount,
                "network_fee": network_fee
            },
            "released_at": escrow.released_at,
            "status": escrow.status.value
        }
    
    async def refund_escrow(self, escrow_id: str, reason: str) -> Dict[str, Any]:
        """Refund escrow to buyer (in case of dispute or cancellation)"""
        
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow agreement not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        if escrow.status not in [EscrowStatus.FUNDED, EscrowStatus.DISPUTED]:
            return {"success": False, "error": f"Cannot refund escrow in {escrow.status.value} status"}
        
        # Update escrow status
        escrow.status = EscrowStatus.REFUNDED
        escrow.dispute_reason = reason
        escrow.released_at = datetime.now(timezone.utc).isoformat()
        
        # Move to history
        self.escrow_history.append(escrow)
        del self.active_escrows[escrow_id]
        self._save_escrow_data()
        
        print(f"↩️ Escrow {escrow_id} refunded to buyer")
        print(f"   Refund amount: ${escrow.funded_amount:.2f}")
        print(f"   Reason: {reason}")
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "refund_amount": escrow.funded_amount,
            "refund_to": escrow.buyer_address,
            "reason": reason,
            "status": escrow.status.value
        }
    
    async def dispute_escrow(self, escrow_id: str, dispute_reason: str, disputer_address: str) -> Dict[str, Any]:
        """Create a dispute for an escrow agreement"""
        
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow agreement not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        if disputer_address not in [escrow.buyer_address, escrow.seller_address]:
            return {"success": False, "error": "Only buyer or seller can dispute"}
        
        if escrow.status not in [EscrowStatus.FUNDED, EscrowStatus.VERIFIED]:
            return {"success": False, "error": f"Cannot dispute escrow in {escrow.status.value} status"}
        
        escrow.status = EscrowStatus.DISPUTED
        escrow.dispute_reason = dispute_reason
        self._save_escrow_data()
        
        print(f"⚠️ Dispute created for escrow {escrow_id}")
        print(f"   Disputer: {disputer_address}")
        print(f"   Reason: {dispute_reason}")
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "dispute_reason": dispute_reason,
            "disputer": disputer_address,
            "status": escrow.status.value
        }
    
    async def check_expired_escrows(self):
        """Check and handle expired escrows"""
        current_time = datetime.now(timezone.utc)
        expired_escrows = []
        
        for escrow_id, escrow in list(self.active_escrows.items()):
            expires_at = datetime.fromisoformat(escrow.expires_at.replace('Z', '+00:00'))
            
            if current_time > expires_at and escrow.status in [EscrowStatus.CREATED, EscrowStatus.FUNDED]:
                escrow.status = EscrowStatus.EXPIRED
                expired_escrows.append(escrow_id)
                
                # If funded, refund automatically
                if escrow.status == EscrowStatus.FUNDED:
                    await self.refund_escrow(escrow_id, "Escrow expired")
        
        return expired_escrows
    
    def _generate_verification_hash(self, escrow_id: str, buyer: str, seller: str, nft_id: str) -> str:
        """Generate verification hash for escrow agreement"""
        data = f"{escrow_id}:{buyer}:{seller}:{nft_id}:{datetime.now(timezone.utc).isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_escrow_status(self, escrow_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of an escrow agreement"""
        
        # Check active escrows
        if escrow_id in self.active_escrows:
            escrow = self.active_escrows[escrow_id]
        else:
            # Check history
            escrow = next((e for e in self.escrow_history if e.escrow_id == escrow_id), None)
        
        if not escrow:
            return None
        
        return {
            "escrow_id": escrow.escrow_id,
            "buyer_address": escrow.buyer_address,
            "seller_address": escrow.seller_address,
            "nft_token_id": escrow.nft_token_id,
            "escrow_amount": escrow.escrow_amount,
            "funded_amount": escrow.funded_amount,
            "status": escrow.status.value,
            "created_at": escrow.created_at,
            "expires_at": escrow.expires_at,
            "released_at": escrow.released_at,
            "fees": {
                "platform_fee": escrow.platform_fee,
                "seller_fee": escrow.seller_fee
            },
            "verification_hash": escrow.verification_hash,
            "dispute_reason": escrow.dispute_reason
        }
    
    def get_active_escrows(self) -> List[Dict[str, Any]]:
        """Get all active escrow agreements"""
        return [
            {
                "escrow_id": escrow.escrow_id,
                "buyer_address": escrow.buyer_address,
                "seller_address": escrow.seller_address,
                "nft_token_id": escrow.nft_token_id,
                "escrow_amount": escrow.escrow_amount,
                "status": escrow.status.value,
                "created_at": escrow.created_at,
                "expires_at": escrow.expires_at
            }
            for escrow in self.active_escrows.values()
        ]

# Global escrow manager instance
escrow_manager = AdvancedEscrowManager()

# Convenience functions
async def create_escrow(buyer_address: str, seller_address: str, nft_token_id: str, purchase_price: float) -> str:
    """Convenience function to create escrow agreement"""
    return await escrow_manager.create_escrow_agreement(buyer_address, seller_address, nft_token_id, purchase_price)

async def get_escrow_status(escrow_id: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get escrow status"""
    return escrow_manager.get_escrow_status(escrow_id)

if __name__ == "__main__":
    # Test the advanced escrow manager
    async def test_escrow():
        manager = AdvancedEscrowManager()
        
        print("🧪 Testing Advanced Escrow Manager")
        
        # Create escrow
        escrow_id = await manager.create_escrow_agreement(
            buyer_address="0xbuyer123",
            seller_address="0xseller456", 
            nft_token_id="memory_001",
            purchase_price=250.0
        )
        
        # Fund escrow
        fund_result = await manager.fund_escrow(escrow_id, 267.5, "0xbuyer123")
        print(f"Funding result: {fund_result}")
        
        # Verify NFT transfer
        verify_result = await manager.verify_nft_transfer(escrow_id, "0xabcdef123456...")
        print(f"Verification result: {verify_result}")
        
        # Check final status
        status = manager.get_escrow_status(escrow_id)
        print(f"Final status: {status}")
    
    asyncio.run(test_escrow())