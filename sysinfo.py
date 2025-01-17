import psutil
from rich.console import Console
from rich.table import Table
from rich.text import Text
import shutil
import argparse
import platform
import datetime
import socket

console = Console()

# Function to display system resources
def display_system_resources():
    table = Table(title="System Resources", show_header=True, header_style="bold magenta")
    table.add_column("Resource", style="bold cyan", width=35)
    table.add_column("Stats", justify="right", style="bold green")

    # Memory Usage
    mem = psutil.virtual_memory()
    total_gb = mem.total / (1024 ** 3)
    used_gb = mem.used / (1024 ** 3)
    available_gb = mem.available / (1024 ** 3)

    table.add_row("[bold magenta]---- RAM Stats ----[/bold magenta]", "")
    table.add_row("Percentage of RAM in use", f"{mem.percent}%")
    table.add_row("Total amount of system RAM in GB", f"{total_gb:.2f} GB")
    table.add_row("Total RAM in GB currently in use", f"{used_gb:.2f} GB")
    table.add_row("Total RAM in GB available", f"{available_gb:.2f} GB")

    # CPU Usage
    cpu = psutil.cpu_percent(interval=1)
    cpu_stats = psutil.cpu_stats()

    table.add_row("\n[bold magenta]---- CPU Stats ----[/bold magenta]", "")
    table.add_row("Logical CPUs on the system", f"{psutil.cpu_count()}")
    table.add_row("Total CPU usage", f"{cpu}%")
    table.add_row("CPU Stats", "")
    table.add_row("  Context Switches", f"{cpu_stats.ctx_switches}")
    table.add_row("  Interrupts", f"{cpu_stats.interrupts}")
    table.add_row("  Soft Interrupts", f"{cpu_stats.soft_interrupts}")
    table.add_row("  System Calls", f"{cpu_stats.syscalls}")

    # Drive Info
    table.add_row("\n[bold magenta]---- Partition Info ----[/bold magenta]", "")
    partitions = psutil.disk_partitions()
    for part in partitions:
        try:
            disk_usage = shutil.disk_usage(part.mountpoint)
            total_gb = disk_usage.total / (1024 ** 3)
            used_gb = disk_usage.used / (1024 ** 3)
            free_gb = disk_usage.free / (1024 ** 3)

            table.add_row(f"Drive: {part.device}", f"Mountpoint: {part.mountpoint}")
            table.add_row("  Total space: ", f"{total_gb:.2f} GB")
            table.add_row("  Used space:", f"{used_gb:.2f} GB")
            table.add_row("  Free Space", f"{free_gb:.2f} GB")
        except PermissionError:
            table.add_row(f"Drive: {part.device}", "Permission Denied")

    console.print(table)

# Function to display system information
def display_system_information():
    table = Table(title="System Information", show_header=True, header_style="bold magenta")
    table.add_column("Resource", style="bold cyan", width=35)
    table.add_column("Stats", justify="right", style="bold green")

    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    table.add_row("Boot Time", f"{boot_time}")
    table.add_row("Hostname", f"{platform.node()}")
    table.add_row("IP Address", f"{socket.gethostbyname(socket.gethostname())}")
    table.add_row("Operating System", f"{platform.platform()}")
    table.add_row("System Architecture", f"{platform.architecture()[0]}")
    table.add_row("Kernel Version", f"{platform.version()}")
    table.add_row("Python Version", f"{platform.python_version()}")

    console.print(table)

# Main function to parse arguments
def main():
    parser = argparse.ArgumentParser(description="System Information and Resources Viewer")
    parser.add_argument("--resources", action="store_true", help="Display the current system resources")
    parser.add_argument("--sysinfo", action="store_true", help="Display the current system information")
    parser.add_argument("--all", action="store_true", help="Display both system information and resources")

    args = parser.parse_args()

    if args.resources:
        display_system_resources()
    elif args.sysinfo:
        display_system_information()
    elif args.all:
        display_system_information()
        display_system_resources()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

