#!/bin/bash

# Set the server URL
SERVER_URL="http://10.250.60.58:8000"

# Function to register a new user
register_user() {
  local username="$1"
  local password="$2"
  local repeat_password="$3"

  # Create a JSON request body
  local json_data="{\"username\":\"$username\",\"password\":\"$password\",\"repeat_password\":\"$repeat_password\"}"

  curl -X POST "$SERVER_URL/register" -H "Content-Type: application/json" -d "$json_data"
}

# Function to login and get a token
login_user() {
  local username="$1"
  local password="$2"

  local token
  token=$(curl -X POST "$SERVER_URL/login" -d "username=$username" -d "password=$password")
  echo "Login successful. Token: $token"
}

# Function to logout using a token
logout_user() {
  local token="$1"

  curl -X POST "$SERVER_URL/logout?token=$token"
}

# Main script
while true; do
  clear
  echo "=== FastAPI Server Interaction ==="
  echo "1. Register a new user"
  echo "2. Login"
  echo "3. Logout"
  echo "4. Exit"

  read -p "Enter your choice: " choice
  case $choice in
    1)
      read -p "Enter username: " username
      read -sp "Enter password: " password
      echo ""
      read -sp "Repeat password: " repeat_password
      echo ""
      register_user "$username" "$password" "$repeat_password"
      echo "Registration successful."
      ;;
    2)
      read -p "Enter username: " username
      read -sp "Enter password: " password
      echo ""
      login_user "$username" "$password"
      ;;
    3)
      read -p "Enter token: " token
      logout_user "$token"
      echo "Logout successful."
      ;;
    4)
      echo "Exiting script."
      exit 0
      ;;
    *)
      echo "Invalid choice. Please select a valid option."
      ;;
  esac

  read -p "Press Enter to continue..."
done
