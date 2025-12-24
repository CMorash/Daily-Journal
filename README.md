# Daily Ideas Archive

A simple app for you and someone special to jot down daily ideas together. Each entry stays hidden until you export them as a printable PDF of business cards—perfect for a jar of memories or a creative keepsake.

## What It Does

- Write short daily ideas (up to 250 characters)
- Two people can use it with separate security keys
- Entries stay hidden from the UI (no peeking!)
- Export everything to a PDF formatted as business cards (3.5" x 2")
- Summary page shows stats: total entries, date range, who wrote what

## Tech Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL (Neon) for production, SQLite for local dev
- **PDF Generation**: ReportLab
- **Hosting**: Vercel (serverless)

---

## Local Development

Want to run this on your own machine? Here's how.

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repo and cd into it:

```bash
git clone https://github.com/yourusername/daily-journal.git
cd daily-journal/Daily-Journal
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your secrets:

```env
USER_KEY_1=your-secret-key
USER_KEY_2=partner-secret-key
PDF_PASSWORD=export-password
SECRET_KEY=flask-secret-key
USER1=YourName
USER2=PartnerName
```

5. Run it:

```bash
python app.py
```

Open http://localhost:5000 and you're good to go. The app uses SQLite by default, so no database setup needed.

---

## Deploying to Vercel + Neon

### Step 1: Set Up Neon Database

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project
3. Copy your connection string—it looks like:
   ```
   postgresql://username:password@ep-something.region.aws.neon.tech/dbname?sslmode=require
   ```

### Step 2: Deploy to Vercel

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) and import your repository
3. In the project settings, add these environment variables:

| Variable | Value |
|----------|-------|
| `USE_POSTGRES` | `true` |
| `DATABASE_URL` | Your Neon connection string |
| `USER_KEY_1` | Your entry key |
| `USER_KEY_2` | Partner's entry key |
| `PDF_PASSWORD` | Password for PDF exports |
| `SECRET_KEY` | Random secret (generate one) |
| `USER1` | Your display name |
| `USER2` | Partner's display name |

4. Deploy! Vercel will build and host your app automatically.

### Step 3: Initialize the Database

The database table gets created automatically on first request. Just visit your deployed URL and you're set.

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `USE_POSTGRES` | No | Set to `true` for PostgreSQL. Omit for SQLite. |
| `DATABASE_URL` | If Postgres | Neon connection string |
| `USER_KEY_1` | Yes | Security key for user 1 |
| `USER_KEY_2` | Yes | Security key for user 2 |
| `USER1` | No | Display name for user 1 (default: "User 1") |
| `USER2` | No | Display name for user 2 (default: "User 2") |
| `PDF_PASSWORD` | Yes | Password to export PDFs |
| `SECRET_KEY` | Yes | Flask secret key for sessions |
| `PORT` | No | Server port (default: 5000) |

---

## Usage

### Recording an Entry

1. Enter your security key
2. Write your idea (keep it under 250 characters)
3. Hit "Record Entry"

That's it. Your idea is saved and hidden away.

### Exporting to PDF

1. Click "Export to PDF"
2. Enter the PDF password
3. Select a year
4. Download your printable business cards

The PDF includes a summary page with stats, followed by pages of business-card-sized entries you can cut out.

---

## Troubleshooting

**Database reset (local SQLite):**
```bash
rm entries.db
python app.py
```

**Port conflict:**
```bash
PORT=5001 python app.py
```

**Vercel deployment issues:**
- Double-check your environment variables
- Make sure `USE_POSTGRES=true` is set
- Verify your Neon connection string includes `?sslmode=require`

