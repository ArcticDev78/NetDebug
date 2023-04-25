""" IMPORTS """
# Import required libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import sys
from tabulate import tabulate
import requests

""" STARTUP """
# Print ASCII art of "NetDebug" on startup.
header = """
     __     _      ___     _                 
  /\ \ \___| |_   /   \___| |__  _   _  __ _ 
 /  \/ / _ \ __| / /\ / _ \ '_ \| | | |/ _` |
/ /\  /  __/ |_ / /_//  __/ |_) | |_| | (_| |
\_\ \/ \___|\__/___,' \___|_.__/ \__,_|\__, |
                                       |___/ 
"""  # noqa

# Print header
print(blue(header, 'bold'))

# Print init messages
print(yellow(' => netdebug v0.1', 'bold'))
print(yellow(' => dns-check - speedtest - router-check - ping - show [choice] - assistant', 'bold'))  # noqa
print(green(' => 3 modules ready to use', 'bold'))
print(blue(' => "Having network issues? This tool could help you solve them!"', ['bold', 'italic']))  # noqa

# Set variables for printing network configuration
gateway = os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()  # noqa
gateway = gateway.replace("\n", "")

up_interface = os.popen("route | awk '/Iface/{getline; print $8}'").read()
up_interface = up_interface.replace("\n", "")

# n_name = os.popen('iwgetid -r').read()  # Get wireless network name

# Work-around to get it working on Fedora Linux
n_name = os.popen('nmcli -t -f NAME connection show --active').read()

