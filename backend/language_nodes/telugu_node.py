"""
Telugu Language Node
Specialized node for processing Telugu queries with South Indian cultural context
"""

import asyncio
import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_node import BaseLanguageNode

logger = logging.getLogger(__name__)

class TeluguNode(BaseLanguageNode):
    """
    Telugu language federated learning node with South Indian cultural context
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("te", config)
        
        # Telugu-specific configurations
        self.script_patterns = {
            "telugu": re.compile(r'[\u0C00-\u0C7F]+'),
            "roman": re.compile(r'[a-zA-Z]+')
        }
        
        # Cultural knowledge domains
        self.cultural_domains = [
            "festivals", "food", "traditions", "literature", 
            "agriculture", "arts", "temples"
        ]
        
    async def _load_cultural_context(self):
        """Load Telugu/South Indian cultural context"""
        logger.info("Loading Telugu cultural context...")
        
        self.cultural_context = {
            "festivals": {
                "ఉగాది": {
                    "english": "Ugadi",
                    "significance": "Telugu New Year, marking the beginning of new lunar calendar",
                    "timing": "March/April (Chaitra Suddha Padyami)",
                    "traditions": [
                        "ఉగాది పచ్చడి తయారీ",
                        "బొమ్మలు అలంకరణ",
                        "పంచాంగ శ్రవణం",
                        "కొత్త బట్టలు దానం"
                    ],
                    "special_food": ["ఉగాది పచ్చడి", "పులిహోర", "బోబ్బట్టు"]
                },
                "దసరా": {
                    "english": "Dussehra",
                    "significance": "Victory of good over evil, celebrating Goddess Durga",
                    "timing": "September/October",
                    "traditions": [
                        "గోలు అలంకరణ",
                        "నవరాత్రి ఉత్సవాలు", 
                        "సరస్వతీ పూజ",
                        "విజయదశమి"
                    ]
                },
                "దీపావళి": {
                    "english": "Deepavali",
                    "significance": "Festival of lights in South Indian tradition",
                    "timing": "October/November",
                    "traditions": [
                        "దీపాలు వెలిగించడం",
                        "రంగోలీ అలంకరణ",
                        "తెల్లవారుజామున గంగాస్నానం",
                        "నూతన వస్త్రాలు ధరించడం"
                    ]
                },
                "శ్రీరామనవమి": {
                    "english": "Sri Rama Navami",
                    "significance": "Birthday of Lord Rama",
                    "timing": "March/April",
                    "traditions": [
                        "రామ కళ్యాణోత్సవాలు",
                        "రామాయణ పారాయణ",
                        "భజనలు మరియు కీర్తనలు"
                    ]
                }
            },
            
            "food": {
                "సాంప్రదాయిక వంటకాలు": {
                    "అన్నం వంటలు": [
                        "పులిహోర", "వడ్డభాత్", "దధ్యోదనం", "కోకినాడు ఖిచిడీ",
                        "అవకాయ అన్నం", "గాజు వంకాయ అన్నం"
                    ],
                    "కూరలు": [
                        "సాంబార్", "రసం", "పప్పు", "ముంతకాయ కూర",
                        "గోంగూర కూర", "పాలకూర పప్పు"
                    ],
                    "తినుబండారాలు": [
                        "దోశ", "ఇడ్లీ", "వడ", "ఉత్తప్పం", "పెసలు అట్టు",
                        "రాగి రోట్టి", "జొన్న రోట్టి"
                    ],
                    "తీపిలు": [
                        "అరిశెలు", "లడ్డూ", "మైసూరుపాకు", "ఖజూర్",
                        "బోబ్బట్టు", "అప్పగింతలు"
                    ]
                },
                "పండుగల ఆహారం": {
                    "ఉగాది": ["ఉగాది పచ్చడి", "పులిహోర", "బోబ్బట్టు"],
                    "దసరా": ["గోధుమ లడ్డూ", "గుల్లకంచు", "మిగపకలు"],
                    "దీపావళి": ["అరిశెలు", "మిఠాయిలు", "చక్రలు"]
                }
            },
            
            "literature": {
                "క్లాసికల్ కవులు": {
                    "ఆదికవి నన్నయ": "మహాభారత భాష్యకర్త",
                    "తిక్కన": "మహాభారత మధ్య భాగం", 
                    "యెర్రప్రగడ": "మహాభారత చివరి భాగం",
                    "శ్రీనాథుడు": "కాశీఖండం రచయిత"
                },
                "ఆధునిక సాహిత్యం": {
                    "గురజాడ అప్పారావు": "నాటక రచయిత",
                    "విశ్వనాథ సత్యనారాయణ": "రామాయణ కల్పవృక్షం",
                    "దేవులపల్లి కృష్ణశాస్త్రి": "కవిసార్వభౌముడు"
                }
            },
            
            "agriculture": {
                "వ్యవసాయ కాలాలు": {
                    "ఖరీఫ్": "వర్షాకాలంలో (జూన్-ఆక్టోబర్)",
                    "రబీ": "శీతాకాలంలో (అక్టోబర్-మార్చి)",
                    "జాయిద్": "వేసవిలో (మార్చి-జూన్)"
                },
                "ప్రధాన పంటలు": {
                    "ధాన్యాలు": ["వరి", "మొక్కజొన్న", "చొల్లు", "రాగి"],
                    "దాలిలు": ["కందులు", "పెసలు", "ఉలవలు", "మినుములు"],
                    "నూనె గింజలు": ["వేరుశనగ", "కుసుమ", "ఎండ్రకాయ"]
                }
            },
            
            "temples": {
                "ప్రసిద్ధ దేవాలయాలు": {
                    "తిరుమల వెంకటేశ్వర స్వామి": "చిత్తూరు జిల్లా",
                    "భద్రాచలం రామ స్వామి": "భద్రాద్రి కొత్తగూడెం జిల్లా", 
                    "శ్రీశైలం మల్లికార్జున స్వామి": "కర్నూలు జిల్లా",
                    "కాళహస్తి శ్రీకాళహస్తీశ్వర స్వామి": "చిత్తూరు జిల్లా"
                }
            },
            
            "traditions": {
                "సంస్కారాలు": [
                    "నామకరణం", "అన్నప్రాశన", "చౌళం", "ఉపనయనం",
                    "వివాహం", "గృహప్రవేశం"
                ],
                "కళలు": [
                    "కుచిపుడి నృత్యం", "కరగం", "వీరనాట్యం", 
                    "యక్షగానం", "హరికథ"
                ]
            }
        }
        
        logger.info("Telugu cultural context loaded successfully")
        
    async def process_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process Telugu search query with cultural context and real-world data"""
        start_time = datetime.now()
        
        try:
            logger.info(f"Processing Telugu query: {query[:50]}...")
            
            # Detect script and language validation
            script_info = await self._detect_script(query)
            
            # Extract cultural context
            cultural_context = await self._detect_cultural_context(query)
            
            # Process query based on intent
            intent = await self._classify_intent(query)
            
            # Get real-world data if available
            real_world_data = {}
            try:
                from ..core.real_world_data import GoogleCSEIntegration, RealWorldDataAggregator
                
                google_cse = GoogleCSEIntegration()
                aggregator = RealWorldDataAggregator(google_cse)
                
                logger.info(f"🔍 Fetching real-world data for Telugu query: {query}")
                real_world_data = aggregator.get_real_world_context(query, "telugu", cultural_context)
                logger.info(f"✅ Found {len(real_world_data.get('search_results', []))} real results")
                
            except Exception as rwd_error:
                logger.warning(f"Real-world data fetch failed: {rwd_error}")
                real_world_data = {"search_results": [], "error": str(rwd_error)}
            
            # Generate culturally-aware response with real-world data
            response = await self._generate_response(query, intent, cultural_context, real_world_data)
            
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
                "response_time_ms": response_time,
                "has_real_world_data": len(real_world_data.get('search_results', [])) > 0
            })
            
            return {
                "query": query,
                "language": "telugu",
                "script": script_info,
                "intent": intent,
                "cultural_context": cultural_context,
                "real_world_data": real_world_data,
                "response": response,
                "confidence": 0.87,  # Simulated confidence
                "response_time_ms": round(response_time, 2),
                "timestamp": start_time.isoformat()
            }
            
        except Exception as e:
            # Update metrics for failed query
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_metrics(False, response_time)
            
            logger.error(f"Error processing Telugu query: {e}")
            return {
                "error": str(e),
                "query": query,
                "language": "telugu",
                "timestamp": start_time.isoformat()
            }
            
    async def _detect_script(self, query: str) -> Dict[str, Any]:
        """Detect script used in Telugu query"""
        telugu_chars = len(self.script_patterns["telugu"].findall(query))
        roman_chars = len(self.script_patterns["roman"].findall(query))
        
        total_chars = len(query.replace(" ", ""))
        
        if total_chars == 0:
            return {"primary_script": "unknown", "telugu_ratio": 0, "roman_ratio": 0}
            
        telugu_ratio = telugu_chars / total_chars
        roman_ratio = roman_chars / total_chars
        
        primary_script = "telugu" if telugu_ratio > roman_ratio else "roman"
        
        return {
            "primary_script": primary_script,
            "telugu_ratio": round(telugu_ratio, 2),
            "roman_ratio": round(roman_ratio, 2),
            "mixed_script": telugu_ratio > 0.1 and roman_ratio > 0.1
        }
        
    async def _detect_cultural_context(self, query: str) -> Dict[str, Any]:
        """Detect cultural context in Telugu query"""
        context = {
            "festivals": [],
            "food_items": [],
            "literature": [],
            "temples": [],
            "agricultural_topics": [],
            "traditional_arts": []
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
        for category, items in self.cultural_context["food"]["సాంప్రదాయిక వంటకాలు"].items():
            for item in items:
                if item in query:
                    context["food_items"].append({
                        "item": item,
                        "category": category
                    })
                    
        # Literature detection
        for author, work in self.cultural_context["literature"]["క్లాసికల్ కవులు"].items():
            if author in query:
                context["literature"].append({
                    "author": author,
                    "work": work
                })
                
        # Temple detection
        for temple, location in self.cultural_context["temples"]["ప్రసిద్ధ దేవాలయాలు"].items():
            if any(word in query for word in temple.split()):
                context["temples"].append({
                    "temple": temple,
                    "location": location
                })
                
        return context
        
    async def _classify_intent(self, query: str) -> str:
        """Classify Telugu query intent"""
        query_lower = query.lower()
        
        # Telugu question words and intent classification
        if any(word in query for word in ["ఎలా", "ఎలాగ", "ఎప్పుడు", "ఎందుకు", "ఎక్కడ", "ఏమిటి"]):
            if any(word in query for word in ["చేయాలి", "తయారు", "వండాలి"]):
                return "how_to"
            elif any(word in query for word in ["ఎప్పుడు", "కాలం", "సమయం"]):
                return "timing_information"
            elif any(word in query for word in ["ఏమిటి", "ఎవరు", "ఏది"]):
                return "factual_question"
            else:
                return "informational"
        elif any(word in query for word in ["కావాలి", "కాలి", "సూచన"]):
            return "search_recommendation"
        elif any(word in query for word in ["చికిత్స", "మందు", "వైద్యం"]):
            return "healthcare_advice"
        else:
            return "general_query"
            
    async def _generate_response(self, query: str, intent: str, cultural_context: Dict, real_world_data: Dict = None) -> Dict[str, Any]:
        """Generate culturally-aware Telugu response with real-world data integration"""
        
        # Check if we have real-world data
        search_results = real_world_data.get('search_results', []) if real_world_data else []
        has_real_data = len(search_results) > 0
        
        if has_real_data:
            # Generate response with real-world data
            top_result = search_results[0]
            real_content = top_result.get('content', top_result.get('snippet', ''))[:500]
            real_sources = [r.get('source', 'Unknown') for r in search_results[:3]]
            
            response_content = f"""
**వాస్తవ సమాచారం**: {real_content}

**మూలాలు**: {', '.join(real_sources)}

**అదనపు సందర్భం**: ఈ విషయంపై మరిన్ని వివరాలు అందుబాటులో ఉన్నాయి।
            """.strip()
            
            return {
                "type": "real_world_response",
                "cultural_introduction": f"మీ ప్రశ్న '{query}' గురించి వాస్తవ సమాచారం:",
                "main_content": response_content,
                "practical_advice": "🌐 **వాస్తవ డేటా**: ఈ సమాచారం ఇంటర్నెట్ నుండి పొందబడింది।",
                "additional_resources": [
                    {
                        "title": result.get('title', 'No title'),
                        "link": result.get('link', ''),
                        "source": result.get('source', 'Unknown'),
                        "snippet": result.get('snippet', '')[:100] + "..." if result.get('snippet') else ""
                    }
                    for result in search_results[:3]
                ],
                "confidence_level": "high"
            }
        
        # Fallback to cultural context responses
        if intent == "how_to" and cultural_context["festivals"]:
            # Festival-related how-to query
            festival = cultural_context["festivals"][0]
            return {
                "type": "cultural_guide",
                "title": f"{festival['name']} ఎలా జరుపుకోవాలి",
                "content": self._generate_festival_guide(festival["name"]),
                "cultural_significance": festival["significance"],
                "traditional_practices": self.cultural_context["festivals"][festival["name"]].get("traditions", [])
            }
            
        elif cultural_context["food_items"]:
            # Food-related query
            food_item = cultural_context["food_items"][0]
            return {
                "type": "culinary_information",
                "dish": food_item["item"],
                "category": food_item["category"],
                "preparation_info": f"{food_item['item']} తయారీ విధానం",
                "cultural_context": "తెలుగు వంట సంప్రదాయం"
            }
            
        elif cultural_context["temples"]:
            # Temple-related query
            temple = cultural_context["temples"][0]
            return {
                "type": "temple_information",
                "temple": temple["temple"],
                "location": temple["location"],
                "significance": "పవిత్ర క్షేత్రం మరియు ఆధ్యాత్మిక కేంద్రం"
            }
            
        else:
            # General response
            return {
                "type": "general_response",
                "content": f"మీ ప్రశ్న '{query}' గురించి సమాచారం అందించడానికి ప్రయత్నిస్తున్నాము.",
                "suggestion": "దయచేసి మరింత నిర్దిష్ట సమాచారం కోసం ప్రశ్నను స్పష్టంగా చెప్పండి.",
                "confidence_level": "medium"
            }
            
    def _generate_festival_guide(self, festival_name: str) -> str:
        """Generate Telugu festival preparation guide"""
        if festival_name == "ఉగాది":
            return """
            ఉగాది పండుగ జరుపుకోవడానికి:
            1. ఇంటిని శుభ్రం చేసి, రంగోలీ వేయండి
            2. ఉగాది పచ్చడి తయారు చేయండి (జగ్గేరి, ఉప్పు, కారం, వేప, తమరింద్, నిమ్మ)
            3. కొత్త బట్టలు కొనుక్కోండి
            4. పంచాంగ శ్రవణం చేయండి
            5. దేవుళ్ళకు ప్రార్థనలు చేయండి
            """
        elif festival_name == "దసరా":
            return """
            దసరా పండుగ జరుపుకోవడానికి:
            1. గోలు దిద్దండి (బొమ్మల అలంకరణ)
            2. నవరాత్రి పూజలు చేయండి
            3. సరస్వతీ దేవికి పూజ చేయండి
            4. విజయదశమి రోజున కొత్త పనులు మొదలు పెట్టండి
            """
        else:
            return f"{festival_name} సాంప్రదాయిక జరుపుకోవడం గురించి సమాచారం."
