#!/usr/bin/python3

#here we are importing all necessary modules
import argparse
import os
import csv
import logging
import shutil
import subprocess
import psutil  # Requires `psutil` package for system monitoring



# Setup logging for any errors in the script
logging.basicConfig(filename="error_log.log", level=logging.ERROR, format="%(asctime)s: %(message)s")

#This function is checking is the user already exists or not.
def user_exists(username):
    try:
        output = subprocess.run(
            ["id", username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output.returncode == 0
    except Exception as e:
        logging.error(f'Error checking user existence: {e}')
        return False


# Validate username format
def is_valid_username(username):
    if not username or " " in username:
        logging.error(f"Invalid username format: '{username}'. Usernames should not contain spaces.")
        print(f"[ERROR] Invalid username format: '{username}'. Usernames should not contain spaces.")
        return False
    return True


# User Management Functions
def create_user(username, role):
    try:
        if not username or not role:
            logging.error("Missing username or role.")
            print("[ERROR] Missing username or role.")
            return

        if not is_valid_username(username):
            return

        if user_exists(username):
            logging.error(f"User {username} already exists.")
            print(f"[INFO] User {username} already exists.")
            return

        if role not in ["admin", "user"]:
            logging.error(f"Invalid role: {role}. Must be 'admin' or 'user'.")
            print(f"[ERROR] Invalid role: {role}.")
            return

        print(f"[INFO] Creating user '{username}' with role '{role}'")

        # Add the user
        subprocess.run(["sudo", "useradd", "-m", username], check=True)
        print(f"[INFO] User '{username}' created successfully.")

        # Assign role-based permissions (e.g., add to a group)
        if role == "admin":
            subprocess.run(["sudo", "usermod", "-aG", "sudo", username], check=True)
            print(f"[INFO] Role 'admin' assigned with sudo permissions.")
        else:
            print(f"[INFO] Role 'user' assigned with standard permissions.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to create user '{username}': {e}")
        print(f"[ERROR] Failed to create user '{username}'.")

#this function utilizes the csv module to create users from csv file
def create_users_from_csv(csv_file):
    try:
        if not os.path.exists(csv_file):
            logging.error(f"CSV file not found: {csv_file}")
            print(f"[ERROR] CSV file not found: {csv_file}")
            return

        print(f"[INFO] Creating users from CSV file: {csv_file}")
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row.get("username")
                role = row.get("role")
                password = row.get("password")

                if not username or not role or not password:
                    logging.error(f"Invalid row in CSV: {row}")
                    print(f"[ERROR] Invalid row in CSV: {row}")
                    continue
                if is_valid_username(username):
                    create_user(username, role)
                    # Set the user's password
                    command = f"echo '{username}:{password}' | sudo chpasswd"
                    subprocess.run(command, shell=True, check=True)
                    #subprocess.run(["sudo", "echo", f"{username}:{password}", "|", "sudo", "chpasswd"], shell=True)
    except Exception as e:
        logging.error(f"Error processing CSV file: {e}")
        print(f"[ERROR] Error processing CSV file.")


def delete_user(username):
    try:
        if not username:
            logging.error("Missing username for deletion.")
            print("[ERROR] Missing username for deletion.")
            return

        if not is_valid_username(username):
            return

        print(f"[INFO] Deleting user '{username}'")
        subprocess.run(["sudo", "userdel", "-r", username], check=True)
        print(f"[INFO] User '{username}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to delete user '{username}': {e}")
        print(f"[ERROR] Failed to delete user '{username}'.")


def update_user(username, password):
    try:
        if not username or not password:
            logging.error("Missing username or password for update.")
            print("[ERROR] Missing username or password for update.")
            return

        if not is_valid_username(username):
            return

        print(f"[INFO] Updating user '{username}'")
        # Update the user's password
        subprocess.run(["sudo", "echo", f"{username}:{password}", "|", "sudo", "chpasswd"], shell=True)
        print(f"[INFO] Password updated successfully for '{username}'.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to update user '{username}': {e}")
        print(f"[ERROR] Failed to update user '{username}'.")


# Directory Management Functions
def organize_directory(dir_path):
    try:
        if not os.path.exists(dir_path):
            logging.error(f"Directory not found: {dir_path}")
            print(f"[ERROR] Directory not found: {dir_path}")
            return

        print(f"[INFO] Organizing files in {dir_path} by type")
        for file_name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file_name)
            if os.path.isfile(full_path):
                file_extension = os.path.splitext(file_name)[1][1:]  # Get file extension
                target_dir = os.path.join(dir_path, f"{file_extension}_files")
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(full_path, target_dir)
                print(f"[INFO] Moved {file_name} to {target_dir}")
    except Exception as e:
        logging.error(f"Failed to organize directory '{dir_path}': {e}")
        print(f"[ERROR] Failed to organize directory '{dir_path}'.")


# System Health Monitoring Functions
def monitor_system_health():
    log_file = "system_health.log"  # File to log system health data
    print(f"[INFO] Monitoring system health every minute for 10 minutes. Logs will be saved to {log_file}")

    for _ in range(10):
        cpu_usage = psutil.cpu_percent(interval=60)  # Waits 60 seconds while measuring CPU usage
        memory = psutil.virtual_memory()

        # Prepare log message
        log_message = f"CPU Usage: {cpu_usage}%, Memory Usage: {memory.percent}%"

        # Log to file
        with open(log_file, "a") as log:
            log.write(f"{log_message}\n")

        # Print to console
        print(f"[INFO] {log_message}")
        print("[INFO] Logged CPU and memory usage to system_health.log.")


def check_disk_space(dir_path, threshold):
    try:
        if not os.path.exists(dir_path):
            logging.error(f"Directory not found: {dir_path}")
            print(f"[ERROR] Directory not found: {dir_path}")
            return

        usage = shutil.disk_usage(dir_path)
        percent_used = (usage.used / usage.total) * 100
        if percent_used > threshold:
            print(f"[ALERT] Disk usage at {percent_used:.2f}% - consider freeing up space.")
        else:
            print(f"[INFO] Disk usage is under control at {percent_used:.2f}%.")
    except Exception as e:
        logging.error(f"Failed to check disk space for '{dir_path}': {e}")
        print(f"[ERROR] Failed to check disk space for '{dir_path}'.")


# Log Monitoring Function
def monitor_log_file(log_file):
    try:
        if not os.path.exists(log_file):
            logging.error(f"Log file not found: {log_file}")
            print(f"[ERROR] Log file not found: {log_file}")
            return

        print(f"[INFO] Monitoring {log_file} for critical messages")

        # Define patterns for critical messages (can be expanded based on requirements)
        critical_patterns = ["error", "fail", "critical", "disk space low", "unable", "out of memory"]
        critical_messages = []

        with open(log_file, "r") as file:
            for line in file:
                if any(pattern in line.lower() for pattern in critical_patterns):
                    critical_messages.append(line.strip())
                    print(f"[ALERT] Critical message found: {line.strip()}")

        # Log critical messages to a summary file
        if critical_messages:
            with open("error_summary.log", "w") as summary_file:
                summary_file.write("\n".join(critical_messages))
            print(f"[INFO] Logged critical messages to error_summary.log.")
        else:
            print("[INFO] No critical messages found.")

    except Exception as e:
        logging.error(f"Error monitoring log file '{log_file}': {e}")
        print(f"[ERROR] Error monitoring log file '{log_file}'.")


# Main Functionality
def main():
    parser = argparse.ArgumentParser(
        prog="sys_admin.py",
        usage="./sys_admin.py {user, organize, monitor} [options]",
        description="System Administration Script - Manage Users, organize files, and monitor system health.",
        add_help=True
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    # User Management
    user_parser = subparsers.add_parser("user", help="Manage user accounts")
    user_parser.add_argument("--create", action="store_true", help="Create a single user with specified role")
    user_parser.add_argument("--create-batch", action="store_true", help="Create users from a CSV file")
    user_parser.add_argument("--csv", type=str, help="CSV file with user data")
    user_parser.add_argument("--delete", action="store_true", help="Delete a user")
    user_parser.add_argument("--update", action="store_true", help="Update user details")
    user_parser.add_argument("--username", type=str, help="Specify the username")
    user_parser.add_argument("--role", type=str, help="Specify the role (admin/user)")
    user_parser.add_argument("--password", type=str, help="Specify the new password")

    # Directory Management
    organize_parser = subparsers.add_parser("organize", help="Organize directories")
    organize_parser.add_argument("--dir", type=str, help="Directory to organize")
    organize_parser.add_argument("--log-monitor", type=str, help="Monitor log file for critical messages")

    # System Health Monitoring
    monitor_parser = subparsers.add_parser("monitor", help="Monitor system health")
    monitor_parser.add_argument("--system", action="store_true", help="Monitor CPU and memory usage")
    monitor_parser.add_argument("--disk", action="store_true", help="Check disk space")
    monitor_parser.add_argument("--dir", type=str, help="Directory to check disk usage")
    monitor_parser.add_argument("--threshold", type=int, help="Disk usage threshold")

    args = parser.parse_args()

    if args.subcommand == "user":
        if args.create:
            create_user(args.username, args.role)
        elif args.create_batch and args.csv:
            create_users_from_csv(args.csv)
        elif args.delete:
            delete_user(args.username)
        elif args.update:
            update_user(args.username, args.password)
    elif args.subcommand == "organize":
        if args.dir:
            organize_directory(args.dir)
        elif args.log_monitor:
            monitor_log_file(args.log_monitor)
    elif args.subcommand == "monitor":
        if args.system:
            monitor_system_health()
        elif args.disk:
            check_disk_space(args.dir, args.threshold)


if __name__ == "__main__":
    main()
