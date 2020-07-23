import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy
import math
import matplotlib.pyplot as plt
 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)
start = time.time()
ys = []
xs = []

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

while time.time() - start < 20:
    time.sleep(0.1)
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    '''
    mag_offset = [15.15, -18.8, 23.35]
    mag_scale = [0.97, 1, 1.03]
    mag_x = mag_x*mag_scale[0] - mag_offset[0]
    mag_y = mag_y*mag_scale[1] - mag_offset[0]
    mag_z = mag_z*mag_scale[2] - mag_offset[0]
    '''
    #Gives Pitch Data then decides which quadrant the arctan value is and adds/subtracts to give a final output in degrees
    pitch = 180 * numpy.arctan2(accel_x, (accel_y*accel_y + accel_z*accel_z)**0.5)/numpy.pi
    pitch_corrected = 180 * numpy.arctan2(accel_x, (accel_y*accel_y + accel_z*accel_z)**0.5)/numpy.pi
    if accel_x >= 0 and accel_z >= 0 : 
        pass
    elif accel_z <= 0 and accel_x >= 0 :
        pitch_corrected = 180 - pitch
    elif accel_z <= 0 and accel_x < 0 :
        pitch_corrected = 180 - pitch
    elif accel_z >= 0 and accel_x <= 0 :
        pitch_corrected = pitch + 360
    
    print("pitch: " + str(pitch_corrected))   
     
    roll = (180) * numpy.arctan2(accel_y, (accel_x*accel_x + accel_z*accel_z)**0.5)/numpy.pi
    roll_corrected = (180) * numpy.arctan2(accel_y, (accel_x*accel_x + accel_z*accel_z)**0.5)/numpy.pi
    if accel_z >= 0 and accel_y < 0:
        pass
    if accel_z <= 0 and accel_y < 0:
        roll_corrected = 180 - roll
    if accel_z <= 0 and accel_y > 0:
        roll_corrected = 180 - roll
    if accel_z > 0 and accel_y >= 0:
        roll_corrected = roll + 360
      
    print("roll: "+ str(roll_corrected))
    
    roll_rad = roll*numpy.pi/180
    pitch_rad = pitch*numpy.pi/180
    
    mag_x_comp1 = mag_x*math.cos(pitch_rad) + mag_y*math.sin(roll_rad)*math.sin(pitch_rad) + mag_z*math.cos(roll_rad)*math.sin(pitch_rad)
    mag_y_comp1 = mag_y * math.cos(roll_rad) - mag_z * math.sin(roll_rad)
    
    yaw = 180 * numpy.arctan2(-mag_y_comp1, mag_x_comp1)/ numpy.pi
    if yaw < 0:
        yaw = yaw + 360
    print("yaw: " + str(yaw))
    
    xs.append(time.time())
    ys.append(yaw)
    
    heading = 0
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

ax.clear()
ax.scatter(xs,ys,label = "Yaw")
plt.title('Roll Pitch Yaw, Using Accelerometer and Magnetometer')
plt.ylabel('deg')
plt.xlabel('Time')
plt.grid()
plt.legend()
plt.show()
while True:
    pass