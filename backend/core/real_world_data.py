"""
Real-World Data Integration Module
Integrates Google Custom Search API for real-world information
Focus on general search snippets only (no newspaper content extraction)
Includes AI-powered summarization capabilities
"""

import requests
import time
from typing import List, Dict, Optional
import logging
import os
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class GoogleCSEIntegration:
    """Google Custom Search Engine Integration for real-world data"""
    
    def __init__(self, api_key: str = None, cse_id: str = None):
        self.api_key = api_key or os.getenv('GOOGLE_CSE_API_KEY', 'AIzaSyAU1JQ_nsWtUl7HlQk0Cyo4Z0BXEzfEjcc')
        self.cse_id = cse_id or os.getenv('GOOGLE_CSE_ID', '82da8e240e25c4f0c')
        self.base_url = "https://www.googleapis.com/customsearch/v1"
    
    def search_with_language_context(self, query: str, language: str, num_results: int = 5) -> List[Dict]:
        """Search with language and cultural context"""
        enhanced_query = self._enhance_query_for_language(query, language)
        
        params = {
            "q": enhanced_query,
            "key": self.api_key,
            "cx": self.cse_id,
            "num": num_results,
            "lr": self._get_language_restriction(language),
            "gl": "IN",  # Geographic location: India
            "cr": "countryIN"  # Country restriction
        }
        
        try:
            logger.info(f"Searching for: {enhanced_query} in {language}")
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                results = response.json().get("items", [])
                return self._process_search_results(results, language)
            else:
                logger.error(f"Google CSE API Error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error in Google CSE search: {e}")
            return []
    
    def _enhance_query_for_language(self, query: str, language: str) -> str:
        """Add cultural context to search query"""
        enhancements = {
            'hindi': f"{query} हिंदी भारत",
            'telugu': f"{query} తెలుగు భారత్",
            'marathi': f"{query} मराठी भारत",
            'english': f"{query} India English"
        }
        return enhancements.get(language, query)
    
    def _get_language_restriction(self, language: str) -> str:
        """Get Google language restriction code"""
        lang_codes = {
            'hindi': 'lang_hi',
            'telugu': 'lang_te', 
            'marathi': 'lang_mr',
            'english': 'lang_en'
        }
        return lang_codes.get(language, 'lang_en')
    
    def _process_search_results(self, results: List[Dict], language: str) -> List[Dict]:
        """Extract and process content from search results (snippets only)"""
        processed_results = []
        
        for item in results[:3]:  # Limit to top 3 for MVP
            try:
                result_data = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': self._extract_domain(item.get('link', '')),
                    'language': language,
                    'relevance_score': 0.8,  # Default relevance
                    # Use only snippet content for general search
                    'content': item.get('snippet', ''),
                    'extraction_success': True
                }
                
                processed_results.append(result_data)
                
            except Exception as e:
                logger.warning(f"Error processing result {item.get('link', '')}: {e}")
                continue
        
        return processed_results
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            domain = urlparse(url).netloc
            return domain.replace('www.', '') if domain else "Unknown Source"
        except:
            return "Unknown Source"


