"""
Hindi Language Node
Specialized node for processing Hindi queries with Indian cultural context
"""

import asyncio
import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .base_node import BaseLanguageNode

logger = logging.getLogger(__name__)

class HindiNode(BaseLanguageNode):
    """
    Hindi language federated learning node with Indian cultural context
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("hi", config)
        
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
        """Process Hindi search query with cultural context"""
        start_time = datetime.now()
        
        try:
            logger.info(f"Processing Hindi query: {query[:50]}...")
            
            # Detect script and language validation
            script_info = await self._detect_script(query)
            
            # Extract cultural context
            cultural_context = await self._detect_cultural_context(query)
            
            # Process query based on intent
            intent = await self._classify_intent(query)
            
            # Generate culturally-aware response
            response = await self._generate_response(query, intent, cultural_context)
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Update metrics
            self._update_metrics(True, response_time)
            
            # Store query for learning
            self.query_history.append({
                "query": query,
                "timestamp": start_time.isoformat(),
                "intent": intent,
                "cultural_context": cultural_context,
                "response_time_ms": response_time
            })
            
            return {
                "query": query,
                "language": "hindi",
                "script": script_info,
                "intent": intent,
                "cultural_context": cultural_context,
                "response": response,
                "confidence": 0.85,  # Simulated confidence
                "response_time_ms": round(response_time, 2),
                "timestamp": start_time.isoformat()
            }
            
        except Exception as e:
            # Update metrics for failed query
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_metrics(False, response_time)
            
            logger.error(f"Error processing Hindi query: {e}")
            return {
                "error": str(e),
                "query": query,
                "language": "hindi",
                "timestamp": start_time.isoformat()
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
        if festival_name == "दिवाली":
            return """
            दिवाली की तैयारी के लिए:
            1. घर की सफाई और रंगाई-पुताई करें
            2. दीये, मोमबत्तियां और रंगोली तैयार करें  
            3. लक्ष्मी पूजा की सामग्री खरीदें
            4. मिठाइयां और उपहार तैयार करें
            5. नए कपड़े और गहने खरीदें
            """
        elif festival_name == "होली":
            return """
            होली की तैयारी के लिए:
            1. प्राकृतिक रंग तैयार करें या खरीदें
            2. गुजिया और अन्य मिठाइयां बनाएं
            3. ठंडाई तैयार करें
            4. होलिका दहन की तैयारी करें
            """
        else:
            return f"{festival_name} की पारंपरिक तैयारी की जानकारी।"
