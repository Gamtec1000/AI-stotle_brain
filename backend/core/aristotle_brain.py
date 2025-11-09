# backend/core/aristotle_brain.py
"""
AI-stotle: The wise AI science tutor
Supports both Claude (premium quality) and DeepSeek (ultra-low-cost)
With FAISS knowledge base for semantic search
"""

from openai import OpenAI
import os
import sys
from typing import Dict, List, Optional
from dotenv import load_dotenv
import json

# Add knowledge module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from knowledge.faiss_knowledge import AristotleKnowledge

load_dotenv()

class AristotleBrain:
    """
    AI-stotle core intelligence
    Philosophy meets modern AI - wisdom at low cost!
    """
    
    def __init__(self, provider: str = None, use_knowledge: bool = True):
        """
        Initialize AI-stotle with chosen AI provider
        
        Args:
            provider: 'deepseek' or 'claude' (defaults to env ARISTOTLE_AI_PROVIDER)
            use_knowledge: Whether to use FAISS knowledge base
        """
        self.provider = provider or os.getenv('ARISTOTLE_AI_PROVIDER', 'deepseek')
        
        # Initialize AI provider
        if self.provider == 'claude':
            try:
                from anthropic import Anthropic
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if not api_key:
                    raise ValueError('ANTHROPIC_API_KEY not found in environment')
                self.client = Anthropic(api_key=api_key)
                self.model = 'claude-sonnet-4-20250514'
                print(f'🤖 Using Claude Sonnet 4')
            except ImportError:
                print('⚠️ Anthropic package not installed. Install with: pip install anthropic')
                raise
        else:  # deepseek
            api_key = os.getenv('DEEPSEEK_API_KEY')
            if not api_key:
                raise ValueError('DEEPSEEK_API_KEY not found in environment')
            self.client = OpenAI(
                api_key=api_key,
                base_url=os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
            )
            self.model = 'deepseek-chat'
            print(f'🤖 Using DeepSeek Chat (Ultra-low-cost)')
        
        # Initialize knowledge base
        self.knowledge_base = None
        if use_knowledge:
            try:
                self.knowledge_base = AristotleKnowledge()
                stats = self.knowledge_base.get_stats()
                print(f'✅ Knowledge base loaded: {stats[\"total_passages\"]} passages')
            except Exception as e:
                print(f'⚠️ Could not load knowledge base: {e}')
        
        # AI-stotle's philosophical personality
        self.personality = \"\"\"
        I am AI-stotle (Aristotle + AI), a wise and enthusiastic science tutor 
        for Carls Newton shows in Dubai!
        
        PHILOSOPHY:
        - \"Wonder is the beginning of wisdom\" - I encourage curiosity
        - \"The more you know, the more you know you don't know\" - Humble learning
        - \"We are what we repeatedly do\" - Practice and hands-on experiments
        
        PERSONALITY:
        - Wise but never condescending
        - Patient and encouraging
        - Excited about discovery
        - Makes complex ideas simple
        - Connects science to philosophy and life
        - Uses analogies and metaphors
        
        COMMUNICATION STYLE:
        - Clear, age-appropriate language
        - Short answers (2-3 sentences) unless asked for more
        - Real-world examples and connections
        - Encourages hands-on experimentation
        - Occasional philosophical wisdom
        
        SIGNATURE PHRASES:
        - \"Ah, a curious mind asks...\"
        - \"Let me enlighten you...\"
        - \"As the great philosophers knew...\"
        - \"Science and wisdom combined show us...\"
        \"\"\"
    
    def ask_aristotle(self,
                     question: str,
                     student_age: int = 10,
                     context: Optional[Dict] = None,
                     use_rag: bool = True) -> Dict:
        \"\"\"
        Ask AI-stotle a question
        
        Args:
            question: Student's question
            student_age: Age for appropriate language
            context: Current show context
            use_rag: Whether to use knowledge base (RAG)
            
        Returns:
            Dictionary with answer and metadata
        \"\"\"
        
        # Search knowledge base if available
        knowledge_passages = []
        if use_rag and self.knowledge_base:
            results = self.knowledge_base.search(question, top_k=3)
            knowledge_passages = [r['text'] for r in results]
            print(f'🔍 Found {len(knowledge_passages)} relevant passages')
        
        # Build prompt
        prompt = self._build_prompt(
            question=question,
            age=student_age,
            context=context,
            knowledge=knowledge_passages
        )
        
        # Get response from AI
        try:
            if self.provider == 'claude':
                return self._ask_claude(prompt)
            else:
                return self._ask_deepseek(prompt)
                
        except Exception as e:
            return {
                'answer': f'Apologies, young scholar. I encountered an error: {str(e)}',
                'success': False,
                'error': str(e)
            }
    
    def _ask_claude(self, prompt: str) -> Dict:
        \"\"\"Query Claude\"\"\"
        from anthropic import Anthropic
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            temperature=float(os.getenv('TEMPERATURE', 0.7)),
            system=self.personality,
            messages=[{
                'role': 'user',
                'content': prompt
            }]
        )
        
        answer = response.content[0].text
        
        return {
            'answer': answer,
            'success': True,
            'model': self.model,
            'provider': 'claude',
            'cost': self._estimate_cost_claude(response.usage),
            'tokens_used': response.usage.input_tokens + response.usage.output_tokens
        }
    
    def _ask_deepseek(self, prompt: str) -> Dict:
        \"\"\"Query DeepSeek\"\"\"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self.personality},
                {'role': 'user', 'content': prompt}
            ],
            temperature=float(os.getenv('TEMPERATURE', 0.7)),
            max_tokens=500,
            stream=False
        )
        
        answer = response.choices[0].message.content
        
        return {
            'answer': answer,
            'success': True,
            'model': self.model,
            'provider': 'deepseek',
            'cost': self._estimate_cost_deepseek(response.usage),
            'tokens_used': response.usage.total_tokens
        }
    
    def _build_prompt(self,
                     question: str,
                     age: int,
                     context: Optional[Dict],
                     knowledge: Optional[List[str]]) -> str:
        \"\"\"Build prompt for AI\"\"\"
        
        prompt_parts = [f'STUDENT AGE: {age} years old\n']
        
        # Add knowledge base if available
        if knowledge and len(knowledge) > 0:
            prompt_parts.append('RELEVANT KNOWLEDGE FROM CARLS NEWTON:\n')
            for i, k in enumerate(knowledge, 1):
                prompt_parts.append(f'\n{i}. {k}\n')
            prompt_parts.append('\n')
        
        # Add context
        if context:
            prompt_parts.append(f'CURRENT CONTEXT:\n{json.dumps(context, indent=2)}\n\n')
        
        # Add question
        prompt_parts.append(f'STUDENT QUESTION:\n{question}\n\n')
        
        # Add instructions
        prompt_parts.append(f\"\"\"
INSTRUCTIONS:
1. Answer clearly for a {age}-year-old student
2. Use the knowledge provided above when relevant
3. Keep answer engaging and concise (2-3 sentences)
4. Add a touch of philosophical wisdom when appropriate
5. Encourage hands-on learning

AI-STOTLE'S WISE RESPONSE:
\"\"\")
        
        return ''.join(prompt_parts)
    
    def _estimate_cost_claude(self, usage) -> float:
        \"\"\"Claude Sonnet 4: `$`3 input / `$`15 output per 1M tokens\"\"\"
        input_cost = (usage.input_tokens / 1_000_000) * 3.0
        output_cost = (usage.output_tokens / 1_000_000) * 15.0
        return round(input_cost + output_cost, 6)
    
    def _estimate_cost_deepseek(self, usage) -> float:
        \"\"\"DeepSeek: `$`0.14 input / `$`0.28 output per 1M tokens\"\"\"
        input_cost = (usage.prompt_tokens / 1_000_000) * 0.14
        output_cost = (usage.completion_tokens / 1_000_000) * 0.28
        return round(input_cost + output_cost, 6)


# Quick test
if __name__ == '__main__':
    print('\n' + '='*60)
    print('🏛️ AI-STOTLE: THE WISE AI TUTOR WITH KNOWLEDGE BASE')
    print('='*60)
    
    # Test questions
    test_questions = [
        ('Why does elephant toothpaste create so much foam?', 10),
        ('What is a catalyst?', 8),
        ('How does dry ice make fog?', 12),
        ('Can I be a scientist?', 7)
    ]
    
    # Test with DeepSeek
    print(f'\n🤖 Testing with DEEPSEEK')
    print('='*60)
    
    try:
        aristotle = AristotleBrain(provider='deepseek', use_knowledge=True)
        
        total_cost = 0
        
        for question, age in test_questions:
            print(f'\n👤 Student ({age}yo): {question}')
            
            response = aristotle.ask_aristotle(
                question=question,
                student_age=age,
                use_rag=True
            )
            
            if response['success']:
                print(f'🏛️ AI-stotle: {response[\"answer\"]}')
                print(f'💰 Cost: `$`{response[\"cost\"]:.6f}')
                print(f'🔢 Tokens: {response[\"tokens_used\"]}')
                total_cost += response['cost']
            else:
                print(f'❌ Error: {response[\"error\"]}')
        
        print(f'\n💰 Total cost for 4 questions: `$`{total_cost:.6f}')
        print(f'📊 Compared to Claude: ~`$`{total_cost * 40:.4f} (40x more expensive!)')
        print(f'💵 Savings: ~`$`{(total_cost * 40) - total_cost:.4f} (97.5%!)')
        
    except Exception as e:
        print(f'⚠️ DeepSeek not configured: {e}')
        print('Please add DEEPSEEK_API_KEY to .env file')
    
    print('\n' + '='*60)