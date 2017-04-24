#!/usr/bin/env python

# Import dependencies
import paramiko
import time
import sys

# Defining constants
SSH_DEST = "192.168.1.1"
SSH_USER = "user"
SSH_PASS = "password"

# function to fetch the shell prompt of remote SSH server
def get_prompt():
	remote_conn.send("\n")
	return remote_conn.recv(500)

# function to disable paging for long contents
def disable_paging(command="terminal length 0\n"):
	remote_conn.send("\n")
	remote_conn.send(command)

# function to dispay pre-defined commands to be run in SSH server
def display_standard_commands():
	print '-'*40
	for i in range(0, len(commands)):
		print '| ', i, ' | ', commands[i], ' |'

	print '-'*40

# this function takes the command as input and sends it to SSH server
def execute_command(command, delay=1):
	remote_conn.send(command + "\n")
	time.sleep(delay)
	return remote_conn.recv(65535)

if __name__ == "__main__":
	if 'sys.argv[1]' in globals() and sys.argv[1] != "":
		ip = sys.argv[1]
	else:
		ip = SSH_DEST

	if 'sys.argv[2]' in globals() and sys.argv[2] != "":
		user = sys.argv[2]
	else:
		user = SSH_USER

	if 'sys.argv[3]' in globals() and sys.argv[3] != "":
		password = sys.argv[3]
	else:
		password = SSH_PASS

	# Declaring standard commands
	commands = [
			'show ip interface brief',
			'show interfaces summary',
			'show version',
			'conf t'
		]
	
	conn = paramiko.SSHClient()
	
	# Ignore SSH Key
	conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	# Connect
	conn.connect(ip, username=user, password=password)
	
	# Invoke Shell
	remote_conn = conn.invoke_shell()

	# Get prompt
	prompt = get_prompt()
	
	# disable paging
	disable_paging()

	#displaying standard commands
	display_standard_commands()

	loop = 1
	while loop == 1:
		# Ask user for command to run
		#prompt = "Run command: "
		input = raw_input(prompt + " ")
		if input == "bye" or input == "quit":
			loop = 0
			print "Exiting Program..."
		else:
			if input.isdigit():
				input = int(input)
				command = commands[input]
				print "Running '", command, "'..."
				output = execute_command(command)
			else:
				print "Running '" + input + "'..."
				output = execute_command(input)
			
			prompt = output.split('\n')[-1]
			print output
			print "=" * 70

	conn.close()
