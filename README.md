# BattleRoster

**Author:** Tyler Worth

- GitHub: [@CutbackTG](https://github.com/CutbackTG)
- Project Link: [https://github.com/CutbackTG/BattleRoster](https://github.com/CutbackTG/BattleRoster)
- Deployment URL: https://cutbacktg.github.io/BattleRoster/ 

BattleRoster is a Django-based web application designed to streamline tabletop game management for both players and dungeon masters. Players can easily create, edit, and organize their character sheets, while dungeon masters can oversee groups, manage player sheets, and coordinate campaigns.

Built with extensibility in mind, the system supports modular character sheet templates, making it adaptable for multiple game systems such as Dungeons & Dragons or BattleTech. The site emphasizes usability with responsive design, lightweight interactivity, and secure role-based permissions to protect player data.

## 🎯 Features

### User Roles & Authentication
- **Player Account:** Create, edit, and delete own character sheets; invite others to groups
- **Dungeon Master Account:** Manage all sheets in their group; send group invites
- **Authentication:** Extended Django User model with role-based permissions (Player, DM)

### Character Sheet Management
- Full CRUD operations for character sheets
- Fields include Name, Race, Class, Stats, Equipment, and more
- Save individual field values dynamically
- Support for multiple character sheets per player account

### Group System
- Groups contain one Dungeon Master and multiple Players
- Group invites via email or username
- **Permissions:** Players manage their own sheets; DMs manage all sheets in their group

### Game System Extensibility
- Modular character sheet templates for different game systems
- Currently supports D&D 5e with plans for BattleTech and other systems
- Easy-to-extend template system for adding new game types

### Future Features
- Real-time chat integration
- Built-in dice rolling tools
- Campaign notes and session logs
- Character sheet export options (PDF, JSON)
- Mobile app companion

## 🛠️ Tech Stack

- **Backend:** Django 5.2.7, Python 3.12+
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Database:** SQLite (development), PostgreSQL (production recommended)
- **APIs:** Google Sheets API integration
- **Authentication:** Django's built-in auth with custom user roles
- **Version Control:** Git & GitHub

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.12 or higher
- pip (Python package manager)
- Git
- A code editor (VS Code, PyCharm, etc.)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/CutbackTG/BattleRoster.git
cd BattleRoster
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist yet, install the core dependencies:
```bash
pip install django==5.2.7
pip install google-auth google-auth-oauthlib google-api-python-client
```

Then create the requirements file:
```bash
pip freeze > requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=your-database-url

# Google API (if using Google Sheets integration)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

**Important:** Never commit your `.env` file to Git!

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

### 8. Access the Admin Panel

Visit: **http://127.0.0.1:8000/admin/**
Login with your superuser credentials.

## 📁 Project Structure

```
BattleRoster/
├── battleroster_project/       # Main Django project settings
│   ├── __init__.py
│   ├── settings.py            # Project configuration
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI server config
│   └── asgi.py                # ASGI server config
│
├── accounts/                   # User authentication & profiles
│   ├── models.py              # User model extensions
│   ├── views.py               # Login, registration views
│   ├── urls.py
│   └── templates/
│
├── game_characters/            # Character management
│   ├── models.py              # Character model
│   ├── views.py               # CRUD operations
│   ├── forms.py
│   └── templates/
│
├── sheets/                     # Character sheets
│   ├── models.py              # Sheet templates
│   ├── views.py               # Sheet rendering
│   ├── google_client.py       # Google Sheets integration
│   └── templates/
│
├── static/                     # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                  # Base templates
│   └── base.html
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in Git)
├── .gitignore                 # Git ignore rules
└── README.md                   # This file
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Run tests for a specific app:
```bash
python manage.py test accounts
python manage.py test game_characters
```

## 🌐 Deployment

BattleRoster is a Django application and requires a Python-capable hosting platform. **GitHub Pages will NOT work** as it only hosts static files.

### Recommended Deployment Platforms:

1. **Heroku** (Easy, free tier available)
   - [Heroku Django Deployment Guide](https://devcenter.heroku.com/articles/django-app-configuration)

2. **PythonAnywhere** (Great for beginners)
   - [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)

3. **Railway** (Modern, simple)
   - [Railway Django Guide](https://docs.railway.app/guides/django)

4. **Render** (Free tier available)
   - [Render Django Deployment](https://render.com/docs/deploy-django)

5. **DigitalOcean** (More control, requires server management)
   - [DigitalOcean Django Guide](https://www.digitalocean.com/community/tutorials/how-to-deploy-django)

### Pre-Deployment Checklist:

- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up a production database (PostgreSQL recommended)
- [ ] Configure static file serving (`collectstatic`)
- [ ] Set up environment variables securely
- [ ] Enable HTTPS/SSL
- [ ] Set up proper SECRET_KEY management

## 🔒 Security Notes

- Never commit `.env` files or sensitive credentials
- Always use environment variables for secrets
- Keep `DEBUG=False` in production
- Use strong `SECRET_KEY` values
- Implement CSRF protection (Django default)
- Use HTTPS in production

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/BattleRoster.git
   ```
3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "Add: description of your feature"
   ```
5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a Pull Request** with a clear description of your changes

### Contribution Guidelines:
- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Keep pull requests focused on a single feature/fix

## 🐛 Known Issues

- Google Sheets integration requires OAuth setup
- Mobile responsiveness needs improvement in some views
- Character sheet templates need additional game system support

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- **Code Institute** - For guidance and support throughout development
- **Django Documentation** - Comprehensive framework documentation
- **Bootstrap** - Frontend component library
- The tabletop gaming community for inspiration

---

**Happy Gaming! 🎲**