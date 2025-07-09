"""
Main API Gateway
Central API gateway that routes requests to appropriate language nodes
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GlobalMind FL API Gateway",
    description="Federated Learning for Multilingual AI Search Intelligence",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:5500", "http://localhost:5500", "*"],  # React frontend and test HTML
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Language node endpoints
LANGUAGE_NODES = {
    "hindi": "http://localhost:8001",
    "telugu": "http://localhost:8002", 
    "marathi": "http://localhost:8003",
    "english": "http://localhost:8004"
}

# Language detection patterns (simplified for MVP)
LANGUAGE_PATTERNS = {
    "hindi": ["दिवाली", "होली", "करवा", "चौथ", "नमस्ते", "धन्यवाद", "कैसे", "क्या", "कहाँ"],
    "telugu": ["ఉగాది", "దసరా", "దీపావళి", "నమస్తే", "ధన్యవాదాలు", "ఎలా", "ఎప్పుడు", "ఎక్కడ"],
    "marathi": ["गणेशचतुर्थी", "गुढी", "पाडवा", "नमस्कार", "धन्यवाद", "कसे", "कधी", "कुठे"],
    "english": ["hello", "thank", "please", "how", "what", "where", "when", "cricket", "india"]
}

class QueryRequest(BaseModel):
    query: str
    language: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    detected_language: str
    response: Dict[str, Any]
    processing_time_ms: float
    timestamp: str
    node_endpoint: str

# Request/Response models for agentic features
class AgenticSearchRequest(BaseModel):
    query: str
    language: str = "auto"
    approach: Optional[str] = "hybrid"  # "lightweight", "agentic", or "hybrid"
    max_results: int = 3

class SummarizerConfigRequest(BaseModel):
    use_agentic_by_default: Optional[bool] = None
    min_results_threshold: Optional[int] = None
    min_content_length: Optional[int] = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "GlobalMind FL API Gateway",
        "version": "1.0.0",
        "description": "Federated Learning for Multilingual AI Search Intelligence",
        "supported_languages": list(LANGUAGE_NODES.keys()),
        "endpoints": {
            "query": "/api/v1/query",
            "health": "/health",
            "language_detection": "/api/v1/detect-language",
            "federation_status": "/api/v1/federation/status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check language node availability
    node_health = {}
    for language, endpoint in LANGUAGE_NODES.items():
        try:
            # In MVP, we simulate health checks
            # In production, this would be actual HTTP requests
            node_health[language] = {
                "status": "healthy",
                "endpoint": endpoint,
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            node_health[language] = {
                "status": "unhealthy",
                "endpoint": endpoint,
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    overall_health = "healthy" if all(
        node["status"] == "healthy" for node in node_health.values()
    ) else "degraded"
    
    return {
        "status": overall_health,
        "timestamp": datetime.now().isoformat(),
        "nodes": node_health,
        "version": "1.0.0"
    }

@app.post("/api/v1/detect-language")
async def detect_language(request: QueryRequest):
    """Detect language of the input query"""
    query = request.query.lower()
    
    # Simple keyword-based language detection for MVP
    language_scores = {}
    
    for language, keywords in LANGUAGE_PATTERNS.items():
        score = sum(1 for keyword in keywords if keyword in query)
        if score > 0:
            language_scores[language] = score
    
    if language_scores:
        detected_language = max(language_scores, key=language_scores.get)
        confidence = language_scores[detected_language] / len(LANGUAGE_PATTERNS[detected_language])
    else:
        # Default fallback - could be enhanced with actual language detection
        detected_language = "english"  # Default to English for MVP
        confidence = 0.5
    
    return {
        "query": request.query,
        "detected_language": detected_language,
        "confidence": round(confidence, 2),
        "all_scores": language_scores,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process multilingual query and route to appropriate language node"""
    start_time = datetime.now()
    
    try:
        # Language detection
        if request.language:
            detected_language = request.language
        else:
            detection_result = await detect_language(request)
            detected_language = detection_result["detected_language"]
        
        # Validate language support
        if detected_language not in LANGUAGE_NODES:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{detected_language}' not supported. Supported languages: {list(LANGUAGE_NODES.keys())}"
            )
        
        # Route to appropriate language node
        node_endpoint = LANGUAGE_NODES[detected_language]
        
        # For MVP, we'll use actual real-world data processing
        # In production, this would be actual HTTP requests to language nodes
        node_response = await actual_node_processing(detected_language, request.query, request.context)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return QueryResponse(
            query=request.query,
            detected_language=detected_language,
            response=node_response,
            processing_time_ms=round(processing_time, 2),
            timestamp=start_time.isoformat(),
            node_endpoint=node_endpoint
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def actual_node_processing(language: str, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Actual language node processing with real Google Custom Search"""
    
    # Import real-world data integration
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        from core.real_world_data import GoogleCSEIntegration, RealWorldDataAggregator
        
        # Initialize Google CSE
        google_cse = GoogleCSEIntegration()
        aggregator = RealWorldDataAggregator(google_cse)
        
        logger.info(f"🔍 Fetching real-world data for: {query} in {language}")
        
        # Get actual real-world data
        real_world_data = aggregator.get_real_world_context(query, language, {})
        
        logger.info(f"✅ Found {len(real_world_data.get('search_results', []))} real results")
        
        # Generate response based on language
        if language == "hindi":
            return await generate_real_hindi_response(query, real_world_data)
        elif language == "telugu":
            return await generate_real_telugu_response(query, real_world_data)
        elif language == "marathi":
            return await generate_real_marathi_response(query, real_world_data)
        elif language == "english":
            return await generate_real_english_response(query, real_world_data)
        else:
            raise ValueError(f"Unsupported language: {language}")
        
    except Exception as e:
        logger.error(f"❌ Real-world data fetch failed: {e}")
        # Fallback to basic response
        await asyncio.sleep(0.1)
        return {
            "query": query,
            "language": language,
            "response": {
                "type": "basic_response",
                "content": f"तकनीकी समस्या के कारण वर्तमान में पूरी जानकारी उपलब्ध नहीं है। query: {query}",
                "error": str(e)
            },
            "confidence": 0.3,
            "response_time_ms": 100,
            "timestamp": datetime.now().isoformat(),
            "real_world_data": None
        }

async def generate_real_hindi_response(query: str, real_world_data: Dict) -> Dict[str, Any]:
    """Generate Hindi response with real Google search results"""
    
    # Extract real information from Google search results
    search_results = real_world_data.get('search_results', [])
    has_real_data = len(search_results) > 0
    
    if has_real_data:
        # Use real search results (snippets only for global general search)
        top_result = search_results[0]
        real_content = top_result.get('snippet', '')[:500]  # Use snippet only
        real_sources = [r.get('source', 'Unknown') for r in search_results[:3]]
        
        # Check if AI summary is available
        ai_summary_text = ""
        if real_world_data.get('ai_summary') and real_world_data['ai_summary'].get('ai_summary'):
            ai_summary_text = f"\n\n{real_world_data['ai_summary']['ai_summary']}"
        
        response_content = f"""
**वास्तविक जानकारी**: {real_content}

**स्रोत**: {', '.join(real_sources)}{ai_summary_text}

**अतिरिक्त संदर्भ**: इस विषय पर और भी जानकारी उपलब्ध है।
        """.strip()
    else:
        response_content = f"'{query}' के बारे में वर्तमान में विस्तृत जानकारी उपलब्ध नहीं है।"
    
    return {
        "query": query,
        "language": "hindi",
        "script": {"primary_script": "devanagari", "mixed_script": False},
        "intent": "general_query",
        "cultural_context": {
            "festivals": [],
            "food_items": [],
            "healthcare_topics": []
        },
        "real_world_data": real_world_data,
        "response": {
            "type": "real_world_response",
            "cultural_introduction": f"आपके प्रश्न '{query}' के बारे में वास्तविक जानकारी:",
            "main_content": response_content,
            "practical_advice": "🌐 **वास्तविक डेटा**: यह जानकारी इंटरनेट से प्राप्त की गई है।",
            "additional_resources": [
                {
                    "title": result.get('title', 'No title'),
                    "link": result.get('link', ''),
                    "source": result.get('source', 'Unknown'),
                    "snippet": result.get('snippet', '')[:100] + "..." if result.get('snippet') else ""
                }
                for result in search_results[:3]
            ],
            "confidence_level": "high" if has_real_data else "low"
        },
        "confidence": 0.9 if has_real_data else 0.4,
        "response_time_ms": 150,
        "timestamp": datetime.now().isoformat(),
        "node_id": "hindi_node_real_world"
    }

async def generate_real_telugu_response(query: str, real_world_data: Dict) -> Dict[str, Any]:
    """Generate Telugu response with real Google search results"""
    
    search_results = real_world_data.get('search_results', [])
    has_real_data = len(search_results) > 0
    
    if has_real_data:
        top_result = search_results[0]
        real_content = top_result.get('snippet', '')[:500]  # Use snippet only
        real_sources = [r.get('source', 'Unknown') for r in search_results[:3]]
        
        # Check if AI summary is available
        ai_summary_text = ""
        if real_world_data.get('ai_summary') and real_world_data['ai_summary'].get('ai_summary'):
            ai_summary_text = f"\n\n{real_world_data['ai_summary']['ai_summary']}"
        
        response_content = f"""
**వాస్తవ సమాచారం**: {real_content}

**మూలాలు**: {', '.join(real_sources)}{ai_summary_text}
        """.strip()
    else:
        response_content = f"'{query}' గురించి ప్రస్తుతం వివరణాత్మక సమాచారం అందుబాటులో లేదు।"
    
    return {
        "query": query,
        "language": "telugu",
        "script": {"primary_script": "telugu", "mixed_script": False},
        "intent": "general_query",
        "cultural_context": {"festivals": [], "literature": [], "temples": []},
        "real_world_data": real_world_data,
        "response": {
            "type": "real_world_response",
            "cultural_introduction": f"మీ ప్రశ్న '{query}' గురించి వాస్తవ సమాచారం:",
            "main_content": response_content,
            "practical_advice": "🌐 **వాస్తవ డేటా**: ఈ సమాచారం ఇంటర్నెట్ నుండి పొందబడింది।",
            "confidence_level": "high" if has_real_data else "low"
        },
        "confidence": 0.9 if has_real_data else 0.4,
        "response_time_ms": 150,
        "timestamp": datetime.now().isoformat()
    }

async def generate_real_marathi_response(query: str, real_world_data: Dict) -> Dict[str, Any]:
    """Generate Marathi response with real Google search results"""
    
    search_results = real_world_data.get('search_results', [])
    has_real_data = len(search_results) > 0
    
    if has_real_data:
        top_result = search_results[0]
        real_content = top_result.get('snippet', '')[:500]  # Use snippet only
        real_sources = [r.get('source', 'Unknown') for r in search_results[:3]]
        
        # Check if AI summary is available
        ai_summary_text = ""
        if real_world_data.get('ai_summary') and real_world_data['ai_summary'].get('ai_summary'):
            ai_summary_text = f"\n\n{real_world_data['ai_summary']['ai_summary']}"
        
        response_content = f"""
**वास्तविक माहिती**: {real_content}

**स्रोत**: {', '.join(real_sources)}{ai_summary_text}
        """.strip()
    else:
        response_content = f"'{query}' बद्दल सध्या तपशीलवार माहिती उपलब्ध नाही।"
    
    return {
        "query": query,
        "language": "marathi",
        "script": {"primary_script": "devanagari", "mixed_script": False},
        "intent": "general_query",
        "cultural_context": {"festivals": [], "business": [], "arts": []},
        "real_world_data": real_world_data,
        "response": {
            "type": "real_world_response",
            "cultural_introduction": f"तुमच्या प्रश्न '{query}' बद्दल वास्तविक माहिती:",
            "main_content": response_content,
            "practical_advice": "🌐 **वास्तविक डेटा**: ही माहिती इंटरनेटवरून मिळवली आहे।",
            "confidence_level": "high" if has_real_data else "low"
        },
        "confidence": 0.9 if has_real_data else 0.4,
        "response_time_ms": 150,
        "timestamp": datetime.now().isoformat()
    }

async def generate_real_english_response(query: str, real_world_data: Dict) -> Dict[str, Any]:
    """Generate English response with real Google search results"""
    
    search_results = real_world_data.get('search_results', [])
    has_real_data = len(search_results) > 0
    
    if has_real_data:
        top_result = search_results[0]
        real_content = top_result.get('snippet', '')[:500]  # Use snippet only
        real_sources = [r.get('source', 'Unknown') for r in search_results[:3]]
        
        # Check if AI summary is available
        ai_summary_text = ""
        if real_world_data.get('ai_summary') and real_world_data['ai_summary'].get('ai_summary'):
            ai_summary_text = f"\n\n{real_world_data['ai_summary']['ai_summary']}"
        
        response_content = f"""
**Real Information**: {real_content}

**Sources**: {', '.join(real_sources)}{ai_summary_text}
        """.strip()
    else:
        response_content = f"'{query}' - Detailed information is currently not available."
    
    return {
        "query": query,
        "language": "english",
        "script": {"primary_script": "latin", "mixed_script": False},
        "intent": "general_query",
        "cultural_context": {"festivals": [], "business": [], "technology": []},
        "real_world_data": real_world_data,
        "response": {
            "type": "real_world_response",
            "cultural_introduction": f"Real-world information about '{query}':",
            "main_content": response_content,
            "practical_advice": "🌐 **Live Data**: This information was retrieved from the internet.",
            "confidence_level": "high" if has_real_data else "low"
        },
        "confidence": 0.9 if has_real_data else 0.4,
        "response_time_ms": 150,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/federation/status")
async def get_federation_status():
    """Get federation learning status"""
    # For MVP, return simulated federation status
    return {
        "federation_active": True,
        "participating_nodes": list(LANGUAGE_NODES.keys()),
        "current_round": 1,
        "last_update": datetime.now().isoformat(),
        "global_model_version": "1.0.0",
        "performance_metrics": {
            "average_accuracy": 0.85,
            "cultural_relevance": 0.88,
            "average_response_time": 150,
            "total_queries_processed": 1000
        }
    }

@app.get("/api/v1/languages")
async def get_supported_languages():
    """Get list of supported languages with details"""
    languages = {
        "hindi": {
            "code": "hi",
            "name": "Hindi",
            "script": "Devanagari",
            "speakers": "600M+",
            "regions": ["North India", "Central India"],
            "cultural_domains": ["festivals", "food", "healthcare", "education", "government"]
        },
        "telugu": {
            "code": "te", 
            "name": "Telugu",
            "script": "Telugu Script",
            "speakers": "95M+",
            "regions": ["Andhra Pradesh", "Telangana"],
            "cultural_domains": ["festivals", "literature", "agriculture", "temples", "arts"]
        },
        "marathi": {
            "code": "mr",
            "name": "Marathi", 
            "script": "Devanagari",
            "speakers": "95M+",
            "regions": ["Maharashtra", "Goa"],
            "cultural_domains": ["festivals", "business", "arts", "history", "literature"]
        },
        "english": {
            "code": "en",
            "name": "English",
            "script": "Latin",
            "speakers": "300M+ (India)",
            "regions": ["All India", "Urban Areas", "Business"],
            "cultural_domains": ["business", "technology", "education", "government", "global"]
        }
    }
    
    return {
        "supported_languages": languages,
        "total_languages": len(languages),
        "total_speakers": "1090M+",
        "last_updated": datetime.now().isoformat()
    }

# Example queries endpoint for testing
@app.get("/api/v1/examples")
async def get_example_queries():
    """Get example queries for each language"""
    examples = {
        "hindi": [
            "दिवाली की सफाई कैसे करें?",
            "होली के रंग कैसे बनाएं?",
            "बुखार के लिए घरेलू नुस्खे क्या हैं?",
            "प्रधानमंत्री आवास योजना कैसे apply करें?"
        ],
        "telugu": [
            "ఉగాది పండుగ ఎలా జరుపుకోవాలి?",
            "దసరా గోలు ఎలా అలంకరించాలి?",
            "సాంప్రదాయిక తెలుగు వంటకాలు ఏవి?",
            "తిరుమల దర్శనం కోసం ఎలా బుక్ చేయాలి?"
        ],
        "marathi": [
            "गणेशचतुर्थी कसे साजरे करावे?",
            "गुढी पाडवा च्या गुढी कशी बनवावी?",
            "महाराष्ट्रीयन व्यापार संधी कोणत्या आहेत?",
            "पुण्यात IT जॉब कसे मिळवावे?"
        ],
        "english": [
            "What are the latest cricket updates?",
            "How to start a business in India?",
            "Best tourist places in India",
            "How to apply for Indian passport?"
        ]
    }
    
    return {
        "example_queries": examples,
        "usage": "Use these queries to test the language detection and processing capabilities",
        "note": "Each query demonstrates cultural context understanding in respective languages. English queries focus on general information and business topics."
    }

# New agentic search endpoint
@app.post("/api/v1/agentic-search")
async def agentic_search(request: AgenticSearchRequest):
    """Advanced search with agentic AI summarization"""
    try:
        # Import here to avoid circular imports
        from core.hybrid_summarizer import hybrid_summarizer
        
        logger.info(f"🤖 Agentic search request: {request.query} ({request.language}) using {request.approach}")
        
        # Use the real-world data aggregator
        search_results = await process_real_world_search(request.query, request.language, request.max_results)
        
        if 'error' in search_results:
            return JSONResponse(
                status_code=500,
                content={"error": search_results['error']}
            )
        
        # Get the raw search results
        raw_results = search_results.get('search_results', [])
        
        # Apply agentic summarization with specified approach
        if request.approach == "lightweight":
            summary_result = hybrid_summarizer.summarize_search_results(
                raw_results, request.query, request.language,
                force_lightweight=True
            )
        elif request.approach == "agentic":
            summary_result = hybrid_summarizer.summarize_search_results(
                raw_results, request.query, request.language,
                force_agentic=True
            )
        else:  # hybrid
            summary_result = hybrid_summarizer.summarize_search_results(
                raw_results, request.query, request.language
            )
        
        # Combine results
        response = {
            "query": request.query,
            "language": request.language,
            "approach_requested": request.approach,
            "approach_used": summary_result.get('approach_used', 'unknown'),
            "execution_time": summary_result.get('execution_time', 0),
            "ai_summary": summary_result.get('ai_summary', ''),
            "key_insights": summary_result.get('key_insights', []),
            "confidence_score": summary_result.get('confidence_score', 0.0),
            "search_results": raw_results,
            "source_count": len(raw_results),
            "timestamp": datetime.now().isoformat(),
            "execution_details": summary_result.get('execution_details', {})
        }
        
        logger.info(f"✅ Agentic search completed using {summary_result.get('approach_used')} approach")
        return response
        
    except Exception as e:
        logger.error(f"❌ Agentic search failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Agentic search failed: {str(e)}"
        )

# Summarizer configuration endpoint
@app.get("/api/v1/summarizer/config")
async def get_summarizer_config():
    """Get current summarizer configuration"""
    try:
        from core.hybrid_summarizer import hybrid_summarizer
        
        config = hybrid_summarizer.get_summarizer_info()
        return {
            "config": config,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get summarizer config: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get configuration: {str(e)}"
        )

@app.post("/api/v1/summarizer/config")
async def update_summarizer_config(request: SummarizerConfigRequest):
    """Update summarizer configuration"""
    try:
        from core.hybrid_summarizer import hybrid_summarizer
        
        # Prepare configuration updates
        config_updates = {}
        
        if request.use_agentic_by_default is not None:
            config_updates['use_agentic_by_default'] = request.use_agentic_by_default
            
        if request.min_results_threshold is not None or request.min_content_length is not None:
            agentic_thresholds = {}
            if request.min_results_threshold is not None:
                agentic_thresholds['min_results'] = request.min_results_threshold
            if request.min_content_length is not None:
                agentic_thresholds['min_content_length'] = request.min_content_length
            config_updates['agentic_thresholds'] = agentic_thresholds
        
        # Apply configuration
        if config_updates.get('use_agentic_by_default') is not None:
            hybrid_summarizer.configure(use_agentic_by_default=config_updates['use_agentic_by_default'])
            
        if config_updates.get('agentic_thresholds'):
            hybrid_summarizer.configure(agentic_thresholds=config_updates['agentic_thresholds'])
        
        # Return updated configuration
        updated_config = hybrid_summarizer.get_summarizer_info()
        
        logger.info(f"🔧 Summarizer configuration updated: {config_updates}")
        
        return {
            "message": "Configuration updated successfully",
            "updates_applied": config_updates,
            "new_config": updated_config,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to update summarizer config: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )

# Summarizer benchmarking endpoint
@app.post("/api/v1/summarizer/benchmark")
async def benchmark_summarizers(request: SearchRequest):
    """Benchmark different summarization approaches"""
    try:
        from core.hybrid_summarizer import hybrid_summarizer
        import time
        
        logger.info(f"📊 Benchmarking summarizers for: {request.query} ({request.language})")
        
        # Get search results first
        search_results = await process_real_world_search(request.query, request.language, 3)
        
        if 'error' in search_results:
            return JSONResponse(
                status_code=500,
                content={"error": search_results['error']}
            )
        
        raw_results = search_results.get('search_results', [])
        
        # Benchmark both approaches
        results = {}
        
        # Test lightweight approach
        start_time = time.time()
        lightweight_result = hybrid_summarizer.summarize_search_results(
            raw_results, request.query, request.language, force_lightweight=True
        )
        lightweight_time = time.time() - start_time
        
        results['lightweight'] = {
            'execution_time': lightweight_time,
            'approach_used': lightweight_result.get('approach_used'),
            'summary_length': len(lightweight_result.get('ai_summary', '')),
            'confidence_score': lightweight_result.get('confidence_score', 0),
            'insights_count': len(lightweight_result.get('key_insights', [])),
            'summary': lightweight_result.get('ai_summary', '')[:200] + "..." if len(lightweight_result.get('ai_summary', '')) > 200 else lightweight_result.get('ai_summary', '')
        }
        
        # Test agentic approach (with fallback handling)
        start_time = time.time()
        try:
            agentic_result = hybrid_summarizer.summarize_search_results(
                raw_results, request.query, request.language, force_agentic=True
            )
            agentic_time = time.time() - start_time
            
            results['agentic'] = {
                'execution_time': agentic_time,
                'approach_used': agentic_result.get('approach_used'),
                'summary_length': len(agentic_result.get('ai_summary', '')),
                'confidence_score': agentic_result.get('confidence_score', 0),
                'insights_count': len(agentic_result.get('key_insights', [])),
                'execution_details': agentic_result.get('execution_details', {}),
                'summary': agentic_result.get('ai_summary', '')[:200] + "..." if len(agentic_result.get('ai_summary', '')) > 200 else agentic_result.get('ai_summary', '')
            }
        except Exception as e:
            agentic_time = time.time() - start_time
            results['agentic'] = {
                'execution_time': agentic_time,
                'approach_used': 'error',
                'error': str(e),
                'summary': 'Failed to generate agentic summary'
            }
        
        # Performance comparison
        comparison = {
            'speed_difference': f"{abs(lightweight_time - agentic_time):.3f}s",
            'faster_approach': 'lightweight' if lightweight_time < agentic_time else 'agentic',
            'quality_difference': abs(results['lightweight'].get('confidence_score', 0) - results['agentic'].get('confidence_score', 0)) if 'confidence_score' in results['agentic'] else 'N/A'
        }
        
        return {
            "query": request.query,
            "language": request.language,
            "source_count": len(raw_results),
            "benchmark_results": results,
            "performance_comparison": comparison,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Benchmark failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Benchmark failed: {str(e)}"
        )

if __name__ == "__main__":
    logger.info("Starting GlobalMind FL API Gateway...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
