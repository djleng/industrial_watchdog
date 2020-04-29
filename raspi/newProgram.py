from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
from temperature_sensor_simulator import get_temperature_data

class shadowCallbackContainer:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # Custom Shadow callback
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        global LEDPIN
        payloadDict = json.loads(payload)
        isLEDOn=payloadDict["state"]["isLEDOn"]
        deltaMessage = json.dumps(payloadDict["state"])
        #print(deltaMessage)
        if isLEDOn == "true":
            print("Turn on LED")
            GPIO.output(LEDPIN, GPIO.HIGH) # Turn on
        else:
            print("Turn off LED")
            GPIO.output(LEDPIN, GPIO.LOW) # Turn on    
        #print("Request to update the reported state...")
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
        
# LEDPIN=14
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)    # Ignore warning for now
# GPIO.setup(LEDPIN, GPIO.OUT, initial=GPIO.LOW)

clientId="RaspberryPi"
thingName="RaspberryPi"
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
myAWSIoTMQTTShadowClient.configureEndpoint("a3embdqzx7199y-ats.iot.us-west-1.amazonaws.com", 8883)
myAWSIoTMQTTShadowClient.configureCredentials("AmazonRootCA1.pem", "RaspberryPi-private.pem.key", "RaspberryPi-certificate.pem.crt")

# AWSIoTMQTTShadowClient connection configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10) # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5) # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()
#myAWSIoTMQTTShadowClient.publish("this/info", "connected", 0)
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)

# # Listen on deltas
# deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta)

# Delete current shadow JSON doc
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

# Loop forever
while True:
    temp = get_temperature_data()

    # Display moisture and temp readings
    #print("Moisture Level: {}".format(moistureLevel))
    print("Temperature: {}".format(temp))
    
    # Create message payload
    payload = {"state":{"reported":{"temp":str(temp)}}}

    # Update shadow
    deviceShadowHandler.shadowUpdate(json.dumps(payload), customShadowCallback_Update, 5)
    time.sleep(1)

