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
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Language node endpoints
LANGUAGE_NODES = {
    "hindi": "http://localhost:8001",
    "telugu": "http://localhost:8002", 
    "marathi": "http://localhost:8003"
}

# Language detection patterns (simplified for MVP)
LANGUAGE_PATTERNS = {
    "hindi": ["दिवाली", "होली", "करवा", "चौथ", "नमस्ते", "धन्यवाद", "कैसे", "क्या", "कहाँ"],
    "telugu": ["ఉగాది", "దసరా", "దీపావళి", "నమస్తే", "ధన్యవాదాలు", "ఎలా", "ఎప్పుడు", "ఎక్కడ"],
    "marathi": ["गणेशचतुर्थी", "गुढी", "पाडवा", "नमस्कार", "धन्यवाद", "कसे", "कधी", "कुठे"]
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
        detected_language = "hindi"  # Default to Hindi for MVP
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
        
        # For MVP, we'll simulate the node communication
        # In production, this would be actual HTTP requests to language nodes
        node_response = await simulate_node_processing(detected_language, request.query, request.context)
        
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

async def simulate_node_processing(language: str, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Simulate language node processing (MVP implementation)"""
    
    # For MVP, we'll create a simple response simulation
    # In a real implementation, this would route to actual language nodes
    await asyncio.sleep(0.1)  # Simulate processing time
    
    if language == "hindi":
        return await simulate_hindi_response(query)
    elif language == "telugu":
        return await simulate_telugu_response(query)
    elif language == "marathi":
        return await simulate_marathi_response(query)
    else:
        raise ValueError(f"Unsupported language: {language}")

async def simulate_hindi_response(query: str) -> Dict[str, Any]:
    """Simulate Hindi node response"""
    return {
        "query": query,
        "language": "hindi",
        "script": {"primary_script": "devanagari", "mixed_script": False},
        "intent": "general_query",
        "cultural_context": {
            "festivals": [],
            "food_items": [],
            "healthcare_topics": [],
            "government_schemes": []
        },
        "response": {
            "type": "general_response",
            "content": f"आपके प्रश्न '{query}' के बारे में जानकारी प्रदान करने का प्रयास कर रहे हैं।",
            "suggestion": "कृपया अधिक विशिष्ट जानकारी के लिए प्रश्न को स्पष्ट करें।"
        },
        "confidence": 0.85,
        "response_time_ms": 100,
        "timestamp": datetime.now().isoformat()
    }

async def simulate_telugu_response(query: str) -> Dict[str, Any]:
    """Simulate Telugu node response"""
    return {
        "query": query,
        "language": "telugu",
        "script": {"primary_script": "telugu", "mixed_script": False},
        "intent": "general_query",
        "cultural_context": {
            "festivals": [],
            "literature": [],
            "temples": []
        },
        "response": {
            "type": "general_response",
            "content": f"మీ ప్రశ్న '{query}' గురించి సమాచారం అందించడానికి ప్రయత్నిస్తున్నాము.",
            "suggestion": "దయచేసి మరింత నిర్దిష్ట సమాచారం కోసం ప్రశ్నను స్పష్టపరచండి."
        },
        "confidence": 0.85,
        "response_time_ms": 100,
        "timestamp": datetime.now().isoformat()
    }

async def simulate_marathi_response(query: str) -> Dict[str, Any]:
    """Simulate Marathi node response"""
    return {
        "query": query,
        "language": "marathi",
        "script": {"primary_script": "devanagari", "mixed_script": False},
        "intent": "general_query",
        "cultural_context": {
            "festivals": [],
            "business": [],
            "arts": []
        },
        "response": {
            "type": "general_response", 
            "content": f"तुमच्या प्रश्न '{query}' बद्दल माहिती देण्याचा प्रयत्न करत आहोत.",
            "suggestion": "कृपया अधिक विशिष्ट माहितीसाठी प्रश्न स्पष्ट करा."
        },
        "confidence": 0.85,
        "response_time_ms": 100,
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
        }
    }
    
    return {
        "supported_languages": languages,
        "total_languages": len(languages),
        "total_speakers": "790M+",
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
        ]
    }
    
    return {
        "example_queries": examples,
        "usage": "Use these queries to test the language detection and processing capabilities",
        "note": "Each query demonstrates cultural context understanding in respective languages"
    }

if __name__ == "__main__":
    logger.info("Starting GlobalMind FL API Gateway...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
