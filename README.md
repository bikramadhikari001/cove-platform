# Covenant Tracking Asset Management Platform

## Overview
The Covenant Tracking Asset Management Platform is a web application designed to assist asset managers in monitoring financial covenants within loan and bond documents. It provides automated compliance monitoring and alerts for potential breaches.

## Key Features
- User Authentication via Auth0
- Document Analysis using LLM for covenant extraction
- Automated covenant monitoring
- Compliance tracking
- Alert system for potential breaches

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Flask (Python)
- Authentication: Auth0
- Document Analysis: Language Learning Model (LLM)
- Version Control: Git

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd covenant-tracking-platform
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
AUTH0_DOMAIN=your_auth0_domain
AUTH0_CALLBACK_URL=http://localhost:5000/callback
AUTH0_LOGOUT_URL=http://localhost:5000/logout
```

5. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Project Structure
```
covenant-tracking-platform/
├── README.md
├── .gitignore
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/
│   │   ├── layout.html
│   │   ├── index.html
│   │   └── auth/
│   │       ├── login.html
│   │       └── signup.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
└── docs/
    └── CONTRIBUTING.md
```

## Contributing
Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License.
