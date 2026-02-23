/**
 * Dashboard Page
 * Main hub after authentication - contains nav, questionnaire, recommendations, chatbot
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import Questionnaire from '../components/Questionnaire';
import RecommendationsView from '../components/RecommendationsView';
import ChatBot from '../components/ChatBot';
import Navigation from '../components/Navigation';
import '../styles/dashboard.css';

const Dashboard = () => {
  const { user, profile } = useAuth();
  const [currentView, setCurrentView] = useState('questionnaire'); // questionnaire, recommendations, chat
  const [recommendations, setRecommendations] = useState(null);

  const handleQuestionnaireComplete = (recs) => {
    console.log('[Dashboard] Questionnaire completed with recommendations:', recs);
    if (!recs || recs.length === 0) {
      console.error('[Dashboard] ERROR: Recommendations array is empty or null!');
      return;
    }
    console.log('[Dashboard] Setting recommendations state and changing view to recommendations');
    setRecommendations(recs);
    setCurrentView('recommendations');
    console.log('[Dashboard] State updated - view should now show recommendations');
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
          {currentView === 'questionnaire' && (
            <Questionnaire onComplete={handleQuestionnaireComplete} />
          )}

          {currentView === 'recommendations' && recommendations && (
            <RecommendationsView
              recommendations={recommendations}
              profile={profile}
              onBack={handleRetakeAssessment}
            />
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
