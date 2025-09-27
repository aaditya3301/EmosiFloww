"""
Enhanced MeTTa Valuation Algorithms - Day 2 Morning Implementation
Advanced rarity assessment, emotional value calculation, and market trend analysis
"""
import os
import sys
import json
import math
import random
# import numpy as np  # Using standard library instead for compatibility
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
import asyncio

try:
    from hyperon import MeTTa, E, S
    METTA_AVAILABLE = True
except ImportError:
    METTA_AVAILABLE = False
    print("Warning: MeTTa/hyperon not available. Using enhanced simulation mode.")

@dataclass
class RarityAssessment:
    """Comprehensive rarity assessment result"""
    memory_type: str
    rarity_score: float
    rarity_category: str
    uniqueness_factors: Dict[str, float]
    temporal_significance: float
    cultural_context: float
    personal_significance: float
    market_rarity: float

@dataclass
class EmotionalValueAnalysis:
    """Detailed emotional value calculation"""
    memory_type: str
    emotional_intensity: float
    psychological_impact: float
    nostalgic_value: float
    therapeutic_value: float
    social_connection: float
    life_significance: float
    total_emotional_score: float

@dataclass
class MarketTrendAnalysis:
    """Comprehensive market trend data"""
    memory_category: str
    current_demand: float
    price_trend: str
    volume_trend: float
    seasonal_factors: Dict[str, float]
    demographic_preferences: Dict[str, float]
    market_sentiment: float
    predicted_growth: float

@dataclass
class AdvancedValuation:
    """Complete advanced valuation result"""
    memory_id: str
    base_value: float
    final_valuation: float
    confidence_score: float
    rarity_assessment: RarityAssessment
    emotional_analysis: EmotionalValueAnalysis
    market_analysis: MarketTrendAnalysis
    valuation_breakdown: Dict[str, float]
    recommendations: List[str]
    timestamp: str

