# Village Problem Portal

A web-based platform where villagers can report local issues (infrastructure, health, water, education, etc.) and admins can track and manage them.

## Features

✨ **Villager Features:**
- 📝 Simple form to report problems
- 🏷️ Problem categorization (Infrastructure, Health, Water, Education, Other)
- 📞 Contact information submission (phone or email)
- ✅ Real-time form validation
- 📱 Mobile-friendly responsive design

✨ **Admin Features:**
- 📊 Dashboard to view all submitted problems
- 🔍 Filter by category and status
- 📋 Manage problem status (New, In Progress, Resolved)
- 🗑️ Delete problems
- 📄 Pagination support for large datasets

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **ORM:** SQLAlchemy

## Setup Instructions

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### 2. Clone or Download the Project
```bash
cd my_python_project
```

### 3. Create a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python main.py
```

The application will start on `http://localhost:5000`

### 6. Access the Portal
- **Villager Form:** http://localhost:5000/
- **Admin Dashboard:** http://localhost:5000/admin

## Project Structure

```
my_python_project/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   └── routes.py             # Flask routes and API endpoints
├── templates/
│   ├── submit.html           # Villager problem submission form
│   └── admin.html            # Admin dashboard
├── static/
│   ├── css/
│   │   └── style.css         # Global styling
│   └── js/
│       └── form.js           # Form validation and dashboard interactions
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── village_portal.db         # SQLite database (auto-created)
```

## Database Schema

### Problems Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| name | String | Villager's name |
| category | String | Problem category |
| description | Text | Problem description |
| contact | String | Phone or email |
| status | String | Current status (New, In Progress, Resolved) |
| created_at | DateTime | Submission timestamp |

## API Endpoints

### GET `/`
Displays the villager problem submission form.

### POST `/submit`
Submits a new problem.
- **Body:** Form data (name, category, description, contact)
- **Response:** JSON with success status

### GET `/admin`
Displays the admin dashboard with all problems.
- **Query Parameters:** 
  - `page` - Page number for pagination (default: 1)
  - `category` - Filter by category
  - `status` - Filter by status

### GET `/api/problems`
Get all problems as JSON.
- **Query Parameters:** Same as `/admin`
- **Response:** JSON array of problems

### PUT `/api/problems/<id>/status`
Update a problem's status.
- **Body:** JSON with status field
- **Response:** Success message

### DELETE `/api/problems/<id>`
Delete a problem.
- **Response:** Success message

## Form Validation

The submission form includes client-side validation:
- ✓ Name: Required, minimum 3 characters
- ✓ Category: Required selection
- ✓ Description: Required, minimum 10 characters
- ✓ Contact: Required, valid phone (10+ digits) or email format

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the last line in `main.py`:
```python
app.run(debug=True, port=8000)  # Use 8000 or another available port
```

### Database Issues
To reset the database, delete `village_portal.db` and restart the application.

### Virtual Environment Issues
If `source venv/bin/activate` doesn't work:
- **macOS/Linux:** Use `bash` instead of `zsh`, or use `source venv/bin/activate.csh`
- **Windows:** Use `venv\Scripts\activate.bat`

## Future Enhancements

🚀 Planned features:
- Admin authentication (login/password)
- Email notifications for admins
- Problem tracking reference number for villagers
- Export reports (PDF/CSV)
- Mobile app version
- Multi-language support
- Image attachments for problems
- Comments/notes on problems

## License

Open source - feel free to modify and use for your community.

## Support

For issues or questions, please contact the project maintainer.

---

**Built with ❤️ for village communities**
