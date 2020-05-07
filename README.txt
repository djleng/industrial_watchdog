EE250 Final Project: Industrial Watchdog
Rana Eltahir
Daniel Leng

Demo Link:

Nodes: Raspberry Pi transmitting temperature data, AWS MQTT, Client-side data processing & visualization

Instructions: 
1. clone respository onto local machine & raspberypi (git@github.com:djleng/industrial_watchdog.git)
2. run raspberrypi publisher in the directory industrial_watchdog/raspi with the command:
	python3 tempSim.py
3. run client subscriber in directory industrial_watchdog/client with the command:
	python3 client.py
   -note: uncomment "Data Processing & Visualization Demonstration" 

External Libraries: AWS Python SDK, ast, numpy, matplotlib, random
