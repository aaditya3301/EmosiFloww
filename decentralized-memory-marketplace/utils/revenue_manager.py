"""
Revenue Sharing Manager
Advanced revenue distribution system for the memory marketplace
Handles platform fees, creator royalties, agent commissions, and network rewards
"""
import os
import json
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from collections import defaultdict

class RevenueType(Enum):
    PLATFORM_FEE = "platform_fee"
    CREATOR_ROYALTY = "creator_royalty"
    AGENT_COMMISSION = "agent_commission"
    NETWORK_REWARD = "network_reward"
    REFERRAL_BONUS = "referral_bonus"
    VALIDATOR_REWARD = "validator_reward"

@dataclass
class RevenueDistribution:
    """Individual revenue distribution record"""
    distribution_id: str
    transaction_id: str
    revenue_type: RevenueType
    recipient_address: str
    amount: float
    percentage: float
    source_transaction: str
    nft_token_id: Optional[str]
    created_at: str
    processed_at: Optional[str] = None
    status: str = "pending"  # pending, processed, failed

@dataclass
class RevenuePool:
    """Revenue pool for specific time period"""
    pool_id: str
    period_start: str
    period_end: str
    total_revenue: float
    platform_share: float
    agent_share: float
    creator_share: float
    network_share: float
    distributions: List[RevenueDistribution]
    status: str = "active"  # active, closed, distributed

