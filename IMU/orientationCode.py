import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy
import math
 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)
 
while True:
    time.sleep(5)
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    #Gives Pitch Data then decides which quadrant the arctan value is and adds/subtracts to give a final output in degrees
    pitch = 180 * numpy.arctan2(accel_x, (accel_y*accel_y + accel_z*accel_z)**0.5)/numpy.pi
    if accel_x >= 0 and accel_z >= 0 : 
        pass
    elif accel_z <= 0 and accel_x >= 0 :
        pitch = 180 - pitch
    elif accel_z <= 0 and accel_x < 0 :
        pitch = 180 - pitch
    elif accel_z >= 0 and accel_x <= 0 :
        pitch = pitch + 360
    
    print("pitch: " + str(pitch))   
     
    roll = (-180) * numpy.arctan2(accel_y, (accel_x*accel_x + accel_z*accel_z)**0.5)/numpy.pi
    if accel_z >= 0 and accel_y < 0:
        pass
    if accel_z <= 0 and accel_y < 0:
        roll = 180 - roll
    if accel_z <= 0 and accel_y > 0:
        roll = 180 - roll
    if accel_z > 0 and accel_y >= 0:
        roll = roll + 360
      
    print("roll: "+ str(roll))
    
    roll_rad = roll*math.pi/180
    pitch_rad = pitch*math.pi/180
    
    mag_x_comp1 = mag_x*math.cos(pitch_rad) + mag_y*math.sin(roll_rad)*math.sin(pitch_rad) + mag_z*math.cos(roll_rad)*math.sin(pitch_rad)
    mag_y_comp1 = mag_y * math.cos(roll_rad) - mag_z * math.sin(roll_rad)
                                                                
    yaw = 180 * numpy.arctan2(-mag_y_comp1, mag_x_comp1)/ numpy.pi
    if yaw < 0:
        yaw = yaw + 360
    print("yaw: " + str(yaw))
    
    if heading > 0 and heading > 270:
        heading_dir = str(heading) + " (NorthWest)"
    if math.isclose(heading, 0.0, abs_tol=0.1):
        heading_dir = str(heading) + " (North)"
    if math.isclose(heading, 270.0, abs_tol=0.1):
        heading_dir = str(heading) + " (West)"
    if math.isclose(heading, 180.0, abs_tol=0.1):
        heading_dir = str(heading) + " (South)"
    if math.isclose(heading, 90.0, abs_tol=0.1):
        heading_dir = str(heading) + " (East)"
    if heading > 0 and heading < 90:
        heading_dir = str(heading) + " (NorthEast)"
    if heading > 90 and heading < 180:
        heading_dir = str(heading) + " (SouthEast)"
    if heading > 180 and heading < 270:
        heading_dir = str(heading) + " (SouthWest)"
    
    print("Heading:" + str(heading_dir))
