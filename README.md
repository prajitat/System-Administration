# System-Administration
This project tests the understanding of Python scripting for system administration tasks. I developed a Python script using one-level subcommands, with each subcommand handling a specific system-level operation. Tasks include automating backups, user management, file organization, and monitoring system health on a CentOS 9 virtual machine.


Project Requirements

User Requirements Analysis & Pseudocode Design

Draft of detailed pseudocode based on project requirements.

User Management 

User Creation and Deletion: Allow creation and deletion of users with role-based 
access.

Role-Based Access Control: Assign permissions based on admin or user roles.

User Information Update: Command-line argument to update user information.

Subcommand: user

• Create Users: Add single users or multiple users from a CSV file with role-based
  access.

• Delete Users: Remove existing users.

• Update Users: Modify user passwords and detail.

Directory organization

•	Organize files based on file types.

•	Monitor specific logs for critical messages and summarize
  them.

•	Track and log file access events.

System Health Monitoring 

Subcommand: monitor

• CPU and Memory Usage Monitoring: Log CPU and memory usage every
minute for 10 minutes.

• Disk Space Check: Alert if disk usage exceeds a threshold.

• Process Management: List and filter processes by name.

Security and Error Handling 

• Error Logging: Centralized error logging with timestamps.

• Security Validation and Input Sanitization: Check for valid inputs and safe
  handling of sensitive information.




