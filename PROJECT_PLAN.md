# Daily Idea Archive - Project Plan

## Project Overview
A simple web application for recording daily ideas (single sentences) that are archived and hidden until export. Entries can be exported to PDF for printing on business cards.

## Core Requirements

### Functional Requirements
1. **Daily Entry Form**
   - Single text input field for daily idea (one sentence)
   - Security key input field
   - Submit button to record entry
   - Date automatically recorded on submission

2. **Data Storage**
   - Store: entry text, security key, date/timestamp
   - Entries hidden after submission (not visible in UI)
   - Entries persist until export

3. **Security**
   - Simple authentication mechanism (single key/password)
   - Prevents unauthorized entries
   - Key stored with each entry for verification

4. **PDF Export**
   - Export all entries to PDF
   - Format optimized for business card printing
   - Include entry text and date
   - Possibly include security key (TBD)

### Non-Functional Requirements
- Simple, minimal UI
- Fast and lightweight
- Easy to deploy and maintain
- Secure enough to prevent casual unauthorized access

## Technical Architecture (Finalized)

### Frontend
- **Technology**: HTML/CSS/JavaScript with Flask templating
- **UI**: Minimal single-page application
- **Features**:
  - Entry form (text input + key input + submit)
  - Export button (hidden/admin access only)
  - Simple success/error messaging
  - No entry display in UI (completely hidden)

### Backend
- **Technology**: **Python Flask** (chosen)
- **API Endpoints**:
  - `POST /` or `POST /submit` - Submit new entry
  - `GET /export` - Generate and download PDF
  - `GET /` - Display entry form

### Database
- **Technology**: **SQLite** (works well with free hosting, file-based)
- **Schema**:
  ```sql
  entries:
    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
    - text (TEXT, NOT NULL)
    - user_key (TEXT, NOT NULL)  -- stores which key was used (user1/user2)
    - entry_date (DATETIME, NOT NULL)
    - created_at (DATETIME DEFAULT CURRENT_TIMESTAMP)
  ```

### Security
- **Two Authorized Keys**: 
  - User key 1 (your personal key)
  - User key 2 (significant other's key)
- **Storage**: Keys stored in environment variables or config file (not in database)
- **Validation**: On submission, verify key matches one of the two authorized keys
- **User Tracking**: Store which key was used (user1/user2) to differentiate entries

### PDF Generation
- **Library**: **ReportLab** (Python, reliable, good for business cards)
- **Format**: Business card size (3.5" x 2" / 85mm x 55mm)
- **Content per card**: Entry text + date (user key optional, TBD)
- **Layout**: One entry per card, arranged in grid for printing

### Free Hosting Options

#### Recommended: **Render** (render.com)
- ✅ Free tier: 750 hours/month (enough for always-on)
- ✅ Supports Flask + SQLite
- ✅ Automatic HTTPS
- ✅ Easy deployment from GitHub
- ✅ Free PostgreSQL if needed later
- ⚠️ Spins down after 15 min inactivity (wakes on request)

#### Alternative: **Railway** (railway.app)
- ✅ $5 free credit monthly (usually enough for small apps)
- ✅ Supports Flask + SQLite
- ✅ Good documentation
- ⚠️ Requires credit card (but free tier available)

#### Alternative: **PythonAnywhere** (pythonanywhere.com)
- ✅ Free tier available
- ✅ Flask-friendly
- ✅ SQLite supported
- ⚠️ Limited to one web app on free tier
- ⚠️ URL includes "pythonanywhere.com" domain

#### Alternative: **Fly.io** (fly.io)
- ✅ Free tier with generous limits
- ✅ Good for Python apps
- ⚠️ Slightly more complex setup

**Recommendation**: Start with **Render** - easiest free deployment, good for Flask apps.

## Requirements Clarified ✅

### 1. Technology Stack ✅
- **Chosen**: Python Flask
- **Deployment**: Free cloud hosting (Render recommended)

### 2. Security Key Implementation ✅
- **Two authorized keys**: One for you, one for significant other
- **Storage**: Keys in environment variables/config (not in database)
- **Tracking**: Store which key was used (user1/user2) with each entry
- **Purpose**: Differentiate entries and restrict access

### 3. PDF Export Format (Remaining Questions)
- **Business card size**: Standard US (3.5" x 2") or EU (85mm x 55mm)? 
- **Content per card**: Entry text + date? Include user indicator (user1/user2)?
- **Order**: Chronological or reverse chronological?
- **Layout**: One entry per card confirmed

### 4. Entry Management ✅
- **Visibility**: Completely hidden from UI until export
- **Database access**: Direct database access OK for viewing
- **Editing**: Write-once only (no editing/deletion in UI)
- **Character limit**: Should we set a max length? (e.g., 200-300 chars for business card fit)

### 5. Deployment & Access ✅
- **Hosting**: Free cloud hosting (Render recommended)
- **Access**: Multiple devices via internet
- **Type**: Simple web app

### 6. Additional Features (Remaining Questions)
- **Export confirmation**: Should there be a confirmation dialog before PDF generation?
- **Summary page**: Include summary stats (total entries, date range) in PDF?
- **Backup**: Any backup/restore functionality needed?

## Implementation Phases

### Phase 1: Core Functionality
1. Set up project structure
2. Create database schema
3. Build entry submission form
4. Implement backend API for storing entries
5. Basic security key validation

### Phase 2: PDF Export
1. Research business card PDF format
2. Implement PDF generation
3. Create export endpoint
4. Test PDF output and printing

### Phase 3: Polish & Security
1. Improve UI/UX
2. Enhance security (key hashing, input validation)
3. Error handling and validation
4. Testing

### Phase 4: Deployment
1. Choose deployment method
2. Set up hosting/server
3. Configure and deploy
4. Documentation

## Final Decisions ✅

1. **Business card size**: ✅ US standard (3.5" x 2")
2. **PDF content**: ✅ Entry text + date + user indicator (user1/user2)
3. **Character limit**: ✅ 250 characters maximum
4. **Export confirmation**: ✅ Simple export button (no confirmation dialog)
5. **PDF summary**: ✅ Include summary page with stats (total entries, date range)

## Implementation Plan

### Phase 1: Project Setup & Core Functionality
1. Initialize Flask project structure
2. Set up SQLite database with schema
3. Create entry submission form (HTML template)
4. Implement key validation (two authorized keys)
5. Store entries with user tracking
6. Basic error handling

### Phase 2: PDF Export
1. Install and configure ReportLab
2. Create PDF generation function
3. Format for business card size
4. Implement export endpoint
5. Test PDF output

### Phase 3: UI/UX Polish
1. Clean, minimal design
2. Success/error messaging
3. Form validation
4. Responsive design (mobile-friendly)

### Phase 4: Deployment Preparation
1. Create requirements.txt
2. Add environment variable configuration
3. Create deployment documentation
4. Test locally
5. Deploy to Render (or chosen platform)

## Next Steps
1. Answer remaining questions (or I can proceed with sensible defaults)
2. Begin implementation
3. Test locally
4. Deploy to free hosting

