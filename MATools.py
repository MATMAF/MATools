from termcolor import colored
import speedtest
import socket
import requests
import psutil
import platform
from datetime import datetime
import GPUtil
from tabulate import tabulate
import qrcode

# functions

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# header

print(colored("\nMATools\n\n", "magenta"))

print(colored("More on https://mat.run/\n", "cyan"))

# menu

while True:

    print(colored("1 - Speedtest", "green"))
    print(colored("2 - Hostname to IP", "green"))
    print(colored("3 - What's my IP", "green"))
    print(colored("4 - PC Informations", "green"))
    print(colored("5 - QR Code generator", "green"))
    print(colored("\n0 - Exit", "yellow"))

    menu = input("\nYour choice : ")


    if menu == '0':

        # 0 - Exit

        break
    
    elif menu == '1':
        
        # 1 - Speedtest

        st = speedtest.Speedtest()
        
        print(colored(f"\nDownload speed : {round(st.download() / 1000 / 1000, 1)} Mbit/s\nUpload speed : {round(st.upload() / 1000 / 1000, 1)} Mbit/s", "red"))

        break

    elif menu == '2':

        # 2 - Hostname to IP

        hostnameToIP = socket.gethostbyname(input("\nEnter hostname : "))

        print(colored(f"\nThe IP is {hostnameToIP}", "red"))

        break

    elif menu == '3':

        # 3 - What's my IP

        whatsMyIP = requests.get("https://api.ipify.org/?format=json").json()['ip']

        print(colored(f"\nYour public IP address is {whatsMyIP}", "red"))

        break

    elif menu == '4':

        # 4 - PC Informations
        while True:
            print(colored("\n1 - System", "red"))
            print(colored("2 - Boot Time", "red"))
            print(colored("3 - CPU", "red"))
            print(colored("4 - Memory", "red"))
            print(colored("5 - Disk", "red"))
            print(colored("6 - GPU", "red"))
            print(colored("7 - Network", "red"))

            menuPC = input("\nYour choice : ")

            if menuPC == '1':

                # 1 - System

                uname = platform.uname()
                print(colored("\nSystem Information", "green"))
                print(colored(f"System: {uname.system}", "yellow"))
                print(colored(f"Node Name: {uname.node}", "yellow"))
                print(colored(f"Release: {uname.release}", "yellow"))
                print(colored(f"Version: {uname.version}", "yellow"))
                print(colored(f"Machine: {uname.machine}", "yellow"))
                print(colored(f"Processor: {uname.processor}", "yellow"))

                break

            elif menuPC == '2':

                # 2 - Boot Time

                print(colored("\nBoot Time", "green"))
                boot_time_timestamp = psutil.boot_time()
                bt = datetime.fromtimestamp(boot_time_timestamp)
                print(colored(f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}", "yellow"))

                break

            elif menuPC == '3':

                # 3 - CPU

                print(colored("\nCPU Info", "green"))
                # number of cores
                print(colored(f"Physical cores: {psutil.cpu_count(logical=False)}", "yellow"))
                print(colored(f"Total cores: {psutil.cpu_count(logical=True)}", "yellow"))
                # CPU frequencies
                cpufreq = psutil.cpu_freq()
                print(colored(f"Max Frequency: {cpufreq.max:.2f}Mhz", "yellow"))
                print(colored(f"Min Frequency: {cpufreq.min:.2f}Mhz", "yellow"))
                print(colored(f"Current Frequency: {cpufreq.current:.2f}Mhz", "yellow"))
                # CPU usage
                print(colored("CPU Usage Per Core:", "yellow"))
                for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                    print(colored(f"Core {i}: {percentage}%", "yellow"))
                print(colored(f"Total CPU Usage: {psutil.cpu_percent()}%", "yellow"))

                break

            elif menuPC == '4':

                # 4 - Memory

                print(colored("\nMemory Information", "green"))
                # get the memory details
                svmem = psutil.virtual_memory()
                print(colored(f"Total: {get_size(svmem.total)}", "yellow"))
                print(colored(f"Available: {get_size(svmem.available)}", "yellow"))
                print(colored(f"Used: {get_size(svmem.used)}", "yellow"))
                print(colored(f"Percentage: {svmem.percent}%", "yellow"))
                print(colored("SWAP", "green"))
                # get the swap memory details (if exists)
                swap = psutil.swap_memory()
                print(colored(f"Total: {get_size(swap.total)}", "yellow"))
                print(colored(f"Free: {get_size(swap.free)}", "yellow"))
                print(colored(f"Used: {get_size(swap.used)}", "yellow"))
                print(colored(f"Percentage: {swap.percent}%", "yellow"))

                break

            elif menuPC == '5':

                # 5 - Disk

                print(colored("\nDisk Information", "green"))
                print(colored("Partitions and Usage:", "yellow"))
                # get all disk partitions
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    print(colored(f"=== Device: {partition.device} ===", "green"))
                    print(colored(f"  Mountpoint: {partition.mountpoint}", "yellow"))
                    print(colored(f"  File system type: {partition.fstype}", "yellow"))
                    try:
                        partition_usage = psutil.disk_usage(partition.mountpoint)
                    except PermissionError:
                        # this can be catched due to the disk that
                        # isn't ready
                        continue
                    print(colored(f"  Total Size: {get_size(partition_usage.total)}", "yellow"))
                    print(colored(f"  Used: {get_size(partition_usage.used)}", "yellow"))
                    print(colored(f"  Free: {get_size(partition_usage.free)}", "yellow"))
                    print(colored(f"  Percentage: {partition_usage.percent}%", "yellow"))
                # get IO statistics since boot
                disk_io = psutil.disk_io_counters()
                print(colored(f"Total read: {get_size(disk_io.read_bytes)}", "red"))
                print(colored(f"Total write: {get_size(disk_io.write_bytes)}", "red"))

                break

            elif menuPC == '6':

                # 6 - GPU

                print(colored("GPU Details", "green"))
                gpus = GPUtil.getGPUs()
                list_gpus = []
                for gpu in gpus:
                    # get the GPU id
                    gpu_id = colored(gpu.id, "yellow")
                    # name of GPU
                    gpu_name = colored(gpu.name, "yellow")
                    # get % percentage of GPU usage of that GPU
                    gpu_load = colored(f"{gpu.load*100}%", "yellow")
                    # get free memory in MB format
                    gpu_free_memory = colored(f"{gpu.memoryFree}MB", "yellow")
                    # get used memory
                    gpu_used_memory = colored(f"{gpu.memoryUsed}MB", "yellow")
                    # get total memory
                    gpu_total_memory = colored(f"{gpu.memoryTotal}MB", "yellow")
                    # get GPU temperature in Celsius
                    gpu_temperature = colored(f"{gpu.temperature} °C", "yellow")
                    gpu_uuid = colored(gpu.uuid, "yellow")
                    list_gpus.append((
                        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                        gpu_total_memory, gpu_temperature, gpu_uuid
                    ))

                break

            elif menuPC == '7':

                # 7 - Network

                print(colored("Network Information", "green"))
                # get all network interfaces (virtual and physical)
                if_addrs = psutil.net_if_addrs()
                for interface_name, interface_addresses in if_addrs.items():
                    for address in interface_addresses:
                        print(colored(f"=== Interface: {interface_name} ===", "green"))
                        if str(address.family) == 'AddressFamily.AF_INET':
                            print(colored(f"  IP Address: {address.address}", "yellow"))
                            print(colored(f"  Netmask: {address.netmask}", "yellow"))
                            print(colored(f"  Broadcast IP: {address.broadcast}", "yellow"))
                        elif str(address.family) == 'AddressFamily.AF_PACKET':
                            print(colored(f"  MAC Address: {address.address}", "yellow"))
                            print(colored(f"  Netmask: {address.netmask}", "yellow"))
                            print(colored(f"  Broadcast MAC: {address.broadcast}", "yellow"))
                # get IO statistics since boot
                net_io = psutil.net_io_counters()
                print(colored(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}", "red"))
                print(colored(f"Total Bytes Received: {get_size(net_io.bytes_recv)}", "red"))

                break
            
            else:

                # Don't choose a valid option

                print(colored("\nError please choose a valid option\n", "red"))

        break

    elif menu == '5':

        # 5 - QR Code generator

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_Q
        )
        qr.add_data(input("\nEnter an URL : "))
        qr.make(fit=True)
        qr.make_image(fill_color="black", back_color="white")
        qr.print_ascii()

        break

    else:

        # Don't choose a valid option

        print(colored("\nError please choose a valid option\n", "red"))

# footer

print(colored("\n\nThanks for using this script <3", "magenta"))
input("")

# end