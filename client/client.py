from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from temperature_sensor_simulator import get_temperature_data
import ast
import numpy as np
import matplotlib.pyplot as plt
import random as ran

#################################################
# Data Processing & Visualization Demonstration #
#################################################
dx = 1
x = np.arange(1, 3601, dx)
# log to represent annealing curve of quartz
y = np.log(x)

# perterbate the system
for i in np.nditer(x, op_flags=['readwrite']):
    i[...] = i + ran.uniform(0.0, 200.0)

# data processing
y_avg = np.mean(y.reshape(-1, 5), axis=1)
x_avg = np.arange(0, 3600, 5)

# visualize
plt.plot(x, y*60 + 400, label="original")
plt.plot(x_avg, y_avg*60+400, label="avg")
# plt.plot(x,y_ema, label = "ema")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.ylabel('Temperature(F)')
plt.xlabel('Time (min)')
plt.show()
###########################################################
###########################################################
data = np.zeros(shape=(3600,))


def customCallback(client, userdata, message):
    print("Received a new message: ")
    dict_str = message.payload.decode("UTF-8")
    myData = ast.literal_eval(dict_str)
    temp = myData["message"]
    print(myData["message"])

    print(message.topic)
    print("--------------\n\n")


def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data[0])
    print("++++++++++++++\n\n")


clientId = "Client"
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(
    "a3embdqzx7199y-ats.iot.us-west-1.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials(
    "AmazonRootCA1.pem", "client-private.pem.key", "client-certificate.pem.crt")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# Infinite offline Publish queueing
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTClient.connect()


myAWSIoTMQTTClient.subscribe("info/test", 1, customCallback)


while True:
    time.sleep(1)
