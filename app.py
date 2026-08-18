import json
import random
import string
from pathlib import Path
from datetime import datetime

import streamlit as st

DATABASE = Path(__file__).parent / "data.json"


# Data layer


def load_data():
    if DATABASE.exists():
        try:
            with open(DATABASE) as fs:
                return json.load(fs)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_data(data):
    with open(DATABASE, "w") as fs:
        json.dump(data, fs, indent=4)


def generate_account_number(data):
    while True:
        account = "".join(random.choices(string.digits, k=10))
        if not any(i["accountNo."] == account for i in data):
            return account


def find_account(data, acc_no, pin):
    for i in data:
        if i["accountNo."] == acc_no and i["pin"] == pin:
            return i
    return None


def log_transaction(account, kind, amount):
    account.setdefault("history", []).append(
        {
            "type": kind,
            "amount": amount,
            "balance_after": account["balance"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )



# Streamlit setup


st.set_page_config(page_title="Bank Management System", page_icon="🏦", layout="centered")

if "data" not in st.session_state:
    st.session_state.data = load_data()

if "authed_account" not in st.session_state:
    st.session_state.authed_account = None  # holds account dict once logged in for a session


def refresh():
    """Re-pull the in-memory account object after a save, so the UI reflects latest state."""
    if st.session_state.authed_account:
        acc_no = st.session_state.authed_account["accountNo."]
        for i in st.session_state.data:
            if i["accountNo."] == acc_no:
                st.session_state.authed_account = i
                break


st.title("🏦 Bank Management System")

menu = st.sidebar.radio(
    "Menu",
    [
        "Create Account",
        "Login",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Update Details",
        "Delete Account",
    ],
)

if st.session_state.authed_account:
    st.sidebar.success(f"Logged in as {st.session_state.authed_account['name']}")
    st.sidebar.write(f"Acc No: {st.session_state.authed_account['accountNo.']}")
    if st.sidebar.button("Log out"):
        st.session_state.authed_account = None
        st.rerun()


# Create Account


if menu == "Create Account":
    st.header("Create a New Account")

    with st.form("create_account_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        email = st.text_input("Email")
        pin = st.text_input("4-digit PIN", type="password", max_chars=4)
        initial_deposit = st.number_input("Initial Deposit (optional)", min_value=0, step=100)
        submitted = st.form_submit_button("Create Account")

    if submitted:
        errors = []
        if not name.strip():
            errors.append("Name cannot be empty.")
        if age < 18:
            errors.append("You must be 18 or older to open an account.")
        if not email.strip() or "@" not in email:
            errors.append("Please enter a valid email address.")
        if len(pin) != 4 or not pin.isdigit():
            errors.append("PIN must be exactly 4 digits.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            info = {
                "name": name.strip(),
                "age": int(age),
                "email": email.strip(),
                "pin": pin,
                "accountNo.": generate_account_number(st.session_state.data),
                "balance": int(initial_deposit),
                "history": [],
            }
            if initial_deposit:
                log_transaction(info, "Initial Deposit", int(initial_deposit))

            st.session_state.data.append(info)
            save_data(st.session_state.data)

            st.success("Account created successfully! Please note down your account number below.")
            st.info(f"**Account Number:** `{info['accountNo.']}`")
            with st.expander("Account Summary"):
                st.json({k: v for k, v in info.items() if k != "pin"})


# Login (used to gate deposit/withdraw/details/update/delete)


if menu == "Login":
    st.header("Login to Your Account")

    with st.form("login_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Login")

    if submitted:
        account = find_account(st.session_state.data, acc_no.strip(), pin.strip())
        if account:
            st.session_state.authed_account = account
            st.success(f"Welcome back, {account['name']}!")
            st.rerun()
        else:
            st.error("No matching account found. Check your account number and PIN.")


# Guard: everything below requires login


needs_login = menu in {
    "Deposit Money",
    "Withdraw Money",
    "Account Details",
    "Update Details",
    "Delete Account",
}

if needs_login and not st.session_state.authed_account:
    st.warning("Please log in first from the **Login** tab to access this feature.")
    st.stop()


# Deposit


if menu == "Deposit Money":
    st.header("Deposit Money")
    account = st.session_state.authed_account
    st.metric("Current Balance", f"₹{account['balance']:,}")

    with st.form("deposit_form", clear_on_submit=True):
        amount = st.number_input("Amount to Deposit", min_value=1, max_value=10000, step=100)
        submitted = st.form_submit_button("Deposit")

    if submitted:
        account["balance"] += int(amount)
        log_transaction(account, "Deposit", int(amount))
        save_data(st.session_state.data)
        refresh()
        st.success(f"Deposited ₹{amount:,} successfully!")
        st.metric("New Balance", f"₹{account['balance']:,}")


# Withdraw


if menu == "Withdraw Money":
    st.header("Withdraw Money")
    account = st.session_state.authed_account
    st.metric("Current Balance", f"₹{account['balance']:,}")

    with st.form("withdraw_form", clear_on_submit=True):
        amount = st.number_input("Amount to Withdraw", min_value=1, max_value=10000, step=100)
        submitted = st.form_submit_button("Withdraw")

    if submitted:
        if amount > account["balance"]:
            st.error("Insufficient balance for this withdrawal.")
        else:
            account["balance"] -= int(amount)
            log_transaction(account, "Withdrawal", -int(amount))
            save_data(st.session_state.data)
            refresh()
            st.success(f"Withdrew ₹{amount:,} successfully!")
            st.metric("New Balance", f"₹{account['balance']:,}")


# Details


if menu == "Account Details":
    st.header("Account Details")
    account = st.session_state.authed_account

    col1, col2 = st.columns(2)
    col1.metric("Name", account["name"])
    col2.metric("Balance", f"₹{account['balance']:,}")

    st.write(f"**Account Number:** {account['accountNo.']}")
    st.write(f"**Age:** {account['age']}")
    st.write(f"**Email:** {account['email']}")

    history = account.get("history", [])
    if history:
        st.subheader("Transaction History")
        st.dataframe(
            [
                {
                    "Date": h["timestamp"],
                    "Type": h["type"],
                    "Amount": h["amount"],
                    "Balance After": h["balance_after"],
                }
                for h in reversed(history)
            ],
            use_container_width=True,
        )
    else:
        st.caption("No transactions yet.")


# Update details


if menu == "Update Details":
    st.header("Update Account Details")
    account = st.session_state.authed_account
    st.caption("Age, account number, and balance cannot be changed here.")

    with st.form("update_form"):
        new_name = st.text_input("Name", value=account["name"])
        new_email = st.text_input("Email", value=account["email"])
        new_pin = st.text_input("New PIN (leave blank to keep current)", type="password", max_chars=4)
        submitted = st.form_submit_button("Save Changes")

    if submitted:
        if new_pin and (len(new_pin) != 4 or not new_pin.isdigit()):
            st.error("PIN must be exactly 4 digits.")
        elif not new_email.strip() or "@" not in new_email:
            st.error("Please enter a valid email address.")
        else:
            account["name"] = new_name.strip() or account["name"]
            account["email"] = new_email.strip()
            if new_pin:
                account["pin"] = new_pin
            save_data(st.session_state.data)
            refresh()
            st.success("Details updated successfully!")


# Delete account


if menu == "Delete Account":
    st.header("Delete Account")
    account = st.session_state.authed_account

    st.warning(f"You're about to permanently delete account **{account['accountNo.']}** "
               f"({account['name']}). This cannot be undone.")

    confirm = st.checkbox("I understand this action is permanent.")
    if st.button("Delete My Account", disabled=not confirm, type="primary"):
        st.session_state.data = [
            i for i in st.session_state.data if i["accountNo."] != account["accountNo."]
        ]
        save_data(st.session_state.data)
        st.session_state.authed_account = None
        st.success("Account deleted successfully.")
        st.rerun()