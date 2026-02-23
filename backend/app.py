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

# Load environment variables reliably whether app is run from project root or backend folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))
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
print(f"[INFO] Chatbot LLM key linked: {bool(chatbot.groq_api_key)} | model: {chatbot.groq_model}")

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

        # Generate token (store identity as string to ensure JWT 'sub' is a string)
        access_token = create_access_token(identity=str(user.id))

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

        # Create token (store identity as string to ensure JWT 'sub' is a string)
        access_token = create_access_token(identity=str(user.id))

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

def _pick_path_config(selected_skill: str, career_goal: str):
    """Best-effort match to an existing career path config."""
    selected = (selected_skill or '').strip().lower()
    goal = (career_goal or '').strip().lower()
    paths = recommendation_engine.CAREER_PATHS

    for name, cfg in paths.items():
        if name.lower() == selected:
            return name, cfg

    for name, cfg in paths.items():
        if selected and (selected in name.lower() or name.lower() in selected):
            return name, cfg

    for name, cfg in paths.items():
        if goal and (name.lower() in goal or any(d.lower() in goal for d in cfg.get('related_domains', []))):
            return name, cfg

    return None, None


def _phase_duration_strings(skill_level: int, experience_level: int, study_time: int):
    """Generate realistic phase durations from user baseline and weekly hours."""
    readiness = (skill_level + experience_level) / 2.0
    if readiness <= 2:
        total_weeks = 28
    elif readiness <= 3.5:
        total_weeks = 22
    else:
        total_weeks = 16

    if study_time <= 4:
        total_weeks += 6
    elif study_time <= 8:
        total_weeks += 3
    elif study_time >= 15:
        total_weeks -= 3

    total_weeks = max(10, total_weeks)
    beginner_weeks = max(4, int(round(total_weeks * 0.35)))
    intermediate_weeks = max(4, int(round(total_weeks * 0.40)))
    advanced_weeks = max(3, total_weeks - beginner_weeks - intermediate_weeks)

    return {
        'beginner': f'{beginner_weeks} weeks',
        'intermediate': f'{intermediate_weeks} weeks',
        'advanced': f'{advanced_weeks} weeks'
    }


def _build_weekly_plan(study_time: int):
    """Create a simple weekly structure based on available hours."""
    study_time = max(3, int(study_time))
    theory = max(1, int(round(study_time * 0.40)))
    practice = max(1, int(round(study_time * 0.35)))
    project = max(1, study_time - theory - practice)

    return [
        f'Monday-Tuesday ({theory}h): Learn concepts and take concise notes.',
        f'Wednesday-Thursday ({practice}h): Hands-on exercises and coding challenges.',
        f'Friday-Saturday ({project}h): Build project features and document progress.',
        'Sunday (30-60 min): Weekly review, retrospective, and next-week planning.'
    ]


def _career_readiness_label(skill_level: int, experience_level: int):
    score = (skill_level * 0.45) + (experience_level * 0.55)
    if score >= 4.2:
        return 'High - interview ready with a strong portfolio'
    if score >= 3.2:
        return 'Medium - close to ready with consistent project execution'
    if score >= 2.2:
        return 'Developing - focus on fundamentals and practical depth'
    return 'Early stage - build core skills before specialization'


