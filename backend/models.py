"""
Advanced Database Models for Career Recommendation System
Uses SQLAlchemy ORM with proper relationships and validation.
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    """User account model with authentication."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profiles = db.relationship('UserProfile', backref='user', cascade='all, delete-orphan', lazy=True)
    conversations = db.relationship('ChatMessage', backref='user', cascade='all, delete-orphan', lazy=True)
    recommendations = db.relationship('Recommendation', backref='user', cascade='all, delete-orphan', lazy=True)

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class UserProfile(db.Model):
    """User skill profile and preferences."""
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Skills (1-5 rating)
    coding_proficiency = db.Column(db.Integer, default=3)
    math_comfort = db.Column(db.Integer, default=3)
    creativity = db.Column(db.Integer, default=3)
    communication_skill = db.Column(db.Integer, default=3)
    leadership_potential = db.Column(db.Integer, default=3)
    domain_expertise = db.Column(db.Integer, default=2)

    # Preferences
    preferred_domains = db.Column(db.JSON, default=list)  # ['AI', 'Web', etc.]
    career_goal = db.Column(db.String(50))  # 'job', 'startup', 'research'
    teamwork_preference = db.Column(db.Boolean, default=True)
    project_experience_level = db.Column(db.Integer, default=2)
    work_environment = db.Column(db.String(50))  # 'remote', 'hybrid', 'onsite'
    salary_expectation = db.Column(db.String(50))  # 'low', 'medium', 'high'

    # Motivations and concerns
    primary_motivation = db.Column(db.String(100))  # 'impact', 'learning', 'stability', 'wealth'
    key_concerns = db.Column(db.JSON, default=list)  # ['work-life balance', 'growth', etc.]
    growth_areas = db.Column(db.JSON, default=list)  # Areas user wants to improve

    # Metadata
    completed = db.Column(db.Boolean, default=False)
    confidence_level = db.Column(db.Integer, default=2)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recommendations = db.relationship('Recommendation', backref='profile', lazy=True)
    assessment_history = db.relationship('AssessmentHistory', backref='profile', cascade='all, delete-orphan')

    def get_skill_summary(self):
        """Get summary of all skills."""
        return {
            'coding': self.coding_proficiency,
            'math': self.math_comfort,
            'creativity': self.creativity,
            'communication': self.communication_skill,
            'leadership': self.leadership_potential,
            'domain_expertise': self.domain_expertise
        }

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skills': self.get_skill_summary(),
            'preferred_domains': self.preferred_domains,
            'career_goal': self.career_goal,
            'teamwork_preference': self.teamwork_preference,
            'project_experience': self.project_experience_level,
            'work_environment': self.work_environment,
            'motivation': self.primary_motivation,
            'confidence': self.confidence_level,
            'completed': self.completed
        }


class AssessmentHistory(db.Model):
    """Track changes to user profile over time."""
    __tablename__ = 'assessment_history'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    previous_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    changes_made = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Recommendation(db.Model):
    """Career path recommendations for user."""
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)

    rank = db.Column(db.Integer)  # 1, 2, 3 (top recommendations)
    career_path = db.Column(db.String(100), nullable=False)
    alignment_score = db.Column(db.Float)  # 0-100
    confidence = db.Column(db.String(20))  # 'High', 'Medium', 'Moderate'

    # Detailed reasoning
    reasoning = db.Column(db.Text)  # Why this path was recommended
    strength_alignment = db.Column(db.JSON)  # Which skills align
    growth_opportunities = db.Column(db.JSON)  # Areas to develop

    # Detailed guidance
    beginner_projects = db.Column(db.JSON, default=list)
    intermediate_projects = db.Column(db.JSON, default=list)
    learning_roadmap = db.Column(db.JSON, default=list)
    skill_gap_analysis = db.Column(db.JSON)  # Skills to develop
    timeline_estimate = db.Column(db.String(100))  # e.g., "6-12 months"

    # Alternative paths
    similar_paths = db.Column(db.JSON, default=list)  # Alternative recommendations
    comparison_insights = db.Column(db.Text)  # Why this over alternatives

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'rank': self.rank,
            'career_path': self.career_path,
            'alignment_score': self.alignment_score,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'strength_alignment': self.strength_alignment,
            'growth_opportunities': self.growth_opportunities,
            'beginner_projects': self.beginner_projects,
            'intermediate_projects': self.intermediate_projects,
            'learning_roadmap': self.learning_roadmap,
            'skill_gap_analysis': self.skill_gap_analysis,
            'timeline_estimate': self.timeline_estimate,
            'similar_paths': self.similar_paths,
            'comparison_insights': self.comparison_insights
        }


class ChatMessage(db.Model):
    """Conversational history with chatbot."""
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Message metadata
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20))  # 'positive', 'negative', 'neutral'
    intent = db.Column(db.String(100))  # Detected intent

    # Context
    recommendation_context = db.Column(db.String(100))  # Which path being discussed
    confidence_indicator = db.Column(db.String(20))  # 'confident', 'uncertain', 'exploring'

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'sender': self.sender,
            'content': self.content,
            'sentiment': self.sentiment,
            'intent': self.intent,
            'created_at': self.created_at.isoformat()
        }


class PredefinedPath(db.Model):
    """Predefined career paths with detailed information."""
    __tablename__ = 'predefined_paths'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    # Path characteristics
    required_skills = db.Column(db.JSON)  # {'coding': 0.3, 'math': 0.2, ...}
    related_domains = db.Column(db.JSON)  # ['AI', 'Web', ...]
    ideal_traits = db.Column(db.JSON)  # Personality/trait fit
    salary_range = db.Column(db.String(100))
    market_demand = db.Column(db.String(50))  # 'high', 'medium', 'emerging'

    # Detailed roadmap
    beginner_skills = db.Column(db.JSON)  # First things to learn
    intermediate_skills = db.Column(db.JSON)
    advanced_skills = db.Column(db.JSON)

    job_titles = db.Column(db.JSON)  # Related job titles
    companies = db.Column(db.JSON)  # Example companies
    growth_trajectory = db.Column(db.Text)  # Career progression

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SkillPath(db.Model):
    """Individual skill components and learning paths."""
    __tablename__ = 'skill_paths'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(50))  # 'technical', 'soft', 'domain'

    progression_steps = db.Column(db.JSON)  # ['Beginner', 'Intermediate', 'Advanced', 'Expert']
    resources = db.Column(db.JSON)  # Learning resources
    estimated_time = db.Column(db.String(100))  # Time to master
    difficulty = db.Column(db.Integer)  # 1-5
