# Crime Management System

## Overview

This is a comprehensive web application for crime management and reporting, built using Flask and MySQL. The system provides features for users and police personnel to  SOS ,  register complaints, track criminals, and analyze crime data.

## Features

### User Features
- User Registration
- View Criminals Database
- Register Complaints
- SOS Location Tracking
- Complaint Submission with Photo/Video Evidence
- Encrypted Data Storage

### Police Features
- View SOS Locations
- View and Manage Criminals Database
- View and Update Complaint Statuses
- Crime Data Visualization

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Encryption**: Fernet Encryption
- **Data Visualization**: Matplotlib
- **Additional Libraries**: 
  - mysql-connector-python
  - pandas
  - cryptography
  - python-dotenv

## Prerequisites

- Python 3.8+
- MySQL Server
- FFmpeg (for video conversion)
- Required Python Packages (see `requirements.txt`)

## Installation Steps

1. Clone the repository
```bash
git clone https://github.com/your-username/crime-management-system.git
cd crime-management-system
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file with the following:
```
SECRET_KEY=your_secret_key
FERNET_KEY=your_fernet_encryption_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
```

5. Set up MySQL Database
```sql
CREATE DATABASE crime;
USE crime;
-- Run database setup scripts for creating necessary tables
```

## Configuration

- Database Connection: Configured in `dbconnection()` function
- Secret Key: Loaded from environment variables
- Encryption: Uses Fernet symmetric encryption

## Key Components

### Routes
- `/`: Home page
- `/login`: User/Police authentication
- `/userregister`: User registration
- `/complaintreg`: Complaint registration
- `/crimerates`: Crime data visualization

### Security Features
- User authentication
- Data encryption at rest
- Secure file uploads
- Environment-based configuration

## Running the Application

```bash
python app.py
```

Access the application at `http://localhost:5000`

## Data Privacy

- All sensitive information is encrypted using Fernet symmetric encryption
- Supports secure storage of complaint details, personal information

## Visualization Features

- Generates graphs for:
  - Property stolen vs recovered
  - Property recovery value
  - Rape victims by age group

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.



