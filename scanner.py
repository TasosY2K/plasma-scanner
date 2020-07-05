import requests
import random
import threading
import sys
from pyfiglet import Figlet

print(Figlet(font='Graffiti').renderText('plasma-scanner'))

api_url = "http://localhost:3000"
api_token = "416c41ac-f05f-48d5-ad5f-8b04952b7394"

def GetIP():
	ip = ""
	ip += str(random.randint(1,255)) + "."
	ip += str(random.randint(1,255)) + "."
	ip += str(random.randint(1,255)) + "."
	ip += str(random.randint(1,255))
	return ip

def CheckConnection(url, key):
	try:
		print("[*] Checking API credidentials and connection...")
		req = requests.get(url, timeout=10)
		if req.status_code == 200:
			try:
				req = requests.get(f"{url}/bots/token/{key}", timeout=10)
				if req.status_code == 404:
					print("[-] Could not authenticate token | " + key)
					return False
				else:
					print("[+] Authenticated | " + key)
					return True
			except:
				pass
		else:
			print("[-] API seems to be down")
			return False
	except:
		print("[-] API seems to be down")
		return False

def CheckIp(ip):
	try:
		req = requests.get("http://" + ip, timeout=10, allow_redirects=True)
		if req.status_code == 200:
			try:
				req = requests.post(f"{api_url}/devices/{ip}/{api_token}", timeout=30)
				if req.status_code == 201:
					print('[↑] ' + ip)
				else:
					print('[↓] ' + req.text)
			except:
				print("[-] API seems to be down")
				pass
	except:
		pass

def Loop():
	while True:
		CheckIp(GetIP())

if __name__ == '__main__':
	if (CheckConnection(api_url, api_token)):
		for i in range(400):
			threading.Thread(target=Loop).start()
	else:
		sys.exit()
