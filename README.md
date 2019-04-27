
# Design Overview

### App

Links Drone and controller and dispatches chance to execute



### Drone

Links Sensors and Motors and contains core stabalization logic, 
controlled with operations such as XYZ

### Controller

Differnt controllers permit different types of operations, 
the controller is responsible for determining overall navigation
(Smallest case: reading inputs from a remote control or phone app 
vs Largest Case: Autonomous flight such as flying to a proscribed 
destination etc)

### MotorMatrix 

Controlled from the Drone class

Links motor speeds into pitch, yaw, roll operations

### SensorData

Managed from the Drone  class

Manages position sensor that provides accelaration, and accumulates those
accelarations into velocity and position information.   

Also contains calibration logic


# Operating the Drone

## Calibration 

In the first 2 seconds the drone must be on a flat level surface. 
During this time the drone is reading sensor data and normalizing the readings 
To represent a zero acceleration scenario

TODO: Full deflection and senstivity calculation is not occuring


## Testing

Run `./test.sh` to trigger test cases
Must install gnuplot to see test graphs


## References
 
 MPU 9250 Interface Derived from https://github.com/PiStuffing/Quadcopter/blob/master/Quadcopter.py


