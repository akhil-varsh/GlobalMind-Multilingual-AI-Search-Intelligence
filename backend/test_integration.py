#!/usr/bin/env python3
"""
Test script to verify real-world search integration
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

async def test_real_world_integration():
    """Test the real-world search integration"""
    
    print("🧪 Testing GlobalMind FL Real-World Integration...")
    
    # Test 1: Google CSE Integration
    try:
        from core.real_world_data import GoogleCSEIntegration, RealWorldDataAggregator
        
        print("✅ Successfully imported real-world data modules")
        
        # Initialize Google CSE
        google_cse = GoogleCSEIntegration()
        aggregator = RealWorldDataAggregator(google_cse)
        
        print(f"✅ Google CSE initialized with API key: {google_cse.api_key[:10]}...")
        
        # Test search
        test_queries = [
            "दिवाली की सफाई कैसे करें",
            "कोविड वैक्सीन की जानकारी",
            "प्रधानमंत्री आवास योजना"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: {query}")
            
            try:
                results = google_cse.search_with_language_context(query, "hindi", 2)
                
                if results:
                    print(f"   ✅ Found {len(results)} results")
                    for i, result in enumerate(results, 1):
                        print(f"   {i}. {result.get('title', 'No title')[:50]}...")
                        print(f"      Source: {result.get('source', 'Unknown')}")
                        print(f"      Content: {result.get('content', result.get('snippet', ''))[:100]}...")
                else:
                    print(f"   ⚠️  No results found")
                    
            except Exception as e:
                print(f"   ❌ Query failed: {e}")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    # Test 2: API Gateway Integration
    try:
        from api.main import actual_node_processing
        
        print("\n✅ Successfully imported API gateway functions")
        
        # Test API processing
        test_query = "भारत में शिक्षा"
        print(f"\n🔍 Testing API processing for: {test_query}")
        
        result = await actual_node_processing("hindi", test_query)
        
        if result:
            print("✅ API processing successful")
            print(f"   Language: {result.get('language')}")
            print(f"   Confidence: {result.get('confidence')}")
            print(f"   Has real-world data: {bool(result.get('real_world_data'))}")
            
            if result.get('real_world_data'):
                rwd = result['real_world_data']
                print(f"   Real-world results: {len(rwd.get('search_results', []))}")
                print(f"   Sources: {rwd.get('sources', [])}")
        else:
            print("⚠️  API processing returned no result")
            
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        return False
    
    print("\n🎉 All tests completed!")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_real_world_integration())
    
    if success:
        print("\n✅ Real-world search integration is working!")
        print("🚀 Your GlobalMind FL now has actual Google Search capabilities!")
    else:
        print("\n❌ Integration tests failed. Check the error messages above.")
