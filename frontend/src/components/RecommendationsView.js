/**
 * Recommendations View Component
 * Displays career recommendations with details and visualizations
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import RecommendationCard from './RecommendationCard';
import '../styles/recommendations.css';

const RecommendationsView = ({ recommendations, profile, onBack }) => {
  const [expandedCard, setExpandedCard] = useState(0);

  return (
    <div className="recommendations-container">
      {/* Header */}
      <motion.div
        className="recommendations-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1>🎯 Your Career Recommendations</h1>
        <p className="subtitle">
          Based on your skills, interests, and goals. Here are your top matching paths.
        </p>
      </motion.div>

      {/* Cards Grid */}
      <div className="recommendations-grid">
        {recommendations.map((rec, idx) => (
          <RecommendationCard
            key={idx}
            recommendation={rec}
            isExpanded={expandedCard === idx}
            onToggle={() =>
              setExpandedCard(expandedCard === idx ? -1 : idx)
            }
          />
        ))}
      </div>

      {/* Back Button */}
      <motion.button
        className="btn btn-secondary"
        onClick={onBack}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        ← Retake Assessment
      </motion.button>
    </div>
  );
};

export default RecommendationsView;
