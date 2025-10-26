# BattleRoster

**Author:** Tyler Worth

<img src= static/images/readme_images/amiresponsive.png  alt ="Am I responsive image portraying website view on multiple devices" width= 800>

- GitHub: [@CutbackTG](https://github.com/CutbackTG)
- Project Link: [https://github.com/CutbackTG/BattleRoster](https://github.com/CutbackTG/BattleRoster)
- Deployment URL: https://battlerosterhost-e22dbecc83dc.herokuapp.com/

BattleRoster is a Django-based web application designed to streamline tabletop game management for both players and dungeon masters. Players can easily create, edit, and organize their character sheets, while dungeon masters can oversee groups, manage player sheets, and coordinate campaigns.

Built with extensibility in mind, the system supports modular character sheet templates, making it adaptable for multiple game systems such as Dungeons & Dragons or BattleTech. The site emphasizes usability with responsive design, lightweight interactivity, and secure role-based permissions to protect player data.

## Features

### User Roles & Authentication
- **Player Account:** Create, edit, and delete own character sheets; invite others to groups
- **Dungeon Master Account:** Manage all sheets in their group; send group invites
- **Authentication:** Extended Django User model with role-based permissions (Player, DM)

### Character Sheet Management
- Full CRUD operations for character sheets
- Fields include Name, Race, Class, Stats, Equipment, and more
- Save individual field values dynamically
- Support for multiple character sheets per player account

### Party System
- Parties contain one Dungeon Master and multiple Players
- Party invites via email or username
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

## Tech Stack

### **Backend**
- **Python 3.12+** – Core programming language  
- **Django 5.2.7** – Web framework for routing, models, templates, and ORM  
- **SQLite** – Default development database

### **Frontend**
- **HTML5** and **CSS3** – Base template structure and styling  
- **Bootstrap 5** – Responsive and consistent UI framework  
- **JavaScript (Vanilla JS)** – Client-side interactivity  
- **Django Template Language (DTL)** – Server-side rendering for dynamic content

### **Authentication & Authorization**
- **Django’s built-in auth system** – Handles user accounts, sessions, and permissions  
- **Custom roles:**
  - *Player* – Owns Characters  
  - *Dungeon Master* – Manages Parties

### **Core Features**
- Character management (CRUD using Django models and forms)  
- Party management (Many-to-Many relationships between Characters and Parties)  
- Local character sheets stored in the database  
- Role-based relationships between Players, Characters, and DMs  

### **Development & Tooling**
- **Virtual Environment (`venv`)** – Isolated development environment  
- **pip** – Python package management  
- **Git & GitHub** – Version control and collaboration  
- **dotenv / python-decouple** – Secure environment variable management  
- **pytest / Django TestCase** – Automated testing framework

### **Deployment**
- **Gunicorn / Daphne (optional)** – WSGI/ASGI servers for production  
- **Heroku / Render / Railway / PythonAnywhere** – Supported hosting options  
- **Whitenoise** – Static file management for production

## User Stories

### 1. New User — Quick Character Creator
As a **new visitor**,  
I want to **create a single character sheet without signing up**,  
so that I can quickly test the tool or make a one-off character for a session.

### 2. New User — Player Building Multiple Characters
As a **new registered player**,  
I want to **sign up and create multiple characters**,  
so that I can prepare for different campaigns and track their progress in one place.

### 3. Dungeon Master — Managing Parties and Campaigns
As a **Dungeon Master**,  
I want to **create and manage parties of players**,  
so that I can keep an eye on each player’s character sheets and view their stats during gameplay.

### 4. Experienced D&D Player — Multi-Party Management
As an **experienced player**,  
I want to **build several characters and assign them to different parties**,  
so that I can easily switch between campaigns and coordinate with different groups of friends.

### 5. Returning User — Accessing Saved Characters
As a **returning user**,  
I want to **log back into my account and access all my previously saved characters and parties**,  
so that I can pick up where I left off without recreating my data.

### Table of expectations

| **Persona** | **Description** | **Primary Goals** | **Key Actions in BattleRoster** |
|--------------|-----------------|-------------------|----------------------------------|
| **Guest User** | A first-time visitor who doesn’t want to sign up yet but wants to try out the tool. | Quickly create a one-off character sheet for a session or test the system. | - Use the quick character creator<br>- Export or save locally if available |
| **New Player** | A beginner who registers to manage multiple characters. | Build and store multiple character sheets for different games. | - Sign up<br>- Create and edit characters<br>- View saved characters |
| **Dungeon Master (DM)** | A game organizer who runs campaigns and manages parties. | Oversee multiple parties and monitor players’ character stats during gameplay. | - Create and manage parties<br>- Add or view player characters<br>- Track stats during sessions |
| **Experienced Player** | A long-time D&D player involved in several parties or campaigns. | Manage a roster of characters for multiple groups and easily switch between them. | - Create multiple characters<br>- Assign characters to different parties<br>- Manage party compositions |
| **Returning User** | A previous user returning to continue gameplay. | Retrieve and update saved data without starting over. | - Log in<br>- View and edit saved characters<br>- Rejoin or create new parties |

## Battleroster Entity Relationship Diagram

<img src= static/images/readme_images/battleroster_erd.png  alt ="ERD for the battleroster project" width= 800>

The Entity Relationship Diagram (ERD) outlines the central database structure for the BattleRoster project and the relationships that exist between users, characters, and parties.

There are two main types of users — Players and Dungeon Masters (DMs) — both of which are based on Django's built-in user model.

User (Player) records represent ordinary players that can create and maintain multiple Characters. Each Character will include characteristics such as name, level, race, class type, health, mana, and equipment, and can be associated back to its owner (the player) through a Foreign Key (player_id).

User (Dungeon Master) records represent users responsible for creating game sessions and for the Parties. Each Party will have its own unique ID, a Foreign Key (dungeon_master_id) that associates it with the DM that created it, and set up with a Many-To-Many relationship to multiple Characters (their members). This arrangement will allow one DM to run several parties, and each party to have several player characters. 

Extra local versions of users and characters are also created — User (local) and Character (local). These represent offline or stand-alone character sheets that can exist without an account as an online registered user. The local entities will use the same structure as those that are created online, but link only to the owner instead of an authenticated user, using the owner_id Foreign Key.

## Url to View Map

| **URL Pattern**                      | **View Function**        | **Name**                 | **Purpose / Description**                                                                           |
| ------------------------------------ | ------------------------ | ------------------------ | --------------------------------------------------------------------------------------------------- |
| `/characters/`                       | `characters_view`        | `characters`             | Main character list and creation page. Displays all characters for a player or all players (if DM). |
| `/characters/<int:pk>/`              | `characters_view`        | `character_edit`         | Edit an existing character’s sheet.                                                                 |
| `/characters/delete/<int:pk>/`       | `character_delete`       | `character_delete`       | Delete a character (player or DM permissions).                                                      |
| `/characters/party/`                 | `party_view`             | `party`                  | Displays either the DM party dashboard or the player’s current party view.                          |
| `/characters/party/<int:pk>/`        | `party_detail`           | `party_detail`           | Shows detailed info about a specific party, including all member characters.                        |
| `/characters/party/<int:pk>/remove/` | `party_remove_member`    | `party_remove_member`    | Remove a member from a party (DM or authorized member).                                             |
| `/characters/party/<int:pk>/invite/` | `party_invite`           | `party_invite`           | Invite another user to join a party.                                                                |
| `/characters/party/<int:pk>/select/` | `party_select_character` | `party_select_character` | Players select which of their characters to use in the current party.                               |
| `/characters/dm/parties/`            | `dm_party_list`          | `dm_party_list`          | Dungeon Master dashboard — view, create, or delete managed parties.                                 |


## BattleRoster Test Documentation

### Lighthouse Scores & W3C Validation checks

Homepage index.html

<img src= static\images\readme_images\Lighthouse_score_index.png  alt ="index.html lighthouse score" width= 600>

<img src= static\images\readme_images\W3c_test_index.png alt ="index.html W3C valiadation check" width= 600>

characters.html

<img src= static\images\readme_images\Lighthouse_score_characters.png alt ="characters.html lighthouse score" width= 600>

<img src= static\images\readme_images\W3c_test_characters.png  alt ="charcters.html W3C valiadation check" width= 600>

signup_login.html

<img src= static\images\readme_images\Lighthouse_score_signup.png alt ="signup_login.html lighthouse score" width= 600>

<img src= static\images\readme_images\W3c_test_party.png alt ="party.html W3C valiadation check" width= 600>

contact.html

<img src= static\images\readme_images\Lighthouse_score_contact.png alt ="contact.html lighthouse score" width= 600>

<img src= static\images\readme_images\W3c_test_contact.png alt ="contact.html W3C valiadation check" width= 600>

### Test Runs

| Issue / Feature | Test | Result / Fix |
|------------------|-------|---------------|
| User Registration & Login | Register new users (Player & DM) via `/register/`, log in and out, test session persistence. | Works as expected. If login fails, verify `AUTH_USER_MODEL` and session middleware in `settings.py`. |
| Character Creation | Add a new Character from Player account — ensure all attributes (name, level, race, stats, etc.) save correctly. | Data saves correctly. If failure occurs, check model `Character` and form validation fields. |
| Character Ownership | Verify each Character links to its Player (`ForeignKey` relationship). Ensure Player can only view their own characters. | Access not restricted — add view filtering: `Character.objects.filter(player=request.user)`. |
| Party Creation | Create Party as Dungeon Master; confirm Party is linked to correct DM and visible in DM’s dashboard. | Works. If Party not linking, confirm `dungeon_master` field in `Party` form uses `request.user`. |
| Party Membership | Add multiple Characters to a Party (ManyToMany). Ensure changes reflect for all members. | Characters not updating in reverse relation — ensure `related_name='members'` or call `.save_m2m()`. |
| CharacterLocal Save | Create and update local characters. Test ownership restriction (only owner can modify/delete). | Works. If unauthorized edits occur, add object-level permission check. |
| Data Persistence | Restart app and confirm characters, parties, and users persist (SQLite DB check). | Works. If lost data, verify DB path and migrations (`python manage.py migrate`). |
| Dice Roller (if used) | Simulate dice rolls (e.g., `/roll/1d20/`) and confirm correct random generation. | Values not random — check randomization function or seed reset. |
| UI Rendering | Load templates for dashboard, character sheets, and party list; verify all pages render without error. | Templates render. Fix missing static files with `python manage.py collectstatic`. |
| Error Handling | Submit invalid form data (e.g., missing name, negative level) and confirm validation errors appear. | Validation messages display correctly. |
| Security | Try accessing another user’s character or party via URL ID. Should return 403 or redirect. | Data leak risk — add user ownership checks in views. |
| Deployment Check | Run on production environment (Heroku or similar). Verify DB connections and media/static paths. | Static files not loading — update `STATIC_ROOT` and add `whitenoise`. |

### Automated Test Cases (Django / Pytest)

| Area | Test | Expected Result |
|-------|-------|----------------|
| Models: Character | Create a `Character` object and verify default stats (e.g. level=1, health=100). | Character created successfully with expected default values. |
| Models: Party | Add multiple Characters to a Party (ManyToMany). | All related Characters appear in `party.members.all()`. |
| Models: CharacterLocal | Create and update local character, ensure ownership is correctly linked. | Object saves and retrieves correctly under `owner`. |
| Views: Character List | Access character list endpoint while logged in as Player. | Only that Player’s Characters are returned in the response context. |
| Views: Party Detail | Access Party detail as the Dungeon Master. | Page loads with correct members; unauthorized users receive 403. |
| Forms: CharacterForm | Submit form with valid and invalid data. | Valid data saves successfully; invalid data raises `form.errors`. |
| Auth: Registration | POST to `/register/` with new credentials. | User created; redirected to dashboard or login page. |
| Auth: Login / Logout | Login with valid credentials; logout; access restricted pages. | Authenticated views accessible when logged in; denied after logout. |
| Permissions | Try editing another Player’s Character via direct URL. | Forbidden (403) response or redirect to home. |
| Templates | Render core templates (character list, party view, dashboard). | All templates render without errors using `TemplateResponse`. |
| Dice Roller Utility | Call dice roll function (e.g., `roll_dice('1d20')`). | Returns random integer within correct range; never outside dice bounds. |
| Database Integrity | Run migrations and ensure models create properly. | No migration or schema errors on `python manage.py makemigrations` and `migrate`. |

## UI & UX Design

### Wireframes

Homepage
<img src= static\images\readme_images\homepage_concept.png alt ="homepage wireframe concept" width= 300>

Characters
<img src= static\images\readme_images\characters_concept.png alt ="Characters wireframe concept" width= 300>

Signup/ Login
<img src= static\images\readme_images\signup_concept.png alt ="signup/ login wireframe concept" width= 300>

Contact
<img src= static\images\readme_images\contact_concept.png alt ="Contact wireframe concept" width= 300>

### Colour Scheme

A simple, bold and striking colour scheme was chosen, gold accents and warm browns add to the effect of gold on wood and chests of gold, a goal for many role-players and one that fits with the Dungeons & Dragons game.

<img src= static\images\readme_images\colour_scheme.png alt ="Battleroster colour scheme" width= 600>

I tested this scheme on Huemint to see its overall appearance and experiment with alternatives, it was here that I decided to add some browns here and there throughout to break through the colder, more warning colours of the plain black and yellow.

<img src= static\images\readme_images\huemint_scheme.png alt ="Testing colour scheme on Huemint." width= 800>

## Installation & Deployment

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher  
- pip (Python package manager)  
- Git  
- A code editor (VS Code, PyCharm, etc.)

## Installation & Setup

### 1.Clone the Repository

```bash
git clone https://github.com/CutbackTG/BattleRoster.git
cd BattleRoster
```
### 2.Create a virtual environment

Windows:
``` bash
python -m venv .venv
.venv\Scripts\activate
```
Mac/Linux:
``` bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3.Install Dependencies
``` bash
pip install -r requirements.txt
```
If requirements.txt doesn't exist yet, install Django manually:
``` bash
pip install django==5.2.7
pip freeze > requirements.txt
```
### Environment Variables
Create a .env file in the project root:

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

### Database configuration (for production)
DATABASE_URL=your-database-url

### Database Setup
Run the following commands to prepare your database:
``` bash
python manage.py makemigrations
python manage.py migrate
```
### Create a Superuser
``` bash
python manage.py createsuperuser
```
### Run the Development Server
``` bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

### Access the Admin Panel

Visit: http://127.0.0.1:8000/admin/
Login with your superuser credentials.

### Project Structure

<img src= static/images/readme_images/project_structure.png  alt ="a diagram outlaying the project folder structure" width= 800>

### Testing
Run the full test suite:
``` bash
python manage.py test
```
Run tests for a specific app:
``` bash
python manage.py test accounts
python manage.py test game_characters
```
### Deployment

BattleRoster is a Django application and requires a Python-capable hosting platform.
GitHub Pages will NOT work, as it only hosts static files.

Recommended Deployment Platforms:
Heroku
PythonAnywhere
Render
Railway

### Pre-Deployment Checklist

 Set DEBUG=False in production
 Configure ALLOWED_HOSTS
 Set up a production database (PostgreSQL recommended)
 Configure static file serving (collectstatic)
 Set up environment variables securely
 Enable HTTPS/SSL
 Use a strong SECRET_KEY

 ### Contributing

 Contributions are welcome, please follow the following steps to help develop BattleRoster.

### Fork the repository

Clone your fork:
``` bash
git clone https://github.com/YOUR-USERNAME/BattleRoster.git
```

### Create a feature branch:
``` bash
git checkout -b feature/your-feature-name
```
### Make your changes and commit:
``` bash
git add .
git commit -m "Add: description of your feature"
```
### Push to your fork:
``` bash
git push origin feature/your-feature-name
```
Submit a Pull Request with a clear description of your changes

### Contribution Guidelines

Follow PEP 8 style guide for Python code
Write clear commit messages
Add tests for new features
Update documentation as needed
Keep pull requests focused on a single feature/fix