# Get network MAC address
n_mac = os.popen(
    "ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read()  # noqa

# Local IP address
n_ip = os.popen("hostname -I").read()
# Hostname
# n_host = os.popen("hostname").read()

# Print network configuration header
print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════════════╕
│                         Your Network Configuration                      │
╘═════════════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa

# Print network configuration , using tabulate as table.
table = [["IP Address", "MAC Address", "Gateway", "Iface", "SSID"],
         # ["", "", "", "", ""],
         [n_ip, n_mac.upper(), gateway, up_interface, n_name]]
print(tabulate(table, stralign="center",
               tablefmt="fancy_grid", headers="firstrow"))
print()
print(f'{green("[+] Please type", "bold")} {yellow("help", "bold")} {green("to view commands", "bold")}')  # noqa
print()

""" EXIT FUNCTION """


# Message to be printed when using exit command or Ctrl-C inputted
def exit():
    sys.exit(success_message('Shutting down NetDebug ... Bye! ( ^_^)/'))

# Error message font style


def error_message(error_msg, solution=None):
    if solution:
        print(f'[{red("!", "bold")}] {error_msg} {green(solution, "bold")}')  # noqa
    else:
        print(f'[{red("!", "bold")}] {error_msg}')


# Success message font style
def success_message(success_msg):
    print(f'[{green("+", "bold")}] {success_msg}')


# Info message font style
def info_message(info_msg):
    print(f'[{yellow("*", "bold")}] {info_msg}')


# Custom input style
def custom_input(input_msg=None):
    if input_msg:
        return input(f'[{green(">", "bold")}] {cyan(input_msg, "bold")}')  # noqa
    else:
        return input(f'[{green(">", "bold")}] ')  # noqa


""" FUNCTIONS """


def dns_check():
    print(f'{yellow("netdebug", "underlined")} => {blue("(dns-check)", "bold")}\n')  # noqa
    print(f'{green("Available DNS servers:", "underlined")}\n{cyan("1", "bold")} - Cloudflare DNS (1.1.1.1) [Recommended]\n{cyan("2", "bold")} - Google DNS (8.8.8.8)\n{cyan("3", "bold")} - Other (enter server address)\n')  # noqa
    dns_server_choice = custom_input('Which DNS server would you like to use? (1/2/3): ')  # noqa
    if dns_server_choice == '1':
        print()
        info_message('Running DNS Check using CloudFlare DNS (1.1.1.1)...\n')
        response = os.system('ping -c 5 1.1.1.1')
        if response == 0:
            print()
            print('═════════════════════════════════════════════════════════════')  # noqa
            print(yellow("""
╒═════════════════════════════════════════════════════════════╕
│                       DNS Check Results                     │
╘═════════════════════════════════════════════════════════════╛""", "bold"))  # noqa
            print()
            info_message('DNS is working properly.')
            # Statistics
            print(""" \033[1;36m
╒══════════════════════════════════════════════════╕
│                    STATISTICS                    │
╘══════════════════════════════════════════════════╛     \033[1;m""")  # noqa
            lastLine = os.popen('ping 1.1.1.1 -c 5 | tail -n 1').read()
            lastLine2 = lastLine.replace('rtt ', '')
            ping_ar = lastLine2.split()

            min_ping = float(ping_ar[2].split('/')[0])
            average_ping = float(ping_ar[2].split('/')[1])
            max_ping = float(ping_ar[2].split('/')[2])

            table = [["Minimum Ping", "Average Ping", "Maximum Ping"],
                     [f'{min_ping} ms', f'{average_ping} ms', f'{max_ping} ms']]  # noqa
            print(tabulate(table, stralign="center",
                           tablefmt="fancy_grid", headers="firstrow"))
            # Results
            if average_ping <= 30:
                # info_message('Your (average) ping is normal. [Average ping is less <= 30]')  # noqa
                print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════╕
│                         CONCLUSION                          │
╘═════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                table = [["Status", "Condition met"],
                         [f'Your (average) ping is {green("NORMAL", ["bold", "underlined"])}', f'Average ping is {yellow("less <= 30", "bold")}']]  # noqa

                print(tabulate(table, stralign="center",
                               tablefmt="fancy_grid", headers="firstrow"))
            elif average_ping > 30 and average_ping <= 100:
                # print()
                # info_message('Your (average) ping is OK. [y]')  # noqa
                print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════╕
│                         CONCLUSION                          │
╘═════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                table = [["Status", "Condition met"],
                         [f'Your (average) ping is {green("OK", ["bold", "underlined"])}', f'Average ping is {yellow("> 30 and <= 100", "bold")}']]  # noqa
            elif average_ping > 100 and average_ping <= 200:
                # print()
                # info_message('Your (average) ping is high. [Average ping is >= 200]')  # noqa
                print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════╕
│                         CONCLUSION                          │
╘═════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                table = [["Status", "Condition met"],
                         [f'Your (average) ping is {red("HIGH", ["bold", "underlined"])}', f'Average ping is {yellow("> 100 and <= 200", "bold")}']]  # noqa
            elif average_ping > 200 and average_ping <= 500:
                # print()
                # info_message('Your (average) ping is VERY HIGH. [Average ping is >= 500')  # noqa
                print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════╕
│                         CONCLUSION                          │
╘═════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                table = [["Status", "Condition met"],
                         [f'Your (average) ping is {red("VERY HIGH", ["bold", "underlined"])}', f'Average ping is {yellow("> 200 and <= 500", "bold")}']]  # noqa

            print()
            prompt()

        else:
            print()
            error_message('Unable to reach DNS server. This could be because of the following reasons:\n1. The DNS server is down.\n2. Please check your internet connection if it is working.')  # noqa
            prompt()
    elif dns_server_choice == '2':
        print()
        info_message('Running DNS Check using Google DNS (8.8.8.8)...\n')
        response = os.system('ping -c 5 8.8.8.8')
        if response == 0:
            print()
            print('═════════════════════════════════════════════════════════════')  # noqa
            print(yellow("""
╒═════════════════════════════════════════════════════════════╕
│                       DNS Check Results                     │
╘═════════════════════════════════════════════════════════════╛""", "bold"))  # noqa
            print()
            info_message('DNS is working properly.\n')
            # Statistics
            print(""" \033[1;36m
╒══════════════════════════════════════════════════╕
│                    STATISTICS                    │
╘══════════════════════════════════════════════════╛     \033[1;m""")  # noqa
            lastLine = os.popen('ping 8.8.8.8 -c 5 | tail -n 1').read()
            lastLine2 = lastLine.replace('rtt ', '')
            ping_ar = lastLine2.split()

            min_ping = float(ping_ar[2].split('/')[0])
            average_ping = float(ping_ar[2].split('/')[1])
            max_ping = float(ping_ar[2].split('/')[2])

            table = [["Minimum Ping", "Average Ping", "Maximum Ping"],
                     [f'{min_ping} ms', f'{average_ping} ms', f'{max_ping} ms']]  # noqa
            print(tabulate(table, stralign="center",
                           tablefmt="fancy_grid", headers="firstrow"))
            # Results
            if average_ping <= 30:
                # info_message('Your (average) ping is normal. [Average ping is less <= 30]')  # noqa
                print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════╕
│                         CONCLUSION                          │
╘═════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                table = [["Status", "Condition met"],
                         [f'Your (average) ping is {green("NORMAL", ["bold", "underlined"])}', f'Average ping is {yellow("less <= 30", "bold")}']]  # noqa

                print(tabulate(table, stralign="center",
                               tablefmt="fancy_grid", headers="firstrow"))
            elif average_ping < 30 and average_ping >= 100:
                print()
                info_message('Your (average) ping is OK. [Average ping is >= 100]')  # noqa
            elif average_ping < 100 and average_ping >= 200:
                print()
                info_message('Your (average) ping is high. [Average ping is >= 200]')  # noqa
            elif average_ping < 200 and average_ping >= 500:
                print()
                info_message('Your (average) ping is VERY HIGH. [Average ping is >= 500')  # noqa

            print()
            prompt()
            prompt()
        else:
            print()
            error_message('Unable to reach DNS server. Please check your internet connection.')  # noqa
            print()
            success_message('Finished DNS Check.\n')
            prompt()
    elif dns_server_choice == '3':
        print()
        custom_dns_server = custom_input('Enter the address of the DNS server you would like to use: ')  # noqa
        # Check if the DNS server given by the user is valid
        dot_count = custom_dns_server.count('.')
        if dot_count < 3:
            print()
            error_message('The DNS server that you entered is not valid.', 'The DNS server address must contain at least 3 dots. Example: 1.1.1.1\n')  # noqa
            prompt()
        elif dot_count == 3:
            print()
            info_message(f'Running DNS Check using Custom DNS server ({custom_dns_server})...\n')  # noqa
            response = os.system(f'ping -c 5 {custom_dns_server}')
            if response == 0:
                print()
                print('═════════════════════════════════════════════════════════════')  # noqa
                print(yellow("""
╒═════════════════════════════════════════════════════════════╕
│                       DNS Check Results                     │
╘═════════════════════════════════════════════════════════════╛""", "bold"))  # noqa
                print()
                info_message('DNS is working properly.\n')
                # Statistics
                print(""" \033[1;36m
╒══════════════════════════════════════════════════╕
│                    STATISTICS                    │
╘══════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                lastLine = os.popen(f'ping {custom_dns_server} -c 5 | tail -n 1').read()  # noqa
                lastLine2 = lastLine.replace('rtt ', '')
                ping_ar = lastLine2.split()

                min_ping = float(ping_ar[2].split('/')[0])
                average_ping = float(ping_ar[2].split('/')[1])
                max_ping = float(ping_ar[2].split('/')[2])

                table = [["Minimum Ping", "Average Ping", "Maximum Ping"],
                         [f'{min_ping} ms', f'{average_ping} ms', f'{max_ping} ms']]  # noqa
                print(tabulate(table, stralign="center",
                               tablefmt="fancy_grid", headers="firstrow"))
                # Results
                if average_ping <= 30:
                    # info_message('Your (average) ping is normal. [Average ping is less <= 30]')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════╕
│                         CONCLUSION                          │
╘═════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    table = [["Status", "Condition met"],
                         [f'Your (average) ping is {green("NORMAL", ["bold", "underlined"])}', f'Average ping is {yellow("less <= 30", "bold")}']]  # noqa

                    print(tabulate(table, stralign="center",
                                   tablefmt="fancy_grid", headers="firstrow"))
                elif average_ping < 30 and average_ping >= 100:
                    print()
                    info_message('Your (average) ping is OK. [Average ping is >= 100]')  # noqa
                elif average_ping < 100 and average_ping >= 200:
                    print()
                    info_message('Your (average) ping is high. [Average ping is >= 200]')  # noqa
                elif average_ping < 200 and average_ping >= 500:
                    print()
                    info_message('Your (average) ping is VERY HIGH. [Average ping is >= 500')  # noqa

                print()
                prompt()
                prompt()
            else:
                print()
                error_message('Unable to reach DNS server. Please check your internet connection.')  # noqa
                print()
                success_message('Finished DNS Check.\n')
                prompt()
    else:
        print()
        error_message(
            f'Invalid option: "{dns_server_choice}". Please enter a valid choice.')  # noqa
        print()
        prompt()


def speedtest():
    info_message('Running Speedtest (using Ookla Speedtest)...')
    response = os.system('speedtest')
    if response == 0:
        print()
        success_message('Speedtest completed successfully.\n')
    else:
        print()
        error_message('Unable to reach Ookla speedtest servers. Please check your internet connection.\n')  # noqa
    prompt()


def show_ip():
    print(f'{cyan("1", "bold")} - Public IP address\n{cyan("2", "bold")} - Private IP address\n')  # noqa
    choice = custom_input('(1/2): ')
    # choice = input('1 - Public IP address\n2 - Private IP address\n> ')
    if choice == '1':
        try:
            print()
            info_message(f'Public IP address: {requests.get("http://ipecho.net/plain?").text}\n')  # noqa
        except Exception:
            print()
            error_message(
                'Error - Unable to get public IP address. Please check your internet connection.\n')  # noqa
            prompt()
    elif choice == '2':
        priv_ip = os.popen("hostname -I").read()
        if priv_ip == '\n':
            print()
            error_message('Error - Unable to get private IP address. Please check your connection.\n')  # noqa
        else:
            print()
            info_message(f'Private IP address: {priv_ip}')
        # print(f'Private IP address: {os.popen("hostname -I").read()}')
    else:
        error_message('Invalid choice.')
    prompt()


def show_mac():
    # Get network MAC address
    n_mac = os.popen(
    "ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read()  # noqa
    # print(f'MAC address: {n_mac}')
    if n_mac == '':
        error_message('Error - Unable to get MAC address. Please check your connection.\n')  # noqa
    else:
        info_message(f'MAC address: {n_mac}')
    prompt()


def show_ssid():
    n_name = os.popen('nmcli -t -f NAME connection show --active').read()
    # print(f'{n_name}')
    if n_name == '':
        error_message('Error - Unable to get SSID. Please check if you are connected to a network.\n')  # noqa
    else:
        info_message(f'SSID: {n_name}')
    prompt()


def show_gateway():
    gateway = os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()  # noqa
    gateway = gateway.replace("\n", "")
    # print(f'"{gateway}"')
    if gateway == '':
        error_message('Error - Unable to get gateway. Please check your connection.\n')  # noqa
    else:
        info_message(f'Gateway: {gateway}\n')
    prompt()


def show_all(show_all_yes=None):
    # print(f'{green("Available network data to show:", "underlined")}\n{cyan("1", "bold")} - Private/Public IP Address\n{cyan("2", "bold")} - MAC Address\n{cyan("3", "bold")} - SSID (Network name)\n{cyan("4", "bold")} - Gateway\n')  # noqa
    # data_choice = custom_input('Which network data would you like to see? (1/2/3/4): ')  # noqa
    # if data_choice == '1':
    #     print()
    #     show_ip()
    # elif data_choice == '2':
    #     print()
    #     show_mac()
    # elif data_choice == '3':
    #     print()
    #     show_ssid()
    # elif data_choice == '4':
    #     print()
    #     show_gateway()
    # else:
    #     print()
    #     error_message(
    #         f'Invalid option: "{data_choice}". Please enter a valid choice.')
    #     print()
    #     prompt()

    if show_all_yes:
        # print()

        # Print network configuration header
        print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════════════╕
│                         Your Network Configuration                      │
╘═════════════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa

        # Set variables for printing network configuration
        gateway = os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()  # noqa
        gateway = gateway.replace("\n", "")

        up_interface = os.popen(
            "route | awk '/Iface/{getline; print $8}'").read()
        up_interface = up_interface.replace("\n", "")

        # n_name = os.popen('iwgetid -r').read()  # Get wireless network name

        # Work-around to get it working on Fedora Linux
        n_name = os.popen('nmcli -t -f NAME connection show --active').read()

        # Get network MAC address
        n_mac = os.popen(
            "ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read()  # noqa

        # Local IP address
        n_ip = os.popen("hostname -I").read()
        # Hostname
        # n_host = os.popen("hostname").read()

        # Show all the information in a table
        table = [["IP Address", "MAC Address", "Gateway", "Iface", "SSID"],
                 # ["", "", "", "", ""],
                 [n_ip, n_mac.upper(), gateway, up_interface, n_name]]

        print(tabulate(table, stralign="center",
                       tablefmt="fancy_grid", headers="firstrow"))
        print()
        prompt()

    else:
        print(f'{green("Available network data to show:", "underlined")}\n{cyan("1", "bold")} - Private/Public IP Address\n{cyan("2", "bold")} - MAC Address\n{cyan("3", "bold")} - SSID (Network name)\n{cyan("4", "bold")} - Gateway\n{cyan("all", "bold")} - Show all network data\n')  # noqa
        data_choice = custom_input('Which network data would you like to see? (1/2/3/4/all): ')  # noqa
        if data_choice == '1':
            print()
            show_ip()
        elif data_choice == '2':
            print()
            show_mac()
        elif data_choice == '3':
            print()
            show_ssid()
        elif data_choice == '4':
            print()
            show_gateway()
        elif data_choice == 'all':
            show_all('show_all_yes')
        else:
            print()
            error_message(
                f'Invalid option: "{data_choice}". Please enter a valid choice.')  # noqa
            print()
            prompt()


def router_check():
    print(f'{yellow("netdebug", "underlined")} => {blue("(router-check)", "bold")}\n')  # noqa
    gateway = os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()  # noqa
    gateway = gateway.replace("\n", "")
    info_message(f'Running Router Check using gateway ({gateway})...\n')
    response = os.system('ping -c 5 _gateway')
    if response == 0:
        print()
        print('═════════════════════════════════════════════════════════════')  # noqa
        print(yellow("""
╒═════════════════════════════════════════════════════════════╕
│                    Router Check Results                     │
╘═════════════════════════════════════════════════════════════╛""", "bold"))  # noqa
        print()
        info_message('Gateway (router) is working properly.')

        print()
        prompt()

    else:
        print()
        error_message('Unable to reach router (gateway)!\n')  # noqa
        prompt()


def ping(address=None):
    print(f'{yellow("netdebug", "underlined")} => {blue("(ping)", "bold")}\n')  # noqa

    if address:
        target = address
        print()
        info_message(f'Pinging {target} (5 times)...\n')
        os.system(f'ping -c 5 {target}')
        print()
        success_message(f'Finished pinging {target}\n')
        prompt()
    else:
        target = custom_input('Website/IP address to ping: ')
        print()
        info_message(f'Pinging {target} (5 times)...\n')
        os.system(f'ping -c 5 {target}')
        print()
        success_message(f'Finished pinging {target}\n')
        prompt()


def assistant():
    # custom_input('ASSISTANT: What do you need help with?')
    # print(f'{cyan("ASSISTANT:", "bold")} Hello, what do you need help with?')

    print(f'{yellow("netdebug", "underlined")} => {blue("(assistant)", "bold")}\n')  # noqa
    # custom_input('ASSISTANT: What do you need help with?')
    print(f'{cyan("ASSISTANT:", "bold")} Hello, what do you need help with?\n')
    print(f'  {yellow("1. What is my internet (upload/download) speed?", "bold")}\n  ↳ {green("Runs speedtest", "italic")}')  # noqa                                                                                                                               prompt()
    print(f'  {yellow("2. Show me my network info", "bold")}\n  ↳ {green("Shows network data of selection", "italic")}')  # noqa
    print(f'  {yellow("3. What is my (DNS) ping/latency?", "bold")}\n  ↳ {green("Runs dns-check", "italic")}')  # noqa
    print(f'  {yellow("4. Is my device able to reach my router?", "bold")}\n  ↳ {green("Runs a router check by pinging the gateway (router)", "italic")}')  # noqaprint(f'  {yellow("exit", "bold")}            |  {green("exit the program", "italic")}')  # noqa""" PROMPT """
    print(f'  {yellow("5. I need to check if a website is down or up.", "bold")}\n  ↳ {green("Runs ping", "italic")}')  # noqa
    # print(f'  {yellow("clear", "bold")}           |  {green("Clear the [terminal] screen", "italic")}')  # noqa
    # print(f'  {yellow("exit", "bold")}            |  {green("exit the program", "italic")}')  # noqaprint(f'  {yellow("exit", "bold")}            |  {green("exit the program", "italic")}')  # noqa                                  def prompt():
    print()
    user_choice = custom_input('Which one would you like help with? (1/2/3/4/5): ')  # noqa
    if user_choice == '1':
        print()
        speedtest()
    elif user_choice == '2':
        print()
        show_all()
    elif user_choice == '3':
        print()
        dns_check()
    elif user_choice == '4':
        print()
        router_check()
    elif user_choice == '5':
        print()
        ping()
    else:
        print()
        error_message('Invalid choice.\n')
    prompt()


""" PROMPT """


def prompt():
    prompt_input = input(yellow('netdebug', 'underlined') + ' ' + green('>') + ' ')  # noqa

    args = prompt_input.split()
    argsLength = len(args)
    command = args[0]

    if argsLength == 0:
        # error_message('Please enter a valid command.')
        prompt()
    else:
        if command == 'dns-check':
            print()
            dns_check()

        elif command == 'router-check':
            print()
            router_check()

        elif command == 'show':
            try:
                if args[1] == 'ip' or args[1] == '1':
                    print()
                    show_ip()
                elif args[1] == 'mac-address' or args[1] == '2':
                    print()
                    show_mac()
                elif args[1] == 'ssid' or args[1] == '3':
                    print()
                    show_ssid()
                elif args[1] == 'gateway' or args[1] == '4':
                    print()
                    show_gateway()
                elif args[1] == 'all':
                    print(show_all('show_all_yes'))
                else:
                    print()
                    error_message(
                        f'Invalid option: "{args[1]}". Please enter a valid choice.')  # noqa
                    print()

            except IndexError:
                print()
                show_all()

        elif command == 'speedtest':
            print()
            speedtest()

        elif command == 'ping':
            print()
            ping()

        elif command == 'assistant':
            print()
            assistant()

        elif command == 'exit':
            exit()

        elif command == 'clear':
            os.system('clear')
            prompt()
        elif command == 'help':
            print()
            print(f'{cyan("Commands", ["bold", "underlined"])}:')
            print(f'  {yellow("help", "bold")}            |  {green("Print this help message", "italic")}')  # noqa
            print(f'  {yellow("show", "bold")} <choice>   |  {green("Show network data of choice (or select from menu)", "italic")}')  # noqa
            print(f'  {yellow("dns-check", "bold")}       |  {green("Run a DNS check by pinging DNS servers", "italic")}')  # noqa
            print(f'  {yellow("router-check", "bold")}    |  {green("Run a router check by pinging the gateway (router)", "italic")}')  # noqa
            print(f'  {yellow("ping", "bold")}            |  {green("Run a ping check by pinging the specified address or IP", "italic")}')  # noqa
            print(f'  {yellow("assistant", "bold")}       |  {green("Solve your network issues with the help of the NetDebug Assistant!", "italic")}')  # noqa
            print(f'  {yellow("speedtest", "bold")}       |  {green("Run a network speed test using Ookla Speedtest", "italic")}')  # noqa
            print(f'  {yellow("clear", "bold")}           |  {green("Clear the [terminal] screen", "italic")}')  # noqa
            print(f'  {yellow("exit", "bold")}            |  {green("exit the program", "italic")}')  # noqaprint(f'  {yellow("exit", "bold")}            |  {green("exit the program", "italic")}')  # noqa
            print()
            prompt()

        else:
            error_message(
                f'Invalid command: "{command}". Please enter a valid command.')
            prompt()


try:
    prompt()
except KeyboardInterrupt:
    print()
    exit()
