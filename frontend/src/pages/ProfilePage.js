import React, { useState } from 'react';
import apiService from '../services/api';
import '../styles/profile.css';

const SkillBar = ({ name, value }) => {
  const pct = Math.round((value / 5) * 100);
  return (
    <div className="skill-row">
      <div className="skill-name">{name}</div>
      <div className="skill-bar">
        <div className="skill-fill" style={{ width: `${pct}%` }} />
      </div>
      <div className="skill-value">{value}/5</div>
    </div>
  );
};

const Heatmap = ({ skills }) => {
  const names = Object.keys(skills);
  const cells = names.map((n) => {
    const v = skills[n] || 0;
    const hue = 200 - (v / 5) * 200; // blue->green->yellow
    const bg = `hsl(${hue},70%,55%)`;
    return (
      <div key={n} className="heat-cell" style={{ background: bg }}>
        <div className="heat-name">{n}</div>
        <div className="heat-value">{v}</div>
      </div>
    );
  });

  return <div className="heatmap-grid">{cells}</div>;
};

const RadarChart = ({ skills }) => {
  const entries = ['coding','math','creativity','communication','leadership','domain_expertise'];
  const size = 220;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 80;

  const toPoint = (i, value) => {
    const angle = (Math.PI * 2 * i) / entries.length - Math.PI / 2;
    const r = (value / 5) * radius;
    return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
  };

  const points = entries.map((k, i) => toPoint(i, skills[k] || 0));
  const polyPoints = points.map(p => p.join(',')).join(' ');

  return (
    <svg width={size} height={size} className="radar-chart" viewBox={`0 0 ${size} ${size}`}>
      {/* grid circles */}
      {[1,2,3,4,5].map(level => (
        <circle key={level} cx={cx} cy={cy} r={(level/5)*radius} stroke="#2b2e4a" strokeWidth="0.8" fill="none" opacity={0.4} />
      ))}
      {/* axes */}
      {entries.map((k,i)=>{
        const [x,y] = toPoint(i,5);
        return <line key={k} x1={cx} y1={cy} x2={x} y2={y} stroke="#2b2e4a" strokeWidth="0.8" opacity={0.6} />
      })}
      {/* polygon */}
      <polygon points={polyPoints} fill="rgba(79,70,229,0.22)" stroke="#4f46e5" strokeWidth="1.6" />
      {/* labels */}
      {entries.map((k,i)=>{
        const [x,y] = toPoint(i,5);
        const lx = cx + (x-cx)*1.15;
        const ly = cy + (y-cy)*1.15;
        return <text key={k} x={lx} y={ly} fontSize="11" fill="#e6eef8" textAnchor={lx>cx? 'start':'end'}>{k.replace('_',' ')}</text>;
      })}
    </svg>
  );
};

const PieChart = ({ skills }) => {
  const entries = ['coding','math','creativity','communication','leadership','domain_expertise'];
  const values = entries.map(k => skills[k] || 0);
  const total = values.reduce((a,b)=>a+b, 0) || 1;
  const size = 160;
  const cx = size/2, cy = size/2, r = size/2 - 4;
  let acc = 0;
  const colors = ['#7c3aed','#06b6d4','#f97316','#ef4444','#10b981','#60a5fa'];

  const slices = values.map((v,i) => {
    const start = acc/total * Math.PI*2 - Math.PI/2;
    acc += v;
    const end = acc/total * Math.PI*2 - Math.PI/2;
    const x1 = cx + r * Math.cos(start);
    const y1 = cy + r * Math.sin(start);
    const x2 = cx + r * Math.cos(end);
    const y2 = cy + r * Math.sin(end);
    const large = (end - start) > Math.PI ? 1 : 0;
    const path = `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} Z`;
    return { path, color: colors[i % colors.length], label: entries[i], value: v };
  });

  return (
    <div style={{textAlign:'center'}}>
      <svg width={size} height={size} className="pie-chart">
        {slices.map((s, idx) => (
          <path key={idx} d={s.path} fill={s.color} stroke="#071428" strokeWidth="0.5" />
        ))}
      </svg>
      <div style={{display:'flex', flexWrap:'wrap', gap:6, justifyContent:'center', marginTop:8}}>
        {slices.map((s, i) => (
          <div key={i} style={{display:'flex', gap:6, alignItems:'center', color:'#cfe8ff', fontSize:12}}>
            <span style={{width:12,height:12,background:s.color,display:'inline-block',borderRadius:3}} />
            <span style={{textTransform:'capitalize'}}>{s.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const ProfilePage = ({ profile: initialProfile }) => {
  const [profile, setProfile] = useState(initialProfile);
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
  const skills = profile.skills || profile || {};

  const refresh = async () => {
    try {
      const res = await apiService.getProfile();
      if (res.data && res.data.success) setProfile(res.data.profile);
    } catch (e) {
      console.warn('Failed to refresh profile', e);
    }
  };

  return (
    <div className="profile-page">
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <h2>👤 Your Profile</h2>
        <div>
          <button className="btn btn-outline" onClick={refresh}>Refresh profile</button>
        </div>
      </div>

      <div className="profile-grid">
        <div className="profile-section">
          <p><strong>Preferred Domains:</strong> {(profile.preferred_domains || []).length ? (profile.preferred_domains || []).join(', ') : 'Not set'}</p>
          <p><strong>Career Goal:</strong> {profile.career_goal || 'Not set'}</p>
          <p><strong>Confidence:</strong> {profile.confidence || profile.confidence_level || 'Not set'}</p>
          {profile.resume_path ? (
            <div>
              <p><strong>Resume:</strong> Uploaded</p>
              <button className="btn btn-primary" onClick={downloadResume}>Download Resume</button>
            </div>
          ) : (
            <p>No resume uploaded.</p>
          )}
        </div>

        <div className="profile-section">
          <h4>Skill Bars</h4>
          {['coding','math','creativity','communication','leadership','domain_expertise'].map(k => (
            <SkillBar key={k} name={k.replace('_',' ')} value={skills[k] || skills[k.replace(' ','_')] || 0} />
          ))}
        </div>

        <div className="profile-section">
          <h4>Skill Heatmap</h4>
          <Heatmap skills={{
            coding: skills.coding || 0,
            math: skills.math || 0,
            creativity: skills.creativity || 0,
            communication: skills.communication || 0,
            leadership: skills.leadership || 0,
            domain_expertise: skills.domain_expertise || 0
          }} />
        </div>

        <div className="profile-section">
          <h4>Skill Radar & Distribution</h4>
          <div className="chart-pair">
            <RadarChart skills={{
              coding: skills.coding || 0,
              math: skills.math || 0,
              creativity: skills.creativity || 0,
              communication: skills.communication || 0,
              leadership: skills.leadership || 0,
              domain_expertise: skills.domain_expertise || 0
            }} />
            <PieChart skills={{
              coding: skills.coding || 0,
              math: skills.math || 0,
              creativity: skills.creativity || 0,
              communication: skills.communication || 0,
              leadership: skills.leadership || 0,
              domain_expertise: skills.domain_expertise || 0
            }} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
