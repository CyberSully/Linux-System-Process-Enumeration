# System-Security-Analysis-Process-Enumeration
# Overview
This project is a system enumeration and memory forensics tool built in Python. It’s designed for security-focused investigations, such as analyzing active processes, enumerating running threads, inspecting loaded modules, and reading memory regions of active processes on a Linux-based system (specifically, a Kali VM). Each function is accessible via command-line parsing, making it easy to execute individual tasks directly from the terminal.

# Features
The script uses command-line arguments to call specific functions for each of the following tasks:

# Enumerate Running Processes
This function lists all active processes on the system. It provides details such as Process ID (PID) and process names. Understanding active processes helps identify what applications and services are currently running, which is useful in security monitoring and forensic analysis.

List Threads within a Process
This function lists all threads running within a specific process, identified by PID. Each thread is identified by its Thread ID. Monitoring threads within a process can help identify multi-threaded applications and detect unexpected or malicious activity within a process.

# Enumerate Loaded Modules
This function lists all modules or libraries loaded by a given process (specified by PID). On Linux, this leverages /proc/[pid]/maps for visibility into libraries currently in use, aiding in understanding dependencies and possible injected libraries.

# Show Executable Memory Pages
This function identifies executable memory regions within a process, based on permissions (i.e., regions marked as r-x in /proc/[pid]/maps). Viewing executable memory regions is essential in investigating code injection or suspicious executable content within a process.

# Read Memory of a Process
This function allows reading a specified memory range of a given process (by providing start and end addresses). This low-level memory reading is restricted on macOS but can be used on Linux to investigate process memory content for sensitive or unexpected data, supporting in-depth forensic analysis.

# Files
enums.py: Main Python script for enumerating processes, threads, modules, executable pages, and memory.

information.txt: Details on the setup, environment, and dependencies required to run this script.

# Requirements
Python 3, MacOS or Linux environment, and the psutil library (install with pip install psutil)

For more setup details, refer to information.txt.

# System Compatibility
This tool is built for Linux (tested on Kali Linux). Some features are limited on macOS due to system-level restrictions. For macOS, alternative commands or tools may be needed for some functions, and error messages will indicate if a function is restricted.

# Disclaimer
This script should be used for educational and lawful purposes only. Unauthorized inspection or manipulation of process memory is against the law and may violate system security policies.
