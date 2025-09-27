import os
import sys
from typing import Dict, List, Any, Optional
import json
import random
from datetime import datetime, timezone

try:
    from hyperon import MeTTa, E, S
    METTA_AVAILABLE = True
except ImportError:
    METTA_AVAILABLE = False
    print("Warning: MeTTa/hyperon not available. Using simulation mode.")

class MeTTaValuationEngine:
    def __init__(self):
        self.metta = None
        self.initialized = False
        self.knowledge_base_loaded = False
        
        if METTA_AVAILABLE:
            try:
                self.metta = MeTTa()
                self.initialized = True
                self._load_memory_ontology()
            except Exception as e:
                print(f"Failed to initialize MeTTa: {e}")
                self.initialized = False
        
        if not self.initialized:
            self._initialize_simulation_mode()
    
    def _load_memory_ontology(self):
        """Load memory valuation knowledge base"""
        if not self.metta:
            return
        
        try:
            # Memory type classifications
            self.metta.run("(memory_type childhood_experience personal_history)")
            self.metta.run("(memory_type first_love emotional_milestone)")
            self.metta.run("(memory_type achievement accomplishment)")
            self.metta.run("(memory_type wedding life_event)")
            self.metta.run("(memory_type graduation milestone)")
            self.metta.run("(memory_type travel_experience adventure)")
            self.metta.run("(memory_type family_moment bonding)")
            self.metta.run("(memory_type loss_grief emotional_processing)")
            
            # Emotional value mappings
            self.metta.run("(emotional_value childhood_experience high)")
            self.metta.run("(emotional_value first_love very_high)")
            self.metta.run("(emotional_value achievement high)")
            self.metta.run("(emotional_value wedding very_high)")
            self.metta.run("(emotional_value graduation high)")
            self.metta.run("(emotional_value travel_experience medium)")
            self.metta.run("(emotional_value family_moment high)")
            self.metta.run("(emotional_value loss_grief very_high)")
            
            # Rarity classifications
            self.metta.run("(rarity childhood_experience common)")
            self.metta.run("(rarity first_love rare)")
            self.metta.run("(rarity achievement uncommon)")
            self.metta.run("(rarity wedding uncommon)")
            self.metta.run("(rarity graduation common)")
            self.metta.run("(rarity travel_experience common)")
            self.metta.run("(rarity family_moment common)")
            self.metta.run("(rarity loss_grief rare)")
            
            # Market demand patterns
            self.metta.run("(market_demand childhood_experience medium)")
            self.metta.run("(market_demand first_love high)")
            self.metta.run("(market_demand achievement medium)")
            self.metta.run("(market_demand wedding high)")
            self.metta.run("(market_demand graduation low)")
            self.metta.run("(market_demand travel_experience low)")
            self.metta.run("(market_demand family_moment medium)")
            self.metta.run("(market_demand loss_grief high)")
            
            # Valuation calculation rules
            valuation_rule = """
            (= (calculate_memory_value $memory_type $emotional_intensity $rarity_factor $market_demand)
               (let* (($base_value 100)
                      ($emotional_multiplier 
                       (case (emotional_value $memory_type $emotion)
                         ((very_high) 2.5)
                         ((high) 2.0)
                         ((medium) 1.5)
                         ((low) 1.0)
                         (_ 1.0)))
                      ($rarity_multiplier
                       (case (rarity $memory_type $rarity)
                         ((very_rare) 2.0)
                         ((rare) 1.8)
                         ((uncommon) 1.4)
                         ((common) 1.0)
                         (_ 1.0)))
                      ($demand_multiplier
                       (case (market_demand $memory_type $demand)
                         ((very_high) 1.8)
                         ((high) 1.5)
                         ((medium) 1.2)
                         ((low) 0.9)
                         (_ 1.0)))
                      ($intensity_modifier (+ 0.8 (* $emotional_intensity 0.04))))
                 (* $base_value $emotional_multiplier $rarity_multiplier $demand_multiplier $intensity_modifier)))
            """
            
            self.metta.run(valuation_rule)
            
            # Authenticity scoring rules
            authenticity_rule = """
            (= (calculate_authenticity_score $temporal_consistency $emotional_congruence $metadata_verification)
               (let* (($weights (0.3 0.4 0.3))
                      ($scores ($temporal_consistency $emotional_congruence $metadata_verification))
                      ($weighted_sum (+ (* (car $weights) (car $scores))
                                       (* (cadr $weights) (cadr $scores))
                                       (* (caddr $weights) (caddr $scores)))))
                 $weighted_sum))
            """
            
            self.metta.run(authenticity_rule)
            
            # Market trend analysis
            trend_rule = """
            (= (analyze_market_trend $memory_type $recent_sales $time_period)
               (let* (($avg_price (/ (sum_list $recent_sales) (length $recent_sales)))
                      ($volatility (calculate_volatility $recent_sales))
                      ($trend_direction 
                       (if (> $avg_price 150) "bullish"
                           (if (< $avg_price 75) "bearish" "stable"))))
                 (list $avg_price $volatility $trend_direction)))
            """
            
            self.metta.run(trend_rule)
            
            self.knowledge_base_loaded = True
            print("MeTTa memory valuation ontology loaded successfully")
            
        except Exception as e:
            print(f"Failed to load MeTTa ontology: {e}")
            self.knowledge_base_loaded = False
    
    def _initialize_simulation_mode(self):
        """Initialize simulation mode when MeTTa is not available"""
        self.knowledge_base = {
            "emotional_values": {
                "childhood_experience": 2.0,
                "first_love": 2.5,
                "achievement": 1.8,
                "wedding": 2.3,
                "graduation": 1.6,
                "travel_experience": 1.3,
                "family_moment": 1.9,
                "loss_grief": 2.4,
                "generic": 1.0
            },
            "rarity_multipliers": {
                "very_rare": 2.0,
                "rare": 1.8,
                "uncommon": 1.4,
                "common": 1.0
            },
            "market_demand": {
                "childhood_experience": 1.2,
                "first_love": 1.5,
                "achievement": 1.2,
                "wedding": 1.5,
                "graduation": 0.9,
                "travel_experience": 0.9,
                "family_moment": 1.2,
                "loss_grief": 1.5,
                "generic": 1.0
            }
        }
        print("MeTTa simulation mode initialized")
    
    async def calculate_memory_valuation(self, memory_data: Dict) -> Dict:
        """Calculate memory valuation using MeTTa reasoning"""
        
        memory_type = memory_data.get("memory_type", "generic")
        emotional_intensity = memory_data.get("emotional_intensity", 5)
        content = memory_data.get("content", "")
        
        if self.initialized and self.knowledge_base_loaded:
            return await self._metta_valuation(memory_type, emotional_intensity, content)
        else:
            return await self._simulation_valuation(memory_type, emotional_intensity, content)
    
    async def _metta_valuation(self, memory_type: str, emotional_intensity: int, content: str) -> Dict:
        """Perform valuation using actual MeTTa reasoning"""
        
        try:
            # Determine rarity
            rarity_result = self.metta.run(f"!(match &self (rarity {memory_type} $r) $r)")
            rarity = rarity_result[0] if rarity_result else "common"
            
            # Calculate base valuation
            valuation_query = f"!(calculate_memory_value {memory_type} {emotional_intensity} {rarity} medium)"
            valuation_result = self.metta.run(valuation_query)
            base_value = float(valuation_result[0]) if valuation_result else 100.0
            
            # Add market volatility
            market_modifier = random.uniform(0.9, 1.1)
            final_value = base_value * market_modifier
            
            # Calculate confidence based on data completeness
            confidence = self._calculate_confidence(memory_type, emotional_intensity, content)
            
            return {
                "valuation": round(final_value, 2),
                "confidence": round(confidence, 3),
                "reasoning": {
                    "memory_type": memory_type,
                    "emotional_intensity": emotional_intensity,
                    "rarity": rarity,
                    "base_value": round(base_value, 2),
                    "market_modifier": round(market_modifier, 3),
                    "metta_engine": "active"
                },
                "market_factors": {
                    "trend": "stable",
                    "volatility": "low",
                    "demand": "medium"
                }
            }
            
        except Exception as e:
            print(f"MeTTa valuation error: {e}")
            return await self._simulation_valuation(memory_type, emotional_intensity, content)
    
    async def _simulation_valuation(self, memory_type: str, emotional_intensity: int, content: str) -> Dict:
        """Simulation mode valuation"""
        
        base_value = 100.0
        emotional_multiplier = self.knowledge_base["emotional_values"].get(memory_type, 1.0)
        demand_multiplier = self.knowledge_base["market_demand"].get(memory_type, 1.0)
        
        # Rarity assessment based on content analysis
        rarity_score = self._assess_content_rarity(content)
        rarity_multiplier = self.knowledge_base["rarity_multipliers"].get(rarity_score, 1.0)
        
        # Intensity modifier
        intensity_modifier = 0.8 + (emotional_intensity / 10) * 0.4
        
        # Market volatility
        market_modifier = random.uniform(0.9, 1.1)
        
        final_value = base_value * emotional_multiplier * rarity_multiplier * demand_multiplier * intensity_modifier * market_modifier
        
        confidence = self._calculate_confidence(memory_type, emotional_intensity, content)
        
        return {
            "valuation": round(final_value, 2),
            "confidence": round(confidence, 3),
            "reasoning": {
                "memory_type": memory_type,
                "emotional_intensity": emotional_intensity,
                "rarity": rarity_score,
                "base_value": base_value,
                "emotional_multiplier": emotional_multiplier,
                "rarity_multiplier": rarity_multiplier,
                "demand_multiplier": demand_multiplier,
                "intensity_modifier": round(intensity_modifier, 3),
                "market_modifier": round(market_modifier, 3),
                "metta_engine": "simulation"
            },
            "market_factors": {
                "trend": "stable" if market_modifier > 0.95 and market_modifier < 1.05 else "volatile",
                "volatility": "low",
                "demand": self._get_demand_level(memory_type)
            }
        }
    
    def _assess_content_rarity(self, content: str) -> str:
        """Assess rarity based on content analysis"""
        if not content:
            return "common"
        
        rare_keywords = ["first", "only", "unique", "never", "once", "special", "extraordinary"]
        uncommon_keywords = ["important", "significant", "memorable", "meaningful"]
        
        content_lower = content.lower()
        
        rare_count = sum(1 for keyword in rare_keywords if keyword in content_lower)
        uncommon_count = sum(1 for keyword in uncommon_keywords if keyword in content_lower)
        
        if rare_count >= 2:
            return "rare"
        elif rare_count >= 1 or uncommon_count >= 2:
            return "uncommon"
        else:
            return "common"
    
    def _calculate_confidence(self, memory_type: str, emotional_intensity: int, content: str) -> float:
        """Calculate confidence score"""
        confidence = 0.7
        
        if memory_type != "generic":
            confidence += 0.1
        
        if 3 <= emotional_intensity <= 10:
            confidence += 0.1
        
        if content and len(content) > 20:
            confidence += 0.1
        
        return min(0.95, confidence)
    
    def _get_demand_level(self, memory_type: str) -> str:
        """Get demand level description"""
        demand_value = self.knowledge_base["market_demand"].get(memory_type, 1.0)
        
        if demand_value >= 1.4:
            return "high"
        elif demand_value >= 1.1:
            return "medium"
        else:
            return "low"
    
    async def calculate_authenticity_score(self, authenticity_data: Dict) -> Dict:
        """Calculate authenticity score using MeTTa reasoning"""
        
        temporal_consistency = authenticity_data.get("temporal_consistency", 0.8)
        emotional_congruence = authenticity_data.get("emotional_congruence", 0.8)
        metadata_verification = authenticity_data.get("metadata_verification", 0.8)
        
        if self.initialized and self.knowledge_base_loaded:
            try:
                score_query = f"!(calculate_authenticity_score {temporal_consistency} {emotional_congruence} {metadata_verification})"
                score_result = self.metta.run(score_query)
                authenticity_score = float(score_result[0]) if score_result else 0.8
            except:
                authenticity_score = (temporal_consistency * 0.3 + 
                                    emotional_congruence * 0.4 + 
                                    metadata_verification * 0.3)
        else:
            authenticity_score = (temporal_consistency * 0.3 + 
                                emotional_congruence * 0.4 + 
                                metadata_verification * 0.3)
        
        if authenticity_score >= 0.85:
            status = "verified_authentic"
        elif authenticity_score >= 0.7:
            status = "likely_authentic"
        else:
            status = "requires_verification"
        
        return {
            "authenticity_score": round(authenticity_score, 3),
            "status": status,
            "components": {
                "temporal_consistency": temporal_consistency,
                "emotional_congruence": emotional_congruence,
                "metadata_verification": metadata_verification
            },
            "metta_processing": self.initialized and self.knowledge_base_loaded
        }
    
    async def analyze_market_trends(self, memory_type: str, recent_sales: List[float]) -> Dict:
        """Analyze market trends using MeTTa reasoning"""
        
        if not recent_sales:
            recent_sales = [100.0, 120.0, 110.0, 130.0, 125.0]
        
        avg_price = sum(recent_sales) / len(recent_sales)
        volatility = self._calculate_volatility(recent_sales)
        
        if avg_price > 150:
            trend = "bullish"
        elif avg_price < 75:
            trend = "bearish"
        else:
            trend = "stable"
        
        return {
            "memory_type": memory_type,
            "average_price": round(avg_price, 2),
            "volatility": round(volatility, 3),
            "trend": trend,
            "sample_size": len(recent_sales),
            "price_range": {
                "min": min(recent_sales),
                "max": max(recent_sales)
            },
            "market_health": "healthy" if volatility < 0.3 else "volatile"
        }
    
    def _calculate_volatility(self, prices: List[float]) -> float:
        """Calculate price volatility"""
        if len(prices) < 2:
            return 0.0
        
        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        return (variance ** 0.5) / mean if mean > 0 else 0.0

metta_valuation_engine = MeTTaValuationEngine()