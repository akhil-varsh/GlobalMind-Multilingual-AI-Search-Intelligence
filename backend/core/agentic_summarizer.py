"""
Advanced Agentic AI Summarizer Module
Implements multi-agent patterns inspired by Google's ADK for real-time summarization
Uses Sequential, Parallel, and Hierarchical Task Decomposition patterns
"""

import logging
from typing import List, Dict, Optional, Any, AsyncGenerator
import asyncio
from datetime import datetime
from abc import ABC, abstractmethod
import re
from collections import Counter
import json
import time

logger = logging.getLogger(__name__)

# Base Agent Classes (Inspired by ADK patterns)

class BaseAgent(ABC):
    """Base agent class inspired by ADK BaseAgent"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.parent_agent: Optional['BaseAgent'] = None
        self.sub_agents: List['BaseAgent'] = []
        
    @abstractmethod
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic"""
        pass
        
    def add_sub_agent(self, agent: 'BaseAgent'):
        """Add a sub-agent"""
        agent.parent_agent = self
        self.sub_agents.append(agent)
        
    def find_agent(self, name: str) -> Optional['BaseAgent']:
        """Find agent by name in hierarchy"""
        if self.name == name:
            return self
        for agent in self.sub_agents:
            found = agent.find_agent(name)
            if found:
                return found
        return None

class SequentialAgent(BaseAgent):
    """Sequential workflow agent - executes sub-agents in order"""
    
    def __init__(self, name: str, description: str = ""):
        super().__init__(name, description)
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sub-agents sequentially, passing context between them"""
        logger.info(f"🔄 {self.name}: Starting sequential execution")
        
        for agent in self.sub_agents:
            logger.info(f"⚡ {self.name}: Executing {agent.name}")
            context = await agent.run_async(context)
            
        logger.info(f"✅ {self.name}: Sequential execution completed")
        return context

class ParallelAgent(BaseAgent):
    """Parallel workflow agent - executes sub-agents concurrently"""
    
    def __init__(self, name: str, description: str = ""):
        super().__init__(name, description)
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sub-agents in parallel"""
        logger.info(f"🔄 {self.name}: Starting parallel execution")
        
        if not self.sub_agents:
            return context
            
        # Create tasks for parallel execution
        tasks = []
        for agent in self.sub_agents:
            # Each agent gets a copy of context to avoid conflicts
            agent_context = context.copy()
            task = asyncio.create_task(agent.run_async(agent_context))
            tasks.append((agent.name, task))
        
        # Wait for all tasks to complete
        results = {}
        for agent_name, task in tasks:
            try:
                result = await task
                results[agent_name] = result
                logger.info(f"⚡ {self.name}: {agent_name} completed")
            except Exception as e:
                logger.error(f"❌ {self.name}: {agent_name} failed: {e}")
                results[agent_name] = {'error': str(e)}
        
        # Merge results back into context
        context['parallel_results'] = results
        logger.info(f"✅ {self.name}: Parallel execution completed")
        return context

# Specialized Agent Classes for Summarization

