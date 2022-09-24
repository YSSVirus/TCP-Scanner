import sys, re, socket, time, threading
from concurrent.futures import ThreadPoolExecutor
from socket import AF_INET
from socket import SOCK_STREAM
from colored import fg
from socket import socket as sk

class format_text:
	def __init__(self, arg):
		# Here we format the list so it is readable, and remove unnessicary characters
		self.formatted_response = arg.replace(',', '\n')
		self.formatted_response = self.formatted_response.replace("'", "")
		self.formatted_response = self.formatted_response.replace(']', '')
		self.formatted_response = self.formatted_response.replace('[', '')
		self.formatted_response = self.formatted_response.replace("'", "")
		self.formatted_response = self.formatted_response.replace(" ", "")
		pass

class Acquire_User_Input:
	def __init__(self):
		self.multi_threading = False
		arg = sys.argv[1:]
		help_menu = 'Thank you for using YSSVirus tcp scanner! Here is how to use!\n\n\n-h/-help			This gets you the help menu, it is what your seeing now\n\n-p/-port/-ports			This is what ports you will be scanning (Example: -p 22)\n\n-speed/-fast/-fast-scan			This is to use a fast multi threaded scan (be careful)\n\n-ip/-network			This is what IP address (that you own or have permission to) you will be scanning.\n\n'
		num = 0

		for var in arg:
			num = num + 1
			if var == '-h' or var == '-help':
				print(help_menu)
				sys.exit('\n\n\n\nNow that you know the commands how about you scan a network?')		

			if var == '-ip' or var == '-network': # cheecking for arguments
				#This code snippet checks the current argument (held by a count in the variable number) then goes ahead one argument to find what the user put, then obtains that.
				self.ip_number = num + 1
				self.ip_number = sys.argv[self.ip_number]		

			if var == '-p' or var == '-port' or var == '-ports':
				#This code snippet checks the current argument (held by a count in the variable number) then goes ahead one argument to find what the user put, then obtains that.
				self.ports = num + 1
				self.ports = sys.argv[self.ports]	

			if var == '-speed' or var == '-fast' or var == '-fast-scan':
				self.multi_threading = True

		if self.ip_number[0:1] == '-' or self.ports[0:1] == '-': #This checks if the first letter is a dash, this weeds out a lot of errors for users
			sys.exit('It seems you may have mis typed an argument try again! or if your having trouble try -h for help!')


def Seperating_ports():
	Acquired_input = Acquire_User_Input()
	regex = '-'
	multi_port_checker = re.findall(regex, Acquired_input.ports)
	tmp_ports = ''	

	if multi_port_checker == ['-']:
		regex = r'\d*'
		ports = re.findall(regex, Acquired_input.ports)
		for port in ports:
			regex = r'\d*'
			tmp_ports += str(re.findall(regex, port))

		ports = tmp_ports
		formatting = format_text(ports)
		ports = formatting.formatted_response
		regex = r'\d*\n'
		ports = re.findall(regex, ports)
		start_port = ports[0]
		start_port = start_port.replace('\n', '')
		end_port = ports[1]
		end_port = end_port.replace('\n', '')
		multi_port_scanner(start_port, end_port)
	else:
		single_port_scan()

def test_port_number(host, port):
    # create and configure the socket
    with sk(AF_INET, SOCK_STREAM) as sock:
        # set a timeout of a few seconds
        sock.settimeout(3)
        # connecting may fail
        try:
            # attempt to connect
            sock.connect((host, port))
            # a successful connection was made
            return True 
        except:
            # ignore the failure
            return False

def single_threaded_multi_scan(start, end):
	Acquired_input = Acquire_User_Input()
	for port in range(int(start), int(end)):
		route = (Acquired_input.ip_number, port)
		a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ping_back = a_socket.connect_ex(route)
		for x in range(3):
			try:
				if ping_back == 0:
					color = fg('green')
					print(f'> {Acquired_input.ip_number}:{port}' + color + ' OPEN')
					color = fg('white')
					print(color)
					break;
				elif x == 0:
					color = fg('red')
					print(f'> {Acquired_input.ip_number}:{port}' + color + ' CLOSED')
					color = fg('white')
					print(color)
			except:
					color = fg('yellow')
					print(f'> {Acquired_input.ip_number}:{port}' + color + ' CLOSED')
					color = fg('white')
					print(color)

def multi_port_scanner(start, end):
	Acquired_input = Acquire_User_Input()
	multi_threading = Acquired_input.multi_threading
	end = int(end) + 1
	if multi_threading == False:
		single_threaded_multi_scan(start, end)
	else:
		port = range(int(start), int(end))
		multi_thread_port_scan(Acquired_input.ip_number, port)

def single_port_scan():
			Acquired_input = Acquire_User_Input()
			ip = Acquired_input.ip_number
			port = Acquired_input.ports
			port = int(port.replace('\n', ''))
			route = (ip, port)
			a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ping_back = a_socket.connect_ex(route)
			for x in range(3):
				try:
					if ping_back == 0:
						color = fg('green')
						print(f'> {Acquired_input.ip_number}:{port}' + color + ' OPEN')
						color = fg('white')
						print(color)
						break;
					elif x == 0:
						color = fg('red')
						print(f'> {Acquired_input.ip_number}:{port}' + color + ' CLOSED')
						color = fg('white')
						print(color)
				except:
						color = fg('yellow')
						print(f'> {Acquired_input.ip_number}:{port}' + color + ' CLOSED')
						color = fg('white')
						print(color)

def multi_thread_port_scan(host, ports):
    # create the thread pool
    with ThreadPoolExecutor(len(ports)) as executor:
        # dispatch all tasks
        results = executor.map(test_port_number, [host]*len(ports), ports)
        # report results in order
        for port,is_open in zip(ports,results):
        	def results(is_open):
        		try:
        			if is_open == True:
	        			color = fg('green')
	        			print(f'> {host}:{port}' + color + ' OPEN')
	        			color = fg('white')
	        			print(color)
	        		else:
	        			color = fg('red')
	        			print(f'> {host}:{port}' + color + ' CLOSED')
	        			color = fg('white')
	        			print(color)
	        	except:
	        		color = fg('yellow')
	        		print(f'> {host}:{port}' + color + ' Error')
	       			color = fg('white')
	       			print(color)
        	results(is_open)



Seperating_ports()
