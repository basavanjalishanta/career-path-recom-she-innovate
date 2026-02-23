"""
Advanced Mentor Chatbot - Context-Aware Conversational AI
Provides sophisticated guidance with understanding of user context.
"""

from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Optional, Tuple
import json
import random
import os
import urllib.request
import urllib.error


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
        self.last_followup_by_user = {}
        self.groq_api_key = os.getenv('GROQ_API_KEY') or os.getenv('GSK_API_KEY')
        self.groq_model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
        self.groq_temperature = float(os.getenv('GROQ_TEMPERATURE', '0.85'))
        self.last_llm_error = None

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

        # Generate response (prefer LLM if configured, fallback to local logic).
        llm_response = self._generate_llm_response(
            message=message,
            intent=intent,
            context=context
        )
        if llm_response:
            response_content = llm_response
        else:
            response_content = self._generate_structured_fallback(message, intent, context)

        # Build follow-up based on sentiment
        follow_up = self._generate_follow_up(user_id, sentiment, intent, context)

        return {
            'response': response_content,
            'sentiment': sentiment['label'],
            'confidence': sentiment['compound'],
            'intent': intent,
            'follow_up': follow_up,
            'guidance_type': self._determine_guidance_type(sentiment, intent),
            'timestamp': self._get_timestamp(),
            'llm_used': bool(llm_response),
            'llm_error': self.last_llm_error
        }

    def _generate_llm_response(self, message: str, intent: str, context: Dict) -> Optional[str]:
        """Generate response from Groq-compatible chat API if key is configured."""
        if not self.groq_api_key:
            self.last_llm_error = 'Missing GROQ_API_KEY/GSK_API_KEY'
            return None

        try:
            self.last_llm_error = None
            profile = context.get('profile') or {}
            recommendations = context.get('recommendations') or []
            message_history = context.get('message_history') or []

            top_paths = []
            weak_areas = []
            if recommendations:
                for rec in recommendations[:3]:
                    path = rec.get('career_path')
                    score = rec.get('alignment_score')
                    if path is not None:
                        if score is not None:
                            top_paths.append(f"{path} ({score}%)")
                        else:
                            top_paths.append(str(path))
                    for item in rec.get('growth_opportunities', []) or []:
                        weak_areas.append(str(item))

            # Fallback weak-area extraction from profile scores.
            if not weak_areas and isinstance(profile, dict):
                score_pairs = [
                    ('coding', profile.get('coding_proficiency', profile.get('coding', 3))),
                    ('math', profile.get('math_comfort', profile.get('math', 3))),
                    ('creativity', profile.get('creativity', 3)),
                    ('communication', profile.get('communication_skill', profile.get('communication', 3))),
                    ('domain expertise', profile.get('domain_expertise', 2))
                ]
                weak_areas = [name for name, val in score_pairs if int(val or 0) <= 2]

            top_paths_text = ', '.join(top_paths) if top_paths else 'No ranked paths available yet'
            weak_areas_text = ', '.join(dict.fromkeys(weak_areas)) if weak_areas else 'No critical weak area detected'
            recent_history = []
            for item in message_history[-6:]:
                sender = item.get('sender', 'user')
                content = item.get('content', '')
                if content:
                    recent_history.append(f"{sender}: {content}")
            history_text = "\n".join(recent_history) if recent_history else "No prior messages."

            system_prompt = """
You are an advanced AI Career Mentor.
Your style is dynamic, practical, warm, and mentorship-first.
You can answer any career, skills, projects, interview, learning, confidence, or roadmap question.
Use the user's profile and recommendations directly.
Avoid generic advice.

Always respond with these sections:
1. Clear Answer
2. Improvement Suggestion
3. Action Steps
4. Short Motivational Close

If data is missing, make the best-possible inference and suggest what to provide next.
"""
            user_prompt = (
                f"User message: {message}\n"
                f"Detected intent: {intent}\n"
                f"Top recommendations: {top_paths_text}\n"
                f"Weak areas: {weak_areas_text}\n"
                f"User profile: {json.dumps(profile, ensure_ascii=True)}\n"
                f"Recent conversation:\n{history_text}\n"
                "Respond in structured bullets, concise but specific, with mentorship tone."
            )

            payload = {
                "model": self.groq_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": self.groq_temperature,
                "max_tokens": 900
            }
            data = json.dumps(payload).encode('utf-8')

            req = urllib.request.Request(
                url='https://api.groq.com/openai/v1/chat/completions',
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.groq_api_key}'
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read().decode('utf-8')

            parsed = json.loads(body)
            return (
                parsed.get('choices', [{}])[0]
                .get('message', {})
                .get('content', '')
                .strip()
            ) or None
        except urllib.error.HTTPError as e:
            try:
                detail = e.read().decode('utf-8')
            except Exception:
                detail = str(e)
            self.last_llm_error = f'HTTP {getattr(e, "code", "error")}: {detail[:200]}'
            return None
        except urllib.error.URLError as e:
            self.last_llm_error = f'Network error: {e.reason}'
            return None
        except (json.JSONDecodeError, KeyError, ValueError, TimeoutError) as e:
            self.last_llm_error = f'Parse/runtime error: {str(e)}'
            return None

    def _fallback_recommendation_block(self, context: Dict) -> str:
        """Ensure fallback responses still include recommendations and weak areas."""
        recommendations = context.get('recommendations') or []
        profile = context.get('profile') or {}

        top = []
        weak = []

        for rec in recommendations[:3]:
            path = rec.get('career_path')
            score = rec.get('alignment_score')
            if path:
                top.append(f"{path} ({int(round(float(score))) if score is not None else 'N/A'}%)")
            for item in rec.get('growth_opportunities', []) or []:
                weak.append(str(item))

        if not weak and isinstance(profile, dict):
            pairs = [
                ('coding', profile.get('coding_proficiency', profile.get('coding', 3))),
                ('math', profile.get('math_comfort', profile.get('math', 3))),
                ('creativity', profile.get('creativity', 3)),
                ('communication', profile.get('communication_skill', profile.get('communication', 3))),
                ('domain expertise', profile.get('domain_expertise', 2))
            ]
            weak = [name for name, val in pairs if int(val or 0) <= 2]

        if not top and not weak:
            return ''

        parts = []
        if top:
            parts.append(f"\n\nTop recommendations: {', '.join(top)}.")
        if weak:
            parts.append(f"\nWeak areas to improve: {', '.join(dict.fromkeys(weak))}.")
            parts.append("\nAction: pick one weak area this week and complete one focused mini-project.")
        return ''.join(parts)

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

    def _generate_follow_up(self, user_id: str, sentiment: Dict, intent: str, context: Dict) -> str:
        """Generate contextual follow-up question."""
        options = []
        if sentiment['uncertain'] or sentiment['label'] == 'negative':
            options = [
                "Which part feels most difficult right now?",
                "Do you want a simpler weekly plan to reduce overwhelm?",
                "Should we focus on one weak area first and make it manageable?"
            ]
        elif intent == 'path_deep_dive':
            options = [
                "Do you want role-wise roadmap or project-wise roadmap?",
                "Should I break this into beginner, intermediate, and advanced steps?",
                "Want hiring-focused tips for this path?"
            ]
        elif intent == 'skill_development':
            options = [
                "Which skill should we improve first this week?",
                "Do you want practice exercises or project ideas first?",
                "Should I suggest free resources for this skill?"
            ]
        elif intent == 'comparison_exploration':
            options = [
                "Is salary, demand, or work-life balance your top priority?",
                "Do you want a side-by-side comparison table?",
                "Should I compare timelines for both paths?"
            ]
        else:
            options = [
                "Do you want next-week action items?",
                "Should I suggest three resume-worthy projects?",
                "Would you like interview preparation tips for your top path?"
            ]

        last = self.last_followup_by_user.get(user_id)
        follow_up = options[0]
        for option in options:
            if option != last:
                follow_up = option
                break
        self.last_followup_by_user[user_id] = follow_up
        return follow_up

    def _generate_dynamic_fallback(self, message: str, context: Dict) -> str:
        """Generate non-repetitive fallback response tied to user's actual message."""
        msg = (message or '').lower()
        if 'project' in msg:
            return "Great, let's focus on projects. I can give beginner-to-advanced ideas aligned to your current skill profile."
        if 'skill' in msg or 'weak' in msg or 'improve' in msg:
            return "Let's target improvement areas first. I'll map your weak skills to practical exercises and a weekly plan."
        if 'job' in msg or 'career' in msg or 'role' in msg:
            return "Let's align your profile to the best-fit roles and define the fastest path to become job-ready."
        if 'time' in msg or 'month' in msg or 'timeline' in msg:
            return "Let's build a realistic timeline based on your current level, study hours, and project depth."
        return "I can help with path selection, weak-area improvement, project planning, and job-readiness steps. Tell me what you want first."

    def _generate_structured_fallback(self, message: str, intent: str, context: Dict) -> str:
        """Return a complete mentor answer when LLM is unavailable."""
        recommendations = context.get('recommendations') or []
        profile = context.get('profile') or {}
        msg = (message or '').lower()
        seed = sum(ord(ch) for ch in msg) if msg else 0

        def pick(options, offset=0):
            if not options:
                return ""
            return options[(seed + offset) % len(options)]

        top = []
        weak = []
        best = recommendations[0] if recommendations else {}

        for rec in recommendations[:3]:
            path = rec.get('career_path')
            score = rec.get('alignment_score')
            if path:
                score_txt = f"{int(round(float(score)))}%" if score is not None else "N/A"
                top.append(f"{path} ({score_txt})")
            for item in rec.get('growth_opportunities', []) or []:
                weak.append(str(item))

        if not weak and isinstance(profile, dict):
            pairs = [
                ('coding', profile.get('coding_proficiency', profile.get('coding', 3))),
                ('math', profile.get('math_comfort', profile.get('math', 3))),
                ('creativity', profile.get('creativity', 3)),
                ('communication', profile.get('communication_skill', profile.get('communication', 3))),
                ('domain expertise', profile.get('domain_expertise', 2))
            ]
            weak = [name for name, val in pairs if int(val or 0) <= 2]

        weak = list(dict.fromkeys(weak))[:4]
        roadmap = best.get('learning_roadmap', [])[:3] if best else []
        timeline = best.get('timeline_estimate', '6-12 months') if best else '6-12 months'

        # Message-aware clear answer
        if 'project' in msg:
            clear_answer = pick([
                "You should prioritize practical projects aligned to your top career path.",
                "Project-first learning will accelerate your growth faster than theory-only study.",
                "A portfolio-driven plan is your best route to stronger career alignment."
            ])
        elif 'weak' in msg or 'skill' in msg or intent == 'skill_development':
            clear_answer = pick([
                "Your fastest growth will come from targeted weak-area practice plus one weekly project.",
                "Close one weak area at a time and convert it into proof through small shipped work.",
                "Skill gains will be strongest if each study cycle ends with a practical deliverable."
            ])
        elif 'timeline' in msg or 'how long' in msg or 'month' in msg:
            clear_answer = pick([
                f"With consistent effort, a realistic job-readiness timeline is {timeline}.",
                f"If you maintain weekly consistency, you can be job-ready in about {timeline}.",
                f"Given your current profile, expect roughly {timeline} to become interview-ready."
            ])
        elif 'compare' in msg or intent == 'comparison_exploration':
            clear_answer = pick([
                "Choose the path with highest alignment and strongest market demand for your profile.",
                "Prioritize the path that balances fit score, growth potential, and your motivation.",
                "Use alignment score first, then compare skill-gap effort before deciding."
            ])
        else:
            clear_answer = pick([
                "Based on your current profile, follow a focused path with weekly measurable outcomes.",
                "A focused weekly execution plan will outperform broad, unfocused study.",
                "The best next move is one clear target path with measurable weekly progress."
            ])

        improvement = (
            pick([
                f"Improve these areas first: {', '.join(weak)}.",
                f"Primary improvement priority: {', '.join(weak)}.",
                f"Focus your upskilling here first: {', '.join(weak)}."
            ], 1)
            if weak else
            pick([
                "Strengthen depth by shipping stronger projects and documenting outcomes.",
                "Improve portfolio depth with measurable outcomes and cleaner technical storytelling.",
                "Advance from basic execution to production-quality project delivery."
            ], 2)
        )
        action_steps = [
            pick([
                f"Pick one target path: {top[0] if top else 'complete assessment to generate top recommendations'}.",
                f"Commit to one primary path this week: {top[0] if top else 'generate recommendations first'}.",
                f"Set your focus path now: {top[0] if top else 'finish assessment and pick top ranked option'}."
            ], 3),
            pick([
                f"Follow roadmap this week: {roadmap[0] if roadmap else 'learn fundamentals for your weakest skill'}.",
                f"Complete one roadmap milestone: {roadmap[0] if roadmap else 'practice weakest skill for 5 focused sessions'}.",
                f"Execute the first learning sprint: {roadmap[0] if roadmap else 'core fundamentals + guided practice'}."
            ], 4),
            pick([
                "Build one mini-project, publish it, and write 3 impact bullets for resume/interviews.",
                "Ship one small project this week and document decisions, results, and improvements.",
                "Create a portfolio artifact from this week’s learning and prepare a short project walkthrough."
            ], 5)
        ]
        motivational = pick([
            "Progress compounds. Small weekly execution beats perfect planning.",
            "Consistency wins. Keep shipping, learning, and refining every week.",
            "You are closer than you think; momentum comes from daily deliberate action."
        ], 6)

        return (
            "1. Clear Answer\n"
            f"- {clear_answer}\n\n"
            "2. Improvement Suggestion\n"
            f"- {improvement}\n\n"
            "3. Action Steps\n"
            f"- {action_steps[0]}\n"
            f"- {action_steps[1]}\n"
            f"- {action_steps[2]}\n"
            f"- Additional context: Top recommendations: {', '.join(top) if top else 'Not available yet'}.\n\n"
            "4. Short Motivational Close\n"
            f"- {motivational}"
        )

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

