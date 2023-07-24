from termcolor import colored
import speedtest
import socket

# header

print(colored("\nMATools\n\n", "magenta"))

print(colored("More on https://mat.run/\n", "cyan"))

# menu

print(colored("1 - Speedtest\n2 - Hostname to IP\n3 - IP to hostname", "green"))

menu = int(input("\nYour choice : "))


if menu == 1:
    
    # 1 - Speedtest

    st = speedtest.Speedtest()
    
    print(colored(f"\nDownload speed : {round(st.download() / 1000 / 1000, 1)} Mbit/s\nUpload speed : {round(st.upload() / 1000 / 1000, 1)} Mbit/s", "red"))

elif menu == 2:

    # 2 - Hostname to IP

    hi = socket.gethostbyname(input("\nEnter hostname : "))

    print(colored(f"\nThe IP is {hi}", "red"))

elif menu == 3:
    
    # 3 - IP to hostname

    ih = socket.gethostbyaddr(input("\nEnter IP : "))

    print(colored(f"\n The hostname is {ih}", "red"))
# footer

print(colored("\n\nThanks for using this script <3", "magenta"))
input("")