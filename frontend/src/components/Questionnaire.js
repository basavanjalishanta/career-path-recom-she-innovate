/**
 * Questionnaire Component
 * Multi-step animated questionnaire for career assessment
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import apiService from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import '../styles/questionnaire.css';

const Questionnaire = ({ onComplete }) => {
  const { updateProfile } = useAuth();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Reset questionnaire when component mounts
  useEffect(() => {
    setStep(0);
    setError('');
    setLoading(false);
  }, []);

  const [formData, setFormData] = useState({
    coding_proficiency: 3,
    math_comfort: 3,
    creativity: 3,
    communication_skill: 3,
    leadership_potential: 3,
    domain_expertise: 2,
    preferred_domains: [],
    career_goal: 'job',
    teamwork_preference: true,
    project_experience_level: 2,
    work_environment: 'hybrid',
    primary_motivation: 'impact',
    key_concerns: [],
    confidence_level: 3,
    resume: null,
  });

  const questions = [
    {
      title: 'Coding Skills',
      description: 'How comfortable are you with programming?',
      type: 'slider',
      key: 'coding_proficiency',
      min: 1,
      max: 5,
      labels: ['Beginner', 'Basic', 'Intermediate', 'Advanced', 'Expert'],
    },
    {
      title: 'Math Comfort',
      description: 'How comfortable are you with mathematics?',
      type: 'slider',
      key: 'math_comfort',
      min: 1,
      max: 5,
      labels: ['Struggling', 'Basic', 'Intermediate', 'Comfortable', 'Expert'],
    },
    {
      title: 'Creativity',
      description: 'How creative do you consider yourself?',
      type: 'slider',
      key: 'creativity',
      min: 1,
      max: 5,
      labels: ['Not at all', 'Somewhat', 'Moderate', 'Very', 'Exceptional'],
    },
    {
      title: 'Communication',
      description: 'How would you rate your communication skills?',
      type: 'slider',
      key: 'communication_skill',
      min: 1,
      max: 5,
      labels: ['Needs improvement', 'Fair', 'Good', 'Very good', 'Excellent'],
    },
    {
      title: 'Interests & Domains',
      description: 'What domains interest you most? (Select multiple)',
      type: 'multi-select',
      key: 'preferred_domains',
      options: ['AI', 'Web', 'Cybersecurity', 'Data Science', 'UI/UX', 'Research'],
    },
    {
      title: 'Career Goal',
      description: 'What is your primary career objective?',
      type: 'select',
      key: 'career_goal',
      options: ['Job', 'Startup', 'Research'],
    },
    {
      title: 'Work Setup',
      description: 'What work environment do you prefer?',
      type: 'select',
      key: 'work_environment',
      options: ['Remote', 'Hybrid', 'Onsite'],
    },
    {
      title: 'Project Experience',
      description: 'How many projects have you completed?',
      type: 'slider',
      key: 'project_experience_level',
      min: 1,
      max: 5,
      labels: ['None', 'Few', 'Several', 'Many', 'Extensive'],
    },
    {
      title: 'Primary Motivation',
      description: 'What motivates you most?',
      type: 'select',
      key: 'primary_motivation',
      options: ['Impact', 'Learning', 'Stability', 'Wealth'],
    },
    {
      title: 'Confidence Level',
      description: 'How confident are you about your direction?',
      type: 'slider',
      key: 'confidence_level',
      min: 1,
      max: 5,
      labels: ['Very uncertain', 'Uncertain', 'Moderate', 'Confident', 'Very confident'],
    },
    {
      title: 'Upload Resume',
      description: 'Upload your resume (PDF) to include with your profile (optional).',
      type: 'file',
      key: 'resume',
      accept: 'application/pdf'
    }
  ];

  const currentQuestion = questions[step];
  const progress = ((step + 1) / questions.length) * 100;

  const handleSliderChange = (key, value) => {
    setFormData((prev) => ({
      ...prev,
      [key]: parseInt(value),
    }));
  };

  const handleSelectChange = (key, value) => {
    setFormData((prev) => ({
      ...prev,
      [key]: value.toLowerCase(),
    }));
  };

  const handleMultiSelect = (key, option) => {
    setFormData((prev) => ({
      ...prev,
      [key]: prev[key].includes(option)
        ? prev[key].filter((item) => item !== option)
        : [...prev[key], option],
    }));
  };

  const handleNext = () => {
    if (
      currentQuestion.type === 'multi-select' &&
      formData[currentQuestion.key].length === 0
    ) {
      setError('Please select at least one option');
      return;
    }
    setError('');
    if (step < questions.length - 1) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  };

  const handlePrevious = () => {
    setError('');
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      // Step 1: Update profile
      console.log('Updating profile with data:', formData);
      const profileResult = await updateProfile({
        ...formData,
        confidence_level: formData.confidence_level,
      });

      if (!profileResult.success) {
        const errorMsg = profileResult.error || 'Failed to update profile';
        console.error('Profile update error:', errorMsg);
        setError(errorMsg);
        setLoading(false);
        return;
      }

      console.log('Profile updated successfully:', profileResult.profile);

      // Step 2: Get recommendations
      console.log('Fetching recommendations...');
      const recsResult = await apiService.getRecommendations(formData);

      console.log('Recommendations response:', recsResult.data);

      if (recsResult.data.success) {
        const recommendations = recsResult.data.recommendations;
        
        // Validate recommendations
        if (!recommendations || recommendations.length === 0) {
          const errorMsg = 'No career recommendations generated. Please ensure all fields are filled correctly.';
          console.error(errorMsg);
          setError(errorMsg);
          setLoading(false);
          return;
        }

        console.log('Successfully generated recommendations:', recommendations);
        // If resume provided upload it (best-effort) after profile update
        if (formData.resume) {
          try {
            const uploadRes = await apiService.uploadResume(formData.resume);
            console.log('Resume upload response:', uploadRes.data);
          } catch (uploadErr) {
            console.warn('Resume upload failed:', uploadErr?.response?.data || uploadErr.message || uploadErr);
            // do not block recommendations, but inform user
            setError('Profile saved, but resume upload failed. You can retry from your profile.');
          }
        }

        onComplete(recommendations);
      } else {
        const errorMsg = recsResult.data.error || 'Failed to generate recommendations';
        console.error('Recommendations error:', errorMsg);
        setError(errorMsg);
      }
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'An error occurred while processing your assessment';
      console.error('Questionnaire submit error:', errorMsg, err);
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="questionnaire-container">
      {/* Progress Bar */}
      <div className="progress-section">
        <div className="progress-bar-bg">
          <motion.div
            className="progress-bar-fill"
            style={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
        <p className="progress-text">
          Question {step + 1} of {questions.length}
        </p>
      </div>

      {/* Question Card */}
      <motion.div
        className="question-card"
        key={step}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
      >
        <h2>{currentQuestion.title}</h2>
        <p className="question-description">{currentQuestion.description}</p>

        {/* Error */}
        {error && (
          <div className="alert alert-error">
            <span>⚠️</span>
            <p>{error}</p>
          </div>
        )}

        {/* Slider */}
        {currentQuestion.type === 'slider' && (
          <div className="slider-section">
            <input
              type="range"
              min={currentQuestion.min}
              max={currentQuestion.max}
              value={formData[currentQuestion.key]}
              onChange={(e) =>
                handleSliderChange(currentQuestion.key, e.target.value)
              }
              className="slider"
            />
            <div className="slider-labels">
              {currentQuestion.labels.map((label, idx) => (
                <span key={idx}>{label}</span>
              ))}
            </div>
            <div className="slider-value">
              {currentQuestion.labels[formData[currentQuestion.key] - 1]}
            </div>
          </div>
        )}

        {/* Select */}
        {currentQuestion.type === 'select' && (
          <div className="select-section">
            {currentQuestion.options.map((option) => (
              <button
                key={option}
                className={`select-option ${
                  formData[currentQuestion.key] === option.toLowerCase()
                    ? 'active'
                    : ''
                }`}
                onClick={() => handleSelectChange(currentQuestion.key, option)}
              >
                {option}
              </button>
            ))}
          </div>
        )}

        {/* Multi-Select */}
        {currentQuestion.type === 'multi-select' && (
          <div className="multi-select-section">
            {currentQuestion.options.map((option) => (
              <button
                key={option}
                className={`multi-select-option ${
                  formData[currentQuestion.key].includes(option) ? 'active' : ''
                }`}
                onClick={() =>
                  handleMultiSelect(currentQuestion.key, option)
                }
              >
                <span className="checkbox">
                  {formData[currentQuestion.key].includes(option) && '✓'}
                </span>
                {option}
              </button>
            ))}
          </div>
        )}

        {/* File Upload */}
        {currentQuestion.type === 'file' && (
          <div className="file-upload-section">
            <input
              type="file"
              accept={currentQuestion.accept || 'application/pdf'}
              onChange={(e) => {
                const f = e.target.files && e.target.files[0];
                setFormData((prev) => ({ ...prev, [currentQuestion.key]: f }));
              }}
            />
            {formData.resume && (
              <div className="file-meta">
                <p>Selected: {formData.resume.name}</p>
                <button className="btn btn-outline" onClick={() => setFormData((prev) => ({ ...prev, resume: null }))}>
                  Remove
                </button>
              </div>
            )}
          </div>
        )}
      </motion.div>

      {/* Navigation Buttons */}
      <div className="questionnaire-nav">
        <button
          className="btn btn-secondary"
          onClick={handlePrevious}
          disabled={step === 0 || loading}
        >
          ← Previous
        </button>

        <button
          className="btn btn-primary"
          onClick={handleNext}
          disabled={loading}
        >
          {loading
            ? '⏳ Generating...'
            : step === questions.length - 1
            ? '✨ Complete'
            : 'Next →'}
        </button>
      </div>
    </div>
  );
};

export default Questionnaire;
