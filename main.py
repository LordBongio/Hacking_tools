import os
from multiprocessing import Process
import ipaddress
from distutils.spawn import find_executable

# functions
def is_tool(name):
    """Check whether `name` is on PATH."""
    if find_executable(name) != None:
        print(f"{name} is installed")
        exit = False
    else:
        print(f"there is no executable named {name},please install it before running this script")
        exit = True
    return exit

def nmap(ip):
    print("started nmap")
    os.system(f'nmap -sC -sV {ip} > ./nmap.txt')
    print("finished nmap")


def scan_cartelle(dominio, wordlist):
    print("started scanning for directories")
    os.system(f"gobuster dir -w {wordlist} -u http://{dominio} -t 100 -s 200,301,403 > ./scan_cartelle.txt")
    print("finished scanning for directories")


def scan_file(dominio, f, wordlist):
    print("started scanning for files")
    os.system(f"gobuster dir -w {wordlist} -u http://{dominio} -x {f} -t 100 -s 200,301,403 > ./scan_file.txt")
    print("finished scanning for files")


def scan_virtualhost(dominio, wordlist):
    print("started scanning for vhost")
    os.system(f"gobuster vhost -w {wordlist} -u {dominio} -t 100 > ./virtual_host.txt")
    print("finished scanning for vhost")


# main
if __name__ == '__main__':
    print("This script is meant to automate the enumeration of HTB or real world machines. Note that we don't take responsibility for your action. \n"
          "This script simply uses gobuster and nmap to scan for ports-directories-files-vhost using pre defined attributes, so it is not reccomended \n"
          "for an accurate results (dont come at us crying if you missed the HTB flag because of this script :/ ) \n"
          "This script has been created with the purpose of saving you about 2 min (per run) of your life, ENJOY! \n \n \n")

    programs = ["gobuster", "nmap"]
    e = False
    for p in programs:
        if is_tool(p) == True:
            e = True
        else:
            continue

    if(e == False):
        # input parameters

        # input ip
        while True:
            try:
                ip = ipaddress.ip_address(input('\nEnter IP address to scan for: '))
                break
            except ValueError:
                continue

        # input domain
        while True:
            domain = input("Please enter the domain to scan for: ")
            if domain == "":
                print("you entered a blanket domain, type a domain")
            else:
                break

        # input wordlist to scan for dir,files,vhosts
        wordlist_dir = input(
            "Enter the wordlist (with absolute path) you want to use for scanning directories (IF LEFT BLANK, DEFAULT WORDLIST WILL BE USED): ")
        if wordlist_dir == "":
            wordlist_dir = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"
        wordlist_file = input(
            "Enter the wordlist (with absolute path) you want to use for scanning files (IF LEFT BLANK, DEFAULT WORDLIST WILL BE USED): ")
        if wordlist_file == "":
            wordlist_file = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"
        wordlist_vhost = input(
            "Enter the wordlist (with absolute path) you want to use for scanning vhost (IF LEFT BLANK, DEFAULT WORDLIST WILL BE USED): ")
        if wordlist_vhost == "":
            wordlist_vhost = "/usr/share/SecLists/Discovery/DNS/namelist.txt"
        formato = int(input("Enter 1 for php, 2 for html: "))

        # input extension
        switcher_estensione = {
            1: "php",
            2: "html",
        }
        f = switcher_estensione.get(formato)

        # DA QUEL CHE SO, QUANDO SI PASSANO I PARAMETRI USANDO I PROCESSI, BISOGNA SEMPRE METTERE UNA VIRGOLA FINALE
        p1 = Process(target=nmap, args=(ip,))
        p2 = Process(target=scan_cartelle, args=(domain, wordlist_dir,))
        p3 = Process(target=scan_file, args=(domain, f, wordlist_file,))
        p4 = Process(target=scan_virtualhost, args=(domain, wordlist_vhost,))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
    else:
        print("make sure to install all the executable needed, then run the script")