class RevenueManager:
    """Advanced revenue sharing and distribution system"""
    
    def __init__(self):
        # Revenue sharing percentages
        self.revenue_rates = {
            "platform_fee": 0.025,      # 2.5% platform fee
            "creator_royalty": 0.05,    # 5% creator royalties on resales
            "agent_commission": 0.01,   # 1% for participating agents
            "network_reward": 0.005,    # 0.5% for network validators
            "referral_bonus": 0.0025,   # 0.25% for referrals
        }
        
        self.agent_addresses = {
            "marketplace_coordinator": "0xcoordinator123",
            "memory_appraiser": "0xappraiser456", 
            "authenticity_validator": "0xvalidator789",
            "trading_legacy_agent": "0xtrading012"
        }
        
        self.revenue_history: List[RevenueDistribution] = []
        self.revenue_pools: Dict[str, RevenuePool] = {}
        self.pending_distributions: Dict[str, RevenueDistribution] = {}
        self.data_file = "revenue_data.json"
        
        self._load_revenue_data()
    
    def _load_revenue_data(self):
        """Load revenue data from storage"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                    # Load revenue history
                    for dist_data in data.get('revenue_history', []):
                        dist_data['revenue_type'] = RevenueType(dist_data['revenue_type'])
                        distribution = RevenueDistribution(**dist_data)
                        self.revenue_history.append(distribution)
                    
                    # Load pending distributions
                    for dist_data in data.get('pending_distributions', []):
                        dist_data['revenue_type'] = RevenueType(dist_data['revenue_type'])
                        distribution = RevenueDistribution(**dist_data)
                        self.pending_distributions[distribution.distribution_id] = distribution
                        
                print(f"📂 Loaded {len(self.revenue_history)} revenue records and {len(self.pending_distributions)} pending")
            else:
                print("📂 No existing revenue data found")
        except Exception as e:
            print(f"⚠️ Error loading revenue data: {e}")
    
    def _save_revenue_data(self):
        """Save revenue data to storage"""
        try:
            serializable_data = {
                "revenue_history": [],
                "pending_distributions": []
            }
            
            # Convert revenue history
            for distribution in self.revenue_history:
                dist_dict = asdict(distribution)
                dist_dict["revenue_type"] = distribution.revenue_type.value
                serializable_data["revenue_history"].append(dist_dict)
            
            # Convert pending distributions  
            for distribution in self.pending_distributions.values():
                dist_dict = asdict(distribution)
                dist_dict["revenue_type"] = distribution.revenue_type.value
                serializable_data["pending_distributions"].append(dist_dict)
            
            with open(self.data_file, 'w') as f:
                json.dump(serializable_data, f, indent=2, default=str)
            
            print(f"💾 Saved {len(self.revenue_history)} revenue records")
        except Exception as e:
            print(f"❌ Error saving revenue data: {e}")
    
    async def process_nft_sale_revenue(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process revenue distribution for NFT sale"""
        
        transaction_id = transaction_data.get("transaction_id")
        sale_price = transaction_data.get("sale_price", 0)
        seller_address = transaction_data.get("seller_address")
        buyer_address = transaction_data.get("buyer_address")
        nft_token_id = transaction_data.get("nft_token_id")
        creator_address = transaction_data.get("creator_address", seller_address)
        is_resale = transaction_data.get("is_resale", False)
        
        distributions = []
        
        # 1. Platform Fee
        platform_fee = sale_price * self.revenue_rates["platform_fee"]
        platform_dist = await self._create_distribution(
            transaction_id=transaction_id,
            revenue_type=RevenueType.PLATFORM_FEE,
            recipient_address="0xplatform_treasury",
            amount=platform_fee,
            percentage=self.revenue_rates["platform_fee"],
            nft_token_id=nft_token_id
        )
        distributions.append(platform_dist)
        
        # 2. Creator Royalty (only on resales)
        if is_resale and creator_address != seller_address:
            royalty_amount = sale_price * self.revenue_rates["creator_royalty"]
            royalty_dist = await self._create_distribution(
                transaction_id=transaction_id,
                revenue_type=RevenueType.CREATOR_ROYALTY,
                recipient_address=creator_address,
                amount=royalty_amount,
                percentage=self.revenue_rates["creator_royalty"],
                nft_token_id=nft_token_id
            )
            distributions.append(royalty_dist)
        
        # 3. Agent Commissions (distributed among participating agents)
        total_agent_commission = sale_price * self.revenue_rates["agent_commission"]
        agent_commission_each = total_agent_commission / len(self.agent_addresses)
        
        for agent_name, agent_address in self.agent_addresses.items():
            agent_dist = await self._create_distribution(
                transaction_id=transaction_id,
                revenue_type=RevenueType.AGENT_COMMISSION,
                recipient_address=agent_address,
                amount=agent_commission_each,
                percentage=self.revenue_rates["agent_commission"] / len(self.agent_addresses),
                nft_token_id=nft_token_id
            )
            distributions.append(agent_dist)
        
        # 4. Network Validator Rewards
        network_reward = sale_price * self.revenue_rates["network_reward"]
        network_dist = await self._create_distribution(
            transaction_id=transaction_id,
            revenue_type=RevenueType.NETWORK_REWARD,
            recipient_address="0xnetwork_validators",
            amount=network_reward,
            percentage=self.revenue_rates["network_reward"],
            nft_token_id=nft_token_id
        )
        distributions.append(network_dist)
        
        # 5. Referral Bonus (if applicable)
        referrer_address = transaction_data.get("referrer_address")
        if referrer_address:
            referral_bonus = sale_price * self.revenue_rates["referral_bonus"]
            referral_dist = await self._create_distribution(
                transaction_id=transaction_id,
                revenue_type=RevenueType.REFERRAL_BONUS,
                recipient_address=referrer_address,
                amount=referral_bonus,
                percentage=self.revenue_rates["referral_bonus"],
                nft_token_id=nft_token_id
            )
            distributions.append(referral_dist)
        
        # Calculate seller amount after all deductions
        total_fees = sum(dist.amount for dist in distributions)
        seller_amount = sale_price - total_fees
        
        print(f"💰 Revenue distribution for transaction {transaction_id}")
        print(f"   Sale Price: ${sale_price:.2f}")
        print(f"   Total Fees: ${total_fees:.2f} ({(total_fees/sale_price)*100:.2f}%)")
        print(f"   Seller Receives: ${seller_amount:.2f}")
        print(f"   Distributions Created: {len(distributions)}")
        
        # Process all distributions
        for distribution in distributions:
            await self._process_distribution(distribution)
        
        self._save_revenue_data()
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "sale_price": sale_price,
            "seller_amount": seller_amount,
            "total_fees": total_fees,
            "fee_percentage": (total_fees/sale_price)*100,
            "distributions": [
                {
                    "type": dist.revenue_type.value,
                    "recipient": dist.recipient_address,
                    "amount": dist.amount,
                    "percentage": dist.percentage * 100
                }
                for dist in distributions
            ]
        }
    
    async def _create_distribution(self, transaction_id: str, revenue_type: RevenueType,
                                 recipient_address: str, amount: float, percentage: float,
                                 nft_token_id: Optional[str] = None) -> RevenueDistribution:
        """Create a new revenue distribution"""
        
        distribution_id = f"dist_{uuid.uuid4().hex[:8]}"
        
        distribution = RevenueDistribution(
            distribution_id=distribution_id,
            transaction_id=transaction_id,
            revenue_type=revenue_type,
            recipient_address=recipient_address,
            amount=amount,
            percentage=percentage,
            source_transaction=transaction_id,
            nft_token_id=nft_token_id,
            created_at=datetime.now(timezone.utc).isoformat()
        )
        
        self.pending_distributions[distribution_id] = distribution
        return distribution
    
    async def _process_distribution(self, distribution: RevenueDistribution):
        """Process a revenue distribution (simulate payment)"""
        
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        # In real implementation, would interact with blockchain/payment system
        # For now, simulate successful processing
        
        distribution.status = "processed"
        distribution.processed_at = datetime.now(timezone.utc).isoformat()
        
        # Move from pending to history
        if distribution.distribution_id in self.pending_distributions:
            del self.pending_distributions[distribution.distribution_id]
        
        self.revenue_history.append(distribution)
        
        print(f"   ✅ Processed {distribution.revenue_type.value}: ${distribution.amount:.2f} → {distribution.recipient_address}")
    
    async def get_revenue_analytics(self, time_period: str = "30d") -> Dict[str, Any]:
        """Get revenue analytics for specified time period"""
        
        # Calculate date range
        end_date = datetime.now(timezone.utc)
        if time_period == "7d":
            start_date = end_date - timedelta(days=7)
        elif time_period == "30d":
            start_date = end_date - timedelta(days=30)
        elif time_period == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)  # Default
        
        # Filter distributions in time period
        period_distributions = [
            dist for dist in self.revenue_history
            if start_date <= datetime.fromisoformat(dist.created_at.replace('Z', '+00:00')) <= end_date
        ]
        
        # Calculate analytics
        total_revenue = sum(dist.amount for dist in period_distributions)
        
        revenue_by_type = defaultdict(float)
        for dist in period_distributions:
            revenue_by_type[dist.revenue_type.value] += dist.amount
        
        # Top recipients
        revenue_by_recipient = defaultdict(float)
        for dist in period_distributions:
            revenue_by_recipient[dist.recipient_address] += dist.amount
        
        top_recipients = sorted(revenue_by_recipient.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "period": time_period,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_revenue": total_revenue,
            "transaction_count": len(set(dist.transaction_id for dist in period_distributions)),
            "revenue_by_type": dict(revenue_by_type),
            "top_recipients": [
                {"address": addr, "amount": amount}
                for addr, amount in top_recipients
            ],
            "average_per_transaction": total_revenue / max(len(period_distributions), 1)
        }
    
    async def get_agent_earnings(self, agent_address: str, time_period: str = "30d") -> Dict[str, Any]:
        """Get earnings for specific agent"""
        
        end_date = datetime.now(timezone.utc)
        if time_period == "7d":
            start_date = end_date - timedelta(days=7)
        elif time_period == "30d":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Filter agent earnings
        agent_distributions = [
            dist for dist in self.revenue_history
            if (dist.recipient_address == agent_address and
                start_date <= datetime.fromisoformat(dist.created_at.replace('Z', '+00:00')) <= end_date)
        ]
        
        total_earnings = sum(dist.amount for dist in agent_distributions)
        
        earnings_by_type = defaultdict(float)
        for dist in agent_distributions:
            earnings_by_type[dist.revenue_type.value] += dist.amount
        
        return {
            "agent_address": agent_address,
            "period": time_period,
            "total_earnings": total_earnings,
            "transaction_count": len(agent_distributions),
            "earnings_by_type": dict(earnings_by_type),
            "average_per_transaction": total_earnings / max(len(agent_distributions), 1)
        }
    
    def get_revenue_rates(self) -> Dict[str, float]:
        """Get current revenue sharing rates"""
        return {
            revenue_type: rate * 100  # Convert to percentages
            for revenue_type, rate in self.revenue_rates.items()
        }
    
    async def update_revenue_rates(self, new_rates: Dict[str, float]) -> Dict[str, Any]:
        """Update revenue sharing rates"""
        
        old_rates = self.revenue_rates.copy()
        
        for revenue_type, rate in new_rates.items():
            if revenue_type in self.revenue_rates:
                self.revenue_rates[revenue_type] = rate / 100  # Convert from percentage
        
        print(f"📈 Updated revenue rates:")
        for revenue_type, new_rate in new_rates.items():
            old_rate = old_rates.get(revenue_type, 0) * 100
            print(f"   {revenue_type}: {old_rate:.2f}% → {new_rate:.2f}%")
        
        return {
            "success": True,
            "old_rates": {k: v * 100 for k, v in old_rates.items()},
            "new_rates": {k: v * 100 for k, v in self.revenue_rates.items()},
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

# Global revenue manager instance
revenue_manager = RevenueManager()

# Convenience functions
async def process_sale_revenue(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to process NFT sale revenue"""
    return await revenue_manager.process_nft_sale_revenue(transaction_data)

async def get_revenue_analytics(time_period: str = "30d") -> Dict[str, Any]:
    """Convenience function to get revenue analytics"""
    return await revenue_manager.get_revenue_analytics(time_period)

if __name__ == "__main__":
    # Test the revenue manager
    async def test_revenue_manager():
        manager = RevenueManager()
        
        print("🧪 Testing Revenue Sharing Manager")
        
        # Test NFT sale revenue processing
        transaction_data = {
            "transaction_id": "tx_test_001",
            "sale_price": 1000.0,
            "seller_address": "0xseller123",
            "buyer_address": "0xbuyer456",
            "nft_token_id": "memory_001",
            "creator_address": "0xcreator789",
            "is_resale": True,
            "referrer_address": "0xreferrer012"
        }
        
        result = await manager.process_nft_sale_revenue(transaction_data)
        print(f"\nRevenue Distribution Result:")
        print(f"Seller receives: ${result['seller_amount']:.2f}")
        print(f"Total fees: ${result['total_fees']:.2f} ({result['fee_percentage']:.2f}%)")
        
        # Get analytics
        analytics = await manager.get_revenue_analytics("30d")
        print(f"\nRevenue Analytics:")
        print(f"Total Revenue: ${analytics['total_revenue']:.2f}")
        print(f"Revenue by Type: {analytics['revenue_by_type']}")
        
        # Get agent earnings
        agent_earnings = await manager.get_agent_earnings("0xappraiser456", "30d")
        print(f"\nAgent Earnings: ${agent_earnings['total_earnings']:.2f}")
    
    asyncio.run(test_revenue_manager())