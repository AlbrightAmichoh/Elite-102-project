import mysql.connector

#  connection to the MySQL database
connection = mysql.connector.connect(
    user='root',
    password='1903920sadA@',
    host='localhost',
    database='elite102_project'
)

def start():
    """Main entry point of the banking system."""
    while True:
        print("\nWelcome to the banking system.")
        print("1. Create an account")
        print("2. Login to your account")

        option = input("Choose an option: ").strip()

        
        print(f"Option received: '{option}'")

        if option == "1":
            print("You chose to create an account.")
            create_account()  # Call create_account() 
            break  # Break the loop 
        elif option == "2":
            print("You chose to login.")
            login()  # Call login() 
            break  # Break the loop t
        else:
            print("Invalid option. Please try again.")

def create_account():
    """Create a new user account."""
    name = input("Enter your name: ")
    pin = input("Enter your pin: ")
    is_admin = input("Are you an admin? (yes/no): ").strip().lower()
    is_admin_value = 1 if is_admin == "yes" else 0

    cursor = connection.cursor(buffered=True)
    query = "INSERT INTO user (name, pin, is_admin) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, pin, is_admin_value))
    connection.commit()
    user_id = cursor.lastrowid
    account_number = f"ACC{user_id + 1000}"

    query = "INSERT INTO account (UserID, account_number, Balance) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, account_number, 0))
    connection.commit()
    cursor.close()

    print(f"Account created successfully for {name}. Your account number is {account_number}")
    print("Please log in with your account number to proceed.")
    login()  # let the user log in

def login():
    """Prompt user to log in."""
    account_number = input("Enter your account number: ").strip()

    cursor = connection.cursor(buffered=True)
    query = "SELECT user_id, name FROM user WHERE user_id IN (SELECT UserID FROM account WHERE account_number = %s)"
    cursor.execute(query, (account_number,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        user_id, name = result
        print(f"Welcome, {name}!")
        main_menu(user_id)  #  show the main menu
    else:
        print("Invalid account number. Please try again.")
        start() 

def main_menu(user_id):
    """Main menu after login."""
    while True:
        print("\nMain Menu")
        print("1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Delete account")
        print("5. Modify account")
        print("6. Exit")
        
        option = input("Choose an option: ").strip()  
        if option == "1":
            check_balance(user_id)
        elif option == "2":
            deposit(user_id)
        elif option == "3":
            withdraw(user_id)
        elif option == "4":
            delete_account(user_id)
        elif option == "5":
            modify_account(user_id)
        elif option == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def check_balance(user_id):
    """Check the account balance."""
    try:
        cursor = connection.cursor(buffered=True)
        query = "SELECT Balance FROM account WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            balance = result[0]
            print(f"Your balance is: ${balance}")
        else:
            print("Account not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def deposit(user_id):
    """Deposit money into the account."""
    try:
        # balance before deposit
        cursor = connection.cursor(buffered=True)
        query = "SELECT Balance FROM account WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            current_balance = result[0]
            print(f"Your current balance is: ${current_balance}")
            
            amount = float(input("Enter the amount to deposit: ").strip())
            
            # balance after deposit
            cursor = connection.cursor()
            query = "UPDATE account SET Balance = Balance + %s WHERE UserID = %s"
            cursor.execute(query, (amount, user_id))
            connection.commit()
            cursor.close()

            print(f"Deposited ${amount} successfully!")
            
            # new balance
            cursor = connection.cursor(buffered=True)
            query = "SELECT Balance FROM account WHERE UserID = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                updated_balance = result[0]
                print(f"Your new balance is: ${updated_balance}")
        else:
            print("Account not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def withdraw(user_id):
    """Withdraw money from the account."""
    try:
        # balance before withdrawal
        cursor = connection.cursor(buffered=True)
        query = "SELECT Balance FROM account WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            current_balance = result[0]
            print(f"Your current balance is: ${current_balance}")
            
            amount = float(input("Enter the amount to withdraw: ").strip())
            
            # balance shown 
            if amount <= current_balance:
                cursor = connection.cursor()
                query = "UPDATE account SET Balance = Balance - %s WHERE UserID = %s"
                cursor.execute(query, (amount, user_id))
                connection.commit()
                cursor.close()

                print(f"Withdrew ${amount} successfully!")
                
                # balance after withdrawal
                cursor = connection.cursor(buffered=True)
                query = "SELECT Balance FROM account WHERE UserID = %s"
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                cursor.close()

                if result:
                    updated_balance = result[0]
                    print(f"Your new balance is: ${updated_balance}")
            else:
                print("Insufficient funds.")
        else:
            print("Account not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def delete_account(user_id):
    """Delete an account."""
    try:
        cursor = connection.cursor()
        query = "DELETE FROM account WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        cursor.close()
        print("Account deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def modify_account(user_id):
    """Modify user account details (name or pin)."""
    try:
        cursor = connection.cursor(buffered=True)

        # Get current user details
        query = "SELECT name FROM user WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            current_name = result[0]
            print(f"\nYour current name is: {current_name}")
            print("You can update your name or PIN.")

            update_name = input("Do you want to change your name? (yes/no): ").strip().lower()
            if update_name == "yes":
                new_name = input("Enter your new name: ").strip()
                query = "UPDATE user SET name = %s WHERE user_id = %s"
                cursor.execute(query, (new_name, user_id))
                connection.commit()
                print("Name updated successfully.")

            update_pin = input("Do you want to change your PIN? (yes/no): ").strip().lower()
            if update_pin == "yes":
                new_pin = input("Enter your new PIN: ").strip()
                query = "UPDATE user SET pin = %s WHERE user_id = %s"
                cursor.execute(query, (new_pin, user_id))
                connection.commit()
                print("PIN updated successfully.")

            if update_name != "yes" and update_pin != "yes":
                print("No changes made.")
        else:
            print("User not found.")
        
        cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# function is only called
if __name__ == "__main__":
    try:
        start()  # Start the system 
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        connection.close()
