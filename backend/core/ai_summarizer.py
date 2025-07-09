"""
AI-Powered Summarizer Module
Uses intelligent text processing for summarization of real-world search results
Supports multilingual summarization for Hindi, Telugu, Marathi, and English
Lightweight version with rule-based AI approach
"""

import logging
from typing import List, Dict, Optional, Any
import re
from datetime import datetime
from collections import Counter
import time

logger = logging.getLogger(__name__)

class AISearchSummarizer:
    """AI-powered summarizer for search results with multilingual support (lightweight version)"""
    
    def __init__(self):
        self.initialized = True  # Always initialized for lightweight version
        
        # Scoring weights for different aspects
        self.scoring_weights = {
            'position_weight': 0.4,  # Earlier results are more important
            'length_weight': 0.3,    # Longer snippets might be more informative
            'keyword_weight': 0.3    # Presence of query keywords
        }
        
        # Stop words for different languages
        self.stop_words = {
            'english': {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'},
            'hindi': {'का', 'के', 'को', 'में', 'और', 'या', 'से', 'पर', 'है', 'हैं', 'था', 'थे', 'यह', 'वह'},
            'telugu': {'మరియు', 'లేదా', 'లో', 'పై', 'కోసం', 'తో', 'ఇది', 'అది', 'ఉంది', 'ఉన్నారు'},
            'marathi': {'आणि', 'किंवा', 'मध्ये', 'वर', 'साठी', 'सोबत', 'हे', 'ते', 'आहे', 'आहेत'}
        }
        
        logger.info("🤖 Lightweight AI summarizer initialized successfully")
    
    def summarize_search_results(
        self, 
        search_results: List[Dict], 
        query: str, 
        language: str,
        max_results: int = 3
    ) -> Dict[str, Any]:
        """Generate intelligent summary from search results"""
        
        if not search_results:
            return self._generate_no_results_summary(query, language)
        
        # Combine and analyze text from top search results
        combined_analysis = self._analyze_search_results(search_results[:max_results], query, language)
        
        # Generate intelligent summary
        ai_summary = self._generate_intelligent_summary(combined_analysis, language)
        
        # Extract key insights
        key_insights = self._extract_key_insights(search_results, language)
        
        # Generate confidence score
        confidence_score = self._calculate_confidence(search_results, ai_summary)
        
        return {
            'query': query,
            'language': language,
            'ai_summary': ai_summary,
            'key_insights': key_insights,
            'confidence_score': confidence_score,
            'source_count': len(search_results),
            'sources': [r.get('source', 'Unknown') for r in search_results[:max_results]],
            'timestamp': datetime.now().isoformat(),
            'summarization_method': 'intelligent_rule_based'
        }
    
    def _analyze_search_results(self, search_results: List[Dict], query: str, language: str) -> Dict:
        """Analyze search results for intelligent summarization"""
        analysis = {
            'sentences': [],
            'query_keywords': self._extract_keywords(query, language),
            'source_reliability': {},
            'content_scores': []
        }
        
        for idx, result in enumerate(search_results):
            snippet = result.get('snippet', '').strip()
            title = result.get('title', '').strip()
            source = result.get('source', 'unknown')
            
            if snippet:
                # Clean and split content
                sentences = self._split_into_sentences(f"{title}. {snippet}")
                
                for sentence in sentences:
                    if len(sentence.split()) > 4:  # Skip very short sentences
                        score = self._score_sentence(sentence, query, idx, language)
                        analysis['sentences'].append({
                            'text': sentence,
                            'score': score,
                            'source': source,
                            'position': idx
                        })
                
                # Score source reliability (simplified)
                analysis['source_reliability'][source] = self._score_source_reliability(source)
        
        return analysis
    
    def _score_sentence(self, sentence: str, query: str, position: int, language: str) -> float:
        """Score a sentence based on relevance, position, and content quality"""
        score = 0.0
        
        # Position weight (earlier results are more important)
        position_score = (3 - position) / 3 * self.scoring_weights['position_weight']
        score += position_score
        
        # Length weight (moderate length sentences are better)
        words = sentence.split()
        length_score = min(len(words) / 20, 1.0) * self.scoring_weights['length_weight']
        score += length_score
        
        # Keyword matching weight
        query_words = set(query.lower().split())
        sentence_words = set(sentence.lower().split())
        stop_words = self.stop_words.get(language, set())
        
        # Remove stop words
        query_words = query_words - stop_words
        sentence_words = sentence_words - stop_words
        
        if query_words:
            keyword_overlap = len(query_words.intersection(sentence_words)) / len(query_words)
            keyword_score = keyword_overlap * self.scoring_weights['keyword_weight']
            score += keyword_score
        
        return min(score, 1.0)
    
    def _score_source_reliability(self, source: str) -> float:
        """Score source reliability (simplified heuristic)"""
        trusted_domains = {
            'wikipedia.org': 0.9,
            'bbc.com': 0.9,
            'timesofindia.com': 0.8,
            'hindustantimes.com': 0.8,
            'thehindu.com': 0.8,
            'indianexpress.com': 0.8,
            'news18.com': 0.7,
            'ndtv.com': 0.8,
            'zeenews.india.com': 0.7
        }
        
        for domain, score in trusted_domains.items():
            if domain in source.lower():
                return score
        
        # Default score for unknown sources
        return 0.6
    
    def _generate_intelligent_summary(self, analysis: Dict, language: str) -> str:
        """Generate intelligent summary from analyzed content"""
        if not analysis['sentences']:
            return self._get_default_message(language, "no_content")
        
        # Sort sentences by score
        top_sentences = sorted(analysis['sentences'], key=lambda x: x['score'], reverse=True)
        
        # Select top 2-3 sentences, ensuring diversity
        selected_sentences = []
        used_sources = set()
        
        for sentence_data in top_sentences[:6]:  # Consider top 6
            if len(selected_sentences) >= 3:
                break
            
            # Ensure source diversity
            if sentence_data['source'] not in used_sources or len(selected_sentences) < 2:
                selected_sentences.append(sentence_data)
                used_sources.add(sentence_data['source'])
        
        # Combine selected sentences
        summary_text = ' '.join([s['text'] for s in selected_sentences])
        
        # Clean and format
        summary_text = self._clean_and_format_summary(summary_text, language)
        
        return self._format_summary_for_language(summary_text, language)
    
    def _clean_and_format_summary(self, text: str, language: str) -> str:
        """Clean and format the summary text"""
        # Remove redundant phrases
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = re.sub(r'\.{2,}', '.', text)  # Fix multiple periods
        
        # Limit length
        max_length = 400
        if len(text) > max_length:
            # Try to cut at sentence boundary
            sentences = self._split_into_sentences(text)
            truncated = ""
            for sentence in sentences:
                if len(truncated + sentence) > max_length:
                    break
                truncated += sentence + " "
            text = truncated.strip()
            if not text.endswith('.'):
                text += "..."
        
        return text.strip()
    
    def _extract_keywords(self, text: str, language: str) -> List[str]:
        """Extract keywords from text"""
        words = re.findall(r'\w+', text.lower())
        stop_words = self.stop_words.get(language, set())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords
        """Combine snippets from search results into coherent text"""
        texts = []
        
        for result in search_results:
            snippet = result.get('snippet', '').strip()
            title = result.get('title', '').strip()
            
            if snippet:
                # Clean and format text
                cleaned_snippet = self._clean_text(snippet)
                if cleaned_snippet:
                    if title:
                        texts.append(f"{title}: {cleaned_snippet}")
                    else:
                        texts.append(cleaned_snippet)
        
        combined = ' '.join(texts)
        
        # Limit text length for model processing
        max_chars = 2000  # Reasonable limit for summarization models
        if len(combined) > max_chars:
            combined = combined[:max_chars] + "..."
        
        return combined
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for better summarization"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        
        # Remove common web artifacts
        text = re.sub(r'https?://\S+', '', text)  # Remove URLs
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = re.sub(r'[^\w\s.,!?;:\u0900-\u097F\u0C00-\u0C7F\u1C80-\u1CBF]', ' ', text)  # Keep essential punctuation and Indian scripts
        
        return text.strip()
    
    def _generate_ai_summary(self, text: str, language: str) -> str:
        """Generate AI-powered summary using transformers"""
        try:
            if not text.strip():
                return self._get_default_message(language, "no_content")
            
            # Choose appropriate model based on language
            model_key = 'english' if language == 'english' else 'multilingual'
            summarizer = self.summarizers.get(model_key)
            
            if not summarizer:
                logger.warning(f"No summarizer available for {model_key}")
                return self._generate_rule_based_summary(text, language)
            
            # Generate summary
            logger.info(f"🤖 Generating AI summary for {language} using {model_key} model")
            
            summary_result = summarizer(text)
            summary_text = summary_result[0]['summary_text'] if summary_result else ""
            
            if summary_text:
                # Post-process summary based on language
                formatted_summary = self._format_summary_for_language(summary_text, language)
                return formatted_summary
            else:
                return self._generate_rule_based_summary(text, language)
                
        except Exception as e:
            logger.error(f"❌ AI summarization failed: {e}")
            return self._generate_rule_based_summary(text, language)
    
    def _generate_rule_based_summary(self, text: str, language: str) -> str:
        """Fallback rule-based summarization"""
        if not text.strip():
            return self._get_default_message(language, "no_content")
        
        sentences = self._split_into_sentences(text)
        
        # Take first 2-3 most informative sentences
        important_sentences = []
        for sentence in sentences[:3]:
            if len(sentence.split()) > 5:  # Skip very short sentences
                important_sentences.append(sentence.strip())
        
        if important_sentences:
            summary = ' '.join(important_sentences)
            # Limit length
            if len(summary) > 300:
                summary = summary[:300] + "..."
            return self._format_summary_for_language(summary, language)
        else:
            return self._get_default_message(language, "processing_error")
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences (basic implementation)"""
        # Simple sentence splitting for multiple languages
        sentences = re.split(r'[.!?।॥]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _format_summary_for_language(self, summary: str, language: str) -> str:
        """Format summary with appropriate language-specific introduction"""
        intros = {
            'hindi': "📝 **AI सारांश**: ",
            'telugu': "📝 **AI సారాంశం**: ",
            'marathi': "📝 **AI सारांश**: ",
            'english': "📝 **AI Summary**: "
        }
        
        intro = intros.get(language, "📝 **AI Summary**: ")
        return f"{intro}{summary}"
    
    def _extract_key_insights(self, search_results: List[Dict], language: str) -> List[str]:
        """Extract key insights from search results"""
        insights = []
        
        # Extract common themes/keywords
        all_text = ' '.join([r.get('snippet', '') + ' ' + r.get('title', '') for r in search_results])
        
        # Simple keyword extraction (can be enhanced with more sophisticated NLP)
        words = all_text.lower().split()
        word_freq = {}
        
        # Count word frequency (excluding common stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'से', 'का', 'के', 'को', 'में', 'और', 'या'}
        
        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Format insights based on language
        if language == 'hindi':
            insights.append(f"🔍 **मुख्य विषय**: {', '.join([k[0] for k in top_keywords])}")
        elif language == 'telugu':
            insights.append(f"🔍 **ముఖ్య విషయాలు**: {', '.join([k[0] for k in top_keywords])}")
        elif language == 'marathi':
            insights.append(f"🔍 **मुख्य विषय**: {', '.join([k[0] for k in top_keywords])}")
        else:
            insights.append(f"🔍 **Key Topics**: {', '.join([k[0] for k in top_keywords])}")
        
        return insights
    
    def _calculate_confidence(self, search_results: List[Dict], summary: str) -> float:
        """Calculate confidence score for the summary"""
        # Base confidence on number of sources and content quality
        source_count = len(search_results)
        content_length = sum(len(r.get('snippet', '')) for r in search_results)
        
        # Calculate confidence (0.0 to 1.0)
        confidence = min(1.0, (source_count * 0.2) + (min(content_length, 1000) / 1000 * 0.6) + 0.2)
        
        return round(confidence, 2)
    
    def _generate_no_results_summary(self, query: str, language: str) -> Dict[str, Any]:
        """Generate summary when no search results are available"""
        return {
            'query': query,
            'language': language,
            'ai_summary': self._get_default_message(language, "no_results"),
            'key_insights': [],
            'confidence_score': 0.0,
            'source_count': 0,
            'sources': [],
            'timestamp': datetime.now().isoformat(),
            'summarization_method': 'fallback'
        }
    
    def _get_default_message(self, language: str, message_type: str) -> str:
        """Get default messages in different languages"""
        messages = {
            'hindi': {
                'no_results': "📝 **AI सारांश**: इस विषय पर वर्तमान में जानकारी उपलब्ध नहीं है।",
                'no_content': "📝 **AI सारांश**: पर्याप्त सामग्री उपलब्ध नहीं है।",
                'processing_error': "📝 **AI सारांश**: जानकारी प्रसंस्करण में समस्या हुई।"
            },
            'telugu': {
                'no_results': "📝 **AI సారాంశం**: ఈ విషయంపై ప్రస్తుతం సమాచారం అందుబాటులో లేదు।",
                'no_content': "📝 **AI సారాంశం**: తగిన కంటెంట్ అందుబాటులో లేదు।",
                'processing_error': "📝 **AI సారాంశం**: సమాచార ప్రాసెసింగ్‌లో సమస్య."
            },
            'marathi': {
                'no_results': "📝 **AI सारांश**: या विषयावर सध्या माहिती उपलब्ध नाही।",
                'no_content': "📝 **AI सारांश**: पुरेशी सामग्री उपलब्ध नाही।",
                'processing_error': "📝 **AI सारांश**: माहिती प्रक्रियेत समस्या."
            },
            'english': {
                'no_results': "📝 **AI Summary**: Information on this topic is currently not available.",
                'no_content': "📝 **AI Summary**: Insufficient content available.",
                'processing_error': "📝 **AI Summary**: Error in information processing."
            }
        }
        
        return messages.get(language, messages['english']).get(message_type, "No information available.")

# Global instance
ai_summarizer = AISearchSummarizer()
