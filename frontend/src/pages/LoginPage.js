/**
 * Login Page
 * Premium authentication form for existing users
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import '../styles/auth.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login, isLoading, error, clearError } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
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

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      setLocalError('Email and password are required');
      return;
    }

    const result = await login(formData.email, formData.password);

    if (result.success) {
      setSuccess('Welcome back! Redirecting to dashboard...');
      console.log('Login successful for:', formData.email);
      setTimeout(() => {
        navigate('/dashboard', { replace: true });
      }, 1000);
    } else {
      setLocalError(result.error);
      console.error('Login error:', result.error);
    }
  };

  // Demo credentials hint
  const fillDemoCredentials = () => {
    setFormData({
      email: 'demo@example.com',
      password: 'demo12345',
    });
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
            <h1>Welcome Back</h1>
            <p>Sign in to access your career dashboard</p>
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
            </div>

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary btn-large" disabled={isLoading}>
              {isLoading ? '⏳ Signing In...' : '🚀 Sign In'}
            </button>

            {/* Demo Hint */}
            <motion.button
              type="button"
              className="btn btn-secondary"
              onClick={fillDemoCredentials}
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              💡 Try Demo Account
            </motion.button>
          </motion.form>

          {/* Footer */}
          <motion.div className="auth-footer" variants={itemVariants}>
            <p>
              Don't have an account?{' '}
              <Link to="/signup" className="auth-link">
                Sign up here
              </Link>
            </p>
          </motion.div>
        </motion.div>

        {/* Side Info */}
        <motion.div className="auth-info" variants={itemVariants}>
          <h3>Your Career Path Awaits</h3>
          <ul className="info-list">
            <li>
              <span className="icon">🎯</span>
              <span>Get personalized recommendations</span>
            </li>
            <li>
              <span className="icon">💬</span>
              <span>Chat with AI career mentor</span>
            </li>
            <li>
              <span className="icon">📊</span>
              <span>Track your progress</span>
            </li>
            <li>
              <span className="icon">🎓</span>
              <span>Access learning resources</span>
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  );
};

export default LoginPage;
