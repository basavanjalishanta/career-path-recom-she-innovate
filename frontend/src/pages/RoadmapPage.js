import React, { useMemo, useState } from 'react';
import apiService from '../services/api';
import '../styles/roadmap.css';

const defaultForm = {
  selected_skill: '',
  skill_level: 2,
  experience_level: 2,
  study_time: 8,
  career_goal: ''
};

const skills = [
  'AI Engineer',
  'Full Stack Developer',
  'Cybersecurity Analyst',
  'Cloud Engineer',
  'DevOps Engineer',
  'Data Analyst',
  'UI/UX Designer',
  'Software Engineer',
  'Machine Learning Engineer'
];

const genericCareerWords = new Set(['job', 'career', 'work', 'employment']);

const RoadmapPage = ({ profile }) => {
  const [form, setForm] = useState(() => ({
    ...defaultForm,
    selected_skill: '',
    career_goal: profile?.career_goal || ''
  }));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const tips = useMemo(() => ([
    'Be consistent: small weekly progress compounds faster than bursts.',
    'Ship projects publicly and document outcomes for your resume.',
    'Review and adjust your plan every week based on blockers.'
  ]), []);

  const onChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const generate = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    const normalizedSkill = form.selected_skill.trim().toLowerCase();
    if (!normalizedSkill || genericCareerWords.has(normalizedSkill)) {
      setError('Please choose a specific career path (e.g., AI Engineer, Full Stack Developer).');
      return;
    }

    try {
      setLoading(true);
      const res = await apiService.generateLearningRoadmap({
        selected_skill: form.selected_skill,
        skill_level: Number(form.skill_level),
        experience_level: Number(form.experience_level),
        study_time: Number(form.study_time),
        career_goal: form.career_goal
      });

      if (res?.data?.success) {
        setResult(res.data.roadmap_plan);
      } else {
        setError(res?.data?.error || 'Failed to generate roadmap.');
      }
    } catch (err) {
      setError(err?.response?.data?.error || 'Roadmap generation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="roadmap-page">
      <div className="roadmap-header">
        <h2>🗺️ Learning Roadmap Generator</h2>
        <p>Generate roadmap tips, phases, projects, and career readiness.</p>
      </div>

      <div className="roadmap-grid">
        <section className="roadmap-card">
          <h3>Roadmap Inputs</h3>
          <form onSubmit={generate} className="roadmap-form">
            <label>
              Selected Skill / Career
              <input
                list="skills"
                value={form.selected_skill}
                onChange={(e) => onChange('selected_skill', e.target.value)}
                placeholder="e.g., Full Stack Developer"
              />
              <datalist id="skills">
                {skills.map((s) => <option key={s} value={s} />)}
              </datalist>
            </label>

            <label>
              Current Skill Level (1-5)
              <input
                type="number"
                min="1"
                max="5"
                value={form.skill_level}
                onChange={(e) => onChange('skill_level', e.target.value)}
              />
            </label>

            <label>
              Experience Level (1-5)
              <input
                type="number"
                min="1"
                max="5"
                value={form.experience_level}
                onChange={(e) => onChange('experience_level', e.target.value)}
              />
            </label>

            <label>
              Study Time per Week (hours)
              <input
                type="number"
                min="1"
                max="40"
                value={form.study_time}
                onChange={(e) => onChange('study_time', e.target.value)}
              />
            </label>

            <label>
              Career Goal
              <input
                value={form.career_goal}
                onChange={(e) => onChange('career_goal', e.target.value)}
                placeholder="e.g., Get internship in 6 months"
              />
            </label>

            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? 'Generating...' : 'Generate Roadmap'}
            </button>
          </form>
          {error && <p className="roadmap-error">{error}</p>}
        </section>

        <section className="roadmap-card">
          <h3>Roadmap Tips</h3>
          <ul className="tips-list">
            {tips.map((tip) => <li key={tip}>{tip}</li>)}
          </ul>
        </section>
      </div>

      {result && (
        <section className="roadmap-card roadmap-output">
          <h3>{result.career}</h3>
          <p>{result.importance}</p>

          <div className="phase-grid">
            {['beginner', 'intermediate', 'advanced'].map((phase) => (
              <div className="phase-card" key={phase}>
                <h4>{phase.toUpperCase()}</h4>
                <p><strong>Duration:</strong> {result.roadmap?.[phase]?.duration}</p>
                <p><strong>Skills:</strong> {(result.roadmap?.[phase]?.skills || []).join(', ')}</p>
                <p><strong>Concepts:</strong> {(result.roadmap?.[phase]?.concepts || []).join(', ')}</p>
                <p><strong>Exercises:</strong> {(result.roadmap?.[phase]?.exercises || []).join(' | ')}</p>
              </div>
            ))}
          </div>

          {Array.isArray(result.recommended_careers) && result.recommended_careers.length > 0 && (
            <>
              <h4>Recommended Careers (From Skill Section)</h4>
              <p>
                {result.recommended_careers
                  .map((r) => `${r.career} (${r.alignment_score}%)`)
                  .join(' | ')}
              </p>
            </>
          )}

          <h4>Projects</h4>
          <p><strong>Beginner:</strong> {(result.projects?.beginner || []).join(', ')}</p>
          <p><strong>Intermediate:</strong> {(result.projects?.intermediate || []).join(', ')}</p>
          <p><strong>Advanced:</strong> {(result.projects?.advanced || []).join(', ')}</p>

          <h4>Tools & Career</h4>
          <p><strong>Tools Required:</strong> {(result.tools_required || []).join(', ')}</p>
          <p><strong>Weekly Plan:</strong> {(result.weekly_plan || []).join(' | ')}</p>
          <p><strong>Milestones:</strong> {(result.milestones || []).join(' | ')}</p>
          <p><strong>Career Opportunities:</strong> {(result.career_opportunities || []).join(', ')}</p>
          <p><strong>Career Readiness:</strong> {result.career_readiness_level}</p>

        </section>
      )}
    </div>
  );
};

export default RoadmapPage;
