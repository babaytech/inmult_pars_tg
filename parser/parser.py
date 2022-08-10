####################################################
from threading import Thread 
import time
####################################################

def loop():
	while True:
		print("1")
		time.sleep(1)

def loop1():
	while True:
		print("2")
		time.sleep(1)

Thread(target=loop).start().join()
Thread(target=loop1).start().join()
