from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')

# Business card dimensions (US standard: 3.5" x 2")
CARD_WIDTH = 3.5 * inch
CARD_HEIGHT = 2.0 * inch
MAX_TEXT_LENGTH = 250

# Get authorized keys from environment variables
USER_KEY_1 = os.environ.get('USER_KEY_1', 'change-me-key-1')
USER_KEY_2 = os.environ.get('USER_KEY_2', 'change-me-key-2')

# PDF export password
PDF_PASSWORD = os.environ.get('PDF_PASSWORD', 'change-me-pdf-password')

# User display names for PDF
USER_NAMES = {
    'user1': 'Cale',
    'user2': 'Carolyn'
}

DATABASE = 'entries.db'


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            user_key TEXT NOT NULL,
            entry_date DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def validate_key(key):
    """Validate if the provided key matches one of the authorized keys"""
    if key == USER_KEY_1:
        return 'user1'
    elif key == USER_KEY_2:
        return 'user2'
    return None


@app.route('/')
def index():
    """Display the entry form"""
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_entry():
    """Handle entry submission"""
    text = request.form.get('text', '').strip()
    key = request.form.get('key', '').strip()
    
    # Validation
    if not text:
        flash('Please enter your daily idea.', 'error')
        return redirect(url_for('index'))
    
    if not key:
        flash('Please enter your security key.', 'error')
        return redirect(url_for('index'))
    
    if len(text) > MAX_TEXT_LENGTH:
        flash(f'Entry is too long. Maximum {MAX_TEXT_LENGTH} characters.', 'error')
        return redirect(url_for('index'))
    
    # Validate key
    user = validate_key(key)
    if not user:
        flash('Invalid security key.', 'error')
        return redirect(url_for('index'))
    
    # Store entry
    try:
        conn = get_db()
        conn.execute(
            'INSERT INTO entries (text, user_key, entry_date) VALUES (?, ?, ?)',
            (text, user, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        flash('Entry recorded successfully!', 'success')
    except Exception as e:
        flash('Error saving entry. Please try again.', 'error')
    
    return redirect(url_for('index'))


@app.route('/export', methods=['GET', 'POST'])
def export_pdf():
    """Handle PDF export with password protection"""
    if request.method == 'GET':
        # Show password form with current year selected
        current_year = datetime.now().year
        return render_template('export_password.html', current_year=current_year)
    
    # POST - verify password and generate PDF
    password = request.form.get('password', '').strip()
    year_str = request.form.get('year', '').strip()
    
    # Validate password
    if password != PDF_PASSWORD:
        flash('Invalid password. Access denied.', 'error')
        current_year = datetime.now().year
        return render_template('export_password.html', current_year=current_year)
    
    # Validate year
    try:
        year = int(year_str)
        if year < 2024 or year > 2099:
            flash('Year must be between 2024 and 2099.', 'error')
            current_year = datetime.now().year
            return render_template('export_password.html', current_year=current_year)
    except (ValueError, TypeError):
        flash('Invalid year selected.', 'error')
        current_year = datetime.now().year
        return render_template('export_password.html', current_year=current_year)
    
    return generate_pdf(year)


def generate_pdf(year=None):
    """Generate and download PDF with entries filtered by year"""
    try:
        conn = get_db()
        
        # Filter entries by year if specified
        if year:
            # Get entries from the specified year
            # entry_date is stored as ISO format: YYYY-MM-DDTHH:MM:SS.ffffff
            year_start = f'{year}-01-01T00:00:00'
            year_end = f'{year}-12-31T23:59:59.999999'
            entries = conn.execute(
                'SELECT * FROM entries WHERE entry_date >= ? AND entry_date <= ? ORDER BY entry_date ASC',
                (year_start, year_end)
            ).fetchall()
        else:
            # Get all entries (fallback)
            entries = conn.execute(
                'SELECT * FROM entries ORDER BY entry_date ASC'
            ).fetchall()
        
        conn.close()
        
        if not entries:
            year_msg = f' for year {year}' if year else ''
            flash(f'No entries to export{year_msg}.', 'error')
            return redirect(url_for('index'))
        
        # Create PDF in memory
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        page_width, page_height = letter
        
        # Calculate cards per page (accounting for margins)
        # Letter size: 8.5" x 11"
        # Business cards: 3.5" x 2"
        margin = 0.25 * inch
        usable_width = page_width - (2 * margin)
        usable_height = page_height - (2 * margin)
        
        cards_per_row = int(usable_width / CARD_WIDTH)
        cards_per_col = int(usable_height / CARD_HEIGHT)
        cards_per_page = cards_per_row * cards_per_col
        
        # Calculate spacing to evenly distribute cards
        total_cards_width = cards_per_row * CARD_WIDTH
        total_cards_height = cards_per_col * CARD_HEIGHT
        
        # Horizontal spacing: distribute remaining space evenly
        if cards_per_row > 1:
            remaining_width = usable_width - total_cards_width
            h_spacing = remaining_width / (cards_per_row + 1)
        else:
            h_spacing = (usable_width - CARD_WIDTH) / 2  # Center single card
        
        # Vertical spacing: distribute remaining space evenly, with minimum spacing
        if cards_per_col > 1:
            remaining_height = usable_height - total_cards_height
            v_spacing = remaining_height / (cards_per_col + 1)
            # Ensure minimum spacing to prevent overlap
            min_v_spacing = 0.1 * inch
            if v_spacing < min_v_spacing:
                # Recalculate with minimum spacing
                total_needed_height = total_cards_height + (min_v_spacing * (cards_per_col - 1))
                if total_needed_height <= usable_height:
                    v_spacing = min_v_spacing
                else:
                    v_spacing = (usable_height - total_cards_height) / (cards_per_col + 1)
        else:
            v_spacing = (usable_height - CARD_HEIGHT) / 2  # Center single card
        
        # Add summary page
        pdf.setFont("Helvetica-Bold", 24)
        title = f"Daily Ideas Archive - {year}" if year else "Daily Ideas Archive"
        pdf.drawString(margin, page_height - margin - 40, title)
        
        pdf.setFont("Helvetica", 14)
        y_pos = page_height - margin - 80
        
        total_entries = len(entries)
        user1_count = sum(1 for e in entries if e['user_key'] == 'user1')
        user2_count = sum(1 for e in entries if e['user_key'] == 'user2')
        
        # Get date range
        dates = [datetime.fromisoformat(e['entry_date']) for e in entries]
        if dates:
            first_date = min(dates).strftime('%B %d, %Y')
            last_date = max(dates).strftime('%B %d, %Y')
        else:
            first_date = last_date = 'N/A'
        
        summary_lines = [
            f"Year: {year}" if year else "All Years",
            f"Total Entries: {total_entries}",
            f"{USER_NAMES.get('user1', 'User 1')} Entries: {user1_count}",
            f"{USER_NAMES.get('user2', 'User 2')} Entries: {user2_count}",
            f"Date Range: {first_date} to {last_date}",
            "",
            "Each card contains:",
            "- Entry text",
            "- Date",
            "- Author name"
        ]
        
        for line in summary_lines:
            pdf.drawString(margin, y_pos, line)
            y_pos -= 20
        
        pdf.showPage()
        
        # Generate business cards
        card_index = 0
        for entry in entries:
            if card_index > 0 and card_index % cards_per_page == 0:
                pdf.showPage()
            
            # Calculate position on page with proper spacing
            row = (card_index % cards_per_page) // cards_per_row
            col = (card_index % cards_per_page) % cards_per_row
            
            # Position from top-left of usable area, accounting for spacing
            x = margin + h_spacing + col * (CARD_WIDTH + h_spacing)
            y = page_height - margin - v_spacing - (row + 1) * CARD_HEIGHT - row * v_spacing
            
            # Draw card border
            pdf.rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            
            # Add content
            text_x = x + 0.2 * inch
            text_y = y + CARD_HEIGHT - 0.3 * inch
            
            # Entry text (with word wrapping)
            pdf.setFont("Helvetica", 10)
            text_lines = []
            words = entry['text'].split()
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if pdf.stringWidth(test_line, "Helvetica", 10) <= CARD_WIDTH - 0.4 * inch:
                    current_line = test_line
                else:
                    if current_line:
                        text_lines.append(current_line)
                    current_line = word
            
            if current_line:
                text_lines.append(current_line)
            
            # Draw text lines (limit to fit on card)
            max_lines = 8
            for i, line in enumerate(text_lines[:max_lines]):
                pdf.drawString(text_x, text_y - (i * 12), line)
            
            # Add date and author name at bottom
            entry_date = datetime.fromisoformat(entry['entry_date'])
            date_str = entry_date.strftime('%m/%d/%Y')
            author_name = USER_NAMES.get(entry['user_key'], entry['user_key'])
            
            pdf.setFont("Helvetica", 8)
            pdf.drawString(text_x, y + 0.2 * inch, date_str)
            pdf.drawString(text_x, y + 0.1 * inch, f"By: {author_name}")
            
            card_index += 1
        
        pdf.save()
        buffer.seek(0)
        
        # Include year in filename if filtering by year
        if year:
            filename = f"daily_ideas_{year}.pdf"
        else:
            filename = f"daily_ideas_{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)
        
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

