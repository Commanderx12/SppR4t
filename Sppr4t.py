import random
import os
import sys
import time
import socket
from time import sleep

loading = int(1)

for loading in range(loading):
    rand2 = ["0.1", "0.3", "0.6", "0.2"]
    response = os.system("clear")
    for i in range(101):
        j = float(random.choice(rand2))
        sys.stdout.write('\r')
        a = float(random.choice(rand2))
        if i > 10:
            a = 0
        if i > 29:
            a = j
        if i > 33:
            a = 0
        if i > 60:
            a = j
        if i > 68:
            a = 0
        time.sleep(a)
        sys.stdout.write("loading sppr console [%-10s] %d%%" % ('='*i, 1*i))
        sys.stdout.flush()
        sleep(0.08)


def logo():
    respone = os.system("clear")
    print("  .                                                                       .      ")
    print(" 4                .                                       .                t     ")
    print("dX.             .dXb    __                         __    dXb.             .Xb    ")
    print("9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP    ")
    print(" 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP     ")
    print("  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'      ")
    print("    `9XXXXXXXXXXXP' `9XX'          `98v8P'          `XXP' `9XXXXXXXXXXXP'        ")
    print("        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~            ")
    print("                        )b.  .dbo.dP'`v'`9b.odb.  .dX(                           ")
    print("                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.                          ")
    print("                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb                         ")
    print("                   dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb                         ")
    print("                   9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP                         ")
    print("                     `'      9XXXXXX(   )XXXXXXP      `'                         ")
    print("                              XXXX X.`v'.X XXXX                                  ")
    print("                              XP^X'`b   d'`X^XX                                  ")
    print("                              X. 9  `   '  P )X                                  ")
    print("                              `b  `       '  d'                                  ")
    print("                               `    SppR4t   '                                   ")
    print("           | donations: https://www.donationalerts.com/r/v1xohay_ |              ")
    print("                          | type help for commands |                             ")
    print("                          |   created by v1xohay_  |                             ")

    print("\n")
    mainfunc()

def mainfunc():
    for rand in range(1):
        rand = ["1", "2", "3", "4", "5", "6", "7", "8",
                "9", "10", "11", "12", "13", "14", "15", "16"]
        alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        secs = ['1.2', '0.7', '1', '0.4', '1.5']
        r_secs = float(random.choice(secs))
        pass1 = (random.choice(alph))
        pass2 = int(random.choice(rand))
    main = input("SppR>")

    if main == "help":
        print("ver")
        print("time")
        print("banner")
        print("exit")
        print("getip")
        mainfunc()

    if main == "ver":
        print("you currently using SppR4t pre-alpha version!")
        mainfunc()

    if main == "getip":
        domain = input("domain(example.com):")
        output_ip = socket.gethostbyname(domain)
        print("starting getip on " + domain + "...")
        time.sleep(r_secs)
        print("scan complete in", end=" ")
        print(r_secs, end=" ")
        print(" seconds, result:")
        print("domain: " + domain + "\n" + "ip: " + output_ip)
        mainfunc()

    if main == "time":
        t = time.localtime(time.time())
        cur_time = time.strftime("%H:%M:%S", t)
        print(cur_time)
        cur_year = time.strftime("%Y", t)
        print("year:", cur_year)
        mainfunc()

    if main == "banner":
        logo()

    if main == "exit":
        exit()

    if main == pass1*pass2:
        exit()
    else:
        logo()


logo()