class RealWorldDataAggregator:
    """Aggregates and processes real-world data from multiple sources with AI summarization"""
    
    def __init__(self, google_cse: GoogleCSEIntegration):
        self.google_cse = google_cse
        self.cache = {}  # Simple in-memory cache
        self.cache_timeout = 3600  # 1 hour
        self.ai_summarizer = None
        self._initialize_ai_summarizer()
    
    def get_real_world_context(self, query: str, language: str, cultural_context: Dict) -> Dict:
        """Get real-world data with cultural context and AI summarization"""
        cache_key = f"{query}_{language}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                logger.info(f"Returning cached results for: {query}")
                return cached_data
        
        # Search for real-world information
        logger.info(f"Fetching real-world data for: {query} in {language}")
        search_results = self.google_cse.search_with_language_context(query, language)
        
        # Generate AI-powered summary
        ai_summary_data = self._generate_ai_summary(search_results, query, language)
        
        # Process and summarize results (traditional method as fallback)
        traditional_summary = self._create_cultural_summary(search_results, cultural_context, language)
        
        result = {
            'query': query,
            'language': language,
            'search_results': search_results,
            'summary': traditional_summary,
            'ai_summary': ai_summary_data,  # New AI-powered summary
            'sources': [r['source'] for r in search_results],
            'total_results': len(search_results),
            'has_real_world_data': len(search_results) > 0,
            'timestamp': time.time(),
            'has_ai_summary': ai_summary_data is not None
        }
        
        # Cache the result
        self.cache[cache_key] = (result, time.time())
        
        return result
    
    def _create_cultural_summary(self, results: List[Dict], cultural_context: Dict, language: str) -> str:
        """Create a culturally-aware summary from search results (snippets only)"""
        if not results:
            return self._get_no_results_message(language)
        
        summary_parts = []
        
        # Add most relevant result summary from snippet
        if results:
            top_result = results[0]
            content_preview = top_result.get('snippet', '')[:300]
            
            if language == 'hindi':
                summary_parts.append(f"**मुख्य जानकारी**: {content_preview}")
            elif language == 'telugu':
                summary_parts.append(f"**ప్రధాన సమాచారం**: {content_preview}")
            elif language == 'marathi':
                summary_parts.append(f"**मुख्य माहिती**: {content_preview}")
            elif language == 'english':
                summary_parts.append(f"**Main Information**: {content_preview}")
        
        # Add cultural context if available
        if cultural_context.get('festivals'):
            festival_info = cultural_context['festivals'][0] if cultural_context['festivals'] else None
            if festival_info:
                if language == 'hindi':
                    summary_parts.append(f"**सांस्कृतिक संदर्भ**: यह {festival_info} से संबंधित है।")
                elif language == 'telugu':
                    summary_parts.append(f"**సాంస్కృతిక సందర్భం**: ఇది {festival_info} తో సంబంధించినది।")
                elif language == 'marathi':
                    summary_parts.append(f"**सांस्कृतिक संदर्भ**: हे {festival_info} शी संबंधित आहे।")
                elif language == 'english':
                    summary_parts.append(f"**Cultural Context**: This relates to {festival_info}.")
        
        # Add source attribution
        if results:
            unique_sources = list(set([r['source'] for r in results[:3]]))
            source_text = {
                'hindi': "**स्रोत**: ",
                'telugu': "**మూలాలు**: ",
                'marathi': "**स्रोत**: ",
                'english': "**Sources**: "
            }.get(language, "**Sources**: ")
            summary_parts.append(f"{source_text}{', '.join(unique_sources)}")
        
        return "\n\n".join(summary_parts)
    
    def _get_no_results_message(self, language: str) -> str:
        """Get appropriate no results message for language"""
        messages = {
            'hindi': "इस विषय पर वर्तमान में विस्तृत जानकारी उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।",
            'telugu': "ప్రస్తుతం ఈ విषయంపై వివరణాత్మక సమాచారం అందుబాటులో లేదు। దయచేసి తరువాత మళ్లీ ప్రయత్నించండి।",
            'marathi': "सध्या या विषयावर तपशीलवार माहिती उपलब्ध नाही. कृपया नंतर पुन्हा प्रयत्न करा।",
            'english': "Detailed information on this topic is currently not available. Please try again later."
        }
        return messages.get(language, "Information not currently available.")
    
    def _initialize_ai_summarizer(self):
        """Initialize AI summarizer if available"""
        try:
            from .hybrid_summarizer import hybrid_summarizer
            self.ai_summarizer = hybrid_summarizer
            logger.info("🤖 AI summarizer integrated successfully")
        except ImportError as e:
            logger.warning(f"📝 AI summarizer not available: {e}")
            logger.info("💡 Using rule-based summarization as fallback")
            self.ai_summarizer = None
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI summarizer: {e}")
            self.ai_summarizer = None
    
    def _generate_ai_summary(self, search_results: List[Dict], query: str, language: str) -> Optional[Dict]:
        """Generate AI-powered summary from search results"""
        if not self.ai_summarizer:
            return None
        
        try:
            logger.info(f"🤖 Generating AI summary for '{query}' in {language}")
            summary_data = self.ai_summarizer.summarize_search_results(
                search_results, query, language
            )
            return summary_data
        except Exception as e:
            logger.error(f"❌ AI summarization failed: {e}")
            return None
