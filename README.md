# Daily Ideas Archive

A simple web application for recording daily ideas (single sentences) that are archived and hidden until export. Entries can be exported to PDF for printing on business cards.

## Features

- ✅ Simple entry form with security key authentication
- ✅ Two authorized users (you and your significant other)
- ✅ Entries completely hidden from UI (database access OK)
- ✅ PDF export with business card format (3.5" x 2")
- ✅ Summary page with statistics
- ✅ Character limit: 250 characters per entry
- ✅ Responsive design for mobile and desktop

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **PDF Generation**: ReportLab
- **Frontend**: HTML/CSS/JavaScript

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env.example .env
```

Edit `.env` and set your security keys:
```
USER_KEY_1=your-personal-key-here
USER_KEY_2=significant-other-key-here
PDF_PASSWORD=your-pdf-export-password-here
SECRET_KEY=your-secret-key-here
```

5. Run the application:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Usage

1. **Record an Entry**:
   - Enter your security key
   - Write your daily idea (max 250 characters)
   - Click "Record Entry"

2. **Export to PDF**:
   - Click "Export to PDF" button
   - Enter the PDF export password (separate from entry keys)
   - PDF will download with:
     - Summary page (total entries, date range, author stats)
     - Business cards (one per entry) with text, date, and author name (Cale or Carolyn)

## Database

The SQLite database (`entries.db`) stores:
- Entry text
- User key identifier (user1/user2)
- Entry date
- Created timestamp

You can access the database directly using SQLite tools to view entries:
```bash
sqlite3 entries.db
SELECT * FROM entries;
```

## Deployment to Render (Free Hosting)

### Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push this code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: daily-ideas-archive (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Add Environment Variables:
   - `USER_KEY_1`: Your personal key (for entry submission)
   - `USER_KEY_2`: Your significant other's key (for entry submission)
   - `PDF_PASSWORD`: Password required to export PDFs
   - `SECRET_KEY`: A random secret key (generate one)
   - `PORT`: 10000 (Render's default)
6. Click "Create Web Service"
7. Wait for deployment (first deploy takes a few minutes)

### Step 3: Access Your App

Once deployed, Render will provide a URL like:
`https://daily-ideas-archive.onrender.com`

**Note**: Free tier on Render spins down after 15 minutes of inactivity. First request after spin-down may take 30-60 seconds to wake up.

## Alternative Free Hosting Options

### Railway
- Similar to Render
- $5 free credit monthly
- Requires credit card (but free tier available)

### PythonAnywhere
- Free tier available
- Flask-friendly
- URL includes "pythonanywhere.com" domain

### Fly.io
- Free tier with generous limits
- Good for Python apps
- Slightly more complex setup

## Security Notes

- **Change default keys**: Always set your own `USER_KEY_1` and `USER_KEY_2`
- **Change SECRET_KEY**: Use a strong random secret key in production
- **Database**: The SQLite database file contains all entries. Keep it secure.
- **HTTPS**: Free hosting providers (like Render) provide HTTPS automatically

## PDF Format

- **Card Size**: 3.5" x 2" (US standard business card)
- **Per Card**: Entry text, date, author name (Cale or Carolyn)
- **Layout**: Multiple cards per page (2 per row, 5 per column), evenly spaced
- **Summary**: First page includes statistics (total entries, entries per author, date range)
- **Security**: Password required to generate PDF (separate from entry submission keys)

## Troubleshooting

### Database Issues
If you need to reset the database:
```bash
rm entries.db
python app.py  # Will recreate the database
```

### Port Already in Use
Change the port in `.env` or set environment variable:
```bash
PORT=5001 python app.py
```

### PDF Generation Errors
Ensure ReportLab is installed:
```bash
pip install reportlab
```

## License

This project is for personal use. Feel free to modify as needed.

## Support

For issues or questions, check the database directly or review the code in `app.py`.

