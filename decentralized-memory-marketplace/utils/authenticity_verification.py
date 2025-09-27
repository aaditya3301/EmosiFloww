"""
Advanced Authenticity Verification System
Day 2 Afternoon Features: Multi-agent consensus, deepfake detection, metadata verification, emotional congruence
"""
import asyncio
import json
import hashlib
import re
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import math
import statistics

class AuthenticityLevel(Enum):
    """Levels of authenticity confidence"""
    VERIFIED = "verified"
    LIKELY_AUTHENTIC = "likely_authentic" 
    UNCERTAIN = "uncertain"
    LIKELY_FAKE = "likely_fake"
    FAKE_DETECTED = "fake_detected"

class ConsensusDecision(Enum):
    """Multi-agent consensus decisions"""
    UNANIMOUS_AUTHENTIC = "unanimous_authentic"
    MAJORITY_AUTHENTIC = "majority_authentic"
    SPLIT_DECISION = "split_decision"
    MAJORITY_FAKE = "majority_fake"
    UNANIMOUS_FAKE = "unanimous_fake"

@dataclass
class DeepfakeDetectionResult:
    """Results from deepfake detection analysis"""
    is_deepfake: bool
    confidence_score: float
    detection_method: str
    suspicious_patterns: List[str]
    technical_indicators: Dict[str, float]
    ai_generated_probability: float
    
@dataclass
class MetadataVerification:
    """Metadata verification analysis"""
    timestamp_authentic: bool
    location_consistent: bool
    device_fingerprint_valid: bool
    metadata_tampering_detected: bool
    creation_date_plausible: bool
    file_integrity_score: float
    verification_details: Dict[str, Any]

@dataclass
class EmotionalCongruenceAnalysis:
    """Emotional congruence between content and metadata"""
    emotional_consistency: float
    sentiment_alignment: float
    contextual_appropriateness: float
    psychological_plausibility: float
    narrative_coherence: float
    temporal_consistency: float
    overall_congruence: float

@dataclass
class ConsensusResult:
    """Multi-agent consensus system result"""
    consensus_decision: ConsensusDecision
    confidence_level: float
    participating_agents: List[str]
    individual_scores: Dict[str, float]
    agreement_percentage: float
    outlier_agents: List[str]
    consensus_reasoning: List[str]

@dataclass
class AuthenticityAssessment:
    """Complete authenticity assessment"""
    authenticity_level: AuthenticityLevel
    overall_confidence: float
    deepfake_analysis: DeepfakeDetectionResult
    metadata_verification: MetadataVerification
    emotional_congruence: EmotionalCongruenceAnalysis
    consensus_result: ConsensusResult
    risk_factors: List[str]
    recommendations: List[str]
    verification_timestamp: datetime

