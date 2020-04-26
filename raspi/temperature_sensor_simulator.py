import numpy as np
#from argparse import ArgumentParser

def get_temperature_data():
    time = 0;
    initial_temperature = 48
    rate = 1
    dt = 0.5
    step_count=60
    temp = np.zeros(step_count+2)

    temp[0] = initial_temperature
    for i in range(step_count+1):
        temp[i+1] = temp[i] + rate * dt
    
    return 74

#def __main__():
#    dat = get_temperature_data()
#    print(*dat, sep=", ")


#if __name__ == '__main__':
#    __main__()
   
        
