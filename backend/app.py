"""
Advanced Flask Backend API - Production Grade
Authentication, recommendations, chatbot, and user management.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import nltk
from werkzeug.utils import secure_filename
from flask import send_file
from sqlalchemy import text
from models import db, User, UserProfile, Recommendation, ChatMessage, PredefinedPath, AssessmentHistory
from recommendation_engine import AdvancedRecommendationEngine
from chatbot import AdvancedChatbot

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///career_recommendation.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app, resources={r'/api/*': {'origins': ['http://localhost:3000', 'http://localhost:3001', 'http://127.0.0.1:3000', 'http://127.0.0.1:3001']}}, supports_credentials=True)


def ensure_resume_column():
    """Ensure resume_path column exists in user_profiles table."""
    database_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')

    # Only run for SQLite
    if not database_uri.startswith('sqlite'):
        return

    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Check existing columns
                result = conn.execute(text("PRAGMA table_info(user_profiles)"))
                columns = [row[1] for row in result]

                if 'resume_path' not in columns:
                    print('[INFO] Adding missing column resume_path')
                    conn.execute(text("ALTER TABLE user_profiles ADD COLUMN resume_path TEXT"))
                    conn.commit()

        except Exception as e:
            print(f'[WARN] Could not ensure resume_path column: {e}')

# Ensure the DB has expected columns (best-effort)
ensure_resume_column()

# Ensure app context for requests
@app.before_request
def ensure_context():
    """Ensure app context is available for each request."""
    pass

# Initialize AI engines
recommendation_engine = AdvancedRecommendationEngine()
chatbot = AdvancedChatbot()

# Download NLTK data if needed
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# ============================================================
# ERROR HANDLING
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Register new user account."""
    try:
        data = request.get_json()

        # Validation
        if not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        if len(data.get('password', '')) < 8:
            return jsonify({'success': False, 'error': 'Password must be at least 8 characters'}), 400

        # Check existing email
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already registered'}), 409

        # Create user
        user = User(
            email=data['email'],
            name=data['name']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Create initial profile
        profile = UserProfile(user_id=user.id)
        if data.get('skill_interest'):
            profile.preferred_domains = data.get('skill_interest', [])
        db.session.add(profile)
        db.session.commit()

        # Generate token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

        # Create token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Get latest profile
        profile = UserProfile.query.filter_by(user_id=user_id).order_by(UserProfile.created_at.desc()).first()

        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'profile': profile.to_dict() if profile else None
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (token invalidation handled by client)."""
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


# ============================================================
# QUESTIONNAIRE & PROFILE ROUTES
# ============================================================

@app.route('/api/profile/update', methods=['POST'])
@jwt_required()
def update_profile():
    """Update user skill profile."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        print(f'[INFO] Updating profile for user {user_id} with data: {data}')

        # Get or create profile
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            print(f'[INFO] Created new profile for user {user_id}')

        # Store previous values for history
        previous_values = {
            'coding': profile.coding_proficiency,
            'math': profile.math_comfort,
            'creativity': profile.creativity,
            'communication': profile.communication_skill
        }

        # Update fields
        if 'coding_proficiency' in data:
            profile.coding_proficiency = data['coding_proficiency']
        if 'math_comfort' in data:
            profile.math_comfort = data['math_comfort']
        if 'creativity' in data:
            profile.creativity = data['creativity']
        if 'communication_skill' in data:
            profile.communication_skill = data['communication_skill']
        if 'leadership_potential' in data:
            profile.leadership_potential = data['leadership_potential']
        if 'domain_expertise' in data:
            profile.domain_expertise = data['domain_expertise']

        # Update preferences
        if 'preferred_domains' in data:
            profile.preferred_domains = data['preferred_domains']
        if 'career_goal' in data:
            profile.career_goal = data['career_goal']
        if 'teamwork_preference' in data:
            profile.teamwork_preference = data['teamwork_preference']
        if 'project_experience_level' in data:
            profile.project_experience_level = data['project_experience_level']
        if 'work_environment' in data:
            profile.work_environment = data['work_environment']
        if 'primary_motivation' in data:
            profile.primary_motivation = data['primary_motivation']
        if 'key_concerns' in data:
            profile.key_concerns = data['key_concerns']
        if 'growth_areas' in data:
            profile.growth_areas = data['growth_areas']

        profile.completed = True
        profile.confidence_level = data.get('confidence_level', profile.confidence_level)

        db.session.add(profile)
        db.session.commit()

        print(f'[INFO] Profile updated successfully for user {user_id}: {profile.to_dict()}')

        # Track changes
        history = AssessmentHistory(
            profile_id=profile.id,
            previous_values=previous_values,
            new_values=profile.get_skill_summary(),
            changes_made=data
        )
        db.session.add(history)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Profile updated',
            'profile': profile.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f'[ERROR] Exception in update_profile: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile."""
    try:
        user_id = get_jwt_identity()
        profile = UserProfile.query.filter_by(user_id=user_id).order_by(UserProfile.created_at.desc()).first()

        if not profile:
            return jsonify({'success': False, 'error': 'Profile not found'}), 404

        return jsonify({
            'success': True,
            'profile': profile.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/upload_resume', methods=['POST'])
@jwt_required()
def upload_resume():
    """Upload a resume PDF for the current user. Expects multipart/form-data with 'resume' file."""
    try:
        user_id = get_jwt_identity()

        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No resume file provided'}), 400

        resume_file = request.files['resume']
        if resume_file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        filename = secure_filename(resume_file.filename)
        save_dir = os.path.join(app.root_path, 'instance', 'resumes')
        os.makedirs(save_dir, exist_ok=True)
        timestamp = int(datetime.utcnow().timestamp())
        save_path = os.path.join(save_dir, f"user_{user_id}_{timestamp}_{filename}")

        resume_file.save(save_path)

        # Save path to user's latest profile record
        profile = UserProfile.query.filter_by(user_id=user_id).order_by(UserProfile.created_at.desc()).first()
        if profile:
            # store relative path from app root for portability
            rel_path = os.path.relpath(save_path, app.root_path)
            profile.resume_path = rel_path
            db.session.add(profile)
            db.session.commit()

        return jsonify({'success': True, 'message': 'Resume uploaded', 'path': save_path}), 200

    except Exception as e:
        print(f'[ERROR] upload_resume exception: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/resume', methods=['GET'])
@jwt_required()
def download_resume():
    """Return the current user's uploaded resume file as an attachment."""
    try:
        user_id = get_jwt_identity()
        profile = UserProfile.query.filter_by(user_id=user_id).order_by(UserProfile.created_at.desc()).first()
        if not profile or not profile.resume_path:
            return jsonify({'success': False, 'error': 'No resume found for user'}), 404

        # Construct absolute path
        file_path = os.path.join(app.root_path, profile.resume_path)
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'Resume file not found on server'}), 404

        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path), mimetype='application/pdf')

    except Exception as e:
        print(f'[ERROR] download_resume exception: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# RECOMMENDATION ROUTES
# ============================================================

@app.route('/api/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    """Generate career recommendations for user."""
    try:
        user_id = get_jwt_identity()

        # Get user profile
        profile = UserProfile.query.filter_by(user_id=user_id).order_by(UserProfile.created_at.desc()).first()

        if not profile:
            print(f'[ERROR] No profile found for user {user_id}')
            return jsonify({'success': False, 'error': 'Update your profile first'}), 400

        # Convert stored profile to dict for engine
        profile_dict = profile.to_dict()

        # Prefer assessment data sent in the request body (immediate questionnaire result)
        try:
            request_data = request.get_json(silent=True) or {}
        except Exception:
            request_data = {}

        # Merge request data over stored profile so submitted assessment values take precedence
        if request_data:
            # Only copy known fields to avoid polluting the profile dict
            for k, v in request_data.items():
                if v is not None:
                    profile_dict[k] = v

        print(f'[INFO] Generating recommendations for user {user_id} with profile: {profile_dict}')

        # Generate recommendations using merged profile (assessment data overrides stored profile)
        recommendations = recommendation_engine.get_recommendations(profile_dict)

        # Validate recommendations
        if not recommendations or len(recommendations) == 0:
            print(f'[ERROR] No recommendations generated for user {user_id}')
            return jsonify({'success': False, 'error': 'Failed to generate recommendations. Please ensure your profile is complete.'}), 500

        print(f'[INFO] Generated {len(recommendations)} recommendations for user {user_id}')

        # Store recommendations in database
        Recommendation.query.filter_by(user_id=user_id).delete()

        for rec in recommendations:
            db_rec = Recommendation(
                user_id=user_id,
                profile_id=profile.id,
                rank=rec['rank'],
                career_path=rec['career_path'],
                alignment_score=rec['alignment_score'],
                confidence=rec['confidence'],
                reasoning=rec['reasoning'],
                strength_alignment=rec['strength_alignment'],
                growth_opportunities=rec['growth_opportunities'],
                beginner_projects=rec['beginner_projects'],
                intermediate_projects=rec['intermediate_projects'],
                learning_roadmap=rec['learning_roadmap'],
                skill_gap_analysis=rec['skill_gap_analysis'],
                timeline_estimate=rec['timeline_estimate'],
                similar_paths=rec['similar_paths']
            )
            db.session.add(db_rec)

        db.session.commit()
        print(f'[INFO] Successfully stored {len(recommendations)} recommendations for user {user_id}')

        return jsonify({
            'success': True,
            'recommendations': recommendations
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f'[ERROR] Exception in get_recommendations: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recommendations', methods=['GET'])
@jwt_required()
def fetch_recommendations():
    """Fetch stored recommendations."""
    try:
        user_id = get_jwt_identity()

        recommendations = Recommendation.query.filter_by(user_id=user_id).all()

        if not recommendations:
            return jsonify({'success': True, 'recommendations': []}), 200

        return jsonify({
            'success': True,
            'recommendations': [rec.to_dict() for rec in recommendations]
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recommendations/<path_name>/compare/<compare_with>', methods=['GET'])
@jwt_required()
def compare_recommendations(path_name, compare_with):
    """Compare two career paths."""
    try:
        user_id = get_jwt_identity()
        profile = UserProfile.query.filter_by(user_id=user_id).first()

        if not profile:
            return jsonify({'success': False, 'error': 'Profile not found'}), 404

        comparison = recommendation_engine.compare_paths(path_name, compare_with, profile.to_dict())

        return jsonify({
            'success': True,
            'comparison': comparison
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/skillgap', methods=['POST'])
@jwt_required()
def compute_skill_gap():
    """On-demand skill gap analysis endpoint.

    Request JSON: { user_skills: <list|string>, career_name: <string>, required_skills: <list|string> }
    """
    try:
        data = request.get_json() or {}
        user_id = get_jwt_identity()

        user_skills = data.get('user_skills')
        career_name = data.get('career_name') or data.get('career')
        required_skills = data.get('required_skills') or data.get('required')

        if not career_name:
            return jsonify({'success': False, 'error': 'career_name is required'}), 400

        analysis = recommendation_engine.compute_skill_gap(user_skills, career_name, required_skills)

        return jsonify({'success': True, 'skill_gap': analysis}), 200

    except Exception as e:
        print(f'[ERROR] compute_skill_gap exception: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# CHATBOT ROUTES
# ============================================================

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    """Chat with mentor bot."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        message = data.get('message', '').strip()

        if not message:
            return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400

        # Get user context
        user = User.query.get(user_id)
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        recommendations = Recommendation.query.filter_by(user_id=user_id).all()

        # Get previous messages
        previous_messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at.desc()).limit(5).all()

        # Get response from chatbot
        response = chatbot.get_response(
            message=message,
            user_id=str(user_id),
            user_profile=profile.to_dict() if profile else {},
            recommendations=[rec.to_dict() for rec in recommendations],
            message_history=[msg.to_dict() for msg in reversed(previous_messages)]
        )

        # Store messages
        user_msg = ChatMessage(
            user_id=user_id,
            sender='user',
            content=message,
            sentiment=response['sentiment'],
            intent=response['intent']
        )
        db.session.add(user_msg)

        bot_msg = ChatMessage(
            user_id=user_id,
            sender='bot',
            content=response['response'],
            sentiment=response['sentiment'],
            intent=response['intent']
        )
        db.session.add(bot_msg)
        db.session.commit()

        return jsonify({
            'success': True,
            'response': response['response'],
            'sentiment': response['sentiment'],
            'intent': response['intent'],
            'follow_up': response['follow_up'],
            'guidance_type': response['guidance_type']
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def chat_history():
    """Get chat history."""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)

        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at).limit(limit).all()

        return jsonify({
            'success': True,
            'messages': [msg.to_dict() for msg in messages]
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# INFO ROUTES
# ============================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check."""
    return jsonify({'status': 'healthy', 'message': 'Career Recommendation System v2.0'}), 200


@app.route('/api/career-paths', methods=['GET'])
def get_career_paths():
    """Get all available career paths."""
    try:
        paths = list(recommendation_engine.CAREER_PATHS.keys())
        return jsonify({
            'success': True,
            'career_paths': paths,
            'total': len(paths)
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/domains', methods=['GET'])
def get_domains():
    """Get all available domains."""
    try:
        domains = ['AI', 'Web', 'Cybersecurity', 'Data Science', 'UI/UX', 'Research']
        return jsonify({
            'success': True,
            'domains': domains
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# STARTUP
# ============================================================

# Initialize database tables on app startup
with app.app_context():
    try:
        db.create_all()
        print('[INFO] Database tables created/verified successfully')
    except Exception as e:
        print(f'[ERROR] Failed to create database tables: {str(e)}')

if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_ENV') != 'production',
        host='0.0.0.0',
        port=5000
    )
