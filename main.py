import os
from os import *
from multiprocessing import Process
import time
import timeit

def nmap(ip):
    #print("starting nmap")
    os.system(f'nmap -sC -sV {ip} > ./nmap.txt')
    print("finished nmap")

def scan_cartelle(dominio):
    #print("starting cartelle")
    os.system(f"gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://{dominio} -t 100 -s 200,301,403 > ./scan_cartelle.txt")
    print("finished scan_cartelle")

def scan_file(dominio, f):
    #print("starting file")
    os.system(f"gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://{dominio} -x {f} -t 100 -s 200,301,403 > ./scan_file.txt")
    print("finished scan_file")

def scan_virtualhost(dominio):
    #print("starting vhost")
    os.system(f"gobuster vhost -w /usr/share/SecLists/Discovery/DNS/namelist.txt -u {dominio} -t 100 > ./virtual_host.txt")
    print("finished vhost")

if __name__ == '__main__':
    start = timeit.default_timer()
    ip = input("Please enter the ip to scan for: ")
    dominio = input("Please enter the domain to scan for: ")
    entropia = input("Enter 1 for small wordlist, 2 for medium wordlist, 3 for large wordlist: ")
    formato = int(input("Enter 1 for php, 2 for html: "))
    switcher = {
        1: "php",
        2: "html",
    }
    f = switcher.get(formato)
    p1 = Process(target=nmap, args=(ip,))
    p2 = Process(target=scan_cartelle, args=(dominio,))
    p3 = Process(target=scan_file, args=(dominio, f))
    p4 = Process(target=scan_virtualhost, args=(dominio,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    stop = timeit.default_timer()
    print('Time: ', stop - start)