# SLA-Generation
A Flask-based web application that automates the creation and management of Service Level Agreement (SLA) documents.
The system allows users to upload and verify documents, securely store them, and generate unique digital records for verification.

This project was developed to reduce manual paperwork, improve document verification, and provide a secure digital solution for SLA management.

# Features
1] User Authentication - Secure user login and registration
Passwords stored using hashing for security
 
2] Document Upload - Users can upload SLA-related documents
Files are stored securely on the server

3] Unique Document ID - Each uploaded document receives a unique identifier
Enables easy verification and tracking

4] Document Verification - Users can verify whether a document is valid or tampered
Helps maintain document authenticity

5] Secure Storage - Documents stored in a structured upload directory
Metadata stored in SQLite database

# Tech Stack
* Backend: Python, Flask
* Frontend: HTML, CSS, JavaScript
* Database: SQLite
* Authentication: Flask-Login, Password Hashing
* File Storage: Local server storage (Uploads folder)
* Unique Identification: UUID for document tracking

# Installation
* Clone the Repository
git clone https://github.com/yourusername/sla-generation-system.git
cd sla-generation-system
* Create Virtual Environment
python -m venv venv
Activate it:
Windows - venv\Scripts\activate
Mac/Linux - source venv/bin/activate
* Install Dependencies
pip install flask flask-login
* Run the Application
python app.py
* Then open:
http://localhost:5000

# Future Improvements

* Blockchain-based document verification
* Cloud storage integration
* AI-based document analysis
* Digital signature support
