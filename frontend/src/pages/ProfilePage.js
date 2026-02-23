
import React from 'react';
import apiService from '../services/api';

const ProfilePage = ({ profile }) => {
  const downloadResume = async () => {
    try {
      const res = await apiService.downloadResume();
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'resume.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download resume.');
      console.error(err);
    }
  };

  if (!profile) return <div className="profile-page">No profile loaded.</div>;

  return (
    <div className="profile-page">
      <h2>Your Profile</h2>
      <p><strong>Skills:</strong></p>
      <pre>{JSON.stringify(profile.skills || profile, null, 2)}</pre>
      <p><strong>Preferred Domains:</strong> {(profile.preferred_domains || []).join(', ')}</p>
      <p><strong>Career Goal:</strong> {profile.career_goal}</p>
      <p><strong>Confidence:</strong> {profile.confidence}</p>
      {profile.resume_path ? (
        <div>
          <p><strong>Resume:</strong> Uploaded</p>
          <button className="btn btn-primary" onClick={downloadResume}>Download Resume</button>
        </div>
      ) : (
        <p>No resume uploaded.</p>
      )}
    </div>
  );
};

export default ProfilePage;
