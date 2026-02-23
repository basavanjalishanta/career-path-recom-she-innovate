/**
 * Signup Page
 * Premium authentication form with validation
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import '../styles/auth.css';

const SignupPage = () => {
  const navigate = useNavigate();
  const { signup, isLoading, error, clearError } = useAuth();

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [localError, setLocalError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (localError) setLocalError('');
    if (error) clearError();
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      setLocalError('Name is required');
      return false;
    }
    if (!formData.email.includes('@')) {
      setLocalError('Valid email is required');
      return false;
    }
    if (formData.password.length < 8) {
      setLocalError('Password must be at least 8 characters');
      return false;
    }
    if (formData.password !== formData.confirmPassword) {
      setLocalError('Passwords do not match');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    const result = await signup(formData.email, formData.password, formData.name);

    if (result.success) {
      setSuccess('Account created! Redirecting...');
      console.log('Signup successful for:', formData.email);
      setTimeout(() => {
        navigate('/dashboard', { replace: true });
      }, 1000);
    } else {
      setLocalError(result.error);
      console.error('Signup error:', result.error);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  return (
    <div className="auth-container">
      <div className="auth-background">
        <div className="gradient-blob blob-1"></div>
        <div className="gradient-blob blob-2"></div>
      </div>

      <div className="auth-content">
        <motion.div
          className="auth-card"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Header */}
          <motion.div className="auth-header" variants={itemVariants}>
            <h1>Create Account</h1>
            <p>Start your career journey with AI guidance</p>
          </motion.div>

          {/* Form */}
          <motion.form className="auth-form" onSubmit={handleSubmit} variants={itemVariants}>
            {/* Error Alert */}
            {(localError || error) && (
              <motion.div className="alert alert-error" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <span>⚠️</span>
                <p>{localError || error}</p>
              </motion.div>
            )}

            {/* Success Message */}
            {success && (
              <motion.div className="alert alert-success" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <span>✓</span>
                <p>{success}</p>
              </motion.div>
            )}

            {/* Name Field */}
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="John Doe"
                disabled={isLoading}
              />
            </div>

            {/* Email Field */}
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="you@example.com"
                disabled={isLoading}
              />
            </div>

            {/* Password Field */}
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                disabled={isLoading}
              />
              <small>Minimum 8 characters</small>
            </div>

            {/* Confirm Password Field */}
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="••••••••"
                disabled={isLoading}
              />
            </div>

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary btn-large" disabled={isLoading}>
              {isLoading ? '⏳ Creating Account...' : '✨ Create Account'}
            </button>
          </motion.form>

          {/* Footer */}
          <motion.div className="auth-footer" variants={itemVariants}>
            <p>
              Already have an account?{' '}
              <Link to="/login" className="auth-link">
                Sign in here
              </Link>
            </p>
          </motion.div>
        </motion.div>

        {/* Side Info */}
        <motion.div className="auth-info" variants={itemVariants}>
          <h3>Why Join Us?</h3>
          <ul className="info-list">
            <li>
              <span className="icon">🎯</span>
              <span>Personalized career recommendations</span>
            </li>
            <li>
              <span className="icon">🤖</span>
              <span>AI-powered mentor guidance</span>
            </li>
            <li>
              <span className="icon">📚</span>
              <span>Detailed learning roadmaps</span>
            </li>
            <li>
              <span className="icon">💡</span>
              <span>Project ideas and resources</span>
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  );
};

export default SignupPage;
