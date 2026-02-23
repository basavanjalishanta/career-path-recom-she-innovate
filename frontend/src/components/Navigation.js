/**
 * Navigation Component
 * Header with user menu and navigation buttons
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import '../styles/navigation.css';

const Navigation = ({ user, currentView, setCurrentView }) => {
  const { logout } = useAuth();
  const [showMenu, setShowMenu] = useState(false);

  const handleLogout = async () => {
    await logout();
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        {/* Logo */}
        <div className="navbar-brand">
          <h2>🚀 Career Path</h2>
        </div>

        {/* Navigation Tabs */}
        <div className="navbar-tabs">
          <button
            className={`nav-tab ${currentView === 'questionnaire' ? 'active' : ''}`}
            onClick={() => setCurrentView('questionnaire')}
          >
            📝 Assessment
          </button>
          <button
            className={`nav-tab ${currentView === 'recommendations' ? 'active' : ''}`}
            onClick={() => setCurrentView('recommendations')}
          >
            🎯 Recommendations
          </button>
          <button
            className={`nav-tab ${currentView === 'chat' ? 'active' : ''}`}
            onClick={() => setCurrentView('chat')}
          >
            💬 Mentor
          </button>
        </div>

        {/* User Menu */}
        <div className="navbar-user">
          <div className="user-info">
            <div className="user-avatar">
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="user-text">
              <p className="user-name">{user?.name || 'User'}</p>
              <p className="user-email">{user?.email || ''}</p>
            </div>
          </div>

          {/* User Menu Button */}
          <button className="menu-toggle" onClick={() => setShowMenu(!showMenu)}>
            ⋮
          </button>

          {/* Dropdown Menu */}
          <AnimatePresence>
            {showMenu && (
              <motion.div
                className="dropdown-menu"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                <button className="dropdown-item" onClick={handleLogout}>
                  🚪 Logout
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
