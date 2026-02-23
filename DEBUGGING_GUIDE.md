# Debugging Guide - Questionnaire to Recommendations Flow

## Issue Description
After completing the 10th question, instead of showing the analysis and recommendations, the questionnaire resets to the first question. Additionally, recommendations are empty and the AI mentor shows a processing error.

## Root Causes Identified and Fixed

### 1. **Insufficient Error Handling in Frontend**
**Issue**: The Questionnaire component wasn't properly catching and displaying API errors.
**Fix**: Added comprehensive error handling with detailed console logging to track:
- Profile update success/failure
- Recommendations generation success/failure
- Empty recommendations validation
- Specific error messages from the backend

### 2. **Missing Recommendations Validation**
**Issue**: The API could return success=true with an empty recommendations array.
**Fix**: Added validation to ensure recommendations array is not empty before transitioning views.

### 3. **Insufficient Backend Logging**
**Issue**: Backend errors weren't being logged, making it hard to diagnose issues.
**Fix**: Added detailed logging in both `/api/profile/update` and `/api/recommendations` endpoints.

## Debugging Steps

### Step 1: Check Browser Console Logs
1. Open your browser's Developer Tools (F12)
2. Go to the **Console** tab
3. Complete the questionnaire and observe the logs

**Expected logs should show:**
```
[Questionnaire] Updating profile...
[Questionnaire] Profile updated successfully: [profile data]
[Questionnaire] Fetching recommendations...
[Questionnaire] Recommendations response: [data]
[Questionnaire] Successfully generated recommendations: [array]
[Dashboard] Questionnaire completed with recommendations: [array]
[Dashboard] Setting recommendations state and changing view to recommendations
```

### Step 2: Check Server Logs (Backend Terminal)
Watch your Flask server terminal while completing the questionnaire. You should see:

```
[INFO] Updating profile for user [ID] with data: {...}
[INFO] Profile updated successfully for user [ID]: {...}
[INFO] Generating recommendations for user [ID] with profile: {...}
[INFO] Generated 3 recommendations for user [ID]
[INFO] Successfully stored 3 recommendations for user [ID]
```

### Step 3: Common Issues and Solutions

#### Issue A: "Update your profile first" Error
**Cause**: Profile is not being saved to the database before recommendations are fetched.
**Solution**: 
1. Check if the profile is being created with a user_id
2. Ensure the Questionnaire form data matches the backend field names
3. Verify the JWT token is being sent correctly

#### Issue B: No Recommendations Generated
**Cause**: The recommendation engine might be receiving incomplete profile data.
**Solution**:
1. Check the server log to see the profile data being sent
2. Ensure all required fields are present in the formData
3. Check if the recommendation engine's `get_recommendations()` method is returning an empty list

#### Issue C: API Returns Error 500
**Cause**: The recommendation engine or database operation is throwing an exception.
**Solution**:
1. Check the backend logs for the full stack trace
2. Look for database constraint violations
3. Check if any required JSON fields are malformed

#### Issue D: Frontend Doesn't Transition to Recommendations
**Cause**: The `onComplete` callback is not being called.
**Solution**:
1. Check console logs to see if recommendations are empty
2. Check if there's a network error (Network tab in DevTools)
3. Check if the response status is 200 and success=true

### Step 4: Testing the Flow Manually

1. **Test Profile Update Alone**:
   Open browser console and run:
   ```javascript
   // Get your token
   const token = localStorage.getItem('access_token');
   
   // Test profile update
   fetch('http://localhost:5000/api/profile/update', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
       'Authorization': `Bearer ${token}`
     },
     body: JSON.stringify({
       coding_proficiency: 3,
       math_comfort: 3,
       creativity: 3,
       communication_skill: 3,
       leadership_potential: 3,
       domain_expertise: 2,
       preferred_domains: ['AI'],
       career_goal: 'job',
       teamwork_preference: true,
       project_experience_level: 2,
       work_environment: 'hybrid',
       primary_motivation: 'learning',
       key_concerns: [],
       confidence_level: 3
     })
   }).then(r => r.json()).then(d => console.log('Profile Response:', d));
   ```

2. **Test Recommendations Separately**:
   ```javascript
   const token = localStorage.getItem('access_token');
   
   fetch('http://localhost:5000/api/recommendations', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
       'Authorization': `Bearer ${token}`
     },
     body: JSON.stringify({
       coding_proficiency: 3,
       math_comfort: 3,
       creativity: 3,
       communication_skill: 3,
       leadership_potential: 3,
       domain_expertise: 2,
       preferred_domains: ['AI'],
       career_goal: 'job',
       teamwork_preference: true,
       project_experience_level: 2,
       work_environment: 'hybrid',
       primary_motivation: 'learning',
       key_concerns: [],
       confidence_level: 3
     })
   }).then(r => r.json()).then(d => console.log('Recommendations Response:', d));
   ```

### Step 5: Database Check
Check if the profile and recommendations are being saved:

```python
# In Python shell with Flask app context
from models import User, UserProfile, Recommendation, db

# Find your user (use email from login)
user = User.query.filter_by(email='your-email@example.com').first()

# Check profile
profile = UserProfile.query.filter_by(user_id=user.id).first()
print("Profile exists:", profile is not None)
if profile:
    print("Profile data:", profile.to_dict())

# Check recommendations
recs = Recommendation.query.filter_by(user_id=user.id).all()
print("Recommendations count:", len(recs))
for rec in recs:
    print(f"  - {rec.career_path}: {rec.alignment_score}")
```

## Key Data Flow to Verify

```
Questionnaire Component
  ↓ (User fills 10 questions)
  ↓ handleSubmit()
  ├→ updateProfile(formData) → POST /api/profile/update
  │  └→ Backend saves to UserProfile table
  │
  └→ getRecommendations(formData) → POST /api/recommendations
     ├→ Backend fetches profile from DB
     ├→ Runs recommendation_engine.get_recommendations()
     ├→ Saves results to Recommendation table
     └→ Returns recommendations array
        
        ↓
        If success && recommendations.length > 0:
          ↓
          onComplete(recommendations)
          ↓
          Dashboard.handleQuestionnaireComplete()
          ↓
          setRecommendations(recs)
          setCurrentView('recommendations')
          ↓
          Shows RecommendationsView
```

## Files Modified

1. **frontend/src/components/Questionnaire.js**
   - Added comprehensive error handling
   - Added validation for empty recommendations
   - Added console logging for debugging

2. **frontend/src/pages/Dashboard.js**
   - Added console logging in handleQuestionnaireComplete
   - Added validation to prevent empty recommendations from being displayed

3. **backend/app.py**
   - Added logging to update_profile endpoint
   - Added logging to get_recommendations endpoint
   - Added validation for empty recommendations array

## Next Steps If Issues Persist

1. **Enable Database Logging**:
   Add to Flask app setup:
   ```python
   import logging
   logging.basicConfig()
   logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
   ```

2. **Check Environment Variables**:
   Ensure `REACT_APP_API_URL` is correctly set in your `.env` file

3. **Verify JWT Token**:
   The token should be valid and not expired. Check the token expiration in `app.py`:
   ```python
   app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
   ```

4. **Check CORS Configuration**:
   Verify that your frontend URL is in the allowed origins in `app.py`:
   ```python
   CORS(app, resources={r'/api/*': {'origins': ['http://localhost:3000', 'http://127.0.0.1:3000']}})
   ```

---

**For further assistance, share the console logs and server logs when you encounter the issue.**
