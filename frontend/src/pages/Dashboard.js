/**
 * Dashboard Page
 * Main hub after authentication - contains nav, questionnaire, recommendations, chatbot
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import Questionnaire from '../components/Questionnaire';
import RecommendationsView from '../components/RecommendationsView';
import ChatBot from '../components/ChatBot';
import Navigation from '../components/Navigation';
import '../styles/dashboard.css';
import ProfilePage from './ProfilePage';
import RoadmapPage from './RoadmapPage';

const Dashboard = () => {
  const { user, profile } = useAuth();
  const [currentView, setCurrentView] = useState('questionnaire'); // questionnaire, recommendations, chat
  const [recommendations, setRecommendations] = useState(null);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const apiService = require('../services/api').default;

  // When user navigates to recommendations, auto-generate based on latest profile
  useEffect(() => {
    const fetchRecs = async () => {
      if (currentView !== 'recommendations') return;
      if (recommendations && recommendations.length > 0) return;
      if (!profile) return;

      try {
        setLoadingRecs(true);
        const res = await apiService.getRecommendations(profile);
        if (res.data && res.data.success) {
          const augmented = augmentRecommendations(res.data.recommendations || []);
          setRecommendations(augmented);
        } else {
          console.warn('No recommendations returned', res.data);
        }
      } catch (err) {
        console.error('Failed to fetch recommendations', err);
      } finally {
        setLoadingRecs(false);
      }
    };

    fetchRecs();
  }, [currentView, profile]);

  const handleQuestionnaireComplete = (recs) => {
    console.log('[Dashboard] Questionnaire completed with recommendations:', recs);
    if (!recs || recs.length === 0) {
      console.error('[Dashboard] ERROR: Recommendations array is empty or null!');
      return;
    }
    const augmented = augmentRecommendations(recs);
    console.log('[Dashboard] Setting recommendations state and changing view to recommendations');
    setRecommendations(augmented);
    setCurrentView('recommendations');
    console.log('[Dashboard] State updated - view should now show recommendations');
  };

  // Helper: augment a raw recommendations array with a skill_gap object (reused for testing)
  const augmentRecommendations = (recs) => {
    const normalizeList = (input) => {
      if (!input) return [];
      if (Array.isArray(input)) return input.map(s => String(s).trim().toLowerCase()).filter(Boolean);
      return String(input)
        .split(/[,;|]/)
        .map(s => s.trim().toLowerCase())
        .filter(Boolean);
    };

    const userSkills = normalizeList(profile && profile.skills ? profile.skills : '');

    return recs.map(rec => {
      const careerName = rec.career_path || rec.title || rec.name || 'Target Career';
      const required = normalizeList(rec.required_skills || rec.requiredSkills || rec.required || rec.skills_required || '');
      const matched = required.filter(r => userSkills.includes(r));
      const missing = required.filter(r => !matched.includes(r));
      const fitScore = required.length === 0 ? (typeof rec.alignment_score === 'number' ? Math.round(rec.alignment_score) : 0) : Math.round((matched.length / required.length) * 100);

      const why = `You have ${matched.length} of the key skills for ${careerName}. With focused upskilling in the missing areas you can convert your programming foundation into career-ready capability.`;

      const learning_roadmap = [
        'Study core fundamentals for the missing skills with short courses and weekly practice.',
        'Build 2–3 small projects that apply the new skills and publish them on GitHub.',
        'Create a polished portfolio case study and practice explaining your work in interviews.'
      ];

      return {
        ...rec,
        skill_gap: {
          career: careerName,
          fit_score: fitScore,
          matched,
          missing,
          why,
          learning_roadmap
        }
      };
    });
  };

  // Development helper to load sample recommendations for testing UI
  const loadSampleRecommendations = () => {
    const careerNames = [
      'Cybersecurity Analyst',
      'Cloud Engineer',
      'DevOps Engineer',
      'Machine Learning Engineer',
      'Full Stack Developer',
      'Data Analyst',
      'UI/UX Designer',
      'Blockchain Developer',
      'Mobile App Developer',
      'Software Engineer'
    ];

    const sample = careerNames.map((name, i) => ({
      rank: i + 1,
      career_path: name,
      alignment_score: Math.max(40, 90 - i * 4),
      confidence: i % 3 === 0 ? 'High' : i % 3 === 1 ? 'Medium' : 'Moderate',
      reasoning: `Sample reasoning for ${name}.`,
      strength_alignment: { skills: ['Existing skill A', 'Existing skill B'] },
      growth_opportunities: ['Skill X', 'Skill Y'],
      beginner_projects: ['Starter project 1', 'Starter project 2'],
      learning_roadmap: ['Step 1', 'Step 2', 'Step 3'],
      required_skills: ''
    }));

    const augmented = augmentRecommendations(sample);
    setRecommendations(augmented);
    setCurrentView('recommendations');
  };

  const handleRetakeAssessment = () => {
    setRecommendations(null);
    setCurrentView('questionnaire');
  };

  return (
    <div className="dashboard-container">
      {/* Navigation */}
      <Navigation user={user} currentView={currentView} setCurrentView={setCurrentView} />

      {/* Main Content */}
      <main className="dashboard-main">
        <motion.div
          key={currentView}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          <div style={{display:'flex', gap:8, marginBottom:12}}>
            <button className="btn btn-secondary" onClick={() => setCurrentView('questionnaire')}>Assessment</button>
            <button className="btn btn-secondary" onClick={() => setCurrentView('recommendations')}>Recommendations</button>
            <button className="btn btn-secondary" onClick={() => setCurrentView('roadmap')}>Roadmap</button>
            <button className="btn btn-outline" onClick={loadSampleRecommendations}>Load sample recommendations</button>
          </div>
          {currentView === 'questionnaire' && (
            <Questionnaire onComplete={handleQuestionnaireComplete} />
          )}

          {currentView === 'recommendations' && (
            loadingRecs ? (
              <div>Loading recommendations...</div>
            ) : recommendations && recommendations.length > 0 ? (
              <RecommendationsView
                recommendations={recommendations}
                profile={profile}
                onBack={handleRetakeAssessment}
              />
            ) : (
              <div>No recommendations available. Try taking the assessment or click "Load sample recommendations".</div>
            )
          )}

          {currentView === 'profile' && (
            <ProfilePage profile={profile} />
          )}

          {currentView === 'roadmap' && (
            <RoadmapPage profile={profile} />
          )}

          {currentView === 'chat' && (
            <ChatBot recommendations={recommendations} />
          )}
        </motion.div>
      </main>
    </div>
  );
};

export default Dashboard;
