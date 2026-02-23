/**
 * Recommendation Card Component
 * Individual career path recommendation card with expandable details
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import apiService from '../services/api';

const RecommendationCard = ({ recommendation, isExpanded, onToggle, profile }) => {
  const getConfidenceColor = (confidence) => {
    switch (confidence) {
      case 'High':
        return '#10b981';
      case 'Medium':
        return '#f59e0b';
      case 'Moderate':
        return '#3b82f6';
      default:
        return '#6b7280';
    }
  };

  const [remoteSkillGap, setRemoteSkillGap] = useState(null);
  const [loadingSkillGap, setLoadingSkillGap] = useState(false);
  const [skillGapError, setSkillGapError] = useState(null);

  const fetchRemoteSkillGap = async (e) => {
    e && e.stopPropagation();
    setSkillGapError(null);
    setLoadingSkillGap(true);
    try {
      const userSkills = (profile && (profile.skills || profile.preferred_domains)) || [];
      const payload = {
        user_skills: userSkills,
        career_name: recommendation.career_path,
        required_skills: recommendation.required_skills || recommendation.requiredSkills || ''
      };

      const res = await apiService.skillGap(payload);
      setRemoteSkillGap(res.data.skill_gap || null);
    } catch (err) {
      setSkillGapError(err?.response?.data?.error || err.message || 'Failed to compute skill gap');
    } finally {
      setLoadingSkillGap(false);
    }
  };

  return (
    <motion.div
      className={`recommendation-card ${isExpanded ? 'expanded' : ''}`}
      onClick={onToggle}
      layoutId={`card-${recommendation.rank}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: recommendation.rank * 0.1 }}
    >
      {/* Header */}
      <div className="card-header">
        <div className="card-title">
          <span className="rank-badge">#{recommendation.rank}</span>
          <h3>{recommendation.career_path}</h3>
        </div>
        <div className="confidence-badge" style={{ backgroundColor: getConfidenceColor(recommendation.confidence) }}>
          {recommendation.confidence}
        </div>
      </div>

      {/* Score Bar */}
      <div className="score-section">
        <div className="score-bar-bg">
          <motion.div
            className="score-bar-fill"
            layoutId={`score-${recommendation.rank}`}
            initial={{ width: 0 }}
            animate={{ width: `${recommendation.alignment_score}%` }}
            transition={{ duration: 0.8, delay: 0.2 }}
          />
        </div>
        <p className="score-text">{recommendation.alignment_score}% Alignment</p>
      </div>

      {/* Brief Info */}
      <p className="card-description">{recommendation.description || 'An exciting career path'}</p>

      {/* Expandable Details */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            className="card-details"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* Reasoning */}
            <div className="detail-section">
              <h4>💡 Why This Path?</h4>
              <p>{recommendation.reasoning}</p>
            </div>

            {/* Strengths */}
            {recommendation.strength_alignment && Array.isArray(recommendation.strength_alignment.skills) && recommendation.strength_alignment.skills.length > 0 && (
              <div className="detail-section">
                <h4>✨ Your Strengths</h4>
                <ul>
                  {recommendation.strength_alignment.skills.map((skill, idx) => (
                    <li key={idx}>{skill}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Growth Areas */}
            {recommendation.growth_opportunities && Array.isArray(recommendation.growth_opportunities) && recommendation.growth_opportunities.length > 0 && (
              <div className="detail-section">
                <h4>🌱 Areas to Develop</h4>
                <ul>
                  {recommendation.growth_opportunities.map((area, idx) => (
                    <li key={idx}>{area}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Skill Gap Analysis (optional) */}
            {recommendation.skill_gap && (
              <div className="detail-section">
                <h4>📊 Skill Gap Analysis</h4>
                <p><strong>Career:</strong> {recommendation.skill_gap.career || recommendation.career_path}</p>
                <p><strong>Fit Score:</strong> {typeof recommendation.skill_gap.fit_score !== 'undefined' ? `${recommendation.skill_gap.fit_score}%` : `${recommendation.alignment_score}%`}</p>
                <p><strong>Matched Skills:</strong> {recommendation.skill_gap.matched && recommendation.skill_gap.matched.length > 0 ? recommendation.skill_gap.matched.join(', ') : 'None identified'}</p>
                <p><strong>Missing Skills:</strong> {recommendation.skill_gap.missing && recommendation.skill_gap.missing.length > 0 ? recommendation.skill_gap.missing.join(', ') : 'None identified'}</p>
                {recommendation.skill_gap.why && (
                  <div style={{marginTop:8}}>
                    <h5>Why This Career Suits You</h5>
                    <p>{recommendation.skill_gap.why}</p>
                  </div>
                )}

                {recommendation.skill_gap.learning_roadmap && Array.isArray(recommendation.skill_gap.learning_roadmap) && recommendation.skill_gap.learning_roadmap.length > 0 && (
                  <div style={{marginTop:8}}>
                    <h5>Learning Roadmap</h5>
                    <ol>
                      {recommendation.skill_gap.learning_roadmap.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))}
                    </ol>
                  </div>
                )}
                <div style={{marginTop:10}}>
                  <button className="btn btn-primary" onClick={fetchRemoteSkillGap}>
                    {loadingSkillGap ? 'Computing...' : 'Compute Skill Gap (server)'}
                  </button>
                  {skillGapError && <p style={{color:'var(--danger)', marginTop:8}}>{skillGapError}</p>}
                  {remoteSkillGap && (
                    <div style={{marginTop:12}}>
                      <h5>Server Analysis</h5>
                      <p><strong>Fit Score:</strong> {remoteSkillGap.fit_score}%</p>
                      <p><strong>Matched:</strong> {remoteSkillGap.matched && remoteSkillGap.matched.length ? remoteSkillGap.matched.join(', ') : 'None'}</p>
                      <p><strong>Missing:</strong> {remoteSkillGap.missing && remoteSkillGap.missing.length ? remoteSkillGap.missing.join(', ') : 'None'}</p>
                      {remoteSkillGap.learning_roadmap && (
                        <div>
                          <h6>Roadmap</h6>
                          <ol>
                            {remoteSkillGap.learning_roadmap.map((s, i) => <li key={i}>{s}</li>)}
                          </ol>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Projects */}
            {recommendation.beginner_projects && Array.isArray(recommendation.beginner_projects) && recommendation.beginner_projects.length > 0 && (
              <div className="detail-section">
                <h4>💻 Starter Projects</h4>
                <ul>
                  {recommendation.beginner_projects.map((project, idx) => (
                    <li key={idx}>{project}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Roadmap */}
            {recommendation.learning_roadmap && Array.isArray(recommendation.learning_roadmap) && recommendation.learning_roadmap.length > 0 && (
              <div className="detail-section">
                <h4>📚 Learning Path</h4>
                <ol>
                  {recommendation.learning_roadmap.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
              </div>
            )}

            {/* Additional Info */}
            <div className="detail-footer">
              {recommendation.salary_range && (
                <div className="info-chip">
                  <span>💼</span> {recommendation.salary_range}
                </div>
              )}
              {recommendation.market_demand && (
                <div className="info-chip">
                  <span>🚀</span> {recommendation.market_demand}
                </div>
              )}
              {recommendation.timeline_estimate && (
                <div className="info-chip">
                  <span>⏱️</span> {recommendation.timeline_estimate}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Expand Icon */}
      <div className="expand-icon">
        {isExpanded ? '▲' : '▼'}
      </div>
    </motion.div>
  );
};

export default RecommendationCard;
