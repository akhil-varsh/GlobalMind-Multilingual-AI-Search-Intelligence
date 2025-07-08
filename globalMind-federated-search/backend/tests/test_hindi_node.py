"""
Test cases for Hindi Language Node
"""

import pytest
import asyncio
from backend.language_nodes.hindi_node import HindiNode

@pytest.fixture
async def hindi_node():
    """Create a Hindi node instance for testing"""
    config = {"test_mode": True}
    node = HindiNode(config)
    await node.initialize()
    return node

@pytest.mark.asyncio
async def test_hindi_node_initialization(hindi_node):
    """Test Hindi node initialization"""
    assert hindi_node.language_code == "hi"
    assert hindi_node.status == "ready"
    assert hindi_node.cultural_context is not None
    assert "festivals" in hindi_node.cultural_context

@pytest.mark.asyncio
async def test_diwali_query_processing(hindi_node):
    """Test processing of Diwali-related query"""
    query = "दिवाली की सफाई कैसे करें?"
    
    result = await hindi_node.process_query(query)
    
    assert result["language"] == "hindi"
    assert result["intent"] == "how_to"
    assert len(result["cultural_context"]["festivals"]) > 0
    assert result["cultural_context"]["festivals"][0]["name"] == "दिवाली"
    assert result["response"]["type"] == "cultural_guide"

@pytest.mark.asyncio
async def test_healthcare_query_processing(hindi_node):
    """Test processing of healthcare-related query"""
    query = "बुखार के लिए घरेलू नुस्खे"
    
    result = await hindi_node.process_query(query)
    
    assert result["language"] == "hindi"
    assert result["intent"] == "healthcare_advice"
    assert len(result["cultural_context"]["healthcare_topics"]) > 0

@pytest.mark.asyncio
async def test_script_detection(hindi_node):
    """Test script detection functionality"""
    # Devanagari script
    devanagari_query = "दिवाली की सफाई"
    result = await hindi_node.process_query(devanagari_query)
    assert result["script"]["primary_script"] == "devanagari"
    
    # Roman script
    roman_query = "diwali ki safai"
    result = await hindi_node.process_query(roman_query)
    assert result["script"]["primary_script"] == "roman"

@pytest.mark.asyncio
async def test_cultural_context_detection(hindi_node):
    """Test cultural context detection"""
    query = "होली के रंग कैसे बनाएं?"
    
    cultural_context = await hindi_node._detect_cultural_context(query)
    
    assert len(cultural_context["festivals"]) > 0
    assert any(f["name"] == "होली" for f in cultural_context["festivals"])

@pytest.mark.asyncio
async def test_intent_classification(hindi_node):
    """Test intent classification"""
    test_cases = [
        ("कैसे करें?", "how_to"),
        ("कब मनाते हैं?", "timing_information"),
        ("क्या है?", "factual_question"),
        ("बुखार का इलाज", "healthcare_advice")
    ]
    
    for query, expected_intent in test_cases:
        intent = await hindi_node._classify_intent(query)
        assert intent == expected_intent

@pytest.mark.asyncio
async def test_health_check(hindi_node):
    """Test node health check"""
    health = await hindi_node.health_check()
    
    assert health["node_id"] == "hi_node"
    assert health["language"] == "hi"
    assert health["status"] == "ready"
    assert health["model_loaded"] is True

@pytest.mark.asyncio
async def test_performance_metrics(hindi_node):
    """Test performance metrics tracking"""
    # Process a few queries
    queries = [
        "दिवाली कैसे मनाएं?",
        "होली के रंग कैसे बनाएं?",
        "बुखार का घरेलू इलाज"
    ]
    
    for query in queries:
        await hindi_node.process_query(query)
    
    metrics = hindi_node.performance_metrics
    assert metrics["total_queries"] == len(queries)
    assert metrics["successful_queries"] == len(queries)
    assert metrics["average_response_time"] > 0

if __name__ == "__main__":
    pytest.main([__file__])
