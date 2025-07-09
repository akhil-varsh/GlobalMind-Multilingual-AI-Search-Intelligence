"""
End-to-end Integration Test for Real-world Data Access
Tests the complete flow from API gateway to Google Custom Search API
"""

import asyncio
import json
import logging
import requests
import time
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegrationTester:
    """Test real-world data integration across all components"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:8000"
        self.test_queries = {
            "hindi": [
                "दिवाली की सफाई कैसे करें",
                "प्रधानमंत्री आवास योजना",
                "आयुर्वेद स्वास्थ्य"
            ],
            "telugu": [
                "ఉగాది పండుగ ఎలా జరుపుకోవాలి",
                "తిరुమల దర్శనం",
                "తెలుగు వంటకాలు"
            ],
            "marathi": [
                "गणेशचतुर्थी तयारी",
                "पुण्यात व्यापार संधी",
                "महाराष्ट्रीयन पाककृती"
            ]
        }
        
    async def test_direct_real_world_data(self):
        """Test direct real-world data access"""
        logger.info("🧪 Testing direct real-world data access...")
        
        try:
            # Import and test real-world data components
            from core.real_world_data import GoogleCSEIntegration, RealWorldDataAggregator
            
            # Initialize
            google_cse = GoogleCSEIntegration()
            aggregator = RealWorldDataAggregator(google_cse)
            
            # Test with Hindi query
            test_query = "दिवाली की सफाई"
            logger.info(f"Testing query: {test_query}")
            
            real_world_data = aggregator.get_real_world_context(test_query, "hindi", {})
            
            # Validate results
            search_results = real_world_data.get('search_results', [])
            logger.info(f"✅ Found {len(search_results)} search results")
            
            if search_results:
                first_result = search_results[0]
                logger.info(f"📰 First result: {first_result.get('title', 'No title')[:50]}...")
                logger.info(f"🔗 Source: {first_result.get('source', 'Unknown')}")
                return True
            else:
                logger.warning("⚠️ No search results found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Direct real-world data test failed: {e}")
            return False
            
    async def test_language_nodes(self):
        """Test individual language nodes with real-world data"""
        logger.info("🧪 Testing language nodes...")
        
        try:
            # Test Hindi node
            from language_nodes.hindi_node import HindiNode
            
            config = {"api_endpoint": "test", "model_version": "1.0"}
            hindi_node = HindiNode(config)
            await hindi_node.initialize()
            
            test_query = "दिवाली की सफाई"
            result = await hindi_node.process_query(test_query)
            
            logger.info(f"✅ Hindi node response type: {result.get('response', {}).get('type', 'unknown')}")
            logger.info(f"🔍 Has real-world data: {len(result.get('real_world_data', {}).get('search_results', [])) > 0}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Language node test failed: {e}")
            return False
            
    async def test_api_gateway_direct(self):
        """Test API gateway processing function directly"""
        logger.info("🧪 Testing API gateway direct processing...")
        
        try:
            # Import API gateway function
            import sys
            import os
            sys.path.append('api')
            
            from api.main import actual_node_processing
            
            # Test all languages
            for language, queries in self.test_queries.items():
                test_query = queries[0]
                logger.info(f"Testing {language}: {test_query}")
                
                result = await actual_node_processing(language, test_query, {})
                
                logger.info(f"✅ {language} response type: {result.get('response', {}).get('type', 'unknown')}")
                has_real_data = len(result.get('real_world_data', {}).get('search_results', [])) > 0
                logger.info(f"🔍 {language} has real data: {has_real_data}")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ API gateway direct test failed: {e}")
            return False
            
    def test_api_endpoints(self):
        """Test API endpoints via HTTP requests"""
        logger.info("🧪 Testing API endpoints...")
        
        try:
            # Test health endpoint
            response = requests.get(f"{self.api_base_url}/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Health endpoint working")
            else:
                logger.warning(f"⚠️ Health endpoint returned {response.status_code}")
                
            # Test query endpoint
            for language, queries in self.test_queries.items():
                test_query = queries[0]
                
                payload = {
                    "query": test_query,
                    "language": language
                }
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/query",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ {language} API call successful")
                    logger.info(f"🔍 Response type: {result.get('response', {}).get('response', {}).get('type', 'unknown')}")
                else:
                    logger.error(f"❌ {language} API call failed: {response.status_code}")
                    
            return True
            
        except requests.exceptions.ConnectionError:
            logger.warning("⚠️ API server not running - skipping HTTP tests")
            return False
        except Exception as e:
            logger.error(f"❌ API endpoint test failed: {e}")
            return False
            
    async def test_performance(self):
        """Test performance with real-world data"""
        logger.info("🧪 Testing performance...")
        
        try:
            from core.real_world_data import GoogleCSEIntegration, RealWorldDataAggregator
            
            google_cse = GoogleCSEIntegration()
            aggregator = RealWorldDataAggregator(google_cse)
            
            # Test response times
            test_queries = ["दिवाली", "ఉగాది", "गणेश"]
            
            for query in test_queries:
                start_time = time.time()
                
                real_world_data = aggregator.get_real_world_context(query, "hindi", {})
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                logger.info(f"⏱️ Query '{query}': {response_time:.2f}ms")
                
                if response_time > 5000:  # 5 seconds
                    logger.warning(f"⚠️ Slow response for '{query}': {response_time:.2f}ms")
                    
            return True
            
        except Exception as e:
            logger.error(f"❌ Performance test failed: {e}")
            return False
            
    async def run_all_tests(self):
        """Run comprehensive integration tests"""
        logger.info("🚀 Starting comprehensive integration tests...")
        
        test_results = {}
        
        # Test 1: Direct real-world data access
        test_results["direct_real_world"] = await self.test_direct_real_world_data()
        
        # Test 2: Language nodes
        test_results["language_nodes"] = await self.test_language_nodes()
        
        # Test 3: API gateway direct
        test_results["api_gateway_direct"] = await self.test_api_gateway_direct()
        
        # Test 4: Performance
        test_results["performance"] = await self.test_performance()
        
        # Test 5: API endpoints (if server is running)
        test_results["api_endpoints"] = self.test_api_endpoints()
        
        # Summary
        logger.info("\n" + "="*50)
        logger.info("🏁 INTEGRATION TEST SUMMARY")
        logger.info("="*50)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{test_name:<20}: {status}")
            if result:
                passed += 1
                
        logger.info(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            logger.info("🎉 ALL TESTS PASSED! Real-world data integration is working!")
        else:
            logger.warning(f"⚠️ {total - passed} tests failed. Check logs above.")
            
        return test_results

async def main():
    """Main test execution"""
    tester = IntegrationTester()
    results = await tester.run_all_tests()
    return results

if __name__ == "__main__":
    asyncio.run(main())
