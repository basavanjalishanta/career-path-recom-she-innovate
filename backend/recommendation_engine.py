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
        ,
        'Cybersecurity Analyst': {
            'description': 'Monitors systems and responds to security incidents, analyzes threats and vulnerabilities',
            'required_skills': {'coding': 0.20, 'math': 0.10, 'communication': 0.20, 'creativity': 0.15, 'domain': 0.35},
            'related_domains': ['Cybersecurity', 'Networking', 'Cloud'],
            'ideal_traits': ['analytical', 'meticulous', 'calm-under-pressure', 'curious'],
            'salary_range': '$90k-$160k+',
            'market_demand': 'high',
            'job_titles': ['Security Analyst', 'SOC Analyst', 'Threat Analyst'],
            'beginner_projects': [
                'Set up a home lab and practice monitoring logs',
                'Perform vulnerability scans on a test environment',
                'Write incident response playbook for a mock breach'
            ],
            'intermediate_projects': [
                'Design SIEM rules and alerts',
                'Conduct tabletop incident response exercise',
                'Automate alert triage with scripting'
            ],
            'learning_roadmap': [
                'Learn networking fundamentals and protocols',
                'Study system and log analysis',
                'Master common security tooling (SIEM, IDS/IPS)',
                'Practice incident response and threat hunting'
            ]
        },
        'Cloud Engineer': {
            'description': 'Designs, builds, and manages scalable cloud infrastructure and services',
            'required_skills': {'coding': 0.20, 'math': 0.05, 'communication': 0.15, 'creativity': 0.10, 'domain': 0.50},
            'related_domains': ['Cloud', 'DevOps', 'Infrastructure'],
            'ideal_traits': ['systematic', 'reliable', 'collaborative', 'detail-oriented'],
            'salary_range': '$100k-$180k+',
            'market_demand': 'high',
            'job_titles': ['Cloud Engineer', 'Cloud Architect', 'Site Reliability Engineer'],
            'beginner_projects': [
                'Deploy a simple web service to a cloud provider',
                'Build infrastructure with IaC (Terraform/CloudFormation)',
                'Set up basic monitoring and alerts'
            ],
            'intermediate_projects': [
                'Design multi-region failover',
                'Implement automated scaling and cost optimization',
                'Migrate a service to cloud with minimal downtime'
            ],
            'learning_roadmap': [
                'Learn one major cloud provider (AWS/GCP/Azure)',
                'Master Infrastructure as Code and automation',
                'Study networking and security in cloud',
                'Practice deployment and monitoring patterns'
            ]
        },
        'DevOps Engineer': {
            'description': 'Builds CI/CD pipelines, automates deployments, and enables developer productivity',
            'required_skills': {'coding': 0.25, 'math': 0.05, 'communication': 0.15, 'creativity': 0.10, 'domain': 0.45},
            'related_domains': ['DevOps', 'Cloud', 'SRE'],
            'ideal_traits': ['automation-focused', 'collaborative', 'efficient', 'problem-solver'],
            'salary_range': '$95k-$170k+',
            'market_demand': 'high',
            'job_titles': ['DevOps Engineer', 'CI/CD Engineer', 'Platform Engineer'],
            'beginner_projects': [
                'Create a CI pipeline for a sample app',
                'Automate deployments with scripts',
                'Containerize an application with Docker'
            ],
            'intermediate_projects': [
                'Implement full CI/CD with automated tests',
                'Build self-service developer platform',
                'Integrate security checks into pipeline'
            ],
            'learning_roadmap': [
                'Learn containerization and orchestration (Docker, Kubernetes)',
                'Master CI/CD tools and pipeline design',
                'Automate observable deployments and rollbacks'
            ]
        },
        'Machine Learning Engineer': {
            'description': 'Productionizes machine learning models and builds scalable inference systems',
            'required_skills': {'coding': 0.35, 'math': 0.30, 'creativity': 0.15, 'communication': 0.10, 'domain': 0.10},
            'related_domains': ['AI', 'Data Science', 'MLOps'],
            'ideal_traits': ['analytical', 'pragmatic', 'detail-oriented', 'curious'],
            'salary_range': '$120k-$210k+',
            'market_demand': 'high',
            'job_titles': ['Machine Learning Engineer', 'ML Engineer', 'MLOps Engineer'],
            'beginner_projects': [
                'Train and evaluate a supervised model end-to-end',
                'Experiment with feature engineering on a dataset',
                'Build a model inference API'
            ],
            'intermediate_projects': [
                'Deploy scalable inference with batching',
                'Implement model monitoring and drift detection',
                'Optimize model latency and throughput'
            ],
            'learning_roadmap': [
                'Master ML fundamentals and model evaluation',
                'Learn model deployment and serving frameworks',
                'Study MLOps patterns and scalable architectures'
            ]
        },
        'Blockchain Developer': {
            'description': 'Designs and implements decentralized applications and smart contracts',
            'required_skills': {'coding': 0.45, 'math': 0.10, 'communication': 0.15, 'creativity': 0.15, 'domain': 0.15},
            'related_domains': ['Blockchain', 'Security', 'Cryptography'],
            'ideal_traits': ['detail-oriented', 'security-minded', 'innovative', 'persistent'],
            'salary_range': '$100k-$200k+',
            'market_demand': 'growing',
            'job_titles': ['Blockchain Developer', 'Smart Contract Engineer', 'DApp Developer'],
            'beginner_projects': [
                'Write and deploy a simple smart contract',
                'Build a small DApp interacting with a contract',
                'Explore token standards and wallets'
            ],
            'intermediate_projects': [
                'Audit and secure smart contracts',
                'Design layer-2 interactions',
                'Integrate off-chain data with oracles'
            ],
            'learning_roadmap': [
                'Learn smart contract languages (Solidity, Vyper)',
                'Study blockchain primitives and security',
                'Build and deploy DApps on testnets'
            ]
        },
        'Mobile App Developer': {
            'description': 'Builds native and cross-platform mobile applications',
            'required_skills': {'coding': 0.55, 'math': 0.05, 'communication': 0.15, 'creativity': 0.15, 'domain': 0.10},
            'related_domains': ['Mobile', 'UI/UX', 'Web'],
            'ideal_traits': ['user-focused', 'detail-oriented', 'creative', 'collaborative'],
            'salary_range': '$85k-$160k+',
            'market_demand': 'high',
            'job_titles': ['Mobile Developer', 'iOS Developer', 'Android Developer', 'React Native Developer'],
            'beginner_projects': [
                'Build a simple todo app for mobile',
                'Create a small cross-platform app with React Native',
                'Implement local storage and simple navigation'
            ],
            'intermediate_projects': [
                'Implement native features (camera, sensors)',
                'Optimize performance and animations',
                'Publish an app to app stores'
            ],
            'learning_roadmap': [
                'Learn platform basics (Android/iOS) or cross-platform tools',
                'Study mobile UI/UX and performance',
                'Build and publish production-ready apps'
            ]
        },
        'Software Engineer': {
            'description': 'Designs and implements reliable software systems across stacks',
            'required_skills': {'coding': 0.50, 'math': 0.10, 'communication': 0.20, 'creativity': 0.10, 'domain': 0.10},
            'related_domains': ['Web', 'Systems', 'Cloud'],
            'ideal_traits': ['pragmatic', 'collaborative', 'problem-solver', 'detail-oriented'],
            'salary_range': '$90k-$180k+',
            'market_demand': 'high',
            'job_titles': ['Software Engineer', 'Backend Engineer', 'Systems Engineer'],
            'beginner_projects': [
                'Build a CLI or small backend service',
                'Implement unit tests and CI',
                'Create a small library or package'
            ],
            'intermediate_projects': [
                'Design and implement scalable services',
                'Optimize algorithms and performance',
                'Lead a small engineering project'
            ],
            'learning_roadmap': [
                'Master a programming language deeply',
                'Study system design and architecture',
                'Learn testing, observability, and deployment practices'
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
        # Normalize profile so engine accepts both DB-shaped and form-shaped inputs
        norm_profile = self._normalize_profile(profile)

        # Calculate scores for all paths
        path_scores = {}
        for path_name, path_config in self.paths.items():
            score_data = self._calculate_path_score(norm_profile, path_config)
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

                # Guidance - include a server-side skill gap analysis derived from the user's profile
                'skill_gap_analysis': self._analyze_skill_gaps(norm_profile, path_config),
                'skill_gap': self.compute_skill_gap(
                    user_skills=self._extract_user_skill_names(norm_profile),
                    career_name=path_name,
                    required_skills=list(path_config.get('required_skills', {}).keys())
                ),
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

    def _normalize_profile(self, profile: Dict) -> Dict:
        """Normalize incoming profile dicts from DB or form into a canonical shape the engine expects.

        Accepts either:
        - DB-shaped profile: {'skills': {'coding':.., 'math':..}, 'preferred_domains':..., 'project_experience':..., ...}
        - Form-shaped profile: {'coding_proficiency': .., 'math_comfort': .., ...}
        Returns a dict with top-level keys used throughout the engine.
        """
        norm = {}

        # Skills: prefer explicit top-level keys, otherwise fall back to nested 'skills' dict
        skills = profile.get('skills') if isinstance(profile.get('skills'), dict) else {}

        norm['coding_proficiency'] = profile.get('coding_proficiency') or skills.get('coding') or profile.get('coding') or 3
        norm['math_comfort'] = profile.get('math_comfort') or skills.get('math') or profile.get('math') or 3
        norm['creativity'] = profile.get('creativity') or skills.get('creativity') or 3
        norm['communication_skill'] = profile.get('communication_skill') or skills.get('communication') or 3
        norm['domain_expertise'] = profile.get('domain_expertise') or skills.get('domain_expertise') or skills.get('domain') or 2

        # Preferences and metadata
        norm['preferred_domains'] = profile.get('preferred_domains') or profile.get('preferredDomains') or []
        norm['career_goal'] = (profile.get('career_goal') or profile.get('careerGoal') or profile.get('career'))
        norm['project_experience_level'] = profile.get('project_experience_level') or profile.get('project_experience') or profile.get('projectExperience') or 1
        norm['confidence_level'] = profile.get('confidence_level') or profile.get('confidence') or 2
        norm['primary_motivation'] = profile.get('primary_motivation') or profile.get('motivation')
        norm['completed'] = profile.get('completed', False)

        # Include original for downstream uses
        norm['_original'] = profile
        return norm

    def _extract_user_skill_names(self, profile: Dict) -> List[str]:
        """Return a list of skill names the user has (approx) from normalized profile.

        We consider a skill 'present' if the rating is >= 3.
        """
        skills = []
        mapping = {
            'coding': profile.get('coding_proficiency', 0),
            'math': profile.get('math_comfort', 0),
            'creativity': profile.get('creativity', 0),
            'communication': profile.get('communication_skill', 0),
            'domain': profile.get('domain_expertise', 0)
        }
        for name, val in mapping.items():
            if val and val >= 3:
                skills.append(name)
        # include preferred domains as additional "skills"
        for d in profile.get('preferred_domains', []) or []:
            if isinstance(d, str):
                skills.append(d.lower())

        return skills

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

    def compute_skill_gap(self, user_skills, career_name: str, required_skills) -> Dict:
        """Compute a simple skill gap analysis from lists or comma-separated strings.

        Args:
            user_skills: list or comma-separated string of user skills
            career_name: target career name (string)
            required_skills: list or comma-separated string of required skills

        Returns:
            dict with keys: career, fit_score, matched, missing, why, learning_roadmap
        """
        def normalize(input_val):
            if not input_val:
                return []
            if isinstance(input_val, list):
                return [str(x).strip().lower() for x in input_val if str(x).strip()]
            return [s.strip().lower() for s in str(input_val).split(',') if s.strip()]

        user_list = normalize(user_skills)
        req_list = normalize(required_skills)

        matched = [r for r in req_list if r in user_list]
        missing = [r for r in req_list if r not in user_list]

        fit_score = 0
        if len(req_list) > 0:
            fit_score = round((len(matched) / len(req_list)) * 100)
        elif isinstance(career_name, str) and career_name in self.CAREER_PATHS:
            # fallback to internal alignment if no explicit required list
            # map to internal scoring by using _calculate_path_score
            score_data = self._calculate_path_score({'coding_proficiency': 3, 'math_comfort': 3, 'creativity': 3, 'communication_skill': 3}, self.CAREER_PATHS.get(career_name))
            fit_score = round(score_data['alignment_score'])

        why = f"You match {len(matched)} of {len(req_list)} listed skill(s) for {career_name}. Focused learning on the missing skills will improve your fit and readiness."

        learning_roadmap = [
            f"Learn core concepts for: {', '.join(missing[:3])}" if missing else "Continue building on your current strengths",
            "Apply new skills in 2–3 small projects and publish them.",
            "Create a polished portfolio case study and practice explaining your outcomes."
        ]

        return {
            'career': career_name,
            'fit_score': fit_score,
            'matched': matched,
            'missing': missing,
            'why': why,
            'learning_roadmap': learning_roadmap
        }

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
