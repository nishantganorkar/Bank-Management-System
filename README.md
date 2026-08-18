# 🏦 Bank Management System

A simple and user-friendly **Bank Management System** built with **Python, JSON, and Streamlit**.

This project provides both a **CLI-based banking system** and a **Streamlit web interface** for managing bank accounts and performing basic banking operations.

## 🚀 Features

### 👤 Account Management
- Create a new bank account
- Generate a unique 10-digit account number
- Age validation (18+)
- 4-digit PIN validation
- Update account details
- Delete an account

### 💰 Banking Operations
- Deposit money
- Withdraw money
- Check current balance
- Prevent withdrawal when balance is insufficient
- Deposit/withdrawal limit of ₹10,000

### 🔐 Authentication
- Login using Account Number and PIN
- Session-based authentication in Streamlit
- Protected banking operations

### 📊 Transaction Management
- Transaction history
- Transaction type
- Transaction amount
- Balance after transaction
- Transaction timestamp

### 💾 Data Storage
- Account data stored in `data.json`
- Automatic data saving after every operation
- JSON-based lightweight data persistence

### 🌐 Streamlit Web Interface
- Interactive web-based UI
- Sidebar navigation
- Account creation form
- Login system
- Deposit and withdrawal forms
- Account details dashboard
- Update account information
- Delete account functionality
- Transaction history table

---

## 🛠️ Technologies Used

- **Python**
- **JSON**
- **Pathlib**
- **Random**
- **String**
- **Datetime**
- **Streamlit**

---

## 📂 Project Structure

```text
Bank-Management-System/
│
├── app.py
├── main.py
├── data.json
├── README.md
└── requirements.txt
