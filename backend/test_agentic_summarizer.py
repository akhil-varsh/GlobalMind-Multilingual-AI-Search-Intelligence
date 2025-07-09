#!/usr/bin/env python3
"""
Test script for the new agentic and hybrid AI summarizers
Tests both lightweight and agentic approaches with sample data
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.hybrid_summarizer import hybrid_summarizer
from core.agentic_summarizer import agentic_summarizer
from core.ai_summarizer import ai_summarizer

def create_sample_search_results():
    """Create sample search results for testing"""
    return [
        {
            'title': 'Climate Change Effects on Global Weather Patterns',
            'snippet': 'Climate change is causing significant alterations in global weather patterns, including increased frequency of extreme weather events, rising sea levels, and changes in precipitation patterns worldwide.',
            'source': 'climate-research.org',
            'url': 'https://climate-research.org/patterns'
        },
        {
            'title': 'Impact of Global Warming on Arctic Ice',
            'snippet': 'Arctic ice sheets are melting at an unprecedented rate due to global warming. Scientists report that the Arctic could be ice-free during summers by 2050 if current trends continue.',
            'source': 'arctic-studies.com',
            'url': 'https://arctic-studies.com/ice-melting'
        },
        {
            'title': 'Renewable Energy Solutions for Climate Action',
            'snippet': 'Renewable energy technologies including solar, wind, and hydroelectric power are essential for reducing greenhouse gas emissions and combating climate change effectively.',
            'source': 'green-energy.org',
            'url': 'https://green-energy.org/solutions'
        }
    ]

def create_hindi_sample_results():
    """Create sample Hindi search results"""
    return [
        {
            'title': 'भारत में जलवायु परिवर्तन के प्रभाव',
            'snippet': 'भारत में जलवायु परिवर्तन के कारण मानसून में बदलाव, तापमान वृद्धि और प्राकृतिक आपदाओं में वृद्धि हो रही है। यह कृषि और जल संसाधनों को गंभीर रूप से प्रभावित कर रहा है।',
            'source': 'bharatweather.in',
            'url': 'https://bharatweather.in/climate-change'
        },
        {
            'title': 'नवीकरणीय ऊर्जा का महत्व',
            'snippet': 'सौर ऊर्जा, पवन ऊर्जा और जल विद्युत जैसे नवीकरणीय ऊर्जा स्रोत भारत की ऊर्जा सुरक्षा और पर्यावरण संरक्षण के लिए अत्यंत महत्वपूर्ण हैं।',
            'source': 'energyindia.gov.in',
            'url': 'https://energyindia.gov.in/renewable'
        }
    ]

async def test_agentic_summarizer():
    """Test the agentic summarizer directly"""
    print("\n" + "="*60)
    print("🤖 TESTING AGENTIC SUMMARIZER")
    print("="*60)
    
    sample_results = create_sample_search_results()
    query = "climate change impacts and solutions"
    language = "english"
    
    print(f"📊 Testing with {len(sample_results)} search results")
    print(f"🔍 Query: {query}")
    print(f"🌐 Language: {language}")
    
    start_time = datetime.now()
    
    try:
        result = await agentic_summarizer.summarize_search_results(
            sample_results, query, language
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Agentic summarization completed in {execution_time:.2f} seconds")
        print(f"📝 Summary: {result['ai_summary']}")
        print(f"💡 Key Insights: {result['key_insights']}")
        print(f"🎯 Confidence Score: {result['confidence_score']}")
        print(f"📊 Execution Details: {result.get('execution_details', {})}")
        
    except Exception as e:
        print(f"❌ Agentic summarizer test failed: {e}")
        import traceback
        traceback.print_exc()

def test_lightweight_summarizer():
    """Test the lightweight summarizer"""
    print("\n" + "="*60)
    print("⚡ TESTING LIGHTWEIGHT SUMMARIZER")
    print("="*60)
    
    sample_results = create_sample_search_results()
    query = "climate change impacts"
    language = "english"
    
    print(f"📊 Testing with {len(sample_results)} search results")
    print(f"🔍 Query: {query}")
    print(f"🌐 Language: {language}")
    
    start_time = datetime.now()
    
    try:
        result = ai_summarizer.summarize_search_results(
            sample_results, query, language
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Lightweight summarization completed in {execution_time:.2f} seconds")
        print(f"📝 Summary: {result['ai_summary']}")
        print(f"💡 Key Insights: {result['key_insights']}")
        print(f"🎯 Confidence Score: {result['confidence_score']}")
        print(f"🔧 Method: {result['summarization_method']}")
        
    except Exception as e:
        print(f"❌ Lightweight summarizer test failed: {e}")
        import traceback
        traceback.print_exc()

def test_hybrid_summarizer():
    """Test the hybrid summarizer with different scenarios"""
    print("\n" + "="*60)
    print("🔀 TESTING HYBRID SUMMARIZER")
    print("="*60)
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Simple Query (should use lightweight)',
            'results': create_sample_search_results()[:1],  # Only 1 result
            'query': 'weather',
            'language': 'english'
        },
        {
            'name': 'Complex Query (should use agentic)',
            'results': create_sample_search_results(),
            'query': 'comprehensive analysis of climate change impacts and renewable energy solutions',
            'language': 'english'
        },
        {
            'name': 'Hindi Language Test',
            'results': create_hindi_sample_results(),
            'query': 'जलवायु परिवर्तन',
            'language': 'hindi'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print(f"🔍 Query: {scenario['query']}")
        print(f"🌐 Language: {scenario['language']}")
        print(f"📊 Results count: {len(scenario['results'])}")
        
        start_time = datetime.now()
        
        try:
            result = hybrid_summarizer.summarize_search_results(
                scenario['results'], 
                scenario['query'], 
                scenario['language']
            )
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            print(f"✅ Completed in {execution_time:.2f}s using {result['approach_used']} approach")
            print(f"📝 Summary: {result['ai_summary'][:100]}..." if len(result['ai_summary']) > 100 else result['ai_summary'])
            print(f"🎯 Confidence: {result['confidence_score']}")
            
        except Exception as e:
            print(f"❌ Scenario failed: {e}")

def test_hybrid_configuration():
    """Test hybrid summarizer configuration"""
    print("\n" + "="*60)
    print("⚙️ TESTING HYBRID CONFIGURATION")
    print("="*60)
    
    # Get current configuration
    info = hybrid_summarizer.get_summarizer_info()
    print("📋 Current Configuration:")
    print(json.dumps(info, indent=2))
    
    # Test configuration changes
    print("\n🔧 Testing configuration changes...")
    
    # Force lightweight mode
    hybrid_summarizer.configure(use_agentic_by_default=False)
    result1 = hybrid_summarizer.summarize_search_results(
        create_sample_search_results(), 
        "complex analysis", 
        "english"
    )
    print(f"📊 Forced lightweight result: {result1['approach_used']}")
    
    # Force agentic mode
    hybrid_summarizer.configure(use_agentic_by_default=True)
    result2 = hybrid_summarizer.summarize_search_results(
        create_sample_search_results()[:1],  # Small dataset
        "simple query", 
        "english"
    )
    print(f"📊 Agentic preference result: {result2['approach_used']}")

async def main():
    """Run all tests"""
    print("🚀 STARTING AGENTIC AI SUMMARIZER TESTS")
    print("="*80)
    
    # Test individual components
    test_lightweight_summarizer()
    await test_agentic_summarizer()
    test_hybrid_summarizer()
    test_hybrid_configuration()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)

if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