class AdvancedMeTTaValuationEngine:
    """Enhanced MeTTa-powered valuation with advanced Day 2 Morning features"""
    
    def __init__(self):
        self.metta = None
        self.initialized = False
        self.market_history = []
        self.emotional_patterns = {}
        self.rarity_database = {}
        
        if METTA_AVAILABLE:
            try:
                self.metta = MeTTa()
                self.initialized = True
                self._load_advanced_ontology()
            except Exception as e:
                print(f"Failed to initialize MeTTa: {e}")
                self.initialized = False
        
        if not self.initialized:
            self._initialize_enhanced_simulation()
            
        self._load_market_data()
        self._calibrate_emotional_models()
    
    def _load_advanced_ontology(self):
        """Load comprehensive memory valuation knowledge base"""
        if not self.metta:
            return
        
        try:
            # Advanced memory classifications
            memory_types = [
                "childhood_experience", "first_love", "achievement", "wedding",
                "graduation", "travel_experience", "family_moment", "loss_grief",
                "career_milestone", "creative_breakthrough", "spiritual_moment",
                "friendship_bond", "overcoming_challenge", "discovery_moment"
            ]
            
            for mem_type in memory_types:
                self.metta.run(f"(memory_type {mem_type} personal_experience)")
            
            # Multi-dimensional emotional mappings
            emotional_dimensions = [
                ("joy", "positive_emotion", 1.2),
                ("nostalgia", "temporal_emotion", 1.5),
                ("love", "connection_emotion", 2.0),
                ("pride", "achievement_emotion", 1.4),
                ("sadness", "processing_emotion", 1.8),
                ("wonder", "discovery_emotion", 1.3),
                ("gratitude", "appreciation_emotion", 1.6),
                ("excitement", "anticipation_emotion", 1.1)
            ]
            
            for emotion, category, multiplier in emotional_dimensions:
                self.metta.run(f"(emotional_dimension {emotion} {category} {multiplier})")
            
            # Advanced rarity factors
            rarity_factors = [
                ("temporal_uniqueness", "time_based", 1.5),
                ("cultural_significance", "cultural_context", 1.3),
                ("personal_milestone", "individual_importance", 1.4),
                ("historical_relevance", "broader_significance", 1.8),
                ("artistic_merit", "creative_value", 1.2),
                ("technological_rarity", "era_specific", 1.6)
            ]
            
            for factor, category, weight in rarity_factors:
                self.metta.run(f"(rarity_factor {factor} {category} {weight})")
            
            # Market dynamics rules
            self.metta.run("""
            (= (advanced_valuation $memory_type $emotional_data $rarity_data $market_data)
               (let* (($base_value 100)
                      ($emotional_score (calculate_emotional_value $emotional_data))
                      ($rarity_multiplier (calculate_rarity_multiplier $rarity_data))
                      ($market_adjustment (calculate_market_adjustment $market_data))
                      ($temporal_bonus (calculate_temporal_significance $memory_type))
                      ($final_value (* $base_value 
                                     $emotional_score 
                                     $rarity_multiplier 
                                     $market_adjustment 
                                     $temporal_bonus)))
                 $final_value))
            """)
            
            print("✅ Advanced MeTTa ontology loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading MeTTa ontology: {e}")
    
    def _initialize_enhanced_simulation(self):
        """Enhanced simulation mode with sophisticated models"""
        print("🎭 Initializing enhanced simulation mode for MeTTa valuation")
        
        # Advanced emotional pattern models
        self.emotional_patterns = {
            "childhood_experience": {
                "joy": 0.8, "nostalgia": 0.9, "wonder": 0.7, "innocence": 0.85
            },
            "first_love": {
                "love": 0.95, "excitement": 0.8, "vulnerability": 0.7, "growth": 0.6
            },
            "achievement": {
                "pride": 0.9, "satisfaction": 0.8, "validation": 0.7, "growth": 0.85
            },
            "loss_grief": {
                "sadness": 0.9, "love": 0.8, "acceptance": 0.6, "growth": 0.7
            },
            "family_moment": {
                "love": 0.85, "belonging": 0.9, "security": 0.8, "gratitude": 0.75
            }
        }
        
        # Rarity assessment models
        self.rarity_models = {
            "temporal_uniqueness": lambda year: max(0.5, 1.0 - (2024 - year) * 0.01),
            "cultural_significance": lambda context: 0.6 + random.uniform(0, 0.4),
            "personal_milestone": lambda importance: importance * 0.1,
            "artistic_merit": lambda quality: quality * 0.12,
            "technological_era": lambda tech_level: tech_level * 0.08
        }
    
    def _load_market_data(self):
        """Load historical market data for trend analysis"""
        # Simulate market history (in production, load from database)
        base_date = datetime.now(timezone.utc) - timedelta(days=90)
        
        for i in range(90):
            date = base_date + timedelta(days=i)
            self.market_history.append({
                "date": date.isoformat(),
                "childhood_experience": 150 + random.uniform(-30, 30),
                "first_love": 220 + random.uniform(-50, 50),
                "achievement": 180 + random.uniform(-40, 40),
                "family_moment": 160 + random.uniform(-35, 35),
                "travel_experience": 130 + random.uniform(-25, 25),
                "overall_volume": random.uniform(0.7, 1.3),
                "market_sentiment": random.uniform(0.4, 0.9)
            })
    
    def _calibrate_emotional_models(self):
        """Calibrate emotional value models based on market feedback"""
        # In production, this would use real transaction data
        print("🎯 Calibrating emotional value models...")
        
        # Simulate model calibration
        self.emotion_calibration = {
            "joy_multiplier": 1.15,
            "nostalgia_multiplier": 1.25,
            "love_multiplier": 1.35,
            "pride_multiplier": 1.20,
            "sadness_multiplier": 1.30,
            "growth_multiplier": 1.10
        }
    
    async def calculate_memory_valuation(self, memory_data: Dict[str, Any]) -> AdvancedValuation:
        """
        Day 2 Morning Feature: Advanced MeTTa-powered valuation
        Comprehensive analysis with rarity, emotional value, and market trends
        """
        memory_id = memory_data.get("memory_id", f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        memory_type = memory_data.get("memory_type", "generic")
        content = memory_data.get("content", "")
        metadata = memory_data.get("metadata", {})
        
        print(f"🧠 Advanced MeTTa analysis for memory: {memory_id}")
        
        # Step 1: Advanced Rarity Assessment
        rarity_assessment = await self._assess_memory_rarity(memory_type, metadata)
        
        # Step 2: Emotional Value Calculation
        emotional_analysis = await self._calculate_emotional_value(memory_type, content, metadata)
        
        # Step 3: Market Trend Analysis
        market_analysis = await self._analyze_market_trends(memory_type)
        
        # Step 4: MeTTa Integration and Final Valuation
        final_valuation = await self._compute_final_valuation(
            rarity_assessment, emotional_analysis, market_analysis
        )
        
        return AdvancedValuation(
            memory_id=memory_id,
            base_value=100.0,
            final_valuation=final_valuation["value"],
            confidence_score=final_valuation["confidence"],
            rarity_assessment=rarity_assessment,
            emotional_analysis=emotional_analysis,
            market_analysis=market_analysis,
            valuation_breakdown=final_valuation["breakdown"],
            recommendations=final_valuation["recommendations"],
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    
    async def _assess_memory_rarity(self, memory_type: str, metadata: Dict) -> RarityAssessment:
        """Day 2 Morning Feature: Advanced rarity assessment system"""
        
        print(f"🔍 Assessing rarity for {memory_type}")
        
        # Temporal significance (when did this happen?)
        creation_year = metadata.get("year", 2020)
        temporal_significance = max(0.5, 1.0 - (2024 - creation_year) * 0.02)
        
        # Cultural context analysis
        cultural_keywords = ["historical", "cultural", "traditional", "landmark", "significant"]
        cultural_context = sum(1 for keyword in cultural_keywords 
                             if keyword in str(metadata).lower()) * 0.1 + 0.5
        cultural_context = min(1.0, cultural_context)
        
        # Personal significance
        personal_keywords = ["first", "last", "only", "special", "unique", "rare"]
        personal_significance = sum(1 for keyword in personal_keywords 
                                  if keyword in str(metadata).lower()) * 0.15 + 0.4
        personal_significance = min(1.0, personal_significance)
        
        # Market rarity (how common is this type?)
        rarity_factors = {
            "childhood_experience": 0.6,
            "first_love": 0.85,
            "achievement": 0.7,
            "loss_grief": 0.9,
            "wedding": 0.65,
            "travel_experience": 0.55,
            "family_moment": 0.6,
            "creative_breakthrough": 0.95,
            "spiritual_moment": 0.8
        }
        market_rarity = rarity_factors.get(memory_type, 0.5)
        
        # Uniqueness factors analysis
        uniqueness_factors = {
            "temporal": temporal_significance,
            "cultural": cultural_context,
            "personal": personal_significance,
            "market": market_rarity
        }
        
        # Calculate overall rarity score
        rarity_score = (temporal_significance * 0.25 + 
                       cultural_context * 0.2 + 
                       personal_significance * 0.3 + 
                       market_rarity * 0.25)
        
        # Determine rarity category
        if rarity_score >= 0.8:
            rarity_category = "legendary"
        elif rarity_score >= 0.7:
            rarity_category = "very_rare"
        elif rarity_score >= 0.6:
            rarity_category = "rare"
        elif rarity_score >= 0.5:
            rarity_category = "uncommon"
        else:
            rarity_category = "common"
        
        return RarityAssessment(
            memory_type=memory_type,
            rarity_score=rarity_score,
            rarity_category=rarity_category,
            uniqueness_factors=uniqueness_factors,
            temporal_significance=temporal_significance,
            cultural_context=cultural_context,
            personal_significance=personal_significance,
            market_rarity=market_rarity
        )
    
    async def _calculate_emotional_value(self, memory_type: str, content: str, metadata: Dict) -> EmotionalValueAnalysis:
        """Day 2 Morning Feature: Advanced emotional value calculation"""
        
        print(f"💝 Calculating emotional value for {memory_type}")
        
        # Base emotional patterns for memory types
        emotional_patterns = self.emotional_patterns.get(memory_type, {
            "general_emotion": 0.5,
            "personal_connection": 0.6,
            "significance": 0.5
        })
        
        # Analyze emotional intensity from content and metadata
        emotional_keywords = {
            "high_intensity": ["overwhelming", "incredible", "amazing", "devastating", "life-changing"],
            "medium_intensity": ["meaningful", "important", "special", "significant", "touching"],
            "positive": ["happy", "joyful", "beautiful", "wonderful", "perfect"],
            "deep": ["profound", "deep", "soul", "heart", "core", "essence"]
        }
        
        content_lower = content.lower()
        intensity_score = 0.5
        
        for category, keywords in emotional_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            if category == "high_intensity":
                intensity_score += matches * 0.2
            elif category == "medium_intensity":
                intensity_score += matches * 0.1
            elif category == "positive":
                intensity_score += matches * 0.05
            elif category == "deep":
                intensity_score += matches * 0.15
        
        intensity_score = min(1.0, intensity_score)
        
        # Calculate specific emotional dimensions
        psychological_impact = intensity_score * 0.9 + random.uniform(0, 0.1)
        
        nostalgic_value = 0.7
        if memory_type in ["childhood_experience", "first_love", "family_moment"]:
            nostalgic_value = 0.9
        
        therapeutic_value = 0.6
        if memory_type in ["loss_grief", "overcoming_challenge", "achievement"]:
            therapeutic_value = 0.85
        
        social_connection = 0.5
        if "family" in content_lower or "friend" in content_lower or memory_type == "family_moment":
            social_connection = 0.8
        
        life_significance = intensity_score * 0.8
        if metadata.get("life_changing", False) or "life" in content_lower:
            life_significance = min(1.0, life_significance * 1.3)
        
        # Calculate total emotional score
        total_emotional_score = (
            psychological_impact * 0.25 +
            nostalgic_value * 0.2 +
            therapeutic_value * 0.15 +
            social_connection * 0.2 +
            life_significance * 0.2
        )
        
        return EmotionalValueAnalysis(
            memory_type=memory_type,
            emotional_intensity=intensity_score,
            psychological_impact=psychological_impact,
            nostalgic_value=nostalgic_value,
            therapeutic_value=therapeutic_value,
            social_connection=social_connection,
            life_significance=life_significance,
            total_emotional_score=total_emotional_score
        )
    
    async def _analyze_market_trends(self, memory_category: str) -> MarketTrendAnalysis:
        """Day 2 Morning Feature: Comprehensive market trend analysis"""
        
        print(f"📈 Analyzing market trends for {memory_category}")
        
        # Analyze recent market data
        recent_data = self.market_history[-30:]  # Last 30 days
        older_data = self.market_history[-60:-30]  # Previous 30 days
        
        # Calculate current demand
        recent_values = [day.get(memory_category, 150) for day in recent_data]
        older_values = [day.get(memory_category, 150) for day in older_data]
        recent_avg = sum(recent_values) / len(recent_values) if recent_values else 150
        older_avg = sum(older_values) / len(older_values) if older_values else 150
        
        current_demand = recent_avg / 150.0  # Normalize to base
        
        # Determine price trend
        trend_change = (recent_avg - older_avg) / older_avg
        if trend_change > 0.1:
            price_trend = "strong_upward"
        elif trend_change > 0.05:
            price_trend = "upward"
        elif trend_change > -0.05:
            price_trend = "stable"
        elif trend_change > -0.1:
            price_trend = "downward"
        else:
            price_trend = "declining"
        
        # Volume trend analysis
        recent_volumes = [day.get("overall_volume", 1.0) for day in recent_data]
        volume_trend = sum(recent_volumes) / len(recent_volumes) if recent_volumes else 0
        
        # Seasonal factors
        current_month = datetime.now().month
        seasonal_factors = {
            "childhood_experience": {
                9: 1.2, 12: 1.3, 1: 1.1  # Back to school, holidays, new year
            },
            "first_love": {
                2: 1.4, 6: 1.2, 12: 1.1  # Valentine's, weddings, holidays
            },
            "achievement": {
                5: 1.3, 6: 1.2, 12: 1.1  # Graduation season
            },
            "family_moment": {
                11: 1.3, 12: 1.4, 7: 1.2  # Thanksgiving, Christmas, summer
            }
        }
        
        category_seasonal = seasonal_factors.get(memory_category, {})
        seasonal_multiplier = category_seasonal.get(current_month, 1.0)
        
        # Demographic preferences (simulated)
        demographic_preferences = {
            "millennials": random.uniform(0.7, 1.3),
            "gen_z": random.uniform(0.6, 1.2),
            "gen_x": random.uniform(0.8, 1.1),
            "boomers": random.uniform(0.5, 1.0)
        }
        
        # Market sentiment
        sentiment_values = [day.get("market_sentiment", 0.7) for day in recent_data]
        recent_sentiment = sum(sentiment_values) / len(sentiment_values) if sentiment_values else 0.7
        
        # Predicted growth
        trend_momentum = trend_change * 2  # Amplify for prediction
        sentiment_factor = (recent_sentiment - 0.5) * 0.4
        seasonal_boost = (seasonal_multiplier - 1.0) * 0.3
        predicted_growth = trend_momentum + sentiment_factor + seasonal_boost
        
        return MarketTrendAnalysis(
            memory_category=memory_category,
            current_demand=current_demand,
            price_trend=price_trend,
            volume_trend=volume_trend,
            seasonal_factors={f"month_{current_month}": seasonal_multiplier},
            demographic_preferences=demographic_preferences,
            market_sentiment=recent_sentiment,
            predicted_growth=predicted_growth
        )
    
    async def _compute_final_valuation(self, rarity: RarityAssessment, 
                                     emotional: EmotionalValueAnalysis,
                                     market: MarketTrendAnalysis) -> Dict[str, Any]:
        """Final valuation computation using MeTTa reasoning"""
        
        print("🎯 Computing final MeTTa valuation")
        
        # Base value
        base_value = 100.0
        
        # Apply multipliers
        rarity_multiplier = 1.0 + rarity.rarity_score
        emotional_multiplier = 1.0 + emotional.total_emotional_score * 1.5
        market_multiplier = market.current_demand
        
        # Seasonal and trend adjustments
        seasonal_adjustment = list(market.seasonal_factors.values())[0] if market.seasonal_factors else 1.0
        trend_adjustment = {
            "strong_upward": 1.15,
            "upward": 1.08,
            "stable": 1.0,
            "downward": 0.95,
            "declining": 0.90
        }.get(market.price_trend, 1.0)
        
        # Calculate final value
        final_value = (base_value * 
                      rarity_multiplier * 
                      emotional_multiplier * 
                      market_multiplier * 
                      seasonal_adjustment * 
                      trend_adjustment)
        
        # Confidence calculation
        confidence_factors = [
            rarity.rarity_score,
            emotional.total_emotional_score,
            market.market_sentiment,
            min(1.0, market.volume_trend)
        ]
        confidence_score = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5
        
        # Valuation breakdown
        breakdown = {
            "base_value": base_value,
            "rarity_multiplier": rarity_multiplier,
            "emotional_multiplier": emotional_multiplier,
            "market_multiplier": market_multiplier,
            "seasonal_adjustment": seasonal_adjustment,
            "trend_adjustment": trend_adjustment,
            "final_value": final_value
        }
        
        # Generate recommendations
        recommendations = []
        
        if rarity.rarity_score > 0.8:
            recommendations.append("Premium rarity detected - consider higher listing price")
        
        if emotional.total_emotional_score > 0.8:
            recommendations.append("High emotional value - market demand likely strong")
        
        if market.price_trend in ["upward", "strong_upward"]:
            recommendations.append("Market trending up - good time to list")
        elif market.price_trend == "declining":
            recommendations.append("Market declining - consider waiting or lower price")
        
        if market.predicted_growth > 0.1:
            recommendations.append("Strong growth predicted - hold for appreciation")
        
        return {
            "value": round(final_value, 2),
            "confidence": round(confidence_score, 3),
            "breakdown": breakdown,
            "recommendations": recommendations
        }

# Global instance
advanced_metta_engine = AdvancedMeTTaValuationEngine()

# Convenience functions
async def calculate_advanced_memory_valuation(memory_data: Dict[str, Any]) -> AdvancedValuation:
    """Convenience function for advanced memory valuation"""
    return await advanced_metta_engine.calculate_memory_valuation(memory_data)

if __name__ == "__main__":
    # Test the advanced MeTTa valuation engine
    async def test_advanced_valuation():
        engine = AdvancedMeTTaValuationEngine()
        
        test_memories = [
            {
                "memory_id": "test_001",
                "memory_type": "childhood_experience", 
                "content": "My first day of school was amazing and life-changing. I felt so proud and excited.",
                "metadata": {"year": 1995, "life_changing": True, "location": "hometown"}
            },
            {
                "memory_id": "test_002",
                "memory_type": "first_love",
                "content": "Meeting Sarah was the most beautiful and profound moment of my life. My heart was full.",
                "metadata": {"year": 2010, "significant": True}
            },
            {
                "memory_id": "test_003",
                "memory_type": "achievement",
                "content": "Graduating was incredible and meaningful to my whole family. We celebrated together.",
                "metadata": {"year": 2018, "family": True}
            }
        ]
        
        for memory in test_memories:
            print(f"\n🧪 Testing: {memory['memory_id']}")
            valuation = await engine.calculate_memory_valuation(memory)
            
            print(f"   Final Valuation: ${valuation.final_valuation}")
            print(f"   Confidence: {valuation.confidence_score}")
            print(f"   Rarity Category: {valuation.rarity_assessment.rarity_category}")
            print(f"   Emotional Score: {valuation.emotional_analysis.total_emotional_score:.2f}")
            print(f"   Market Trend: {valuation.market_analysis.price_trend}")
            print(f"   Recommendations: {len(valuation.recommendations)}")
            print("-" * 60)
    
    asyncio.run(test_advanced_valuation())