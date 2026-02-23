"""
Advanced Mentor Chatbot - Context-Aware Conversational AI
Provides sophisticated guidance with understanding of user context.
"""

from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Optional
import json
import random


class AdvancedChatbot:
    """Production-grade mentor chatbot with context awareness."""

    def __init__(self):
        """Initialize chatbot with advanced intent mapping."""
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except:
            self.sentiment_analyzer = None

        # Intent definitions with sophisticated patterns
        self.intents = {
            'path_deep_dive': {
                'patterns': [
                    'tell me more about', 'explain ', 'how do i become', 'what does', 'describe ',
                    'elaborate on', 'dive deeper', 'understand better', 'break it down'
                ],
                'base_responses': [
                    'Based on your profile, {path} offers unique opportunities. Let me break down what makes it compelling for you.',
                    '{path} is fascinating because it combines your strengths in {strengths}. Here\'s what the journey looks like:',
                    'This path aligns well with your {motivation} motivation. Here\'s the detailed breakdown:'
                ],
                'follow_ups': [
                    'Are you most interested in the technical skills or the career trajectory?',
                    'What aspects concern you most - the learning curve or the job market?',
                    'Would you like to know about specific roles or companies in this field?'
                ]
            },

            'skill_development': {
                'patterns': [
                    'how do i improve', 'strengthen my', 'learn ', 'develop ', 'master ',
                    'get better at', 'skill gap', 'what skills', 'practice ',
                    'training for', 'course', 'certification'
                ],
                'base_responses': [
                    'Building {skill} takes structured practice. Here\'s a realistic roadmap:',
                    'Your current {skill} level is {level}/5. Here\'s how to accelerate growth:',
                    'To develop {skill}, the most effective approach combines theory and hands-on experience.'
                ],
                'suggestions': [
                    'Start with fundamentals through courses or books',
                    'Build projects immediately to apply learning',
                    'Join communities and learn from peers',
                    'Seek mentorship from experienced professionals'
                ]
            },

            'uncertainty_doubt': {
                'patterns': [
                    'not sure', 'uncertain', 'confused', 'overwhelmed', 'doubt', 'can i really',
                    'am i capable', 'too hard', 'worried about', 'concerned about', 'imposter'
                ],
                'base_responses': [
                    'Your uncertainty is completely normal and actually a sign of thoughtfulness. Let\'s work through this.',
                    'Doubt is natural when exploring new directions. Every expert started exactly where you are.',
                    'What you\'re feeling is common. Let\'s focus on concrete next steps to build confidence.',
                    'I appreciate your honesty. Let\'s break this down into manageable pieces.'
                ],
                'guidance': [
                    'Focus on one skill at a time',
                    'Set small, achievable milestones',
                    'Celebrate progress, not perfection',
                    'Remember: struggling means you\'re growing'
                ]
            },

            'comparison_exploration': {
                'patterns': [
                    'compare', 'vs', 'which is better', 'difference between', 'pros and cons',
                    'which should i choose', 'better suited', 'trade-off', 'similar to'
                ],
                'base_responses': [
                    'Great question! Let me provide a nuanced comparison:',
                    'These are both excellent paths, but they differ in important ways:',
                    'The choice depends on what matters most to you. Here\'s the breakdown:'
                ],
                'dimensions': ['learning curve', 'market demand', 'salary trajectory', 'growth potential', 'work-life balance']
            },

            'project_brainstorming': {
                'patterns': [
                    'project idea', 'what should i build', 'portfolio', 'practice project',
                    'capstone', 'side hustle', 'startup idea', 'create '
                ],
                'base_responses': [
                    'Based on your profile, here are project ideas that would strengthen your position:',
                    'Let\'s brainstorm a project that combines your interests and builds your skills:',
                    'The best projects solve real problems. Here are ideas aligned with {path}:'
                ]
            },

            'motivation_confidence_boost': {
                'patterns': [
                    'nervous', 'anxious', 'scared', 'afraid', 'excited', 'enthusiastic', 'pumped', 'motivated'
                ],
                'base_responses': [
                    'Your energy is exactly what will drive your success in this field!',
                    'That nervousness shows you care about doing this right.',
                    'Channel that excitement into your first learning milestone.',
                    'Your passion is your greatest asset. Let\'s channel it productively.'
                ]
            },

            'timeline_expectations': {
                'patterns': [
                    'how long', 'how many months', 'timeline', 'when can i', 'how much time',
                    'how quickly', 'fast track', 'accelerate'
                ],
                'base_responses': [
                    'Here\'s a realistic timeline based on your starting point:',
                    'Timeline depends on your current foundation. Here\'s what\'s possible:',
                    'With focused effort, here\'s realistic milestones:'
                ]
            },

            'career_transition': {
                'patterns': [
                    'switch from', 'transition to', 'change careers', 'pivot', 'move from',
                    'new direction', 'shift to'
                ],
                'base_responses': [
                    'Career transitions are increasingly common. Here\'s how to navigate yours:',
                    'Your current experience will be an asset, even in a new field:',
                    'Let\'s build a plan that leverages what you know while developing new skills:'
                ]
            },

            'industry_market_insight': {
                'patterns': [
                    'market demand', 'job market', 'hiring', 'companies', 'industry trends',
                    'job security', 'future proof', 'emerging'
                ],
                'base_responses': [
                    'The job market for {path} is currently strong. Here\'s the analysis:',
                    'Here\'s what we\'re seeing in the industry right now:',
                    'The demand for these skills continues to grow. Here\'s why:'
                ]
            },

            'personal_alignment': {
                'patterns': [
                    'right for me', 'fit my', 'match my', 'align with', 'suits me',
                    'personality', 'values', 'lifestyle', 'work-life'
                ],
                'base_responses': [
                    'Let\'s assess how well this aligns with your values and lifestyle:',
                    'This is deeply personal. Here\'s how to evaluate the fit:',
                    'I\'ll consider what matters most to you in evaluating this path:'
                ]
            },

            'fallback_empathetic': {
                'patterns': ['*'],  # Catch-all
                'base_responses': [
                    'That\'s a thoughtful question. While I might not have a specific answer, here\'s my perspective:',
                    'I appreciate the question. Here\'s what I can offer based on your journey:',
                    'That touches on something important. Let me provide relevant guidance:',
                    'Interesting question. Based on your profile and goals, here\'s what I\'d consider:'
                ]
            }
        }

        self.user_context = {}  # Store context per user

    def get_response(self, message: str, user_id: str, user_profile: Optional[Dict] = None,
                    recommendations: Optional[List[Dict]] = None, message_history: Optional[List[Dict]] = None) -> Dict:
        """
        Generate context-aware response from mentor chatbot.

        Args:
            message: User message
            user_id: User identifier for context tracking
            user_profile: User's skill profile
            recommendations: User's career recommendations
            message_history: Previous messages in conversation

        Returns:
            dict: Response with content, intent, sentiment, and guidance
        """
        if not message or not message.strip():
            return self._generate_empty_response()

        # Analyze sentiment
        sentiment = self._analyze_sentiment(message)

        # Extract intent
        intent, intent_match = self._extract_intent(message)

        # Build context
        context = {
            'user_id': user_id,
            'profile': user_profile,
            'recommendations': recommendations,
            'message_history': message_history or [],
            'sentiment': sentiment
        }

        # Store in user context
        self._update_user_context(user_id, context)

        # Generate response
        response_content = self._generate_response(message, intent, intent_match, context)

        # Build follow-up based on sentiment
        follow_up = self._generate_follow_up(sentiment, intent, context)

        return {
            'response': response_content,
            'sentiment': sentiment['label'],
            'confidence': sentiment['compound'],
            'intent': intent,
            'follow_up': follow_up,
            'guidance_type': self._determine_guidance_type(sentiment, intent),
            'timestamp': self._get_timestamp()
        }

    def _analyze_sentiment(self, text: str) -> Dict:
        """Sophisticated sentiment analysis."""
        if not self.sentiment_analyzer:
            return {'label': 'neutral', 'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1}

        scores = self.sentiment_analyzer.polarity_scores(text)
        compound = scores['compound']

        # Nuanced classification
        if compound >= 0.1:
            label = 'positive'
        elif compound <= -0.1:
            label = 'negative'
        else:
            label = 'neutral'

        # Detect confusion/uncertainty
        uncertainty_keywords = ['unsure', 'not sure', 'confused', 'unclear', 'uncertain', 'how']
        is_uncertain = any(keyword in text.lower() for keyword in uncertainty_keywords)

        return {
            'label': label,
            'compound': compound,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'uncertain': is_uncertain
        }

    def _extract_intent(self, message: str) -> Tuple[str, str]:
        """Extract user intent from message with pattern matching."""
        message_lower = message.lower()

        # Check each intent category
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                if pattern == '*':
                    continue
                if pattern in message_lower:
                    return intent_name, pattern

        return 'fallback_empathetic', None

    def _generate_response(self, message: str, intent: str, pattern: str, context: Dict) -> str:
        """Generate contextual response based on intent and user context."""
        intent_config = self.intents.get(intent, self.intents['fallback_empathetic'])
        base_response = random.choice(intent_config['base_responses'])

        # Personalize with context
        personalized = self._personalize_response(base_response, context)

        # Add specific guidance
        if intent == 'uncertainty_doubt' and context['sentiment']['uncertain']:
            guidance = random.choice(intent_config['guidance'])
            personalized += f"\n\nHere's what I'd focus on: {guidance}"

        if intent == 'skill_development':
            suggestion = random.choice(intent_config['suggestions'])
            personalized += f"\n\n💡 {suggestion}"

        # Add sentiment-aware closing
        if context['sentiment']['label'] == 'negative':
            personalized += "\n\nRemember: every expert faced these doubts. You're asking the right questions."
        elif context['sentiment']['label'] == 'positive':
            personalized += "\n\nI love your enthusiasm. Let's channel it into action."

        return personalized

    def _personalize_response(self, template: str, context: Dict) -> str:
        """Personalize response template with user context."""
        profile = context.get('profile', {})
        recommendations = context.get('recommendations', [])

        # Extract variables from template
        if '{path}' in template and recommendations:
            top_path = recommendations[0]['career_path']
            template = template.replace('{path}', top_path)

        if '{strengths}' in template and recommendations:
            strengths = recommendations[0].get('strength_alignment', {}).get('skills', ['your unique abilities'])
            strength_str = ', '.join(strengths[:2]) if strengths else 'your unique abilities'
            template = template.replace('{strengths}', strength_str)

        if '{skill}' in template:
            skills = ['coding', 'math', 'creativity', 'communication']
            highest_skill = max(
                [(s, profile.get(f'{s}_proficiency', 3)) for s in skills if f'{s}_proficiency' in profile or s == 'coding'],
                key=lambda x: x[1],
                default=('learning', 3)
            )[0]
            template = template.replace('{skill}', highest_skill)

        if '{level}' in template:
            level = profile.get('coding_proficiency', 3)
            template = template.replace('{level}', str(level))

        if '{motivation}' in template:
            motivation = profile.get('primary_motivation', 'growth')
            template = template.replace('{motivation}', motivation)

        return template

    def _generate_follow_up(self, sentiment: Dict, intent: str, context: Dict) -> str:
        """Generate contextual follow-up question."""
        if sentiment['uncertain'] or sentiment['label'] == 'negative':
            return "What aspect concerns you most? Let's tackle it together."

        if intent == 'path_deep_dive':
            return "Would you like to discuss specific projects or learning resources?"

        if intent == 'skill_development':
            return "Which skill would you like to tackle first?"

        if intent == 'comparison_exploration':
            return "What's the most important factor in your decision?"

        return "What else would be helpful to explore?"

    def _determine_guidance_type(self, sentiment: Dict, intent: str) -> str:
        """Determine type of guidance being offered."""
        if sentiment['uncertain'] or sentiment['label'] == 'negative':
            return 'reassurance'
        elif sentiment['label'] == 'positive':
            return 'acceleration'
        else:
            return 'exploration'

    def _update_user_context(self, user_id: str, context: Dict):
        """Store and update user conversation context."""
        if user_id not in self.user_context:
            self.user_context[user_id] = {
                'messages': [],
                'intents': [],
                'sentiments': []
            }

        self.user_context[user_id]['messages'].append(context['profile'])
        self.user_context[user_id]['intents'].append(context)
        self.user_context[user_id]['sentiments'].append(context['sentiment']['label'])

    def _generate_empty_response(self) -> Dict:
        """Generate response for empty input."""
        return {
            'response': 'I\'m here to help. Feel free to ask me about career paths, skills, projects, or anything about your journey. What\'s on your mind?',
            'sentiment': 'neutral',
            'confidence': 0,
            'intent': 'fallback',
            'follow_up': None,
            'guidance_type': 'exploration'
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def offer_encouragement(self, user_id: str, sentiment_label: str) -> str:
        """Offer sentiment-appropriate encouragement."""
        encouragements = {
            'negative': [
                "Your journey is unique. The fact that you're exploring shows real clarity.",
                "Challenges are just learning opportunities in disguise.",
                "Every successful person you admire started exactly where you are now.",
                "Your effort matters more than your current skill level."
            ],
            'positive': [
                "That's the energy that drives success!",
                "Your enthusiasm is contagious. Channel it into your next project.",
                "This momentum will carry you far. Let's build on it.",
                "I can feel your readiness. Let's turn it into action."
            ],
            'neutral': [
                "You're asking smart questions. That's how growth happens.",
                "Thoughtful exploration leads to confident choices.",
                "Let's dig deeper into what excites you.",
                "Your curiosity is your greatest asset."
            ]
        }

        return random.choice(encouragements.get(sentiment_label, encouragements['neutral']))

    def suggest_next_action(self, profile: Dict, recommendations: List[Dict]) -> str:
        """Suggest concrete next action for user."""
        if not recommendations:
            return "Let's start by learning more about your interests through the assessment."

        top_path = recommendations[0]['career_path']
        projects = recommendations[0].get('beginner_projects', [])

        suggestions = [
            f"Build your first {top_path}-related project: {projects[0] if projects else 'something practical'}",
            f"Start with the foundational skill in your learning roadmap for {top_path}.",
            f"Connect with someone working as a {recommendations[0]['job_titles'][0] if recommendations[0].get('job_titles') else 'professional'} and ask about their journey.",
            f"Join a community focused on {top_path} and start participating."
        ]

        return random.choice(suggestions)


# Type hint helper
from typing import Tuple
