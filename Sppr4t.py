import random
import os
import sys
import time
import socket
import datetime
import threading
import requests
import psycopg2
import click
from decouple import config
import traceback

scan_results = {
    "getip": [],
    "portscan": [],
}

def clear_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

rand2=['0.1','0.3','0.6','0.2']
for loading in range(0):
    j = float(random.choice(rand2))
    click.echo('\r', nl=False)
    a = float(random.choice(rand2))
    if loading>10:a=0
    if loading>29:a=j
    if loading>33:a=0
    if loading>60:a=j
    if loading>68:a=0
    time.sleep(a)
    click.echo('loading SppR console [%-10s] %d%%' % ('=' * loading, loading), nl=False)
    click.echo('', nl=True)
    time.sleep(0.08)

report_counter = 1

def generate_report():
    global report_counter
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}_{report_counter}.txt"

    with open(report_filename, "w") as report_file:
        report_file.write("**** Scan Report ****\n")

        report_file.write("\n--- getip Scan Results ---\n")
        if scan_results["getip"]:
            for index, result in enumerate(scan_results["getip"], 1):
                report_file.write(f"Domain: {result['domain']}\nIP: {result['ip']}\nScan Time: {result['scan_time']:.1f} seconds\n")
                report_file.write(f"Timestamp: {result['timestamp']}\n")
                if index < len(scan_results["getip"]):
                    report_file.write("-------------------\n")
        else:
            report_file.write("No getip scans have been performed.\n\n")

        report_file.write("\n--- Port Scan Results ---\n")
        if scan_results["portscan"]:
            for index, result in enumerate(scan_results["portscan"], 1):
                report_file.write(f"Target IP: {result['target_ip']}\n")
                if result['open_ports']:
                    report_file.write(f"Open Ports: {', '.join(map(str, result['open_ports']))}\n")
                else:
                    report_file.write("No open ports found.\n")
                report_file.write(f"Scan Time: {result['scan_time']:.1f} seconds\n")
                report_file.write(f"Timestamp: {result['timestamp']}\n")
                if index < len(scan_results["portscan"]):
                    report_file.write("-------------------\n")
        else:
            report_file.write("No port scans have been performed.\n\n")

    print(f"Scan report has been saved to {report_filename}")
    report_counter += 1

def logo():
    clear_screen()
    with open('ASCII.txt', 'r') as file:
        ascii_art = file.read()
    print(ascii_art)

    print("\n")
    mainfunc()

def scan_ports(target_ip):
    open_ports = []
    ports_to_scan = [20, 21, 22, 23, 25, 53, 80, 443, 8080, 110, 143, 587, 3306, 3389, 5900]

    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    return open_ports

def port_scan_worker(target_ip, start_time):
    try:
        open_ports = scan_ports(target_ip)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time

        scan_results["portscan"].append({
            "target_ip": target_ip,
            "open_ports": open_ports,
            "scan_time": elapsed_time.total_seconds(),
            "timestamp": end_time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        save_scan_results_to_db()

    except socket.gaierror:
        print("Ошибка: Не удалось определить IP-адрес цели. Пожалуйста, проверьте правильность IP.")
    except Exception as e:
        print("Произошла ошибка:", str(e))

def save_scan_results_to_db():
    with open('port.txt', 'r') as file:
        # Читаем содержимое файла
        file_contents = file.read()
    try:
        port = int(file_contents)  # Преобразуем порт в целое число
        connection = psycopg2.connect(
            host=config('host'),
            port=port,
            user=config('user'),
            password=config('password'),
            database=config('database')
        )

        cursor = connection.cursor()

        # Вставка данных сканирования IP
        for result in scan_results["getip"]:
            query = "INSERT INTO getip_scan_results (domain, ip, scan_time, timestamp) VALUES (%s, %s, %s, %s);"
            data = (result["domain"], result["ip"], result["scan_time"], result["timestamp"])
            cursor.execute(query, data)

        # Вставка данных сканирования портов
        for result in scan_results["portscan"]:
            query = "INSERT INTO portscan_scan_results (target_ip, open_ports, scan_time, timestamp) VALUES (%s, %s, %s, %s);"
            data = (result["target_ip"], result["open_ports"], result["scan_time"], result["timestamp"])
            cursor.execute(query, data)

        connection.commit()
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print("Ошибка при сохранении данных в базу данных:", e)
        if 'query' in locals():
            print("Строка запроса:", query)
        if 'data' in locals():
            print("Данные:", data)
        raise  # Перевыбрасываем исключение, чтобы получить полный стек вызовов

    except Exception as e:
        print("Произошла ошибка при сохранении данных в базу данных:", str(e))



def mainfunc():
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    pass1 = (random.choice(alph))
    pass2 = int(random.choice(range(1, 17)))

    command_help = {
        "getip": "Get the IP address of a domain (example.com).",
        "banner": "Clear the console screen and display the program's banner.",
        "clear": "Clear the console screen.",
        "time": "Show the current time and year.",
        "ver": "Display the current version of the program.",
        "help": "Show a list of available commands.",
        "exit": "Exit the program.",
        "report": "Generate and save a scan report.",
        "portscan": "Scan open ports on a target IP address.",
    }

    main = input("SppR>")

    if main == "help":
        print("Available commands:")
        for command, description in command_help.items():
            print(f"{command}: {description}")
        mainfunc()

    if main == "ver":
        print("You are currently using SppR4t pre-alpha version!")
        mainfunc()

    if main == "time":
        t = time.localtime(time.time())
        cur_time = time.strftime("%H:%M:%S", t)
        print(cur_time)
        cur_year = time.strftime("%Y", t)
        print("year:", cur_year)
        mainfunc()

    if main == "report":
        generate_report()
        mainfunc()

    if main == "banner":
        logo()

    if main == "clear":
        clear_screen()

    if main == "exit":
        exit()

    if main == pass1 * pass2:
        exit()

    if main == "getip":
        domain = input("Enter the domain (example.com): ")
        try:
            output_ip = socket.gethostbyname(domain)
            print("Starting getip on " + domain + "...")
            start_time = datetime.datetime.now()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print(f"Scan complete in {elapsed_time.total_seconds():.2f} seconds, result:")
            print(f"Domain: {domain}\nIP: {output_ip}\nTime: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

            scan_results["getip"].append({
                "domain": domain,
                "ip": output_ip,
                "scan_time": round(elapsed_time.total_seconds(), 2),
                "timestamp": end_time.strftime('%Y-%m-%d %H:%M:%S'),
            })

            save_scan_results_to_db()

        except socket.gaierror:
            print("Error: Could not resolve the domain name. Please check if the domain is valid.")
            mainfunc()
        except Exception as e:
            traceback.print_exc()  # Это выведет трассировку стека и поможет определить ошибку\
            mainfunc
        mainfunc()

    if main == "portscan":
        target_ip = input("Enter the target IP address: ")
        try:
            print("Starting portscan on " + target_ip + "...")
            start_time = datetime.datetime.now()

            port_scan_thread = threading.Thread(target=port_scan_worker, args=(target_ip, start_time))
            port_scan_thread.start()

            port_scan_thread.join()

        except Exception as e:
            print("An error occurred:", str(e))

    else:
        print("\033[1;31mInvalid command. Type 'help' for a list of commands.\033[0m")
        mainfunc()
    mainfunc()

if __name__ == "__main__":
    logo()
