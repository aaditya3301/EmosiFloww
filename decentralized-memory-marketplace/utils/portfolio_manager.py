"""
Portfolio Management System
Track and manage user NFT collections, calculate portfolio values, and provide insights
"""
import os
import json
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class MemoryNFT:
    """Individual Memory NFT in user portfolio"""
    token_id: str
    memory_type: str
    content_hash: str
    mint_date: str
    current_value: float
    purchase_price: float
    listing_status: str  # "unlisted", "listed", "sold"
    authenticity_score: float
    rarity_score: float
    metadata: Dict[str, Any]
    
    def get_profit_loss(self) -> float:
        """Calculate profit/loss for this NFT"""
        return self.current_value - self.purchase_price
    
    def get_roi_percentage(self) -> float:
        """Calculate ROI percentage"""
        if self.purchase_price == 0:
            return 0.0
        return ((self.current_value - self.purchase_price) / self.purchase_price) * 100

@dataclass
class PortfolioSummary:
    """Portfolio analysis summary"""
    user_address: str
    total_value: float
    total_nfts: int
    total_investment: float
    total_profit_loss: float
    roi_percentage: float
    top_performer: Optional[MemoryNFT]
    worst_performer: Optional[MemoryNFT]
    category_breakdown: Dict[str, Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
    recommendations: List[str]
    last_updated: str

class PortfolioManager:
    """Manage user NFT portfolios and provide analytics"""
    
    def __init__(self):
        self.portfolio_data = defaultdict(dict)  # user_address -> portfolio data
        self.data_file = "portfolio_data.json"
        self._load_portfolio_data()
    
    def _load_portfolio_data(self):
        """Load portfolio data from storage"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.portfolio_data.update(data)
                print(f"📂 Loaded portfolio data for {len(self.portfolio_data)} users")
            else:
                print("📂 No existing portfolio data found, starting fresh")
        except Exception as e:
            print(f"⚠️ Error loading portfolio data: {e}")
    
    def _save_portfolio_data(self):
        """Save portfolio data to storage"""
        try:
            # Convert dataclasses to dictionaries for JSON serialization
            serializable_data = {}
            for user_address, portfolio in self.portfolio_data.items():
                nfts_data = []
                for nft in portfolio.get("nfts", []):
                    if isinstance(nft, MemoryNFT):
                        nfts_data.append(asdict(nft))
                    elif isinstance(nft, dict):
                        nfts_data.append(nft)
                    else:
                        # Handle any other format by converting to dict
                        nfts_data.append(dict(nft) if hasattr(nft, '__dict__') else nft)
                
                serializable_data[user_address] = {
                    "nfts": nfts_data,
                    "last_updated": portfolio.get("last_updated", datetime.now(timezone.utc).isoformat())
                }
            
            with open(self.data_file, 'w') as f:
                json.dump(serializable_data, f, indent=2, default=str)
            print(f"💾 Saved portfolio data for {len(serializable_data)} users")
        except Exception as e:
            print(f"❌ Error saving portfolio data: {e}")
            # Continue without saving to avoid blocking operations
    
    async def add_nft_to_portfolio(self, user_address: str, nft: MemoryNFT):
        """Add NFT to user portfolio"""
        if user_address not in self.portfolio_data:
            self.portfolio_data[user_address] = {"nfts": [], "last_updated": datetime.now(timezone.utc).isoformat()}
        
        self.portfolio_data[user_address]["nfts"].append(nft)
        self.portfolio_data[user_address]["last_updated"] = datetime.now(timezone.utc).isoformat()
        self._save_portfolio_data()
        
        print(f"➕ Added NFT {nft.token_id} to {user_address} portfolio")
    
    async def remove_nft_from_portfolio(self, user_address: str, token_id: str):
        """Remove NFT from user portfolio (when sold)"""
        if user_address in self.portfolio_data:
            nfts = self.portfolio_data[user_address]["nfts"]
            self.portfolio_data[user_address]["nfts"] = [
                nft for nft in nfts 
                if (isinstance(nft, MemoryNFT) and nft.token_id != token_id) or 
                   (isinstance(nft, dict) and nft.get("token_id") != token_id)
            ]
            self.portfolio_data[user_address]["last_updated"] = datetime.now(timezone.utc).isoformat()
            self._save_portfolio_data()
            print(f"➖ Removed NFT {token_id} from {user_address} portfolio")
    
    async def update_nft_value(self, user_address: str, token_id: str, new_value: float):
        """Update NFT current market value"""
        if user_address in self.portfolio_data:
            for nft_data in self.portfolio_data[user_address]["nfts"]:
                nft = nft_data if isinstance(nft_data, dict) else asdict(nft_data)
                if nft.get("token_id") == token_id:
                    nft["current_value"] = new_value
                    print(f"💰 Updated NFT {token_id} value to ${new_value}")
                    break
            self._save_portfolio_data()
    
    async def calculate_portfolio_value(self, user_address: str) -> PortfolioSummary:
        """Calculate comprehensive portfolio analysis"""
        
        if user_address not in self.portfolio_data or not self.portfolio_data[user_address]["nfts"]:
            # Return empty portfolio for demo
            return await self._create_demo_portfolio(user_address)
        
        user_portfolio = self.portfolio_data[user_address]
        nfts = []
        
        # Convert dict NFTs back to MemoryNFT objects
        for nft_data in user_portfolio["nfts"]:
            if isinstance(nft_data, dict):
                nfts.append(MemoryNFT(**nft_data))
            else:
                nfts.append(nft_data)
        
        # Calculate totals
        total_value = sum(nft.current_value for nft in nfts)
        total_investment = sum(nft.purchase_price for nft in nfts)
        total_profit_loss = total_value - total_investment
        roi_percentage = (total_profit_loss / total_investment * 100) if total_investment > 0 else 0
        
        # Find best and worst performers
        top_performer = max(nfts, key=lambda x: x.get_roi_percentage()) if nfts else None
        worst_performer = min(nfts, key=lambda x: x.get_roi_percentage()) if nfts else None
        
        # Category breakdown
        category_breakdown = self._analyze_categories(nfts)
        
        # Recent activity (simulated)
        recent_activity = self._generate_recent_activity(nfts)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(nfts, roi_percentage)
        
        return PortfolioSummary(
            user_address=user_address,
            total_value=total_value,
            total_nfts=len(nfts),
            total_investment=total_investment,
            total_profit_loss=total_profit_loss,
            roi_percentage=roi_percentage,
            top_performer=top_performer,
            worst_performer=worst_performer,
            category_breakdown=category_breakdown,
            recent_activity=recent_activity,
            recommendations=recommendations,
            last_updated=datetime.now(timezone.utc).isoformat()
        )
    
    async def _create_demo_portfolio(self, user_address: str) -> PortfolioSummary:
        """Create a demo portfolio for users without existing data"""
        
        # Create sample NFTs
        demo_nfts = [
            MemoryNFT(
                token_id="memory_001",
                memory_type="childhood_experience",
                content_hash="QmX1234...",
                mint_date="2024-09-01T10:00:00Z",
                current_value=520.0,
                purchase_price=450.0,
                listing_status="unlisted",
                authenticity_score=0.95,
                rarity_score=8.2,
                metadata={"title": "First Day of School", "year": 1995}
            ),
            MemoryNFT(
                token_id="memory_002", 
                memory_type="first_love",
                content_hash="QmY5678...",
                mint_date="2024-09-05T14:30:00Z",
                current_value=385.0,
                purchase_price=320.0,
                listing_status="unlisted",
                authenticity_score=0.88,
                rarity_score=7.5,
                metadata={"title": "First Kiss at Prom", "year": 2010}
            ),
            MemoryNFT(
                token_id="memory_003",
                memory_type="achievement",
                content_hash="QmZ9012...",
                mint_date="2024-09-10T09:15:00Z",
                current_value=295.0,
                purchase_price=300.0,
                listing_status="listed",
                authenticity_score=0.92,
                rarity_score=6.8,
                metadata={"title": "Graduation Day", "year": 2018}
            ),
            MemoryNFT(
                token_id="memory_004",
                memory_type="travel_experience",
                content_hash="QmA3456...",
                mint_date="2024-09-12T16:45:00Z",
                current_value=180.0,
                purchase_price=150.0,
                listing_status="unlisted",
                authenticity_score=0.85,
                rarity_score=5.9,
                metadata={"title": "Paris Sunset", "year": 2022}
            ),
            MemoryNFT(
                token_id="memory_005",
                memory_type="family_moment",
                content_hash="QmB7890...",
                mint_date="2024-09-15T12:00:00Z",
                current_value=410.0,
                purchase_price=380.0,
                listing_status="unlisted", 
                authenticity_score=0.98,
                rarity_score=8.5,
                metadata={"title": "Grandma's Last Birthday", "year": 2020}
            ),
            MemoryNFT(
                token_id="memory_006",
                memory_type="achievement",
                content_hash="QmC1122...",
                mint_date="2024-09-18T08:30:00Z",
                current_value=225.0,
                purchase_price=280.0,
                listing_status="unlisted",
                authenticity_score=0.90,
                rarity_score=6.2,
                metadata={"title": "First Job Offer", "year": 2019}
            ),
            MemoryNFT(
                token_id="memory_007",
                memory_type="travel_experience", 
                content_hash="QmD3344...",
                mint_date="2024-09-20T19:20:00Z",
                current_value=165.0,
                purchase_price=140.0,
                listing_status="unlisted",
                authenticity_score=0.87,
                rarity_score=5.5,
                metadata={"title": "Tokyo Cherry Blossoms", "year": 2023}
            ),
            MemoryNFT(
                token_id="memory_008",
                memory_type="childhood_experience",
                content_hash="QmE5566...",
                mint_date="2024-09-22T11:10:00Z",
                current_value=340.0,
                purchase_price=290.0,
                listing_status="unlisted",
                authenticity_score=0.94,
                rarity_score=7.8,
                metadata={"title": "Summer Camp Adventure", "year": 1998}
            )
        ]
        
        # Save demo portfolio
        self.portfolio_data[user_address] = {
            "nfts": [asdict(nft) for nft in demo_nfts],
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        self._save_portfolio_data()
        
        # Calculate totals
        total_value = sum(nft.current_value for nft in demo_nfts)
        total_investment = sum(nft.purchase_price for nft in demo_nfts)
        total_profit_loss = total_value - total_investment
        roi_percentage = (total_profit_loss / total_investment * 100) if total_investment > 0 else 0
        
        # Find performers
        top_performer = max(demo_nfts, key=lambda x: x.get_roi_percentage())
        worst_performer = min(demo_nfts, key=lambda x: x.get_roi_percentage())
        
        return PortfolioSummary(
            user_address=user_address,
            total_value=total_value,
            total_nfts=len(demo_nfts),
            total_investment=total_investment, 
            total_profit_loss=total_profit_loss,
            roi_percentage=roi_percentage,
            top_performer=top_performer,
            worst_performer=worst_performer,
            category_breakdown=self._analyze_categories(demo_nfts),
            recent_activity=self._generate_recent_activity(demo_nfts),
            recommendations=self._generate_recommendations(demo_nfts, roi_percentage),
            last_updated=datetime.now(timezone.utc).isoformat()
        )
    
    def _analyze_categories(self, nfts: List[MemoryNFT]) -> Dict[str, Dict[str, Any]]:
        """Analyze NFTs by category"""
        categories = defaultdict(lambda: {"count": 0, "total_value": 0, "avg_value": 0, "profit_loss": 0})
        
        for nft in nfts:
            cat = categories[nft.memory_type]
            cat["count"] += 1
            cat["total_value"] += nft.current_value
            cat["profit_loss"] += nft.get_profit_loss()
        
        # Calculate averages
        for category in categories.values():
            if category["count"] > 0:
                category["avg_value"] = category["total_value"] / category["count"]
        
        return dict(categories)
    
    def _generate_recent_activity(self, nfts: List[MemoryNFT]) -> List[Dict[str, Any]]:
        """Generate recent activity log"""
        activities = []
        
        for nft in nfts[-3:]:  # Last 3 NFTs as "recent"
            activities.append({
                "type": "mint",
                "token_id": nft.token_id,
                "title": nft.metadata.get("title", "Unknown Memory"),
                "date": nft.mint_date,
                "value": nft.purchase_price
            })
        
        return activities
    
    def _generate_recommendations(self, nfts: List[MemoryNFT], roi_percentage: float) -> List[str]:
        """Generate portfolio recommendations"""
        recommendations = []
        
        if roi_percentage > 15:
            recommendations.append("🎉 Strong portfolio performance! Consider taking profits on top performers.")
        elif roi_percentage < -5:
            recommendations.append("📉 Portfolio underperforming. Consider diversifying into higher-demand memory types.")
        else:
            recommendations.append("📊 Balanced portfolio. Continue monitoring market trends.")
        
        # Category-based recommendations
        categories = self._analyze_categories(nfts)
        
        if "childhood_experience" in categories and categories["childhood_experience"]["count"] > 3:
            recommendations.append("👶 High childhood memory concentration. Consider diversifying into other emotional categories.")
        
        if len([nft for nft in nfts if nft.listing_status == "listed"]) < len(nfts) * 0.2:
            recommendations.append("🏷️ Consider listing 1-2 lower-performing memories to optimize portfolio.")
        
        return recommendations
    
    async def get_collection_worth_analysis(self, user_address: str) -> str:
        """Generate natural language collection worth analysis"""
        portfolio = await self.calculate_portfolio_value(user_address)
        
        analysis = f"""📊 **Your Memory Collection Worth Analysis**

**💰 Total Portfolio Value: ${portfolio.total_value:,.2f}**

**📈 Performance Overview:**
• Number of NFTs: {portfolio.total_nfts} memories
• Total Investment: ${portfolio.total_investment:,.2f}
• Profit/Loss: ${portfolio.total_profit_loss:,.2f} ({portfolio.roi_percentage:+.1f}%)
• Average Memory Value: ${portfolio.total_value/portfolio.total_nfts:.2f}

**🏆 Best Performer:**
• {portfolio.top_performer.metadata.get('title', 'Unknown')} ({portfolio.top_performer.memory_type})
• Current Value: ${portfolio.top_performer.current_value:.2f}
• ROI: {portfolio.top_performer.get_roi_percentage():+.1f}%

**📊 Category Breakdown:**"""

        for category, data in portfolio.category_breakdown.items():
            category_name = category.replace("_", " ").title()
            analysis += f"\n• {category_name}: {data['count']} NFTs, ${data['total_value']:.2f} total"

        analysis += f"""

**💡 Key Recommendations:**
{chr(10).join(f"• {rec}" for rec in portfolio.recommendations)}

*Last Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*"""

        return analysis

# Global portfolio manager instance
portfolio_manager = PortfolioManager()

async def get_user_portfolio_summary(user_address: str) -> PortfolioSummary:
    """Convenience function to get portfolio summary"""
    return await portfolio_manager.calculate_portfolio_value(user_address)

async def get_collection_worth(user_address: str) -> str:
    """Convenience function for collection worth analysis"""
    return await portfolio_manager.get_collection_worth_analysis(user_address)

if __name__ == "__main__":
    # Test the portfolio manager
    async def test_portfolio():
        manager = PortfolioManager()
        
        test_user = "0x1234567890abcdef"
        
        print("🧪 Testing portfolio analysis...")
        portfolio = await manager.calculate_portfolio_value(test_user)
        
        print(f"Total Value: ${portfolio.total_value}")
        print(f"ROI: {portfolio.roi_percentage:.1f}%")
        print(f"Best Performer: {portfolio.top_performer.metadata.get('title', 'Unknown')}")
        
        print("\n📊 Collection Worth Analysis:")
        worth_analysis = await manager.get_collection_worth_analysis(test_user)
        print(worth_analysis)
    
    asyncio.run(test_portfolio())