"""
Marathi Language Node
Specialized node for processing Marathi queries with Maharashtra cultural context
"""

import asyncio
import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_node import BaseLanguageNode

logger = logging.getLogger(__name__)

class MarathiNode(BaseLanguageNode):
    """
    Marathi language federated learning node with Maharashtra cultural context
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("mr", config)
        
        # Marathi-specific configurations
        self.script_patterns = {
            "devanagari": re.compile(r'[\u0900-\u097F]+'),
            "roman": re.compile(r'[a-zA-Z]+')
        }
        
        # Cultural knowledge domains
        self.cultural_domains = [
            "festivals", "food", "business", "arts", "history",
            "literature", "traditions", "saints"
        ]
        
    async def _load_cultural_context(self):
        """Load Marathi/Maharashtra cultural context"""
        logger.info("Loading Marathi cultural context...")
        
        self.cultural_context = {
            "festivals": {
                "गणेशचतुर्थी": {
                    "english": "Ganesh Chaturthi",
                    "significance": "Birth celebration of Lord Ganesha, most important festival in Maharashtra",
                    "timing": "August/September (Bhadrapada Shukla Chaturthi)",
                    "traditions": [
                        "गणपती बाप्पा घरात आणणे",
                        "मोदक आणि लाडू तयार करणे",
                        "आरती आणि भजन करणे",
                        "विसर्जन सणात सहभाग घेणे"
                    ],
                    "duration": "1.5, 3, 5, 7, 11 दिवस",
                    "special_locations": ["लालबागचा राजा", "सिद्धिविनायक", "दगडूशेठ हळवाई"]
                },
                "गुढी पाडवा": {
                    "english": "Gudi Padwa",
                    "significance": "Marathi New Year",
                    "timing": "March/April (Chaitra Shukla Pratipada)",
                    "traditions": [
                        "गुढी उभारणे",
                        "घरांना तोरण लावणे",
                        "पूरणपोळी आणि श्रीखंड खाणे",
                        "नवीन कपडे घालणे"
                    ]
                },
                "नवरात्री": {
                    "english": "Navratri",
                    "significance": "Nine nights of Goddess Durga worship",
                    "timing": "September/October",
                    "traditions": [
                        "गरबा आणि डांडिया खेळणे",
                        "देवीची पूजा करणे",
                        "उपास ठेवणे"
                    ]
                },
                "दिवाळी": {
                    "english": "Diwali", 
                    "significance": "Festival of lights",
                    "timing": "October/November",
                    "traditions": [
                        "घरांची सफाई करणे",
                        "रांगोळी काढणे",
                        "दिवे लावणे",
                        "फराळ तयार करणे"
                    ]
                }
            },
            
            "food": {
                "महाराष्ट्रीयन खाना": {
                    "मुख्य जेवण": [
                        "भाकरी", "भात", "डाळ", "भाजी", "रस्सा", "कढी",
                        "सांबर", "आमटी", "वरण", "उसळ"
                    ],
                    "नाश्ता": [
                        "पोहा", "उपमा", "मिसळ पाव", "दही पोहा", "सातू",
                        "शीरा", "खीर", "ज्वारीची भाकरी"
                    ],
                    "फराळ": [
                        "साबुदाणा खिचडी", "राजगिरा लाडू", "आलू वडी",
                        "शिंगदाणा चिकी", "खजूर पाकं"
                    ],
                    "मिठाई": [
                        "मोदक", "पूरणपोळी", "शेवयंची खीर", "श्रीखंड",
                        "आंबे रस", "सोलकढी"
                    ]
                },
                "प्रादेशिक खाना": {
                    "कोंकणी": ["फिश करी", "सोल कढी", "कोकम शर्बत"],
                    "विदर्भ": ["वरण फळ", "भर्ली वांगी", "सांजा"],
                    "मराठवाडा": ["ज्वारीची भाकरी", "झुणका भाकरी", "पिठला भाकरी"]
                }
            },
            
            "business": {
                "महाराष्ट्रीयन व्यापारी समुदाय": {
                    "मारवाडी": "राजस्थानी व्यापारी समुदाय",
                    "गुजराती": "गुजरातची व्यापारी संस्कृती",
                    "महाराष्ट्रीयन": "स्थानिक व्यापारी पारंपरिक"
                },
                "मुख्य व्यापारी केंद्रे": {
                    "मुंबई": "आर्थिक राजधानी, शेअर बाजार",
                    "पुणे": "IT हब, उत्पादन केंद्र",
                    "नागपूर": "भारताचे भौगोलिक केंद्र",
                    "औरंगाबाद": "MIDC, औद्योगिक केंद्र"
                },
                "स्टार्टअप इकोसिस्टम": {
                    "मुंबई": "फिनटेक, मीडिया, एंटरटेनमेंट",
                    "पुणे": "IT, automotive, engineering"
                }
            },
            
            "arts": {
                "नृत्य": [
                    "लावणी", "कथक", "तमाशा", "कोळी गीत",
                    "गोवळण", "धनगरी गौरी"
                ],
                "संगीत": [
                    "नट्यसंगीत", "सुगम संगीत", "लोकगीते",
                    "भावगीते", "भक्तिगीते"
                ],
                "रंगभूमी": [
                    "व्यावसायिक थिएटर", "प्रयोगशील नाटक",
                    "एकांकिका", "बालनाट्य"
                ]
            },
            
            "literature": {
                "आधुनिक मराठी साहित्य": {
                    "कवी": ["कुसुमाग्रज", "बी. एस. मर्ढेकर", "वृंदा करंदीकर"],
                    "कथाकार": ["पु. ल. देशपांडे", "व्यंकटेश माडगूळकर", "बाळ फोंडके"],
                    "नाटककार": ["विजय तेंडुलकर", "गिरीश कर्नाड", "महेश एळकुंचवार"]
                },
                "संत साहित्य": {
                    "संत तुकाराम": "अभंगे आणि गाथा",
                    "संत ज्ञानेश्वर": "ज्ञानेश्वरी",
                    "संत एकनाथ": "एकनाथी भागवत",
                    "संत नामदेव": "भक्ति काव्य"
                }
            },
            
            "history": {
                "मराठा साम्राज्य": {
                    "छत्रपती शिवाजी महाराज": "मराठा साम्राज्याचे संस्थापक",
                    "संभाजी महाराज": "शिवाजी महाराजाचे पुत्र",
                    "राजाराम महाराज": "मराठा प्रतिकार",
                    "ताराबाई": "मराठा राणी"
                },
                "पेशवा काळ": {
                    "बाजीराव पेशवे": "मराठा शक्तीचा विस्तार",
                    "नानासाहेब पेशवे": "मराठा संघराज्य"
                }
            },
            
            "traditions": {
                "धार्मिक परंपरा": [
                    "वारी", "पंढरपूर यात्रा", "गणपती उत्सव",
                    "नवरात्री", "महाशिवरात्री"
                ],
                "सामाजिक परंपरा": [
                    "हळदी कुंकू", "वत पूर्णिमा", "कर्णपिशाचणी",
                    "नामकरण", "जतकर्म"
                ]
            }
        }
        
        logger.info("Marathi cultural context loaded successfully")
        
    async def process_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process Marathi search query with cultural context"""
        start_time = datetime.now()
        
        try:
            logger.info(f"Processing Marathi query: {query[:50]}...")
            
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
                "language": "marathi",
                "script": script_info,
                "intent": intent,
                "cultural_context": cultural_context,
                "response": response,
                "confidence": 0.86,  # Simulated confidence
                "response_time_ms": round(response_time, 2),
                "timestamp": start_time.isoformat()
            }
            
        except Exception as e:
            # Update metrics for failed query
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_metrics(False, response_time)
            
            logger.error(f"Error processing Marathi query: {e}")
            return {
                "error": str(e),
                "query": query,
                "language": "marathi",
                "timestamp": start_time.isoformat()
            }
            
    async def _detect_script(self, query: str) -> Dict[str, Any]:
        """Detect script used in Marathi query"""
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
        """Detect cultural context in Marathi query"""
        context = {
            "festivals": [],
            "food_items": [],
            "business_topics": [],
            "historical_figures": [],
            "arts": [],
            "literature": []
        }
        
        query_lower = query.lower()
        
        # Festival detection
        for festival, info in self.cultural_context["festivals"].items():
            if festival in query or info["english"].lower() in query_lower:
                context["festivals"].append({
                    "name": festival,
                    "english": info["english"],
                    "significance": info["significance"]
                })
                
        # Food detection
        for category, items in self.cultural_context["food"]["महाराष्ट्रीयन खाना"].items():
            for item in items:
                if item in query:
                    context["food_items"].append({
                        "item": item,
                        "category": category
                    })
                    
        # Business context detection
        for business_center, description in self.cultural_context["business"]["मुख्य व्यापारी केंद्रे"].items():
            if business_center in query:
                context["business_topics"].append({
                    "center": business_center,
                    "description": description
                })
                
        # Historical figures detection
        for figure, description in self.cultural_context["history"]["मराठा साम्राज्य"].items():
            if any(word in query for word in figure.split()):
                context["historical_figures"].append({
                    "name": figure,
                    "description": description
                })
                
        return context
        
    async def _classify_intent(self, query: str) -> str:
        """Classify Marathi query intent"""
        query_lower = query.lower()
        
        # Marathi question words and intent classification
        if any(word in query for word in ["कसे", "कसा", "कधी", "का", "काय", "कुठे", "कोण"]):
            if any(word in query for word in ["करावे", "बनवावे", "तयार"]):
                return "how_to"
            elif any(word in query for word in ["कधी", "वेळ", "काळ"]):
                return "timing_information"
            elif any(word in query for word in ["काय", "कोण", "कुठे"]):
                return "factual_question"
            else:
                return "informational"
        elif any(word in query for word in ["हवे", "पाहिजे", "सूचना"]):
            return "search_recommendation"
        elif any(word in query for word in ["व्यापार", "बिझनेस", "धंदा"]):
            return "business_advice"
        else:
            return "general_query"
            
    async def _generate_response(self, query: str, intent: str, cultural_context: Dict) -> Dict[str, Any]:
        """Generate culturally-aware Marathi response"""
        
        if intent == "how_to" and cultural_context["festivals"]:
            # Festival-related how-to query
            festival = cultural_context["festivals"][0]
            return {
                "type": "cultural_guide",
                "title": f"{festival['name']} कसे साजरे करावे",
                "content": self._generate_festival_guide(festival["name"]),
                "cultural_significance": festival["significance"],
                "traditional_practices": self.cultural_context["festivals"][festival["name"]].get("traditions", [])
            }
            
        elif intent == "business_advice" and cultural_context["business_topics"]:
            # Business-related query
            business_topic = cultural_context["business_topics"][0]
            return {
                "type": "business_information",
                "center": business_topic["center"],
                "description": business_topic["description"],
                "business_opportunities": "महाराष्ट्रातील व्यापारी संधी",
                "cultural_context": "महाराष्ट्रीयन व्यापारी संस्कृती"
            }
            
        elif cultural_context["food_items"]:
            # Food-related query
            food_item = cultural_context["food_items"][0]
            return {
                "type": "culinary_information",
                "dish": food_item["item"],
                "category": food_item["category"],
                "preparation_info": f"{food_item['item']} कसे बनवावे",
                "cultural_context": "महाराष्ट्रीयन स्वयंपाक परंपरा"
            }
            
        elif cultural_context["historical_figures"]:
            # Historical query
            figure = cultural_context["historical_figures"][0]
            return {
                "type": "historical_information",
                "figure": figure["name"],
                "description": figure["description"],
                "significance": "मराठा इतिहासातील महत्वपूर्ण व्यक्तिमत्व"
            }
            
        else:
            # General response
            return {
                "type": "general_response",
                "content": f"तुमच्या प्रश्न '{query}' बद्दल माहिती देण्याचा प्रयत्न करत आहे.",
                "suggestion": "कृपया अधिक स्पष्ट माहितीसाठी प्रश्न नक्की करा."
            }
            
    def _generate_festival_guide(self, festival_name: str) -> str:
        """Generate Marathi festival preparation guide"""
        if festival_name == "गणेशचतुर्थी":
            return """
            गणेशचतुर्थी साजरी करण्यासाठी:
            1. घराची सफाई करा आणि तोरण लावा
            2. गणपती मूर्ती घरात आणा
            3. मोदक, लाडू तयार करा
            4. दररोज आरती करा
            5. विसर्जनाची तयारी करा
            """
        elif festival_name == "गुढी पाडवा":
            return """
            गुढी पाडवा साजरा करण्यासाठी:
            1. घराची सफाई करा
            2. गुढी तयार करून उभारा
            3. तोरण लावा
            4. पूरणपोळी आणि श्रीखंड तयार करा
            5. नवीन कपडे घाला
            """
        else:
            return f"{festival_name} ची पारंपरिक साजरी करण्याची माहिती."