class DataFetcherAgent(BaseAgent):
    """Agent responsible for fetching and preprocessing search data"""
    
    def __init__(self):
        super().__init__(
            name="DataFetcher",
            description="Fetches and preprocesses search results for analysis"
        )
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch and preprocess search results"""
        logger.info(f"🔍 {self.name}: Fetching search data")
        
        search_results = context.get('search_results', [])
        query = context.get('query', '')
        language = context.get('language', 'english')
        
        # Process and clean search results
        processed_results = []
        for idx, result in enumerate(search_results):
            processed_result = {
                'title': self._clean_text(result.get('title', '')),
                'snippet': self._clean_text(result.get('snippet', '')),
                'source': result.get('source', 'unknown'),
                'position': idx,
                'relevance_score': self._calculate_initial_relevance(result, query)
            }
            processed_results.append(processed_result)
        
        context['processed_results'] = processed_results
        context['fetch_timestamp'] = datetime.now().isoformat()
        
        logger.info(f"✅ {self.name}: Processed {len(processed_results)} results")
        return context
        
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'https?://\S+', '', text)
        return text.strip()
        
    def _calculate_initial_relevance(self, result: Dict, query: str) -> float:
        """Calculate initial relevance score"""
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        query_words = set(query.lower().split())
        
        # Simple keyword matching
        title_matches = sum(1 for word in query_words if word in title)
        snippet_matches = sum(1 for word in query_words if word in snippet)
        
        if len(query_words) == 0:
            return 0.5
            
        relevance = (title_matches * 2 + snippet_matches) / (len(query_words) * 3)
        return min(relevance, 1.0)

class ContentAnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing content and extracting insights"""
    
    def __init__(self):
        super().__init__(
            name="ContentAnalyzer",
            description="Analyzes content for semantic meaning and extracts key insights"
        )
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content and extract insights"""
        logger.info(f"🧠 {self.name}: Analyzing content")
        
        processed_results = context.get('processed_results', [])
        query = context.get('query', '')
        language = context.get('language', 'english')
        
        # Extract sentences and analyze them
        sentences = []
        themes = Counter()
        entities = []
        
        for result in processed_results:
            content = f"{result['title']}. {result['snippet']}"
            result_sentences = self._extract_sentences(content)
            
            for sentence in result_sentences:
                if len(sentence.split()) > 4:  # Filter short sentences
                    score = self._score_sentence(sentence, query, result['position'], language)
                    sentences.append({
                        'text': sentence,
                        'score': score,
                        'source': result['source'],
                        'position': result['position']
                    })
                    
                    # Extract themes
                    themes.update(self._extract_themes(sentence, language))
                    
                    # Extract entities (simplified)
                    entities.extend(self._extract_entities(sentence))
        
        # Sort sentences by score
        sentences.sort(key=lambda x: x['score'], reverse=True)
        
        context['analyzed_sentences'] = sentences
        context['themes'] = dict(themes.most_common(10))
        context['entities'] = list(set(entities))
        context['analysis_timestamp'] = datetime.now().isoformat()
        
        logger.info(f"✅ {self.name}: Analyzed {len(sentences)} sentences, {len(themes)} themes")
        return context
        
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text"""
        sentences = re.split(r'[.!?।॥]', text)
        return [s.strip() for s in sentences if s.strip()]
        
    def _score_sentence(self, sentence: str, query: str, position: int, language: str) -> float:
        """Score sentence relevance"""
        score = 0.0
        
        # Position weight (earlier results more important)
        position_score = max(0, (5 - position) / 5) * 0.3
        score += position_score
        
        # Length weight (prefer moderate length)
        words = sentence.split()
        length_score = min(len(words) / 15, 1.0) * 0.2
        score += length_score
        
        # Keyword matching
        query_words = set(query.lower().split())
        sentence_words = set(sentence.lower().split())
        
        if query_words:
            overlap = len(query_words.intersection(sentence_words)) / len(query_words)
            score += overlap * 0.5
            
        return min(score, 1.0)
        
    def _extract_themes(self, sentence: str, language: str) -> List[str]:
        """Extract themes from sentence"""
        # Simple theme extraction based on nouns and important words
        words = re.findall(r'\w+', sentence.lower())
        
        # Filter stop words
        stop_words = {
            'english': {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'},
            'hindi': {'का', 'के', 'को', 'में', 'और', 'या', 'से', 'पर', 'है', 'हैं'},
            'telugu': {'మరియు', 'లేదా', 'లో', 'పై', 'కోసం', 'తో', 'ఇది', 'అది'},
            'marathi': {'आणि', 'किंवा', 'मध्ये', 'वर', 'साठी', 'सोबत', 'हे', 'ते'}
        }
        
        relevant_words = [w for w in words if len(w) > 3 and w not in stop_words.get(language, set())]
        return relevant_words[:3]  # Top 3 themes per sentence
        
    def _extract_entities(self, sentence: str) -> List[str]:
        """Extract named entities (simplified)"""
        # Simple capitalized word extraction as entities
        entities = re.findall(r'\b[A-Z][a-z]+\b', sentence)
        return entities

class SummaryGeneratorAgent(BaseAgent):
    """Agent responsible for generating the main summary"""
    
    def __init__(self):
        super().__init__(
            name="SummaryGenerator",
            description="Generates coherent summaries from analyzed content"
        )
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary from analyzed content"""
        logger.info(f"📝 {self.name}: Generating summary")
        
        analyzed_sentences = context.get('analyzed_sentences', [])
        themes = context.get('themes', {})
        language = context.get('language', 'english')
        query = context.get('query', '')
        
        # Select best sentences for summary
        selected_sentences = self._select_summary_sentences(analyzed_sentences, themes)
        
        # Generate coherent summary
        summary_text = self._compose_summary(selected_sentences, language)
        
        # Format for language
        formatted_summary = self._format_summary_for_language(summary_text, language)
        
        context['generated_summary'] = formatted_summary
        context['summary_sentences'] = selected_sentences
        context['generation_timestamp'] = datetime.now().isoformat()
        
        logger.info(f"✅ {self.name}: Generated summary ({len(summary_text)} chars)")
        return context
        
    def _select_summary_sentences(self, sentences: List[Dict], themes: Dict) -> List[Dict]:
        """Select best sentences for summary ensuring diversity"""
        if not sentences:
            return []
            
        selected = []
        used_sources = set()
        theme_coverage = set()
        
        # Sort by score and select diverse sentences
        for sentence_data in sentences[:10]:  # Consider top 10
            if len(selected) >= 3:
                break
                
            source = sentence_data['source']
            sentence_themes = set(self._extract_themes_from_text(sentence_data['text']))
            
            # Prefer sentences from different sources and covering different themes
            source_diversity = source not in used_sources or len(selected) < 2
            theme_diversity = not theme_coverage.intersection(sentence_themes) or len(selected) < 2
            
            if source_diversity and (theme_diversity or sentence_data['score'] > 0.7):
                selected.append(sentence_data)
                used_sources.add(source)
                theme_coverage.update(sentence_themes)
                
        return selected
        
    def _extract_themes_from_text(self, text: str) -> List[str]:
        """Extract themes from text"""
        words = re.findall(r'\w+', text.lower())
        return [w for w in words if len(w) > 4][:3]
        
    def _compose_summary(self, sentences: List[Dict], language: str) -> str:
        """Compose coherent summary from sentences"""
        if not sentences:
            return self._get_no_content_message(language)
            
        # Combine sentences
        summary_parts = [s['text'].strip() for s in sentences]
        summary = ' '.join(summary_parts)
        
        # Clean and limit length
        summary = re.sub(r'\s+', ' ', summary)
        
        # Limit to reasonable length
        max_length = 400
        if len(summary) > max_length:
            # Cut at sentence boundary
            cut_summary = ""
            for sentence in summary.split('.'):
                if len(cut_summary + sentence) > max_length:
                    break
                cut_summary += sentence + ". "
            summary = cut_summary.strip()
            if not summary.endswith('.'):
                summary += "..."
                
        return summary
        
    def _format_summary_for_language(self, summary: str, language: str) -> str:
        """Format summary with appropriate language prefix"""
        prefixes = {
            'hindi': "📝 **AI सारांश**: ",
            'telugu': "📝 **AI సారాంశం**: ",
            'marathi': "📝 **AI सारांश**: ",
            'english': "📝 **AI Summary**: "
        }
        
        prefix = prefixes.get(language, "📝 **AI Summary**: ")
        return f"{prefix}{summary}"
        
    def _get_no_content_message(self, language: str) -> str:
        """Get no content message in appropriate language"""
        messages = {
            'hindi': "पर्याप्त सामग्री उपलब्ध नहीं है।",
            'telugu': "తగిన కంటెంట్ అందుబాటులో లేదు।",
            'marathi': "पुरेशी सामग्री उपलब्ध नाही।",
            'english': "Insufficient content available."
        }
        return messages.get(language, messages['english'])

class CriticAgent(BaseAgent):
    """Agent responsible for critiquing and improving the summary"""
    
    def __init__(self):
        super().__init__(
            name="Critic",
            description="Reviews and improves generated summaries"
        )
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Critique and improve the summary"""
        logger.info(f"🔍 {self.name}: Reviewing summary")
        
        summary = context.get('generated_summary', '')
        query = context.get('query', '')
        language = context.get('language', 'english')
        themes = context.get('themes', {})
        
        # Analyze summary quality
        quality_score = self._analyze_summary_quality(summary, query, themes)
        
        # Generate suggestions for improvement
        suggestions = self._generate_improvement_suggestions(summary, query, language)
        
        # Apply improvements if needed
        improved_summary = self._apply_improvements(summary, suggestions, language)
        
        context['final_summary'] = improved_summary
        context['quality_score'] = quality_score
        context['critic_suggestions'] = suggestions
        context['critique_timestamp'] = datetime.now().isoformat()
        
        logger.info(f"✅ {self.name}: Quality score: {quality_score:.2f}")
        return context
        
    def _analyze_summary_quality(self, summary: str, query: str, themes: Dict) -> float:
        """Analyze the quality of the summary"""
        if not summary:
            return 0.0
            
        score = 0.0
        
        # Length appropriateness (0.3 weight)
        length = len(summary)
        if 100 <= length <= 500:
            score += 0.3
        elif length > 50:
            score += 0.15
            
        # Query relevance (0.4 weight)
        query_words = set(query.lower().split())
        summary_words = set(summary.lower().split())
        if query_words:
            relevance = len(query_words.intersection(summary_words)) / len(query_words)
            score += relevance * 0.4
            
        # Theme coverage (0.3 weight)
        if themes:
            theme_words = set(themes.keys())
            theme_coverage = len(theme_words.intersection(summary_words)) / len(theme_words)
            score += theme_coverage * 0.3
            
        return min(score, 1.0)
        
    def _generate_improvement_suggestions(self, summary: str, query: str, language: str) -> List[str]:
        """Generate suggestions for improving the summary"""
        suggestions = []
        
        # Check length
        if len(summary) < 50:
            suggestions.append("summary_too_short")
        elif len(summary) > 600:
            suggestions.append("summary_too_long")
            
        # Check query relevance
        query_words = set(query.lower().split())
        summary_words = set(summary.lower().split())
        
        if query_words and len(query_words.intersection(summary_words)) == 0:
            suggestions.append("low_query_relevance")
            
        return suggestions
        
    def _apply_improvements(self, summary: str, suggestions: List[str], language: str) -> str:
        """Apply improvements based on suggestions"""
        improved = summary
        
        # Apply improvements based on suggestions
        if "summary_too_long" in suggestions:
            # Truncate to reasonable length
            sentences = improved.split('.')
            if len(sentences) > 3:
                improved = '. '.join(sentences[:3]) + '.'
                
        elif "summary_too_short" in suggestions:
            # Add clarification that content was limited
            clarifications = {
                'hindi': " (सीमित जानकारी के आधार पर)",
                'telugu': " (పరిమిత సమాచారం ఆధారంగా)",
                'marathi': " (मर्यादित माहितीच्या आधारावर)",
                'english': " (based on limited information)"
            }
            clarification = clarifications.get(language, clarifications['english'])
            improved += clarification
            
        return improved

class InsightExtractorAgent(BaseAgent):
    """Agent responsible for extracting key insights"""
    
    def __init__(self):
        super().__init__(
            name="InsightExtractor",
            description="Extracts key insights and metadata from content"
        )
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key insights from the content"""
        logger.info(f"💡 {self.name}: Extracting insights")
        
        themes = context.get('themes', {})
        entities = context.get('entities', [])
        processed_results = context.get('processed_results', [])
        language = context.get('language', 'english')
        
        # Generate key insights
        insights = []
        
        # Top themes insight
        if themes:
            top_themes = list(themes.keys())[:5]
            insight = self._format_themes_insight(top_themes, language)
            insights.append(insight)
            
        # Source diversity insight
        sources = [r['source'] for r in processed_results]
        unique_sources = len(set(sources))
        if unique_sources > 1:
            source_insight = self._format_source_insight(unique_sources, language)
            insights.append(source_insight)
            
        # Entity insights
        if entities:
            entity_insight = self._format_entity_insight(entities[:3], language)
            insights.append(entity_insight)
            
        context['key_insights'] = insights
        context['insight_timestamp'] = datetime.now().isoformat()
        
        logger.info(f"✅ {self.name}: Generated {len(insights)} insights")
        return context
        
    def _format_themes_insight(self, themes: List[str], language: str) -> str:
        """Format themes insight"""
        theme_text = ', '.join(themes)
        
        formats = {
            'hindi': f"🔍 **मुख्य विषय**: {theme_text}",
            'telugu': f"🔍 **ముఖ్య విషయాలు**: {theme_text}",
            'marathi': f"🔍 **मुख्य विषय**: {theme_text}",
            'english': f"🔍 **Key Topics**: {theme_text}"
        }
        
        return formats.get(language, formats['english'])
        
    def _format_source_insight(self, count: int, language: str) -> str:
        """Format source diversity insight"""
        formats = {
            'hindi': f"📊 **स्रोत विविधता**: {count} विभिन्न स्रोतों से जानकारी",
            'telugu': f"📊 **మూల వైవిధ్యం**: {count} వేర్వేరు మూలాల నుండి సమాచారం",
            'marathi': f"📊 **स्रोत विविधता**: {count} वेगवेगळ्या स्रोतांकडून माहिती",
            'english': f"📊 **Source Diversity**: Information from {count} different sources"
        }
        
        return formats.get(language, formats['english'])
        
    def _format_entity_insight(self, entities: List[str], language: str) -> str:
        """Format entity insight"""
        entity_text = ', '.join(entities)
        
        formats = {
            'hindi': f"🏷️ **मुख्य संस्थाएं**: {entity_text}",
            'telugu': f"🏷️ **ముఖ్య సంస్థలు**: {entity_text}",
            'marathi': f"🏷️ **मुख्य संस्था**: {entity_text}",
            'english': f"🏷️ **Key Entities**: {entity_text}"
        }
        
        return formats.get(language, formats['english'])

# Main Agentic Summarizer Coordinator

class AgenticSummarizer(BaseAgent):
    """Main coordinator for agentic summarization using multi-agent patterns"""
    
    def __init__(self):
        super().__init__(
            name="AgenticSummarizer",
            description="Coordinates multi-agent summarization workflow"
        )
        
        # Initialize specialized agents
        self.data_fetcher = DataFetcherAgent()
        self.content_analyzer = ContentAnalyzerAgent()
        self.summary_generator = SummaryGeneratorAgent()
        self.critic = CriticAgent()
        self.insight_extractor = InsightExtractorAgent()
        
        # Create workflow agents
        self._setup_workflow()
        
    def _setup_workflow(self):
        """Setup the multi-agent workflow"""
        
        # Parallel analysis phase
        self.analysis_pipeline = ParallelAgent(
            name="AnalysisPhase",
            description="Parallel content analysis and insight extraction"
        )
        self.analysis_pipeline.add_sub_agent(self.content_analyzer)
        self.analysis_pipeline.add_sub_agent(self.insight_extractor)
        
        # Sequential generation and critique phase
        self.generation_pipeline = SequentialAgent(
            name="GenerationPhase", 
            description="Sequential summary generation and critique"
        )
        self.generation_pipeline.add_sub_agent(self.summary_generator)
        self.generation_pipeline.add_sub_agent(self.critic)
        
        # Main sequential workflow
        self.main_workflow = SequentialAgent(
            name="MainWorkflow",
            description="Main summarization workflow"
        )
        self.main_workflow.add_sub_agent(self.data_fetcher)
        self.main_workflow.add_sub_agent(self.analysis_pipeline)
        self.main_workflow.add_sub_agent(self.generation_pipeline)
        
    async def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the complete agentic summarization workflow"""
        logger.info(f"🤖 {self.name}: Starting agentic summarization")
        start_time = time.time()
        
        try:
            # Execute the main workflow
            result_context = await self.main_workflow.run_async(context)
            
            # Compile final result
            final_result = self._compile_final_result(result_context)
            
            execution_time = time.time() - start_time
            logger.info(f"✅ {self.name}: Completed in {execution_time:.2f}s")
            
            return final_result
            
        except Exception as e:
            logger.error(f"❌ {self.name}: Workflow failed: {e}")
            return self._generate_error_result(context, str(e))
            
    def _compile_final_result(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Compile the final summarization result"""
        
        # Extract results from parallel analysis
        parallel_results = context.get('parallel_results', {})
        content_analysis = parallel_results.get('ContentAnalyzer', {})
        insight_extraction = parallel_results.get('InsightExtractor', {})
        
        return {
            'query': context.get('query', ''),
            'language': context.get('language', 'english'),
            'ai_summary': context.get('final_summary', ''),
            'key_insights': insight_extraction.get('key_insights', []),
            'confidence_score': context.get('quality_score', 0.0),
            'source_count': len(context.get('processed_results', [])),
            'sources': [r.get('source', 'Unknown') for r in context.get('processed_results', [])[:3]],
            'timestamp': datetime.now().isoformat(),
            'summarization_method': 'multi_agent_agentic',
            'execution_details': {
                'themes_found': len(content_analysis.get('themes', {})),
                'entities_found': len(content_analysis.get('entities', [])),
                'sentences_analyzed': len(content_analysis.get('analyzed_sentences', [])),
                'critic_suggestions': context.get('critic_suggestions', []),
                'workflow_stages': ['fetch', 'analyze', 'generate', 'critique']
            }
        }
        
    def _generate_error_result(self, context: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Generate error result"""
        language = context.get('language', 'english')
        
        error_messages = {
            'hindi': "📝 **AI सारांश**: तकनीकी समस्या के कारण सारांश नहीं बना सका।",
            'telugu': "📝 **AI సారాంశం**: సాంకేతిక సమస్య కారణంగా సారాంశం రూపొందించలేకపోయాం।",
            'marathi': "📝 **AI सारांश**: तांत्रिक समस्येमुळे सारांश तयार करू शकलो नाही।",
            'english': "📝 **AI Summary**: Unable to generate summary due to technical issues."
        }
        
        return {
            'query': context.get('query', ''),
            'language': language,
            'ai_summary': error_messages.get(language, error_messages['english']),
            'key_insights': [],
            'confidence_score': 0.0,
            'source_count': 0,
            'sources': [],
            'timestamp': datetime.now().isoformat(),
            'summarization_method': 'error_fallback',
            'error': error
        }
        
    async def summarize_search_results(
        self, 
        search_results: List[Dict], 
        query: str, 
        language: str,
        max_results: int = 3
    ) -> Dict[str, Any]:
        """Public interface for summarizing search results"""
        
        if not search_results:
            return self._generate_no_results_summary(query, language)
            
        # Prepare context for agents
        context = {
            'search_results': search_results[:max_results],
            'query': query,
            'language': language,
            'max_results': max_results,
            'start_timestamp': datetime.now().isoformat()
        }
        
        # Run the agentic workflow
        return await self.run_async(context)
        
    def _generate_no_results_summary(self, query: str, language: str) -> Dict[str, Any]:
        """Generate summary when no search results are available"""
        no_results_messages = {
            'hindi': "📝 **AI सारांश**: इस विषय पर वर्तमान में जानकारी उपलब्ध नहीं है।",
            'telugu': "📝 **AI సారాంశం**: ఈ విషయంపై ప్రస్తుతం సమాచారం అందుబాటులో లేదు।",
            'marathi': "📝 **AI सारांश**: या विषयावर सध्या माहिती उपलब्ध नाही।",
            'english': "📝 **AI Summary**: Information on this topic is currently not available."
        }
        
        return {
            'query': query,
            'language': language,
            'ai_summary': no_results_messages.get(language, no_results_messages['english']),
            'key_insights': [],
            'confidence_score': 0.0,
            'source_count': 0,
            'sources': [],
            'timestamp': datetime.now().isoformat(),
            'summarization_method': 'no_results_fallback'
        }

# Global instance
agentic_summarizer = AgenticSummarizer()

# Synchronous wrapper for backward compatibility
def summarize_search_results_sync(search_results: List[Dict], query: str, language: str, max_results: int = 3) -> Dict[str, Any]:
    """Synchronous wrapper for the agentic summarizer"""
    try:
        # Create a new event loop if one doesn't exist
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async function
        return loop.run_until_complete(
            agentic_summarizer.summarize_search_results(search_results, query, language, max_results)
        )
    except Exception as e:
        logger.error(f"❌ Sync wrapper error: {e}")
        # Fallback to simple summary
        return agentic_summarizer._generate_error_result(
            {'query': query, 'language': language}, 
            str(e)
        )
