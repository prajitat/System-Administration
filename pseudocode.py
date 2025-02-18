START

DEFINE main function:
    PARSE command-line arguments
    IF command is 'user':
        CALL user_management function
    ELSE IF command is 'organize':
        CALL directory_and_file_management function
    ELSE IF command is 'monitor':
        CALL system_health_monitoring function
    ELSE:
        DISPLAY help message
    END IF

DEFINE user_management function:
    PARSE subcommand arguments
    IF subcommand is '--create':
        CALL create_user function
    ELSE IF subcommand is '--create-batch':
        CALL create_batch_users function
    ELSE IF subcommand is '--delete':
        CALL delete_user function
    ELSE IF subcommand is '--update':
        CALL update_user function
    ELSE:
        DISPLAY error message for invalid subcommand
    END IF

DEFINE create_user function:
    PARSE username and role
    IF username is invalid:
        DISPLAY error message
    ELSE IF role is invalid:
        DISPLAY error message
    ELSE:
        CREATE user with home directory
        ASSIGN role and permissions based on role
        DISPLAY success message
    END IF

DEFINE create_batch_users function:
    PARSE CSV file path
    IF file is missing or malformed:
        DISPLAY error message and skip processing
    OPEN CSV file:
        FOR each row in CSV:
            PARSE username, role, and password
            IF username already exists:
                LOG error and skip user
            ELSE IF role or password is invalid:
                LOG error and skip user
            ELSE:
                CREATE user with home directory
                ASSIGN role and permissions
                LOG success
        END FOR
    CLOSE file
    DISPLAY batch creation summary

DEFINE delete_user function:
    PARSE username
    IF username does not exist:
        DISPLAY error message
    ELSE:
        DELETE user and associated data
        DISPLAY success message
    END IF

DEFINE update_user function:
    PARSE username and optional new password
    IF username does not exist:
        DISPLAY error message
    ELSE IF password is provided:
        UPDATE user password
        DISPLAY success message
    ELSE:
        DISPLAY user details updated message
    END IF

DEFINE directory_and_file_management function:
    PARSE subcommand arguments
    IF subcommand is '--dir':
        CALL organize_directory function
    ELSE IF subcommand is '--log-monitor':
        CALL log_monitoring function
    ELSE IF subcommand is '--file-access':
        CALL file_access_monitoring function
    ELSE:
        DISPLAY error message for invalid subcommand
    END IF

DEFINE organize_directory function:
    PARSE directory path
    SCAN all files in directory
    FOR each file in directory:
        IF file is a text file:
            MOVE file to text_files directory
        ELSE IF file is a log file:
            MOVE file to log_files directory
    END FOR
    DISPLAY completion message

DEFINE log_monitoring function:
    PARSE log file path
    MONITOR log file for critical messages
    IF critical message found:
        LOG message in error summary
        DISPLAY alert message
    END IF

DEFINE file_access_monitoring function:
    MONITOR file access events
    LOG and display access events in real-time

DEFINE system_health_monitoring function:
    PARSE subcommand arguments
    IF subcommand is '--system':
        CALL monitor_system_health function
    ELSE IF subcommand is '--disk':
        CALL monitor_disk_space function
    ELSE:
        DISPLAY error message for invalid subcommand
    END IF

DEFINE monitor_system_health function:
    LOG CPU and memory usage every minute for 10 minutes
    IF CPU usage exceeds threshold:
        DISPLAY alert message and log to system_health.log
    END IF

DEFINE monitor_disk_space function:
    PARSE directory and threshold
    CHECK disk space usage for specified directory
    IF disk space exceeds threshold:
        DISPLAY alert message
    END IF

DEFINE error_handling function:
    LOG error messages with timestamps
    VALIDATE user input for security and sanitization
    DISPLAY error messages for invalid input

END