def _normalize_text_list(value):
    """Normalize list-like input into a lowercase list of tokens."""
    if not value:
        return []
    if isinstance(value, list):
        return [str(v).strip().lower() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [s.strip().lower() for s in value.replace(';', ',').split(',') if s.strip()]
    return [str(value).strip().lower()]


def _to_skill_profile(skill_scores: dict):
    """Map incoming skill score keys to engine profile keys."""
    scores = skill_scores or {}
    return {
        'coding_proficiency': int(scores.get('coding', scores.get('coding_proficiency', 3)) or 3),
        'math_comfort': int(scores.get('math', scores.get('math_comfort', 3)) or 3),
        'creativity': int(scores.get('creativity', 3) or 3),
        'communication_skill': int(scores.get('communication', scores.get('communication_skill', 3)) or 3),
        'domain_expertise': int(scores.get('domain', scores.get('domain_expertise', 2)) or 2),
        'leadership_potential': int(scores.get('leadership', scores.get('leadership_potential', 3)) or 3)
    }


def _clamp_profile_scores(profile_dict):
    for k in ['coding_proficiency', 'math_comfort', 'creativity', 'communication_skill', 'domain_expertise', 'leadership_potential']:
        profile_dict[k] = max(1, min(5, int(profile_dict.get(k, 3))))
    return profile_dict

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

        # Debug: print what was received and the final profile used for recommendations
        try:
            print(f'[DEBUG] /api/recommendations request_data: {request_data}')
            print(f'[DEBUG] /api/recommendations profile_dict (merged): {profile_dict}')
        except Exception:
            pass

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


@app.route('/api/recommendations/advanced', methods=['POST'])
@jwt_required()
def advanced_recommendations():
    """Advanced recommendation output using assessment + resume extracted details."""
    try:
        data = request.get_json() or {}

        # Assessment inputs
        skill_scores = data.get('skill_scores') or {}
        preferred_domains = data.get('preferred_domains') or []
        career_goal = data.get('career_goal')
        confidence_level = int(data.get('confidence_level', 2) or 2)
        experience_level = int(data.get('experience_level', 2) or 2)

        # Resume extracted inputs
        resume_skills = _normalize_text_list(data.get('resume_skills'))
        resume_projects = _normalize_text_list(data.get('resume_projects'))
        resume_tools = _normalize_text_list(data.get('resume_tools'))
        resume_certifications = _normalize_text_list(data.get('resume_certifications'))

        # Normalize profile for the existing recommendation engine.
        base_profile = _to_skill_profile(skill_scores)
        profile = _clamp_profile_scores({
            **base_profile,
            'preferred_domains': preferred_domains if isinstance(preferred_domains, list) else _normalize_text_list(preferred_domains),
            'career_goal': career_goal,
            'confidence_level': max(1, min(5, confidence_level)),
            'project_experience_level': max(1, min(5, experience_level)),
            'skills': {
                'coding': base_profile['coding_proficiency'],
                'math': base_profile['math_comfort'],
                'creativity': base_profile['creativity'],
                'communication': base_profile['communication_skill'],
                'domain_expertise': base_profile['domain_expertise']
            }
        })

        recs = recommendation_engine.get_recommendations(profile)
        if not recs:
            return jsonify({'success': False, 'error': 'Could not generate recommendations'}), 500

        top3 = recs[:3]
        top_careers = [
            {'career': r.get('career_path', ''), 'alignment_score': int(round(float(r.get('alignment_score', 0))))}
            for r in top3
        ]
        best = top3[0]
        best_path = best.get('career_path')
        best_cfg = recommendation_engine.CAREER_PATHS.get(best_path, {})

        # Strongest competencies from assessment + resume overlap.
        score_label_map = {
            'coding_proficiency': 'coding',
            'math_comfort': 'math',
            'creativity': 'creativity',
            'communication_skill': 'communication',
            'domain_expertise': 'domain'
        }
        sorted_scores = sorted(
            [(score_label_map[k], v) for k, v in base_profile.items() if k in score_label_map],
            key=lambda x: x[1],
            reverse=True
        )
        strongest_skills = []
        for name, level in sorted_scores:
            marker = 'resume-validated' if name in resume_skills else 'assessment-strong'
            strongest_skills.append(f"{name} ({level}/5, {marker})")
        strongest_skills = strongest_skills[:4]

        # Skill gaps based on top path requirements.
        required = list((best_cfg.get('required_skills') or {}).keys())
        alias = {'communication': 'communication_skill', 'math': 'math_comfort', 'coding': 'coding_proficiency', 'domain': 'domain_expertise'}
        skill_gaps = []
        for req in required:
            key = alias.get(req, req)
            level = int(base_profile.get(key, 2))
            present_in_resume = req in resume_skills
            if level < 3 or not present_in_resume:
                gap_reason = []
                if level < 3:
                    gap_reason.append(f'current level {level}/5')
                if not present_in_resume:
                    gap_reason.append('not evidenced in resume')
                skill_gaps.append(f"{req}: {', '.join(gap_reason)}")
        if not skill_gaps:
            skill_gaps = ['No major foundational gaps; focus on deeper project depth and specialization.']

        # Assessment-resume consistency and AI confidence.
        assessed_present = set([name for name, level in sorted_scores if level >= 3])
        resume_present = set(resume_skills)
        overlap = len(assessed_present & resume_present)
        denom = max(1, len(assessed_present))
        consistency_pct = int(round((overlap / denom) * 100))
        completeness_checks = [
            bool(skill_scores),
            bool(preferred_domains),
            bool(career_goal),
            bool(resume_skills),
            bool(resume_projects or resume_tools or resume_certifications)
        ]
        completeness_pct = int(round((sum(1 for c in completeness_checks if c) / len(completeness_checks)) * 100))
        top_alignment = int(round(float(best.get('alignment_score', 0))))
        ai_confidence_score = int(round((0.45 * top_alignment) + (0.30 * consistency_pct) + (0.25 * completeness_pct)))
        ai_confidence_score = max(0, min(100, ai_confidence_score))

        why_this_career = (
            f"{best_path} fits because your profile aligns at {top_alignment}% with required competencies, "
            f"your strongest areas are {', '.join([s.split(' (')[0] for s in strongest_skills[:3]])}, "
            "and the path matches your stated goals and domain preferences."
        )

        roadmap_steps = list(best_cfg.get('learning_roadmap', []))
        beginner = roadmap_steps[:2] or ['Build fundamentals', 'Practice core workflows']
        intermediate = roadmap_steps[2:4] or ['Apply concepts in projects', 'Improve quality and testing']
        advanced = roadmap_steps[4:] or ['Ship production-grade capstone', 'Prepare portfolio and interviews']

        improvement_suggestions = [
            'Close top 2 skill gaps with weekly focused practice blocks.',
            'Convert resume skills into measurable project outcomes (metrics, impact, scale).',
            'Add one portfolio project per phase with README, architecture notes, and demo.',
            'Target interviews with roles aligned to your top recommended career path.'
        ]

        market_demand = (best_cfg.get('market_demand') or 'stable').lower()
        if market_demand == 'high':
            market_trend = 'High demand trend: strong hiring momentum and broad role availability.'
        elif market_demand in ['growing', 'emerging']:
            market_trend = 'Growing trend: rising demand with increasing opportunities over the next 12-24 months.'
        else:
            market_trend = 'Stable trend: consistent opportunities, with advantage for specialized portfolios.'

        response = {
            "ai_confidence_score": ai_confidence_score,
            "top_careers": top_careers,
            "strongest_skills": strongest_skills,
            "skill_gaps": skill_gaps,
            "why_this_career": why_this_career,
            "improvement_suggestions": improvement_suggestions,
            "roadmap": {
                "beginner": beginner,
                "intermediate": intermediate,
                "advanced": advanced
            },
            "estimated_timeline": best.get('timeline_estimate', '6-12 months'),
            "market_trend": market_trend
        }

        return jsonify(response), 200

    except Exception as e:
        print(f'[ERROR] advanced_recommendations exception: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# CHATBOT ROUTES
# ============================================================



@app.route('/api/learning-roadmap', methods=['POST'])
@jwt_required()
def generate_learning_roadmap():
    """Generate a structured 3-phase learning roadmap and project plan."""
    try:
        data = request.get_json() or {}

        selected_skill = (data.get('selected_skill') or data.get('career') or '').strip()
        skill_level = int(data.get('skill_level', 1))
        experience_level = int(data.get('experience_level', 1))
        study_time = int(data.get('study_time', 6))
        career_goal = (data.get('career_goal') or '').strip()

        generic_terms = {'job', 'career', 'work', 'employment'}
        if not selected_skill or selected_skill.lower() in generic_terms:
            return jsonify({
                'success': False,
                'error': 'selected_skill must be a specific career path (e.g., AI Engineer, Data Analyst).'
            }), 400

        skill_level = max(1, min(5, skill_level))
        experience_level = max(1, min(5, experience_level))
        study_time = max(1, min(40, study_time))

        path_name, cfg = _pick_path_config(selected_skill, career_goal)

        if cfg:
            roadmap_steps = cfg.get('learning_roadmap', [])
            beginner_skills = roadmap_steps[:2] or ['Core fundamentals', 'Essential tooling']
            intermediate_skills = roadmap_steps[2:4] or ['Applied workflows', 'Project architecture']
            advanced_skills = roadmap_steps[4:] or ['Production practices', 'Leadership and scaling']

            importance = (
                f"{path_name} is important because it has {cfg.get('market_demand', 'strong')} market demand, "
                f"translates directly into real products, and opens paths such as {', '.join(cfg.get('job_titles', [])[:3])}."
            )
            tools_required = list(dict.fromkeys(
                ['Git/GitHub', 'VS Code', 'Documentation and note-taking tools'] +
                cfg.get('related_domains', []) +
                [path_name]
            ))
            career_opportunities = cfg.get('job_titles', [])[:5]
            beginner_project_titles = cfg.get('beginner_projects', [])[:3]
            intermediate_project_titles = cfg.get('intermediate_projects', [])[:3]
        else:
            path_name = selected_skill
            beginner_skills = ['Foundational concepts', 'Core tools and setup']
            intermediate_skills = ['Applied techniques', 'Systematic problem-solving']
            advanced_skills = ['Scalable architecture', 'Portfolio polish and specialization']
            importance = (
                f"{selected_skill} is important because it improves problem-solving, boosts employability, "
                "and creates opportunities to build impactful products."
            )
            tools_required = ['Git/GitHub', 'VS Code', 'Roadmap.sh', 'Kaggle/Udemy/Coursera', 'Portfolio site']
            career_opportunities = ['Junior Specialist', 'Associate Engineer', 'Analyst', 'Consultant', 'Freelancer']
            beginner_project_titles = [
                f'{selected_skill} starter challenge app',
                f'Interactive {selected_skill} mini dashboard',
                f'{selected_skill} automation utility'
            ]
            intermediate_project_titles = [
                f'{selected_skill} workflow manager',
                f'Real-time {selected_skill} tracker',
                f'{selected_skill} collaboration platform'
            ]

        durations = _phase_duration_strings(skill_level, experience_level, study_time)

        # Add top career recommendations based on current skill profile.
        rec_profile = {
            'coding_proficiency': skill_level,
            'math_comfort': skill_level,
            'creativity': skill_level,
            'communication_skill': max(1, min(5, round((skill_level + experience_level) / 2))),
            'domain_expertise': max(1, min(5, experience_level)),
            'project_experience_level': experience_level,
            'confidence_level': max(1, min(5, round((skill_level + experience_level) / 2))),
            'career_goal': career_goal or 'job',
            'preferred_domains': cfg.get('related_domains', []) if cfg else []
        }
        recs = recommendation_engine.get_recommendations(rec_profile)[:3]
        recommended_careers = [
            {
                'career': r.get('career_path'),
                'alignment_score': int(round(float(r.get('alignment_score', 0))))
            }
            for r in recs
        ]

        response = {
            'career': path_name,
            'importance': importance,
            'roadmap': {
                'beginner': {
                    'duration': durations['beginner'],
                    'skills': beginner_skills,
                    'concepts': [
                        'Terminology and foundational mental models',
                        'Core workflows and best practices',
                        'How to break big problems into small tasks'
                    ],
                    'exercises': [
                        'Complete daily focused drills (30-45 minutes).',
                        'Rebuild one tutorial project from scratch without copying.',
                        'Write short summaries after each learning session.'
                    ]
                },
                'intermediate': {
                    'duration': durations['intermediate'],
                    'skills': intermediate_skills,
                    'concepts': [
                        'Design patterns and tradeoffs',
                        'Debugging, testing, and quality control',
                        'Performance, reliability, and maintainability'
                    ],
                    'exercises': [
                        'Build reusable modules/components.',
                        'Add tests, logs, and validation to existing projects.',
                        'Refactor one project for readability and scalability.'
                    ]
                },
                'advanced': {
                    'duration': durations['advanced'],
                    'skills': advanced_skills,
                    'concepts': [
                        'System design and production readiness',
                        'Security, monitoring, and deployment strategy',
                        'Mentorship, communication, and impact storytelling'
                    ],
                    'exercises': [
                        'Design and build an end-to-end capstone project.',
                        'Perform code reviews and architecture walkthroughs.',
                        'Prepare a portfolio case study with measurable outcomes.'
                    ]
                }
            },
            'projects': {
                'beginner': beginner_project_titles,
                'intermediate': intermediate_project_titles,
                'advanced': [
                    f'Capstone 1: Production-grade {path_name} solution with documentation and deployment',
                    f'Capstone 2: Real-world {path_name} project integrated with analytics, testing, and CI/CD'
                ]
            },
            'tools_required': tools_required,
            'weekly_plan': _build_weekly_plan(study_time),
            'milestones': [
                'Milestone 1: Complete beginner phase exercises and 3 beginner projects.',
                'Milestone 2: Ship 3 intermediate projects with testing and documentation.',
                'Milestone 3: Deliver 2 advanced capstones and portfolio-ready case studies.'
            ],
            'career_opportunities': career_opportunities,
            'career_readiness_level': _career_readiness_label(skill_level, experience_level),
            'recommended_careers': recommended_careers
        }

        return jsonify({'success': True, 'roadmap_plan': response}), 200

    except Exception as e:
        print(f'[ERROR] generate_learning_roadmap exception: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500
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
            'guidance_type': response['guidance_type'],
            'llm_used': response.get('llm_used', False),
            'llm_error': response.get('llm_error')
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

