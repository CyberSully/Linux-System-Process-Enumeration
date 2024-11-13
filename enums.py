import argparse
import sys
import psutil
import os
import subprocess
import platform

# function for task 1, enumerate all processes

def enumerate_processes():
    print("Enumerating all processes...")
    # Enumerate all processes using psutil
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            print(f"Process ID: {proc.info['pid']}, Name: {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

# function for task 2, enter pid with command to list all thread for a process

def list_threads(pid):
    print(f"Listing threads for process {pid}...")
    try:
        process = psutil.Process(pid)
        threads = process.threads()
        for thread in threads:
            print(f"Thread ID: {thread.id}")
    except psutil.NoSuchProcess:
        print(f"No such process with PID {pid}.")
    except psutil.AccessDenied:
        print(f"Access denied to process {pid}.")

# function for task 3, Enumerate all the loaded modules within the process selected

def list_modules(pid):
    print(f"Listing loaded modules for process {pid}...")
    try:
        process = psutil.Process(pid)
        # On macOS, memory_maps() is not available
        if psutil.MACOS:
            print("Module listing is limited on macOS.")
        else:
            for dll in process.memory_maps():
                print(f"Module: {dll.path}")
    except psutil.NoSuchProcess:
        print(f"No such process with PID {pid}.")
    except psutil.AccessDenied:
        print(f"Access denied to process {pid}.")

# function for task 4, is able to show all the executable pages within the process selected


def show_executable_memory(pid):
    print(f"Showing executable memory pages for process {pid}...")

    if os.name == 'posix' and not sys.platform.startswith("darwin"):
        # Linux
        try:
            with open(f"/proc/{pid}/maps", "r") as maps_file:
                for line in maps_file:
                    # Only interested in executable memory pages (r-x)
                    if "r-x" in line:
                        print(line.strip())
        except FileNotFoundError:
            print(f"No such process with PID {pid} or insufficient permissions.")
        except Exception as e:
            print(f"Error: {e}")

    elif sys.platform.startswith("darwin"):
        # macOS (using vmmap)
        try:
            result = subprocess.run(["vmmap", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                # Search through vmmap output for executable regions (either EXEC or __TEXT)
                found_executable = False
                for line in result.stdout.splitlines():
                    if "EXEC" in line or "__TEXT" in line:  # Looking for either EXEC or __TEXT region
                        print(line.strip())
                        found_executable = True
                if not found_executable:
                    print(f"No executable memory regions found for process {pid}.")
            else:
                print(f"Error running vmmap for process {pid}: {result.stderr.strip()}")
        except FileNotFoundError:
            print(f"vmmap command not found. Please install Xcode command line tools.")
        except Exception as e:
            print(f"Error: {e}")

#   Functions for task 5, Gives us a capability to read the memory (works on Kali Linux, but gives error message if other OS is used)

# Function to read memory for Linux (Kali)
def read_memory_linux(pid, start_address, end_address):
    print(f"Reading memory for process {pid} from {hex(start_address)} to {hex(end_address)}...")
    
    # Check that we have permission to access the memory
    mem_path = f"/proc/{pid}/mem"
    try:
        with open(mem_path, "rb") as mem_file:
            # Seek to the start address
            mem_file.seek(start_address)
            
            # Calculate the size of memory to read
            size = end_address - start_address
            memory = mem_file.read(size)
            
            # Show the memory in hexadecimal format
            print(f"Memory from address {hex(start_address)} to {hex(end_address)}:")
            for i in range(0, len(memory), 16):
                print(" ".join(f"{byte:02x}" for byte in memory[i:i+16]))
            print()
    except FileNotFoundError:
        print(f"Error: No such process or insufficient permissions for PID {pid}.")
    except Exception as e:
        print(f"Error: {e}")

# Function to handle macOS, where reading memory is restricted
def read_memory_mac(pid, start_address, end_address):
    print("Direct memory access is restricted on macOS, especially without specific privileges.")
    print("Please try this operation on a Linux machine.")

# Update read_memory function
def read_memory(pid, start_address, end_address):
    if platform.system() == "Darwin":
        # macOS specific code
        read_memory_mac(pid, start_address, end_address)
    elif platform.system() == "Linux":
        # Kali Linux (Linux) specific code
        read_memory_linux(pid, start_address, end_address)
    else:
        print("Unsupported operating system for memory reading.")




# Set up argparse for command-line flags
def main():

    parser = argparse.ArgumentParser(description="Process and memory management script.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Enumerate processes command
    subparsers.add_parser("enumerate-processes", help="Enumerate all running processes")

    # List threads command
    threads_parser = subparsers.add_parser("list-threads", help="List all threads of a process")
    threads_parser.add_argument("--pid", required=True, type=int, help="Process ID")

    # List modules command
    modules_parser = subparsers.add_parser("list-modules", help="List all loaded modules of a process")
    modules_parser.add_argument("--pid", required=True, type=int, help="Process ID")

    # Show exec memory:
    exec_pages_parser = subparsers.add_parser("show-exec-pages", help="Show executable memory pages of a process")
    exec_pages_parser.add_argument("--pid", required=True, type=int, help="Process ID")

    # Read memory command (restricted on macOS)
    read_memory_parser = subparsers.add_parser("read-memory", help="Read memory of a process within a specified range")
    read_memory_parser.add_argument("--pid", required=True, type=int, help="Process ID")
    read_memory_parser.add_argument("--start-address", required=True, type=lambda x: int(x, 0), help="Start address (e.g., 0x400000)")
    read_memory_parser.add_argument("--end-address", required=True, type=lambda x: int(x, 0), help="End address (e.g., 0x400FFF)")

    args = parser.parse_args()

    # Execute the selected command
    if args.command == "enumerate-processes":
        enumerate_processes()
    elif args.command == "list-threads":
        list_threads(args.pid)
    elif args.command == "list-modules":
        list_modules(args.pid)
    elif args.command == "show-exec-pages":
        show_executable_memory(args.pid)
    elif args.command == "read-memory":
        read_memory(args.pid, args.start_address, args.end_address)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

