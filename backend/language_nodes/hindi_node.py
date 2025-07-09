"""
Hindi Language Node
Enhanced node for processing Hindi queries with real-world data integration
"""

import asyncio
import logging
import re
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .base_node import BaseLanguageNode

logger = logging.getLogger(__name__)

class HindiNode(BaseLanguageNode):
    """
    Enhanced Hindi language federated learning node with real-world data integration
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("hi", config or {})
        
        # Initialize real-world data integration
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from core.real_world_data import GoogleCSEIntegration, RealWorldDataAggregator
            
            self.google_cse = GoogleCSEIntegration()
            self.real_world_aggregator = RealWorldDataAggregator(self.google_cse)
            self.real_world_enabled = True
            logger.info("✅ Real-world data integration enabled for Hindi Node")
        except Exception as e:
            logger.warning(f"⚠️ Real-world data integration disabled: {e}")
            self.real_world_enabled = False
        
        # Hindi-specific configurations
        self.script_patterns = {
            "devanagari": re.compile(r'[\u0900-\u097F]+'),
            "roman": re.compile(r'[a-zA-Z]+')
        }
        
        # Cultural knowledge domains
        self.cultural_domains = [
            "festivals", "food", "healthcare", "education", 
            "traditions", "business", "government"
        ]
        
        # Performance tracking
        self.performance_metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "real_world_queries": 0,
            "average_response_time": 0,
            "total_response_time": 0
        }
        
    async def _load_cultural_context(self):
        """Load Hindi/Indian cultural context"""
        logger.info("Loading Hindi cultural context...")
        
        self.cultural_context = {
            "festivals": {
                "दिवाली": {
                    "english": "Diwali",
                    "significance": "Festival of Lights, celebrating victory of light over darkness",
                    "timing": "October/November (Hindu calendar: Kartik Amavasya)",
                    "traditions": [
                        "घर की सफाई और सजावट",
                        "दीये और मोमबत्तियां जलाना", 
                        "रंगोली बनाना",
                        "मिठाइयां बांटना",
                        "लक्ष्मी पूजा"
                    ],
                    "regional_variations": {
                        "उत्तर भारत": "5 दिन का त्योहार, धनतेरस से भाई दूज तक",
                        "दक्षिण भारत": "नरक चतुर्दशी पर मुख्य उत्सव",
                        "पश्चिम भारत": "गुजराती नव वर्ष के साथ मनाया जाता है"
                    }
                },
                "होली": {
                    "english": "Holi", 
                    "significance": "Festival of Colors, celebrating spring and love",
                    "timing": "March (Hindu calendar: Phalguna Purnima)",
                    "traditions": [
                        "रंग खेलना",
                        "गुजिया और ठंडाई",
                        "होलिका दहन",
                        "मस्ती और उत्सव"
                    ]
                },
                "करवा चौथ": {
                    "english": "Karva Chauth",
                    "significance": "Fast observed by married women for husband's long life",
                    "timing": "October/November (Kartik Krishna Chaturthi)",
                    "traditions": [
                        "चांद देखकर व्रत खोलना",
                        "सुहागन का श्रृंगार",
                        "करवा चौथ की कथा"
                    ]
                }
            },
            
            "food": {
                "पारंपरिक व्यंजन": {
                    "उत्तर भारतीय": [
                        "रोटी", "नान", "पराठा", "राजमा", "छोले", "दाल मखनी",
                        "बिरयानी", "पुलाव", "आलू गोभी", "पनीर मखनी"
                    ],
                    "दक्षिण भारतीय": [
                        "डोसा", "इडली", "वडा", "उत्तपम", "रसम", "सांबर", 
                        "नारियल चटनी", "मीनाक्षी भात"
                    ],
                    "मिठाइयां": [
                        "गुलाब जामुन", "रसगुल्ला", "जलेबी", "खीर", "हलवा",
                        "बर्फी", "लड्डू", "रसमलाई"
                    ]
                },
                "त्योहारी खाना": {
                    "दिवाली": ["गुजिया", "शकरपारे", "नमकीन", "मिठाइयां"],
                    "होली": ["गुजिया", "ठंडाई", "दही भल्ले"],
                    "करवा चौथ": ["सरगी", "फेनी", "मिठाइयां"]
                }
            },
            
            "healthcare": {
                "घरेलू नुस्खे": {
                    "सर्दी-खांसी": [
                        "अदरक और शहद का काढ़ा",
                        "तुलसी की पत्तियों का रस",
                        "गर्म पानी में नमक के गरारे",
                        "हल्दी वाला दूध"
                    ],
                    "बुखार": [
                        "तुलसी और काली मिर्च का काढ़ा", 
                        "गिलोय का रस",
                        "नीम की पत्तियों का काढ़ा"
                    ],
                    "पेट दर्द": [
                        "अजवाइन का पानी",
                        "पुदीने की चाय",
                        "हींग और गुड़ का मिश्रण"
                    ]
                },
                "आयुर्वेदिक सिद्धांत": {
                    "त्रिदोष": ["वात", "पित्त", "कफ"],
                    "षड्रस": ["मधुर", "अम्ल", "लवण", "कटु", "तिक्त", "कषाय"],
                    "दिनचर्या": ["ब्रह्ममुहूर्त जागना", "योग और प्राणायाम", "संतुलित आहार"]
                }
            },
            
            "education": {
                "पारंपरिक शिक्षा": {
                    "गुरुकुल प्रणाली": "गुरु-शिष्य परंपरा",
                    "वेदाध्ययन": "चार वेद - ऋग्वेद, यजुर्वेद, सामवेद, अथर्ववेद",
                    "धर्म और नैतिकता": "सत्य, अहिंसा, करुणा"
                },
                "आधुनिक शिक्षा": {
                    "भाषा": "हिंदी, अंग्रेजी, क्षेत्रीय भाषाएं",
                    "विषय": "गणित, विज्ञान, सामाजिक अध्ययन",
                    "बोर्ड": "CBSE, ICSE, राज्य बोर्ड"
                }
            },
            
            "government_schemes": {
                "केंद्र सरकार": {
                    "प्रधानमंत्री आवास योजना": "गरीबों के लिए पक्के मकान",
                    "जन धन योजना": "बैंक खाते खोलना",
                    "आयुष्मान भारत": "स्वास्थ्य बीमा योजना",
                    "किसान सम्मान निधि": "किसानों को आर्थिक सहायता"
                }
            }
        }
        
        logger.info("Hindi cultural context loaded successfully")
        
    async def process_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Enhanced Hindi search query processing with real-world data"""
        start_time = time.time()
        self.performance_metrics["total_queries"] += 1
        
        try:
            logger.info(f"Processing Hindi query: {query[:50]}...")
            
            # 1. Detect script and language validation
            script_info = await self._detect_script(query)
            
            # 2. Extract cultural context
            cultural_context = await self._detect_cultural_context(query)
            
            # 3. Process query based on intent
            intent = await self._classify_intent(query)
            
            # 4. Determine if real-world data is needed
            needs_real_world_data = await self._should_fetch_real_world_data(query, intent, cultural_context)
            
            # 5. Get real-world data if needed and available
            real_world_data = None
            if needs_real_world_data and self.real_world_enabled:
                try:
                    self.performance_metrics["real_world_queries"] += 1
                    real_world_data = self.real_world_aggregator.get_real_world_context(
                        query, 'hindi', cultural_context
                    )
                except Exception as e:
                    logger.warning(f"Real-world data fetch failed: {e}")
            
            # 6. Generate culturally-aware response
            response = await self._generate_enhanced_response(query, intent, cultural_context, real_world_data)
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000
            
            # Update metrics
            self._update_metrics(True, response_time)
            
            # Store query for learning
            self.query_history.append({
                "query": query,
                "timestamp": start_time,
                "intent": intent,
                "cultural_context": cultural_context,
                "has_real_world_data": real_world_data is not None,
                "response_time_ms": response_time
            })
            
            result = {
                "query": query,
                "language": "hindi",
                "script": script_info,
                "intent": intent,
                "cultural_context": cultural_context,
                "real_world_data": real_world_data,
                "response": response,
                "confidence": self._calculate_confidence(cultural_context, real_world_data),
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.fromtimestamp(start_time).isoformat(),
                "node_id": "hindi_node_enhanced"
            }
            
            self.performance_metrics["successful_queries"] += 1
            logger.info(f"✅ Successfully processed Hindi query in {response_time:.2f}ms")
            
            return result
            
        except Exception as e:
            # Update metrics for failed query
            response_time = (time.time() - start_time) * 1000
            self._update_metrics(False, response_time)
            
            logger.error(f"Error processing Hindi query: {e}")
            return {
                "error": str(e),
                "query": query,
                "language": "hindi",
                "timestamp": datetime.now().isoformat(),
                "response_time_ms": round(response_time, 2)
            }
            
    async def _detect_script(self, query: str) -> Dict[str, Any]:
        """Detect script used in query"""
        devanagari_chars = len(self.script_patterns["devanagari"].findall(query))
        roman_chars = len(self.script_patterns["roman"].findall(query))
        
        total_chars = len(query.replace(" ", ""))
        
        if total_chars == 0:
            return {"primary_script": "unknown", "devanagari_ratio": 0, "roman_ratio": 0}
            
        devanagari_ratio = devanagari_chars / total_chars
        roman_ratio = roman_chars / total_chars
        
        primary_script = "devanagari" if devanagari_ratio > roman_ratio else "roman"
        
        return {
            "primary_script": primary_script,
            "devanagari_ratio": round(devanagari_ratio, 2),
            "roman_ratio": round(roman_ratio, 2),
            "mixed_script": devanagari_ratio > 0.1 and roman_ratio > 0.1
        }
        
    async def _detect_cultural_context(self, query: str) -> Dict[str, Any]:
        """Detect cultural context in Hindi query"""
        context = {
            "festivals": [],
            "food_items": [],
            "healthcare_topics": [],
            "government_schemes": [],
            "cultural_significance": []
        }
        
        query_lower = query.lower()
        
        # Festival detection
        for festival, info in self.cultural_context["festivals"].items():
            if festival in query_lower or info["english"].lower() in query_lower:
                context["festivals"].append({
                    "name": festival,
                    "english": info["english"],
                    "significance": info["significance"]
                })
                
        # Food item detection
        for category, items in self.cultural_context["food"]["पारंपरिक व्यंजन"].items():
            for item in items:
                if item in query_lower:
                    context["food_items"].append({
                        "item": item,
                        "category": category
                    })
                    
        # Healthcare topic detection
        for condition, remedies in self.cultural_context["healthcare"]["घरेलू नुस्खे"].items():
            if any(keyword in query_lower for keyword in condition.split()):
                context["healthcare_topics"].append({
                    "condition": condition,
                    "remedies": remedies
                })
                
        # Government scheme detection
        for scheme in self.cultural_context["government_schemes"]["केंद्र सरकार"].keys():
            if any(word in query_lower for word in scheme.split()):
                context["government_schemes"].append(scheme)
                
        return context
        
    async def _classify_intent(self, query: str) -> str:
        """Classify query intent"""
        query_lower = query.lower()
        
        # Intent classification based on keywords
        if any(word in query_lower for word in ["कैसे", "कैसी", "कब", "क्यों", "क्या", "कहाँ"]):
            if any(word in query_lower for word in ["बनाएं", "करें", "तैयार"]):
                return "how_to"
            elif any(word in query_lower for word in ["कब", "समय", "तारीख"]):
                return "timing_information"
            elif any(word in query_lower for word in ["क्या", "कौन", "किस"]):
                return "factual_question"
            else:
                return "informational"
        elif any(word in query_lower for word in ["खोजें", "चाहिए", "सुझाव"]):
            return "search_recommendation"
        elif any(word in query_lower for word in ["इलाज", "नुस्खा", "दवा"]):
            return "healthcare_advice"
        else:
            return "general_query"
            
    async def _generate_response(self, query: str, intent: str, cultural_context: Dict) -> Dict[str, Any]:
        """Generate culturally-aware response"""
        
        # Generate response based on intent and cultural context
        if intent == "how_to" and cultural_context["festivals"]:
            # Festival-related how-to query
            festival = cultural_context["festivals"][0]
            return {
                "type": "cultural_guide",
                "title": f"{festival['name']} की तैयारी कैसे करें",
                "content": self._generate_festival_guide(festival["name"]),
                "cultural_significance": festival["significance"],
                "traditional_practices": self.cultural_context["festivals"][festival["name"]].get("traditions", [])
            }
            
        elif intent == "healthcare_advice" and cultural_context["healthcare_topics"]:
            # Healthcare query with traditional remedies
            topic = cultural_context["healthcare_topics"][0]
            return {
                "type": "healthcare_advice",
                "condition": topic["condition"],
                "traditional_remedies": topic["remedies"],
                "ayurvedic_approach": "संतुलित आहार और प्राकृतिक उपचार का प्रयोग करें",
                "disclaimer": "गंभीर समस्या होने पर डॉक्टर से सलाह लें"
            }
            
        elif cultural_context["food_items"]:
            # Food-related query
            food_item = cultural_context["food_items"][0]
            return {
                "type": "culinary_information",
                "dish": food_item["item"],
                "category": food_item["category"],
                "preparation_tips": f"{food_item['item']} बनाने की पारंपरिक विधि",
                "cultural_context": "भारतीय खाना पकाने की परंपरा"
            }
            
        else:
            # General response
            return {
                "type": "general_response", 
                "content": f"आपके प्रश्न '{query}' के बारे में जानकारी प्रदान करने का प्रयास कर रहे हैं।",
                "suggestion": "कृपया अधिक विशिष्ट जानकारी के लिए प्रश्न को स्पष्ट करें।"
            }
            
    def _generate_festival_guide(self, festival_name: str) -> str:
        """Generate festival preparation guide"""
    async def health_check(self) -> Dict[str, Any]:
        """Enhanced health check including real-world data status"""
        basic_health = await super().health_check()
        
        # Test real-world data connectivity
        real_world_status = "disconnected"
        if self.real_world_enabled:
            try:
                test_results = self.google_cse.search_with_language_context("भारत", "hindi", 1)
                real_world_status = "connected" if test_results else "limited"
            except:
                real_world_status = "error"
        
        basic_health.update({
            "real_world_data_status": real_world_status,
            "real_world_enabled": self.real_world_enabled,
            "performance_metrics": self.performance_metrics,
            "cache_size": len(self.real_world_aggregator.cache) if self.real_world_enabled else 0,
            "enhanced_features": "enabled" if self.real_world_enabled else "disabled"
        })
        
        return basic_health
        
    async def _should_fetch_real_world_data(self, query: str, intent: str, cultural_context: Dict) -> bool:
        """Determine if real-world data should be fetched"""
        # Fetch real-world data for current events, news, or when cultural context is limited
        real_world_intents = ['current_events', 'news', 'government_schemes', 'recent_information']
        
        if intent in real_world_intents:
            return True
        
        # If cultural context is limited, try real-world data
        if not cultural_context.get('festivals') and not cultural_context.get('food_items'):
            return True
        
        # For healthcare and how-to queries, always get real-world data
        if intent in ['healthcare_advice', 'how_to']:
            return True
        
        return False
    
    async def _generate_enhanced_response(self, query: str, intent: str, cultural_context: Dict, real_world_data: Dict = None) -> Dict:
        """Generate comprehensive response combining cultural and real-world data"""
        
        response = {
            "type": "enhanced_cultural_response",
            "cultural_introduction": self._get_cultural_introduction(cultural_context, query),
            "main_content": "",
            "practical_advice": "",
            "additional_resources": [],
            "confidence_level": "high" if real_world_data else "medium"
        }
        
        # Combine cultural knowledge with real-world information
        if real_world_data and real_world_data.get('has_real_world_data'):
            response["main_content"] = f"""
**पारंपरिक ज्ञान**: {self._get_traditional_knowledge(cultural_context, intent)}

**वर्तमान जानकारी**: {real_world_data['summary']}
            """.strip()
            
            # Add real-world sources
            response["additional_resources"] = [
                {
                    "title": result.get('title', 'No title'),
                    "link": result.get('link', ''),
                    "source": result.get('source', 'Unknown'),
                    "snippet": result.get('snippet', '')[:100] + "..." if result.get('snippet') else ""
                }
                for result in real_world_data.get('search_results', [])[:3]
            ]
        else:
            # Fall back to cultural knowledge only
            response["main_content"] = self._get_traditional_knowledge(cultural_context, intent)
        
        # Add practical advice
        response["practical_advice"] = self._generate_practical_advice(cultural_context, intent, real_world_data)
        
        return response
    
    def _get_cultural_introduction(self, cultural_context: Dict, query: str) -> str:
        """Generate cultural introduction based on context"""
        if cultural_context.get('festivals'):
            return f"भारतीय संस्कृति में '{query}' का विशेष महत्व है।"
        elif cultural_context.get('food_items'):
            return f"भारतीय खाना पकाने की परंपरा में '{query}' की अपनी विशेषता है।"
        elif cultural_context.get('healthcare_topics'):
            return f"आयुर्वेदिक चिकित्सा पद्धति के अनुसार '{query}' के बारे में जानकारी।"
        else:
            return f"आपके प्रश्न '{query}' के बारे में विस्तृत जानकारी प्रस्तुत है।"
    
    def _get_traditional_knowledge(self, cultural_context: Dict, intent: str) -> str:
        """Get traditional knowledge based on context"""
        if cultural_context.get('festivals'):
            festival = cultural_context['festivals'][0]
            festival_name = festival.get('name', 'त्योहार') if isinstance(festival, dict) else str(festival)
            return f"पारंपरिक रूप से {festival_name} का पर्व विशेष महत्व रखता है। इसमें पारंपरिक रीति-रिवाज और सांस्कृतिक मूल्य शामिल हैं।"
        
        if cultural_context.get('healthcare_topics'):
            return "आयुर्वेदिक परंपरा के अनुसार प्राकृतिक उपचार और घरेलू नुस्खे का उपयोग करें। तुलसी, अदरक, हल्दी जैसी जड़ी-बूटियां फायदेमंद हैं।"
        
        if intent == "how_to":
            return "पारंपरिक तरीकों का पालन करते हुए, धैर्य और अभ्यास से बेहतर परिणाम प्राप्त होते हैं।"
        
        return "भारतीय संस्कृति और परंपरा के अनुसार उचित मार्गदर्शन।"
    
    def _generate_practical_advice(self, cultural_context: Dict, intent: str, real_world_data: Dict = None) -> str:
        """Generate practical advice combining traditional and modern knowledge"""
        advice_parts = []
        
        # Traditional advice
        if cultural_context.get('healthcare_topics'):
            advice_parts.append("🌿 **पारंपरिक उपाय**: तुलसी, अदरक, और हल्दी का नियमित उपयोग करें।")
        
        if intent == "how_to":
            advice_parts.append("📋 **व्यावहारिक सुझाव**: चरणबद्ध तरीके से अभ्यास करें।")
        
        # Modern advice from real-world data
        if real_world_data and real_world_data.get('has_real_world_data'):
            advice_parts.append("🌐 **आधुनिक जानकारी**: नवीनतम शोध और विशेषज्ञों की सलाह के अनुसार अपडेटेड जानकारी।")
        
        # Safety advice
        advice_parts.append("⚠️ **सुरक्षा**: किसी भी महत्वपूर्ण निर्णय से पहले विशेषज्ञ से सलाह अवश्य लें।")
        
        return "\n".join(advice_parts) if advice_parts else "विशेषज्ञ सलाह की सिफारिश की जाती है।"
    
    def _calculate_confidence(self, cultural_context: Dict, real_world_data: Dict = None) -> float:
        """Calculate confidence score based on available data"""
        confidence = 0.6  # Base confidence
        
        if cultural_context.get('festivals') or cultural_context.get('food_items'):
            confidence += 0.2
        
        if real_world_data and real_world_data.get('has_real_world_data'):
            confidence += 0.2
            if len(real_world_data.get('search_results', [])) >= 3:
                confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _update_performance_metrics(self, processing_time: float):
        """Update performance metrics"""
        self.performance_metrics["total_response_time"] += processing_time
        self.performance_metrics["average_response_time"] = (
            self.performance_metrics["total_response_time"] / 
            max(self.performance_metrics["total_queries"], 1)
        )