class AdvancedAuthenticityVerifier:
    """Advanced authenticity verification system with Day 2 Afternoon features"""
    
    def __init__(self):
        self.consensus_agents = [
            "authenticity_validator_primary",
            "metadata_analyzer", 
            "deepfake_detector",
            "emotional_analyzer",
            "pattern_recognizer",
            "integrity_checker"
        ]
        self.deepfake_patterns = self._load_deepfake_patterns()
        self.metadata_validators = self._initialize_metadata_validators()
        
    def _load_deepfake_patterns(self) -> Dict[str, List[str]]:
        """Load known deepfake detection patterns"""
        return {
            "linguistic_patterns": [
                "repetitive_phrases",
                "unnatural_transitions", 
                "inconsistent_voice",
                "generic_emotional_expressions",
                "ai_generated_text_markers"
            ],
            "technical_patterns": [
                "compression_artifacts",
                "pixel_inconsistencies",
                "temporal_anomalies",
                "metadata_gaps",
                "digital_fingerprint_mismatches"
            ],
            "behavioral_patterns": [
                "emotional_disconnect",
                "narrative_inconsistencies",
                "implausible_details",
                "timeline_contradictions",
                "context_mismatches"
            ]
        }
        
    def _initialize_metadata_validators(self) -> Dict[str, Any]:
        """Initialize metadata validation systems"""
        return {
            "timestamp_validator": True,
            "location_validator": True,
            "device_fingerprint_analyzer": True,
            "file_integrity_checker": True,
            "creation_metadata_analyzer": True
        }

    async def perform_deepfake_detection(self, memory_data: Dict[str, Any]) -> DeepfakeDetectionResult:
        """Day 2 Afternoon Feature: Advanced deepfake detection"""
        content = memory_data.get("content", "")
        metadata = memory_data.get("metadata", {})
        
        # Analyze linguistic patterns
        linguistic_score = await self._analyze_linguistic_patterns(content)
        
        # Analyze technical indicators
        technical_score = await self._analyze_technical_indicators(memory_data)
        
        # Analyze behavioral patterns
        behavioral_score = await self._analyze_behavioral_patterns(content, metadata)
        
        # Calculate overall AI generation probability
        ai_probability = (linguistic_score + technical_score + behavioral_score) / 3
        
        # Determine if deepfake
        is_deepfake = ai_probability > 0.7
        confidence = min(0.99, max(0.01, abs(ai_probability - 0.5) * 2))
        
        suspicious_patterns = []
        if linguistic_score > 0.6:
            suspicious_patterns.extend(["unnatural_language", "ai_text_markers"])
        if technical_score > 0.6:
            suspicious_patterns.extend(["technical_anomalies", "metadata_inconsistencies"])
        if behavioral_score > 0.6:
            suspicious_patterns.extend(["behavioral_inconsistencies", "narrative_gaps"])
            
        return DeepfakeDetectionResult(
            is_deepfake=is_deepfake,
            confidence_score=confidence,
            detection_method="multi_modal_analysis",
            suspicious_patterns=suspicious_patterns,
            technical_indicators={
                "linguistic_score": linguistic_score,
                "technical_score": technical_score,
                "behavioral_score": behavioral_score
            },
            ai_generated_probability=ai_probability
        )
        
    async def _analyze_linguistic_patterns(self, content: str) -> float:
        """Analyze linguistic patterns for AI generation"""
        indicators = 0
        total_checks = 8
        
        # Check for repetitive phrases
        words = content.lower().split()
        if len(set(words)) / len(words) < 0.6:
            indicators += 1
            
        # Check for AI-common phrases
        ai_phrases = ["absolutely", "incredible", "amazing", "profound", "overwhelming"]
        ai_count = sum(1 for phrase in ai_phrases if phrase in content.lower())
        if ai_count > 3:
            indicators += 1
            
        # Check for unnatural transitions
        sentences = content.split('.')
        if len(sentences) > 2:
            transition_words = ["however", "moreover", "furthermore", "additionally"]
            transition_count = sum(1 for sentence in sentences 
                                 for word in transition_words if word in sentence.lower())
            if transition_count > len(sentences) * 0.3:
                indicators += 1
                
        # Check for generic emotional expressions
        generic_emotions = ["happy", "sad", "excited", "wonderful", "beautiful"]
        emotion_count = sum(1 for emotion in generic_emotions if emotion in content.lower())
        if emotion_count > 2:
            indicators += 1
            
        # Check sentence structure uniformity
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        if sentence_lengths and statistics.stdev(sentence_lengths) < 2:
            indicators += 1
            
        # Check for perfect grammar (suspicious for personal memories)
        grammar_indicators = content.count(',') + content.count(';') + content.count(':')
        if grammar_indicators > len(content.split()) * 0.15:
            indicators += 1
            
        # Check for overly descriptive language
        descriptive_words = ["very", "extremely", "incredibly", "absolutely", "completely"]
        desc_count = sum(1 for word in descriptive_words if word in content.lower())
        if desc_count > len(content.split()) * 0.1:
            indicators += 1
            
        # Check for lack of personal details
        personal_indicators = ["i", "me", "my", "we", "us", "our"]
        personal_count = sum(1 for word in personal_indicators if word in content.lower())
        if personal_count < len(content.split()) * 0.05:
            indicators += 1
            
        return indicators / total_checks
        
    async def _analyze_technical_indicators(self, memory_data: Dict[str, Any]) -> float:
        """Analyze technical indicators for authenticity"""
        indicators = 0
        total_checks = 6
        
        metadata = memory_data.get("metadata", {})
        
        # Check metadata completeness (too complete is suspicious)
        metadata_fields = len(metadata)
        if metadata_fields > 10:  # Too many fields
            indicators += 1
            
        # Check for timestamp inconsistencies
        if "year" in metadata:
            year = metadata["year"]
            current_year = datetime.now().year
            if year > current_year or year < 1950:
                indicators += 1
                
        # Check for perfect metadata formatting
        string_values = [v for v in metadata.values() if isinstance(v, str)]
        if string_values and all(v.islower() or v.replace('_', '').isalnum() for v in string_values):
            indicators += 1
            
        # Check for suspiciously consistent data types
        value_types = [type(v).__name__ for v in metadata.values()]
        type_consistency = len(set(value_types)) / len(value_types) if value_types else 1
        if type_consistency < 0.3:  # Too consistent
            indicators += 1
            
        # Check for missing expected fields
        expected_fields = ["year", "location", "significance"]
        missing_expected = sum(1 for field in expected_fields if field not in metadata)
        if missing_expected == 0:  # Too perfect
            indicators += 1
            
        # Check for artificial precision in numerical values
        numeric_values = [v for v in metadata.values() if isinstance(v, (int, float))]
        if numeric_values and all(isinstance(v, int) for v in numeric_values):
            indicators += 1  # Real memories often have approximate values
            
        return indicators / total_checks
        
    async def _analyze_behavioral_patterns(self, content: str, metadata: Dict[str, Any]) -> float:
        """Analyze behavioral patterns for authenticity"""
        indicators = 0
        total_checks = 7
        
        # Check emotional-metadata consistency
        emotional_words = ["love", "joy", "sad", "angry", "fear", "happy", "excited"]
        emotion_count = sum(1 for word in emotional_words if word in content.lower())
        significance = metadata.get("significance", "low")
        
        if emotion_count > 3 and significance == "low":
            indicators += 1
        elif emotion_count < 1 and significance in ["high", "very_high"]:
            indicators += 1
            
        # Check for narrative coherence
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        if len(sentences) > 2:
            # Check if sentences logically flow
            conjunctions = ["and", "but", "so", "because", "then", "after", "before"]
            conjunction_count = sum(1 for sentence in sentences[1:] 
                                  for conj in conjunctions if sentence.lower().startswith(conj))
            if conjunction_count < len(sentences) * 0.2:
                indicators += 1
                
        # Check temporal consistency
        if "year" in metadata:
            year = metadata["year"]
            # Check if memory type matches typical age
            memory_type = metadata.get("memory_type", "")
            if memory_type == "childhood_experience" and year > 2010:
                # Assuming adult user, childhood should be older
                indicators += 1
                
        # Check for implausible details
        superlatives = ["best", "worst", "most", "greatest", "perfect", "incredible"]
        superlative_count = sum(1 for word in superlatives if word in content.lower())
        if superlative_count > len(content.split()) * 0.08:
            indicators += 1
            
        # Check context-location consistency
        location = metadata.get("location", "").lower()
        if location and location in content.lower():
            # Good consistency
            pass
        elif location and location not in content.lower():
            indicators += 1  # Location mentioned in metadata but not content
            
        # Check for personal pronoun usage
        personal_pronouns = content.lower().count("i ") + content.lower().count("my ") + content.lower().count("me ")
        total_words = len(content.split())
        pronoun_ratio = personal_pronouns / total_words if total_words > 0 else 0
        if pronoun_ratio < 0.02:  # Too few personal references
            indicators += 1
            
        # Check memory specificity
        specific_words = ["remember", "recall", "think", "believe", "feel like", "seems"]
        specificity_count = sum(1 for word in specific_words if word in content.lower())
        if specificity_count == 0 and len(content.split()) > 20:
            indicators += 1  # Too certain for a memory
            
        return indicators / total_checks

    async def verify_metadata_integrity(self, memory_data: Dict[str, Any]) -> MetadataVerification:
        """Day 2 Afternoon Feature: Comprehensive metadata verification"""
        metadata = memory_data.get("metadata", {})
        
        # Timestamp authenticity
        timestamp_authentic = await self._verify_timestamp(metadata)
        
        # Location consistency  
        location_consistent = await self._verify_location(memory_data)
        
        # Device fingerprint validation
        device_valid = await self._verify_device_fingerprint(metadata)
        
        # Tampering detection
        tampering_detected = await self._detect_metadata_tampering(metadata)
        
        # Creation date plausibility
        creation_plausible = await self._verify_creation_date(metadata)
        
        # File integrity score
        integrity_score = await self._calculate_file_integrity(memory_data)
        
        verification_details = {
            "total_fields": len(metadata),
            "suspicious_fields": [],
            "confidence_indicators": [],
            "warning_flags": []
        }
        
        # Add suspicious fields
        for key, value in metadata.items():
            if isinstance(value, str) and len(value) > 100:
                verification_details["suspicious_fields"].append(f"{key}_too_long")
            if isinstance(value, bool) and key not in ["life_changing", "family", "significant"]:
                verification_details["suspicious_fields"].append(f"{key}_unexpected_boolean")
                
        return MetadataVerification(
            timestamp_authentic=timestamp_authentic,
            location_consistent=location_consistent,
            device_fingerprint_valid=device_valid,
            metadata_tampering_detected=tampering_detected,
            creation_date_plausible=creation_plausible,
            file_integrity_score=integrity_score,
            verification_details=verification_details
        )
        
    async def _verify_timestamp(self, metadata: Dict[str, Any]) -> bool:
        """Verify timestamp authenticity"""
        if "year" not in metadata:
            return False
            
        year = metadata["year"]
        current_year = datetime.now().year
        
        # Basic range check
        if year < 1950 or year > current_year:
            return False
            
        # Check for suspiciously round numbers
        if year % 10 == 0 and "decade" not in str(metadata.get("significance", "")):
            return True  # Round years are actually common for memories
            
        return True
        
    async def _verify_location(self, memory_data: Dict[str, Any]) -> bool:
        """Verify location consistency"""
        metadata = memory_data.get("metadata", {})
        content = memory_data.get("content", "")
        
        location = metadata.get("location", "").lower()
        if not location:
            return True  # No location to verify
            
        # Check if location context makes sense
        location_words = location.split()
        content_lower = content.lower()
        
        # Location should have some reference in content or be generic enough
        location_references = sum(1 for word in location_words if word in content_lower)
        if len(location_words) > 1 and location_references == 0:
            return False  # Specific location not mentioned in content
            
        return True
        
    async def _verify_device_fingerprint(self, metadata: Dict[str, Any]) -> bool:
        """Verify device fingerprint if present"""
        # For simulation - in real implementation would check actual device data
        return True
        
    async def _detect_metadata_tampering(self, metadata: Dict[str, Any]) -> bool:
        """Detect if metadata has been tampered with"""
        tampering_indicators = 0
        
        # Check for inconsistent data types
        if "year" in metadata and not isinstance(metadata["year"], int):
            tampering_indicators += 1
            
        # Check for suspiciously perfect data
        string_fields = [v for v in metadata.values() if isinstance(v, str)]
        if len(string_fields) > 3 and all(v.replace('_', '').isalnum() for v in string_fields):
            tampering_indicators += 1
            
        # Check for unusual field combinations
        if len(metadata) > 8:  # Too many fields is suspicious
            tampering_indicators += 1
            
        return tampering_indicators > 1
        
    async def _verify_creation_date(self, metadata: Dict[str, Any]) -> bool:
        """Verify creation date plausibility"""
        year = metadata.get("year")
        if not year:
            return True
            
        # Memory should be from the past
        return year <= datetime.now().year
        
    async def _calculate_file_integrity(self, memory_data: Dict[str, Any]) -> float:
        """Calculate file integrity score"""
        integrity_factors = []
        
        # Content-metadata consistency
        content = memory_data.get("content", "")
        metadata = memory_data.get("metadata", {})
        
        if content and metadata:
            integrity_factors.append(0.8)  # Basic consistency
            
        # Check for expected fields
        expected_fields = ["memory_type", "content"]
        present_fields = sum(1 for field in expected_fields if field in memory_data)
        integrity_factors.append(present_fields / len(expected_fields))
        
        # Metadata reasonableness
        if metadata:
            reasonable_field_count = 3 <= len(metadata) <= 8
            integrity_factors.append(0.9 if reasonable_field_count else 0.6)
            
        return statistics.mean(integrity_factors) if integrity_factors else 0.5

    async def analyze_emotional_congruence(self, memory_data: Dict[str, Any]) -> EmotionalCongruenceAnalysis:
        """Day 2 Afternoon Feature: Emotional congruence analysis"""
        content = memory_data.get("content", "")
        metadata = memory_data.get("metadata", {})
        
        # Emotional consistency between content and metadata
        emotional_consistency = await self._analyze_emotional_consistency(content, metadata)
        
        # Sentiment alignment
        sentiment_alignment = await self._analyze_sentiment_alignment(content, metadata)
        
        # Contextual appropriateness
        contextual_appropriateness = await self._analyze_contextual_appropriateness(memory_data)
        
        # Psychological plausibility
        psychological_plausibility = await self._analyze_psychological_plausibility(content, metadata)
        
        # Narrative coherence
        narrative_coherence = await self._analyze_narrative_coherence(content)
        
        # Temporal consistency
        temporal_consistency = await self._analyze_temporal_consistency(memory_data)
        
        # Overall congruence
        scores = [
            emotional_consistency, sentiment_alignment, contextual_appropriateness,
            psychological_plausibility, narrative_coherence, temporal_consistency
        ]
        overall_congruence = statistics.mean(scores)
        
        return EmotionalCongruenceAnalysis(
            emotional_consistency=emotional_consistency,
            sentiment_alignment=sentiment_alignment,
            contextual_appropriateness=contextual_appropriateness,
            psychological_plausibility=psychological_plausibility,
            narrative_coherence=narrative_coherence,
            temporal_consistency=temporal_consistency,
            overall_congruence=overall_congruence
        )
        
    async def _analyze_emotional_consistency(self, content: str, metadata: Dict[str, Any]) -> float:
        """Analyze consistency between emotional content and metadata"""
        # Extract emotional indicators from content
        positive_emotions = ["happy", "joy", "love", "excited", "wonderful", "amazing", "beautiful"]
        negative_emotions = ["sad", "angry", "fear", "terrible", "awful", "horrible", "devastating"]
        
        content_lower = content.lower()
        positive_count = sum(1 for emotion in positive_emotions if emotion in content_lower)
        negative_count = sum(1 for emotion in negative_emotions if emotion in content_lower)
        
        # Determine content sentiment
        if positive_count > negative_count:
            content_sentiment = "positive"
        elif negative_count > positive_count:
            content_sentiment = "negative"
        else:
            content_sentiment = "neutral"
            
        # Check metadata indicators
        significance = metadata.get("significance", "medium")
        life_changing = metadata.get("life_changing", False)
        memory_type = metadata.get("memory_type", "")
        
        # Memory types that typically have specific sentiments
        positive_types = ["achievement", "first_love", "family_moment", "celebration"]
        negative_types = ["loss_grief", "trauma", "failure"]
        
        # Calculate consistency
        consistency_score = 0.5  # baseline
        
        if memory_type in positive_types and content_sentiment == "positive":
            consistency_score += 0.3
        elif memory_type in negative_types and content_sentiment == "negative":
            consistency_score += 0.3
        elif memory_type in positive_types and content_sentiment == "negative":
            consistency_score -= 0.2
        elif memory_type in negative_types and content_sentiment == "positive":
            consistency_score -= 0.2
            
        if life_changing and (positive_count + negative_count) > 0:
            consistency_score += 0.1
        elif life_changing and (positive_count + negative_count) == 0:
            consistency_score -= 0.1
            
        if significance in ["high", "very_high"] and (positive_count + negative_count) > 1:
            consistency_score += 0.1
            
        return max(0.0, min(1.0, consistency_score))
        
    async def _analyze_sentiment_alignment(self, content: str, metadata: Dict[str, Any]) -> float:
        """Analyze sentiment alignment between content and context"""
        # Simple sentiment analysis
        words = content.lower().split()
        positive_words = ["good", "great", "happy", "love", "wonderful", "amazing", "beautiful", "perfect", "incredible"]
        negative_words = ["bad", "terrible", "sad", "hate", "awful", "horrible", "devastating", "painful"]
        
        positive_score = sum(1 for word in words if word in positive_words)
        negative_score = sum(1 for word in words if word in negative_words)
        total_words = len(words)
        
        if total_words == 0:
            return 0.5
            
        sentiment_intensity = (positive_score + negative_score) / total_words
        
        # Check if sentiment intensity matches memory significance
        significance = metadata.get("significance", "medium")
        expected_intensity = {"low": 0.02, "medium": 0.05, "high": 0.08, "very_high": 0.12}
        
        expected = expected_intensity.get(significance, 0.05)
        intensity_match = 1.0 - abs(sentiment_intensity - expected) / expected if expected > 0 else 0.5
        
        return max(0.0, min(1.0, intensity_match))
        
    async def _analyze_contextual_appropriateness(self, memory_data: Dict[str, Any]) -> float:
        """Analyze if content is appropriate for the context"""
        content = memory_data.get("content", "")
        metadata = memory_data.get("metadata", {})
        memory_type = metadata.get("memory_type", "")
        
        # Check content length appropriateness
        content_length = len(content.split())
        
        # Expected lengths for different memory types
        expected_lengths = {
            "childhood_experience": (10, 50),
            "first_love": (15, 60),
            "achievement": (10, 40),
            "family_moment": (10, 45),
            "travel_experience": (15, 55),
            "loss_grief": (10, 50),
            "creative_breakthrough": (12, 45)
        }
        
        if memory_type in expected_lengths:
            min_len, max_len = expected_lengths[memory_type]
            if min_len <= content_length <= max_len:
                length_score = 1.0
            else:
                deviation = min(abs(content_length - min_len), abs(content_length - max_len))
                length_score = max(0.0, 1.0 - deviation / max_len)
        else:
            length_score = 0.8  # Unknown type, give benefit of doubt
            
        # Check vocabulary appropriateness
        sophisticated_words = ["profound", "transcendent", "paradigm", "quintessential", "juxtaposition"]
        sophisticated_count = sum(1 for word in sophisticated_words if word in content.lower())
        
        # Personal memories shouldn't be too sophisticated unless it's a creative breakthrough
        if memory_type == "creative_breakthrough":
            vocab_score = 1.0
        elif sophisticated_count > 2:
            vocab_score = 0.6  # Too sophisticated for typical personal memory
        else:
            vocab_score = 1.0
            
        return (length_score + vocab_score) / 2
        
    async def _analyze_psychological_plausibility(self, content: str, metadata: Dict[str, Any]) -> float:
        """Analyze psychological plausibility of the memory"""
        plausibility_score = 0.8  # Start optimistic
        
        # Check for psychological consistency
        memory_type = metadata.get("memory_type", "")
        year = metadata.get("year", datetime.now().year)
        current_year = datetime.now().year
        memory_age = current_year - year
        
        # Memories should show some uncertainty for older events
        certainty_words = ["exactly", "precisely", "definitely", "certainly", "absolutely"]
        certainty_count = sum(1 for word in certainty_words if word in content.lower())
        
        if memory_age > 10 and certainty_count > 2:
            plausibility_score -= 0.2  # Too certain for old memory
            
        # Check for appropriate emotional processing
        if memory_type in ["loss_grief", "trauma"]:
            processing_words = ["learned", "grew", "understand", "realize", "helped"]
            processing_count = sum(1 for word in processing_words if word in content.lower())
            if processing_count > 0:
                plausibility_score += 0.1  # Shows healthy processing
                
        # Check for realistic detail level
        specific_details = content.count(',') + content.count(';')
        total_sentences = len([s for s in content.split('.') if s.strip()])
        
        if total_sentences > 0:
            detail_ratio = specific_details / total_sentences
            if detail_ratio > 3:  # Too many details
                plausibility_score -= 0.1
                
        return max(0.0, min(1.0, plausibility_score))
        
    async def _analyze_narrative_coherence(self, content: str) -> float:
        """Analyze narrative coherence of the memory"""
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        if len(sentences) < 2:
            return 0.8  # Short content, hard to judge
            
        coherence_score = 0.7  # Base score
        
        # Check for logical flow
        transition_words = ["then", "after", "before", "when", "while", "because", "so", "but", "and"]
        transitions = sum(1 for sentence in sentences[1:] 
                         for word in transition_words 
                         if sentence.lower().startswith(word))
        
        if transitions > 0:
            coherence_score += min(0.2, transitions * 0.1)
            
        # Check for consistent tense
        past_tense_indicators = ["was", "were", "had", "did", "went", "came", "felt"]
        present_tense_indicators = ["is", "are", "have", "do", "go", "come", "feel"]
        
        past_count = sum(1 for indicator in past_tense_indicators if indicator in content.lower())
        present_count = sum(1 for indicator in present_tense_indicators if indicator in content.lower())
        
        total_tense = past_count + present_count
        if total_tense > 0:
            tense_consistency = max(past_count, present_count) / total_tense
            coherence_score += (tense_consistency - 0.5) * 0.2
            
        return max(0.0, min(1.0, coherence_score))
        
    async def _analyze_temporal_consistency(self, memory_data: Dict[str, Any]) -> float:
        """Analyze temporal consistency of the memory"""
        content = memory_data.get("content", "")
        metadata = memory_data.get("metadata", {})
        
        year = metadata.get("year")
        memory_type = metadata.get("memory_type", "")
        
        if not year:
            return 0.6  # No temporal data to check
            
        consistency_score = 0.8  # Base score
        current_year = datetime.now().year
        memory_age = current_year - year
        
        # Check age-appropriate memory types
        age_appropriate = {
            "childhood_experience": memory_age > 15,  # Assuming adult user
            "first_love": memory_age > 5,
            "achievement": memory_age >= 0,
            "family_moment": memory_age >= 0
        }
        
        if memory_type in age_appropriate:
            if age_appropriate[memory_type]:
                consistency_score += 0.1
            else:
                consistency_score -= 0.2
                
        # Check for anachronisms
        modern_terms = ["internet", "smartphone", "social media", "wifi", "app", "online"]
        modern_count = sum(1 for term in modern_terms if term in content.lower())
        
        if year < 2000 and modern_count > 0:
            consistency_score -= modern_count * 0.1
        elif year < 1990 and modern_count > 0:
            consistency_score -= modern_count * 0.2
            
        return max(0.0, min(1.0, consistency_score))

    async def run_multi_agent_consensus(self, memory_data: Dict[str, Any], 
                                      authenticity_scores: Dict[str, float]) -> ConsensusResult:
        """Day 2 Afternoon Feature: Multi-agent consensus system"""
        
        # Simulate individual agent assessments
        agent_scores = {}
        for agent in self.consensus_agents:
            agent_scores[agent] = await self._simulate_agent_assessment(agent, memory_data, authenticity_scores)
            
        # Calculate consensus metrics
        scores = list(agent_scores.values())
        mean_score = statistics.mean(scores)
        score_std = statistics.stdev(scores) if len(scores) > 1 else 0
        
        # Determine consensus decision
        authentic_votes = sum(1 for score in scores if score > 0.7)
        fake_votes = sum(1 for score in scores if score < 0.3)
        uncertain_votes = len(scores) - authentic_votes - fake_votes
        
        if authentic_votes == len(scores):
            consensus_decision = ConsensusDecision.UNANIMOUS_AUTHENTIC
        elif authentic_votes > len(scores) / 2:
            consensus_decision = ConsensusDecision.MAJORITY_AUTHENTIC
        elif fake_votes == len(scores):
            consensus_decision = ConsensusDecision.UNANIMOUS_FAKE
        elif fake_votes > len(scores) / 2:
            consensus_decision = ConsensusDecision.MAJORITY_FAKE
        else:
            consensus_decision = ConsensusDecision.SPLIT_DECISION
            
        # Calculate agreement percentage
        if consensus_decision in [ConsensusDecision.UNANIMOUS_AUTHENTIC, ConsensusDecision.UNANIMOUS_FAKE]:
            agreement_percentage = 100.0
        else:
            majority_count = max(authentic_votes, fake_votes, uncertain_votes)
            agreement_percentage = (majority_count / len(scores)) * 100
            
        # Identify outlier agents
        outliers = []
        for agent, score in agent_scores.items():
            if abs(score - mean_score) > 2 * score_std and score_std > 0.1:
                outliers.append(agent)
                
        # Generate consensus reasoning
        reasoning = []
        if authentic_votes > fake_votes:
            reasoning.append(f"{authentic_votes}/{len(scores)} agents indicate authenticity")
        if fake_votes > authentic_votes:
            reasoning.append(f"{fake_votes}/{len(scores)} agents detect potential fakery")
        if score_std < 0.1:
            reasoning.append("High agreement among consensus agents")
        elif score_std > 0.3:
            reasoning.append("Significant disagreement requires human review")
            
        confidence_level = max(0.1, min(0.99, 1.0 - score_std))
        
        return ConsensusResult(
            consensus_decision=consensus_decision,
            confidence_level=confidence_level,
            participating_agents=self.consensus_agents,
            individual_scores=agent_scores,
            agreement_percentage=agreement_percentage,
            outlier_agents=outliers,
            consensus_reasoning=reasoning
        )
        
    async def _simulate_agent_assessment(self, agent_name: str, memory_data: Dict[str, Any], 
                                       base_scores: Dict[str, float]) -> float:
        """Simulate individual agent assessment with specialization"""
        
        # Each agent has different strengths and focuses
        agent_specializations = {
            "authenticity_validator_primary": {"weight": 1.0, "focus": "general"},
            "metadata_analyzer": {"weight": 1.2, "focus": "metadata"},
            "deepfake_detector": {"weight": 1.3, "focus": "ai_detection"},
            "emotional_analyzer": {"weight": 1.1, "focus": "emotional"},
            "pattern_recognizer": {"weight": 1.0, "focus": "patterns"},
            "integrity_checker": {"weight": 1.1, "focus": "integrity"}
        }
        
        spec = agent_specializations.get(agent_name, {"weight": 1.0, "focus": "general"})
        base_score = statistics.mean(base_scores.values())
        
        # Apply agent-specific modifications
        if spec["focus"] == "metadata" and "metadata_score" in base_scores:
            agent_score = base_scores["metadata_score"] * spec["weight"]
        elif spec["focus"] == "ai_detection" and "deepfake_score" in base_scores:
            agent_score = base_scores["deepfake_score"] * spec["weight"]
        elif spec["focus"] == "emotional" and "emotional_score" in base_scores:
            agent_score = base_scores["emotional_score"] * spec["weight"]
        else:
            agent_score = base_score * spec["weight"]
            
        # Add small random variation to simulate real agent differences
        import random
        variation = random.uniform(-0.05, 0.05)
        agent_score = max(0.0, min(1.0, agent_score + variation))
        
        return agent_score

    async def perform_comprehensive_authenticity_assessment(self, memory_data: Dict[str, Any]) -> AuthenticityAssessment:
        """Perform comprehensive Day 2 Afternoon authenticity assessment"""
        
        # Run all analysis components
        deepfake_analysis = await self.perform_deepfake_detection(memory_data)
        metadata_verification = await self.verify_metadata_integrity(memory_data)
        emotional_congruence = await self.analyze_emotional_congruence(memory_data)
        
        # Compile scores for consensus
        authenticity_scores = {
            "deepfake_score": 1.0 - deepfake_analysis.ai_generated_probability,
            "metadata_score": metadata_verification.file_integrity_score,
            "emotional_score": emotional_congruence.overall_congruence
        }
        
        # Run multi-agent consensus
        consensus_result = await self.run_multi_agent_consensus(memory_data, authenticity_scores)
        
        # Calculate overall confidence
        component_confidences = [
            deepfake_analysis.confidence_score,
            metadata_verification.file_integrity_score,
            emotional_congruence.overall_congruence,
            consensus_result.confidence_level
        ]
        overall_confidence = statistics.mean(component_confidences)
        
        # Determine authenticity level
        consensus_score = statistics.mean(list(consensus_result.individual_scores.values()))
        
        if consensus_score > 0.9 and overall_confidence > 0.8:
            authenticity_level = AuthenticityLevel.VERIFIED
        elif consensus_score > 0.7:
            authenticity_level = AuthenticityLevel.LIKELY_AUTHENTIC
        elif consensus_score < 0.3:
            authenticity_level = AuthenticityLevel.LIKELY_FAKE
        elif deepfake_analysis.is_deepfake and deepfake_analysis.confidence_score > 0.8:
            authenticity_level = AuthenticityLevel.FAKE_DETECTED
        else:
            authenticity_level = AuthenticityLevel.UNCERTAIN
            
        # Identify risk factors
        risk_factors = []
        if deepfake_analysis.is_deepfake:
            risk_factors.extend(deepfake_analysis.suspicious_patterns)
        if metadata_verification.metadata_tampering_detected:
            risk_factors.append("metadata_tampering_detected")
        if emotional_congruence.overall_congruence < 0.5:
            risk_factors.append("emotional_incongruence")
        if consensus_result.consensus_decision == ConsensusDecision.SPLIT_DECISION:
            risk_factors.append("consensus_disagreement")
            
        # Generate recommendations
        recommendations = []
        if authenticity_level == AuthenticityLevel.UNCERTAIN:
            recommendations.append("Request additional verification from memory creator")
        if len(risk_factors) > 2:
            recommendations.append("Require human expert review before marketplace listing")
        if deepfake_analysis.ai_generated_probability > 0.6:
            recommendations.append("Flag for AI-generated content review")
        if metadata_verification.file_integrity_score < 0.6:
            recommendations.append("Request original source files and metadata")
            
        return AuthenticityAssessment(
            authenticity_level=authenticity_level,
            overall_confidence=overall_confidence,
            deepfake_analysis=deepfake_analysis,
            metadata_verification=metadata_verification,
            emotional_congruence=emotional_congruence,
            consensus_result=consensus_result,
            risk_factors=risk_factors,
            recommendations=recommendations,
            verification_timestamp=datetime.now(timezone.utc)
        )

# Global authenticity verifier instance
advanced_authenticity_verifier = AdvancedAuthenticityVerifier()

async def perform_comprehensive_authenticity_check(memory_data: Dict[str, Any]) -> AuthenticityAssessment:
    """Main function for Day 2 Afternoon authenticity verification"""
    return await advanced_authenticity_verifier.perform_comprehensive_authenticity_assessment(memory_data)