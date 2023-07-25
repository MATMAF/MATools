from termcolor import colored
import speedtest
import socket

# header

print(colored("\nMATools\n\n", "magenta"))

print(colored("More on https://mat.run/\n", "cyan"))

# menu

while True:

    print(colored("1 - Speedtest", "green"))
    print(colored("2 - Hostname to IP", "green"))
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

        hi = socket.gethostbyname(input("\nEnter hostname : "))

        print(colored(f"\nThe IP is {hi}", "red"))

        break

    else:

        # 

        print(colored("\nError please choose a valid option\n", "red"))

# footer

print(colored("\n\nThanks for using this script <3", "magenta"))
input("")

# end