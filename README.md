<h1 align="center">Password Vault (Fernet Encryption) 🔐🐍</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Cryptography-Fernet-green?style=for-the-badge"/>
</div>

---

## 📌 Overview
The Password Vault is a secure, local management tool designed to store and protect sensitive credentials through industrial-grade encryption. By leveraging Fernet symmetric encryption and real-time security protocols, this application ensures that data remains inaccessible without the correct master password.

---

## ⚙️ Core Features
* **Master Password Key Derivation:** Employs SHA-256 hashing to derive a unique 32-byte encryption key from the user's master password, ensuring that credentials are never stored in plain text.
* **Real-Time Strength Analytics:** Features an integrated password strength checker that evaluates character variety (digits, symbols, uppercase) and length as you type.
* **Automated Security Timers:** Includes a 120-second inactivity lock that terminates the session and a 15-second clipboard clearing mechanism to prevent data leakage.
* **Vault Management:** Supports full search functionality within the encrypted database, secure on-demand decryption, and JSON-based import/export for backups.

---

## 🚀 Setup & Usage

### 1. Installation
Clone the repository and install the required dependencies:
pip install cryptography pyperclip

### 2. Running the Vault
Launch the application by running the main script. You will be prompted for a master password to unlock or initialize your vault:
python password-manager/main.py

### 3. Storage & Privacy
Your credentials are encrypted and stored locally in `password-manager/data.json`. It is highly recommended to add this file to your `.gitignore` to prevent your personal data from being committed to version control.

---

**Maintained by [baldyachty](https://github.com/baldyachty)**
