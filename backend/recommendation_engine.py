"""
Advanced Recommendation Engine - Production Grade
Implements sophisticated explainable AI scoring system.
"""

from typing import Dict, List, Tuple
import json


class AdvancedRecommendationEngine:
    """Production-grade recommendation system with explainable scoring."""

    # Career paths with detailed definitions
    CAREER_PATHS = {
        'AI Engineer': {
            'description': 'Develops machine learning models, AI systems, and intelligent applications',
            'required_skills': {'coding': 0.35, 'math': 0.35, 'creativity': 0.15, 'communication': 0.10, 'domain': 0.05},
            'related_domains': ['AI', 'Data Science', 'Web', 'Research'],
            'ideal_traits': ['analytical', 'creative', 'detail-oriented', 'curious'],
            'salary_range': '$120k-$200k+',
            'market_demand': 'high',
            'job_titles': ['Machine Learning Engineer', 'AI Researcher', 'Deep Learning Engineer', 'AI Scientist'],
            'beginner_projects': [
                'Build a CNN image classifier',
                'Create a sentiment analysis model',
                'Develop a recommendation system',
                'Implement NLP text generator'
            ],
            'intermediate_projects': [
                'Deploy ML model to production',
                'Build end-to-end ML pipeline',
                'Implement reinforcement learning agent',
                'Create computer vision application'
            ],
            'learning_roadmap': [
                'Master Python, NumPy, Pandas',
                'Learn Linear Algebra and Calculus',
                'Study Machine Learning fundamentals',
                'Explore Deep Learning frameworks (TensorFlow, PyTorch)',
                'Learn MLOps and model deployment',
                'Build and ship real-world projects'
            ]
        },
        'Full Stack Developer': {
            'description': 'Builds complete web applications from frontend UI to backend infrastructure',
            'required_skills': {'coding': 0.40, 'creativity': 0.20, 'communication': 0.20, 'math': 0.10, 'domain': 0.10},
            'related_domains': ['Web', 'AI', 'UI/UX', 'Cybersecurity'],
            'ideal_traits': ['pragmatic', 'communicative', 'adaptable', 'problem-solver'],
            'salary_range': '$90k-$160k+',
            'market_demand': 'high',
            'job_titles': ['Full Stack Developer', 'Web Developer', 'Software Engineer', 'Product Engineer'],
            'beginner_projects': [
                'Build a todo app with frontend and backend',
                'Create a e-commerce product page',
                'Develop a note-taking application',
                'Build a real-time chat application'
            ],
            'intermediate_projects': [
                'Deploy app to cloud (AWS, Heroku, Vercel)',
                'Implement authentication and authorization',
                'Build scalable database architecture',
                'Create API with proper documentation'
            ],
            'learning_roadmap': [
                'Learn HTML, CSS, JavaScript fundamentals',
                'Master frontend framework (React, Vue, Angular)',
                'Learn backend language (Python, Node.js, Ruby)',
                'Study databases and SQL',
                'Learn DevOps and deployment',
                'Master API design and architecture'
            ]
        },
        'Cybersecurity Specialist': {
            'description': 'Protects systems, networks, and data from digital attacks',
            'required_skills': {'coding': 0.30, 'math': 0.20, 'communication': 0.20, 'creativity': 0.15, 'domain': 0.15},
            'related_domains': ['Cybersecurity', 'Web', 'Data Science'],
            'ideal_traits': ['analytical', 'meticulous', 'proactive', 'collaborative'],
            'salary_range': '$100k-$180k+',
            'market_demand': 'high',
            'job_titles': ['Security Engineer', 'Penetration Tester', 'Security Architect', 'Incident Response'],
            'beginner_projects': [
                'Learn network security basics',
                'Conduct vulnerability assessment',
                'Create a secure authentication system',
                'Build intrusion detection system'
            ],
            'intermediate_projects': [
                'Perform penetration testing',
                'Design security architecture',
                'Implement zero-trust security model',
                'Create incident response playbook'
            ],
            'learning_roadmap': [
                'Master networking fundamentals',
                'Learn cryptography and encryption',
                'Study system security and hardening',
                'Learn pentesting tools and techniques',
                'Pursue certifications (CEH, OSCP)',
                'Develop security mindset'
            ]
        },
        'Data Analyst': {
            'description': 'Transforms data into insights to drive business decisions',
            'required_skills': {'math': 0.35, 'coding': 0.25, 'communication': 0.25, 'creativity': 0.10, 'domain': 0.05},
            'related_domains': ['Data Science', 'AI', 'Web'],
            'ideal_traits': ['analytical', 'curious', 'communicative', 'detail-oriented'],
            'salary_range': '$80k-$150k+',
            'market_demand': 'high',
            'job_titles': ['Data Analyst', 'Business Analyst', 'Analytics Engineer', 'Data Scientist'],
            'beginner_projects': [
                'Analyze public dataset and create visualizations',
                'Build dashboard from raw data',
                'Create predictive model for trends',
                'Perform cohort analysis'
            ],
            'intermediate_projects': [
                'Design data warehouse',
                'Create automated reporting pipeline',
                'Build predictive models',
                'Implement A/B testing framework'
            ],
            'learning_roadmap': [
                'Master Excel and SQL',
                'Learn data visualization (Tableau, Power BI)',
                'Study statistics and probability',
                'Learn Python or R for data analysis',
                'Explore machine learning basics',
                'Master storytelling with data'
            ]
        },
        'UI/UX Designer': {
            'description': 'Creates delightful and intuitive user experiences for digital products',
            'required_skills': {'creativity': 0.40, 'communication': 0.30, 'coding': 0.15, 'math': 0.05, 'domain': 0.10},
            'related_domains': ['UI/UX', 'Web', 'AI'],
            'ideal_traits': ['creative', 'empathetic', 'collaborative', 'user-focused'],
            'salary_range': '$80k-$140k+',
            'market_demand': 'high',
            'job_titles': ['UI Designer', 'UX Designer', 'Product Designer', 'Design Lead'],
            'beginner_projects': [
                'Redesign existing website',
                'Create design system',
                'Conduct user research',
                'Build interactive prototype'
            ],
            'intermediate_projects': [
                'Lead design for mobile application',
                'Implement design thinking process',
                'Create comprehensive design documentation',
                'Conduct usability testing'
            ],
            'learning_roadmap': [
                'Master design fundamentals (color, typography, layout)',
                'Learn design tools (Figma, Adobe XD)',
                'Study user psychology and behavior',
                'Learn prototyping and interaction design',
                'Master user research methods',
                'Develop design leadership skills'
            ]
        },
        'Research Engineer': {
            'description': 'Pushes boundary of technology by implementing and advancing research',
            'required_skills': {'math': 0.35, 'coding': 0.30, 'creativity': 0.20, 'communication': 0.10, 'domain': 0.05},
            'related_domains': ['AI', 'Data Science', 'Research'],
            'ideal_traits': ['curious', 'thorough', 'innovative', 'persistent'],
            'salary_range': '$110k-$200k+',
            'market_demand': 'emerging',
            'job_titles': ['Research Engineer', 'Research Scientist', 'ML Researcher', 'AI Researcher'],
            'beginner_projects': [
                'Reproduce research paper',
                'Contribute to open-source research project',
                'Write technical blog post on research',
                'Implement novel algorithm'
            ],
            'intermediate_projects': [
                'Develop novel research direction',
                'Publish research findings',
                'Lead research collaboration',
                'Create research framework'
            ],
            'learning_roadmap': [
                'Master advanced mathematics',
                'Study research methodology',
                'Read and critically analyze papers',
                'Learn academic writing',
                'Master presentation skills',
                'Build research network'
            ]
        },
        'Startup Builder': {
            'description': 'Creates and launches innovative startups from ideation to scale',
            'required_skills': {'communication': 0.35, 'coding': 0.25, 'creativity': 0.25, 'math': 0.10, 'domain': 0.05},
            'related_domains': ['Web', 'AI', 'UI/UX'],
            'ideal_traits': ['ambitious', 'risk-taker', 'entrepreneur', 'resilient'],
            'salary_range': '$0-∞ (depends on success)',
            'market_demand': 'emerging',
            'job_titles': ['Founder', 'CEO', 'Co-Founder', 'Startup Operator'],
            'beginner_projects': [
                'Validate startup idea',
                'Build MVP (Minimum Viable Product)',
                'Conduct customer interviews',
                'Create pitch deck'
            ],
            'intermediate_projects': [
                'Launch beta product',
                'Raise seed funding',
                'Build founding team',
                'Scale to acquire customers'
            ],
            'learning_roadmap': [
                'Learn business fundamentals',
                'Study market research and validation',
                'Master product development',
                'Learn fundraising and finance',
                'Develop leadership skills',
                'Build network in startup ecosystem'
            ]
        }
    }

    def __init__(self):
        """Initialize recommendation engine."""
        self.paths = self.CAREER_PATHS

    def get_recommendations(self, profile: Dict) -> List[Dict]:
        """
        Generate personalized career recommendations.

        Args:
            profile (dict): User profile with skills, preferences, etc.

        Returns:
            list: Top 3 recommendations with detailed explanations
        """
        # Calculate scores for all paths
        path_scores = {}
        for path_name, path_config in self.paths.items():
            score_data = self._calculate_path_score(profile, path_config)
            path_scores[path_name] = score_data

        # Sort by alignment score
        sorted_paths = sorted(path_scores.items(), key=lambda x: x[1]['alignment_score'], reverse=True)

        # Build recommendations with detailed reasoning
        recommendations = []
        for rank, (path_name, score_data) in enumerate(sorted_paths[:3], 1):
            path_config = self.paths[path_name]

            recommendation = {
                'rank': rank,
                'career_path': path_name,
                'alignment_score': round(score_data['alignment_score'], 1),
                'confidence': self._get_confidence_level(score_data['alignment_score']),

                # Reasoning
                'reasoning': self._generate_reasoning(profile, path_name, score_data),
                'strength_alignment': score_data['strength_alignment'],
                'growth_opportunities': score_data['growth_opportunities'],

                # Projects and learning
                'beginner_projects': path_config['beginner_projects'][:2],
                'intermediate_projects': path_config['intermediate_projects'][:2],
                'learning_roadmap': path_config['learning_roadmap'],

                # Guidance
                'skill_gap_analysis': self._analyze_skill_gaps(profile, path_config),
                'timeline_estimate': self._estimate_timeline(profile, path_config),

                # Alternatives
                'description': path_config['description'],
                'similar_paths': [p[0] for p in sorted_paths[3:6] if p[0] != path_name],
                'salary_range': path_config['salary_range'],
                'market_demand': path_config['market_demand'],
                'job_titles': path_config['job_titles'][:3]
            }

            recommendations.append(recommendation)

        return recommendations

    def _calculate_path_score(self, profile: Dict, path_config: Dict) -> Dict:
        """Calculate detailed alignment score for a path."""
        # Skill alignment (largest weight)
        skill_score = self._calculate_skill_alignment(profile, path_config['required_skills'])

        # Domain alignment
        domain_score = self._calculate_domain_alignment(profile.get('preferred_domains', []), path_config['related_domains'])

        # Career goal alignment
        goal_score = self._calculate_goal_alignment(profile.get('career_goal'), path_config)

        # Trait alignment (personality fit)
        trait_score = self._calculate_trait_alignment(profile, path_config['ideal_traits'])

        # Experience level consideration
        experience_bonus = profile.get('project_experience_level', 1) * 5

        # Combine scores with weights
        final_score = (
            skill_score * 0.40 +
            domain_score * 0.25 +
            goal_score * 0.15 +
            trait_score * 0.15 +
            experience_bonus * 0.05
        )

        return {
            'alignment_score': final_score,
            'skill_score': skill_score,
            'domain_score': domain_score,
            'goal_score': goal_score,
            'trait_score': trait_score,
            'strength_alignment': {
                'skills': self._find_strength_alignment(profile, path_config),
                'domains': [d for d in profile.get('preferred_domains', []) if d in path_config['related_domains']]
            },
            'growth_opportunities': self._identify_growth_opportunities(profile, path_config)
        }

    def _calculate_skill_alignment(self, profile: Dict, required_skills: Dict) -> float:
        """Calculate how well user skills align with path requirements."""
        skill_mapping = {
            'coding': profile.get('coding_proficiency', 3),
            'math': profile.get('math_comfort', 3),
            'creativity': profile.get('creativity', 3),
            'communication': profile.get('communication_skill', 3),
            'domain': profile.get('domain_expertise', 2)
        }

        weighted_score = 0
        total_weight = 0

        for skill, weight in required_skills.items():
            user_level = skill_mapping.get(skill, 3)
            weighted_score += user_level * weight * 20
            total_weight += weight

        return (weighted_score / total_weight) if total_weight > 0 else 0

    def _calculate_domain_alignment(self, user_domains: List[str], path_domains: List[str]) -> float:
        """Align user domain preferences with path requirements."""
        if not user_domains:
            return 0

        matches = sum(1 for domain in user_domains if domain in path_domains)
        return (matches / len(user_domains)) * 100

    def _calculate_goal_alignment(self, user_goal: str, path_config: Dict) -> float:
        """Align user career goal with path fit."""
        goal_fit = {
            'job': {'AI Engineer': 25, 'Full Stack Developer': 25, 'Cybersecurity Specialist': 20, 'Data Analyst': 20, 'UI/UX Designer': 15, 'Research Engineer': 15, 'Startup Builder': 5},
            'startup': {'Startup Builder': 30, 'Full Stack Developer': 25, 'AI Engineer': 20, 'UI/UX Designer': 15, 'Data Analyst': 10, 'Cybersecurity Specialist': 0, 'Research Engineer': 0},
            'research': {'Research Engineer': 30, 'AI Engineer': 25, 'Data Analyst': 20, 'Cybersecurity Specialist': 10, 'Full Stack Developer': 10, 'UI/UX Designer': 5, 'Startup Builder': 0}
        }

        path_name = list(self.CAREER_PATHS.keys())[list(self.CAREER_PATHS.values()).index(path_config)]
        return goal_fit.get(user_goal, {}).get(path_name, 0)

    def _calculate_trait_alignment(self, profile: Dict, ideal_traits: List[str]) -> float:
        """Estimate personality trait alignment (simplified)."""
        # In production, this would use personality assessment data
        # For now, use confidence and other indicators
        confidence = profile.get('confidence_level', 2)
        motivation = profile.get('primary_motivation', 'learning')

        trait_score = confidence * 15
        return min(trait_score, 100)

    def _find_strength_alignment(self, profile: Dict, path_config: Dict) -> List[str]:
        """Find which skills user is strong in for this path."""
        required = path_config['required_skills']
        user_skills = {
            'coding': profile.get('coding_proficiency', 3),
            'math': profile.get('math_comfort', 3),
            'creativity': profile.get('creativity', 3),
            'communication': profile.get('communication_skill', 3),
            'domain': profile.get('domain_expertise', 2)
        }

        strengths = []
        for skill, weight in sorted(required.items(), key=lambda x: x[1], reverse=True):
            if user_skills.get(skill, 1) >= 4:
                strengths.append(f"{skill.replace('_', ' ').title()} ({user_skills.get(skill, 1)}/5)")

        return strengths if strengths else ['General readiness to learn and adapt']

    def _identify_growth_opportunities(self, profile: Dict, path_config: Dict) -> List[str]:
        """Identify which skills need development."""
        required = path_config['required_skills']
        user_skills = {
            'coding': profile.get('coding_proficiency', 3),
            'math': profile.get('math_comfort', 3),
            'creativity': profile.get('creativity', 3),
            'communication': profile.get('communication_skill', 3),
            'domain': profile.get('domain_expertise', 2)
        }

        opportunities = []
        for skill, weight in sorted(required.items(), key=lambda x: x[1], reverse=True):
            user_level = user_skills.get(skill, 1)
            if user_level < 3:
                opportunities.append(f"Strengthen {skill.replace('_', ' ')}")

        return opportunities if opportunities else ['Continue refining current strengths']

    def _analyze_skill_gaps(self, profile: Dict, path_config: Dict) -> Dict:
        """Detailed skill gap analysis."""
        user_skills = {
            'coding': profile.get('coding_proficiency', 3),
            'math': profile.get('math_comfort', 3),
            'creativity': profile.get('creativity', 3),
            'communication': profile.get('communication_skill', 3)
        }

        gaps = {}
        for skill, level in user_skills.items():
            gap = max(0, 4 - level)  # Target is 4/5
            gaps[skill] = {
                'current': level,
                'target': 4,
                'gap': gap,
                'priority': 'high' if gap >= 2 else 'medium'
            }

        return gaps

    def _estimate_timeline(self, profile: Dict, path_config: Dict) -> str:
        """Estimate time to readiness for career path."""
        # Simple heuristic based on experience and confidence
        experience = profile.get('project_experience_level', 1)
        confidence = profile.get('confidence_level', 2)

        if experience >= 3 and confidence >= 3:
            return '3-6 months'
        elif experience >= 2 and confidence >= 2:
            return '6-12 months'
        else:
            return '12-18 months'

    def _generate_reasoning(self, profile: Dict, path_name: str, score_data: Dict) -> str:
        """Generate human-readable reasoning for recommendation."""
        parts = []

        # Identify key factors
        if score_data['skill_score'] > 70:
            parts.append("your strong technical foundation")
        if score_data['domain_score'] > 50:
            parts.append("alignment with your domain interests")
        if score_data['goal_score'] > 15:
            parts.append("fit with your career objectives")

        if not parts:
            parts.append("your profile characteristics")

        reasoning = f"Based on {', '.join(parts)}, {path_name} is a strong match for your goals. "
        reasoning += f"With a {score_data['alignment_score']:.0f}% alignment score, this path leverages your existing strengths "
        reasoning += f"while providing excellent opportunities for growth and development."

        return reasoning

    def _get_confidence_level(self, score: float) -> str:
        """Determine confidence in recommendation."""
        if score >= 80:
            return 'High'
        elif score >= 60:
            return 'Medium'
        elif score >= 40:
            return 'Moderate'
        else:
            return 'Exploratory'

    def get_learning_roadmap(self, path_name: str) -> List[str]:
        """Get learning roadmap for specific career path."""
        if path_name in self.CAREER_PATHS:
            return self.CAREER_PATHS[path_name]['learning_roadmap']
        return []

    def compare_paths(self, path1: str, path2: str, profile: Dict) -> Dict:
        """Compare two career paths for user."""
        config1 = self.CAREER_PATHS.get(path1)
        config2 = self.CAREER_PATHS.get(path2)

        if not config1 or not config2:
            return {}

        score1 = self._calculate_path_score(profile, config1)
        score2 = self._calculate_path_score(profile, config2)

        return {
            'path1': {
                'name': path1,
                'score': score1['alignment_score'],
                'strengths': config1['ideal_traits'][:3],
                'salary': config1['salary_range']
            },
            'path2': {
                'name': path2,
                'score': score2['alignment_score'],
                'strengths': config2['ideal_traits'][:3],
                'salary': config2['salary_range']
            },
            'recommendation': path1 if score1['alignment_score'] > score2['alignment_score'] else path2,
            'difference': abs(score1['alignment_score'] - score2['alignment_score'])
        }
