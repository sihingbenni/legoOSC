A Wrapper for https://pybricks.com/ev3-micropython to control via [OSC](https://opensoundcontrol.stanford.edu/)
- needs WLAN

uses modified https://github.com/SpotlightKid/micropython-osc 

## How to use
1. import this as a Lego-Micropython Projekt (https://pybricks.com/ev3-micropython/startrun.html)
2. run it on the EV3-Brick
3. use the Routes to control the Brick

# Routes:
Placeholders can be:
- `ID` for `IP-Address` or `Name`  
- `PORT` for `a`, `b`, `c`, `d`, `s1`, `s2`, `s3` or `s4` 
- `PORTs` for a `PORTS` or a group of `PORT`, e.g. `a`, `ab`, `bcd`  
- `MOTOR_ACTION` for `coast`, `hold` or `brake`

## Debugging
On any error the OSCBrick should send `/ID/error [Errormessage as string]`  
- `/ID/error/test`  
  replies with a dummy-error
Received OSC can be logged with 
- `/ID/log [boolean]`   
  on `true` will mirror all the received OSC-Messages back as `/ID/log/received [message as string]`  
  disable with `false`


## Identification  
- `/oscbrick/identify` replies with `/NAME [IP as string]`
  replies with the oscbricks name as route and ip as parameter, useful to find bricks in the network  
  Example: `/oscbrick/identify` -> `/brick 192.168.0.99`


## Config 
Can be used to save the 

1. name

of the brick

- `/ID/config/save`  
  saves the current configuration to the brick for future starts
- `/ID/config/load`  
  loads the currently saved configuration
- `/ID/config/reset`  
  resets the current configuration to default values


## Name  
- `/ID/name` replies with `/IP/name/current [NAME as string]`  
  replies with the oscbricks name  
  Example: `/192.168.0.99/name` -> `/192.168.0.99/name/current brick`
- `/ID/name [NEW_NAME as string]` replies with `/OLD_NAME/name/changed [NEW_NAME as string]`
  sets the name of the brick  
  Example: `/brick/name realBrick` -> `/brick/name/changed realBrick`


## Light
- `/ID/light [color as string]`  
  sets the brick lights color. Possible colors are `black`, `blue`, `green`, `yellow`, `red`, `white`, `brown`, `orange` or `purple`  
  Example: `/brick/light yellow` -> buttons glow yellow
- `/ID/light/off`  
  disables the brick lights  
  Example: `/brick/light/off` -> buttons stop glowing


## Beep  
  There can only be one beep. Any new call will dismiss the old one.
- `/ID/beep`  
  lets the brick beep with the default tone and duration
- `/ID/beep [duration as int]`  
  lets the brick beep with the default tone for the given duration in ms  
  Example: `/brick/beep 1000` -> beeps for 1s
- `/ID/beep [duration as int, frequency as int]`  
  lets the brick beep with the given frequency in hz for the given duration in ms  
  Example: `/brick/beep 1000 100` -> beeps for 1s with a low tone
- `/ID/beep/volume [percentage as int]`  
  sets the brick beep volume to the given percentage  
  Example: `/brick/beep/volume 50` -> 50% volume


## TtS
Can only say one text at a time and breaks both if trying to say another, while already speaking
- `/ID/say [word as string]`  
  lets the brick beep with the default tone and duration  
  Example: `/brick/say hello` -> says `hello` 
- `/ID/say/language [language as string]`  
  sets the speaker language. see [here ](https://pybricks.com/ev3-micropython/hubs.html#pybricks.hubs.EV3Brick.speaker.set_speech_options) for available ones  
  Example: `/brick/say/language it` -> italian pronunciation
- `/ID/say/voice [voice as string]`  
  sets the speaker voice. see [here ](https://pybricks.com/ev3-micropython/hubs.html#pybricks.hubs.EV3Brick.speaker.set_speech_options) for available ones  
  Example: `/brick/say/voice m3` -> a male voice
- `/ID/say/speed [speed as int]`  
  sets the speaker speed in words per minute  
  Example: `/brick/say/speed 50` -> 50 word per minute
- `/ID/say/pitch [pitch as int]`  
  sets the speakers pitch from 0 to 99  
  Example: `/brick/say/pitch 50` -> 99 high pitch voice 
- `/ID/say/volume [percentage as int]`  
  sets the brick speech volume to the given percentage  
  Example: `/brick/say/volume 50` -> 50% volume

## Music



## Motor  
- `/ID/motor/PORTs/stop`  
  stops the motor at PORTs  
  Example: `/brick/motor/a/stop` -> motor at port a stops and runs out
- `/ID/motor/PORTs/brake`  
  stops and brakes the motor at PORTs  
  Example: `/brick/motor/a/brake` -> motor at port a stops and brakes  
- `/ID/motor/PORTs/hold`  
  holds the motor at PORTs  
  Example: `/brick/motor/a/hold` -> motor at port a holds the current position
- `/ID/motor/PORTs/angle` -> sends `/ID/motor/PORT/angle/at [angle as int]`  
  returns the current angle of the motor at the given PORTs. Angle can be a negative or positive integer  
  Example: `/brick/motor/a/angle` -> sends `/brick/motor/a/angle/at 271` motor at port a is at 271°
- `/ID/motor/PORTs/angle [angle as int]` -> sends `/ID/motor/PORT/angle/at [angle as int]`  
  sets the current angle of the motor at the given PORTs to the given number. Angle can be a negative or positive integer  
  Example: `/brick/motor/a/angle 90` -> sends `/brick/motor/a/angle/at 90` the motor at port a is set to 90°
- `/ID/motor/PORTs/run [speed as int]`  
  runs the motor at PORTs with the given speed. Speed can be a negative or positive integer  
  Example: `/brick/motor/a/run 100` -> motor at port a runs with speed 100
- `/ID/motor/PORTs/run/until_stalled [speed as int]` -> sends `/ID/motor/PORT/stalled [angle as int]`  
  runs the motor at PORTs with the given speed until blocked and sends the angle it has been stalled. Speed can be a negative or positive integer  
  Example: `/brick/motor/a/run/until_stalled 100` -> `/brick/motor/a/stalled 773` motor at port a ran with speed 100 until it is blocked at 773°
- `/ID/motor/PORTs/run/until_stalled [speed as int, MOTOR_ACTION as string, power as int]` -> sends `/ID/motor/PORT/stalled [int]`  
  runs the motor at PORTs with the given speed until blocked and sends the angle it has been stalled.  
  - Speed can be a negative or positive integer  
  - MOTOR_ACTION defines how the robot should behave after stalling
  - power is the percentage of the motor torque. 0 to 100
  
  Example: `/brick/motor/a/run/until_stalled 100 hold 25` -> `/brick/motor/a/stalled 773` motor at port a ran with speed 100 and 25% torque until it is blocked at 773° and holds its position there
- `/ID/motor/PORTs/run/target [speed as int, angle as int]` -> sends `/ID/motor/PORT/reached/target [angle as int]`  
  runs the motor at PORTs with the given speed to the given angle. Speed and angle can be a negative or positive integer and is in relation to the given angle  
  Example: 
  - `/brick/motor/a/run/target 100 1000` -> `/brick/motor/a/reached/target 1000` motor at port a runs with speed 100 until it reaches 1000°
  - `/brick/motor/a/run/target 250 -300` -> `/brick/motor/a/reached/target -300` motor at port a runs with speed -250 until it reaches -300°
- `/ID/motor/PORTs/run/target [speed as int, angle as int, MOTOR_ACTION as string]` -> sends `/ID/motor/PORT/reached/target [angle as int]`  
  runs the motor at PORTs with the given speed to the given angle and executes the given MOTOR_ACTION. Speed and angle can be a negative or positive integer and is in relation to the given angle   
  Example:  
  - `/brick/motor/a/run/target 100 1000 hold` -> `/brick/motor/a/reached/target 1000` motor at port a runs with speed 100 until it reaches 1000° and holds there   
  - `/brick/motor/a/run/target 100 -500 hold` -> `/brick/motor/a/reached/target -500` motor at port a runs with speed -100 until it reaches 500° and holds there
- `/ID/motor/PORTs/multirun/target [int, ints]` -> sends per `/ID/motor/PORT/reached/target [int]`  
  runs the motor at PORTs with the given speed to the given angle corresponding to the port position. Speed and angles can be a negative or positive integer and is in relation to the given angle    
  Example: `/brick/motor/ab/run/target 100 1000 -1000` -> `/brick/motor/a/reached/target 1000` and `/brick/motor/b/reached/target -1000`  
  - motor at port a runs with speed 100 until it reaches 1000°
  - motor at port b runs with speed -100 until it reaches -1000°
- `/ID/motor/PORTs/multirun/target [int, ints, MOTOR_ACTION]` -> sends per `/ID/motor/PORT/reached/target [int]`  
  runs the motor at PORTs with the given speed to the given angle corresponding to the port position. Speed and angles can be a negative or positive integer and is in relation to the given angle    
  Example: `/brick/motor/ab/run/target 100 1000 -1000 hold` -> `/brick/motor/a/reached/target 1000` and `/brick/motor/b/reached/target -1000`  
  - motor at port a runs with speed 100 until it reaches 1000° and holds there 
  - motor at port b runs with speed -100 until it reaches -1000° and holds there


## Colorsensor
- `/ID/color/PORT` replies with `/ID/color/PORT/is [color as string]`  
  returns the color at PORT. Possible colors are `black`, `blue`, `green`, `yellow`, `red`, `white`, `brown` or `none`  
  Example: `/brick/color/s1` -> `/brick/color/s1/is white` color is `white`
- `/ID/color/PORT/ambient` replies with `/ID/color/PORT/ambient/is [percentage as int]`  
  returns the light intensity at PORT as a percentage  
  Example: `/brick/color/s1/ambient` -> `/brick/color/s1/ambient/is 40` light-intensity is 40% 
- `/ID/color/PORT/reflection` replies with `/ID/color/PORT/reflection/is [percentage as int]`  
  returns the light reflection at PORT as a percentage  
  Example: `/brick/color/s1/reflection` -> `/brick/color/s1/reflection/is 24` light-reflection is 24% 
- `/ID/color/PORT/rgb` replies with `/ID/light/PORT/rgb/is [red as int, green as int, blue as int]`  
  returns the light reflection of red, green and blue light at PORT as a percentage  
  Example: `/brick/color/s1/rgb` -> `/brick/color/s1/rgb/is 10 90 0` light-reflection of red light is 10%, green light 90% and blue light 0%


##  UltrasonicSensor
- `/ID/ultrasonic/PORT/distance` replies with `/ID/ultrasonic/PORT/distance/is [distance as int]`  
  returns the distance at PORT in millimeter. distance is a positive integer  
  Example: `/brick/ultrasonic/s3/distance` -> `/brick/ultrasonic/s3/distance/is 50` distance to measured object is 50mm 
- `/ID/ultrasonic/PORT/distance/silent` replies with `/ID/ultrasonic/PORT/distance/is [distance as int]`  
  returns the distance at PORT in millimeter and disables the sensor afterwards[*](https://pybricks.com/ev3-micropython/ev3devices.html#pybricks.ev3devices.UltrasonicSensor.distance). distance is a positive integer  
  Example: `/brick/ultrasonic/s3/distance/silent` -> `/brick/ultrasonic/s3/distance/is 50` distance to measured object is 50mm and sensor is disabled
- `/ID/ultrasonic/PORT/others` replies with `/ID/ultrasonic/PORT/others/exist [value as boolean]`  
  checks if there are other ultrasonic sensors.  
  Example: `/brick/ultrasonic/s3/others` -> `/brick/ultrasonic/s3/others/exist true` other sensors exist 


##  TouchSensor
- `/ID/touch/PORT` replies with `/ID/touch/PORT/pressed [value as bool]`  
  returns the status at PORT  
  Example: `/brick/touch/s3` -> `/brick/touch/s3/pressed true` sensor is pressed 
- `/ID/touch/PORT/onchange` replies with `/ID/touch/PORT/changed/pressed [value as bool]`  
  sets a listener to relay status changes at PORT  
  Example: `/brick/touch/s3/onchange` -> `/brick/touch/s3/changed/pressed true` when sensor is pressed and `/brick/touch/s3/changed/pressed false` when sensor is released

##  InfraredSensor
- `/ID/infrared/PORT/distance` replies with `/ID/infrared/PORT/distance/is [distance as int]`  
  returns the distance at PORT in 0 to 100 percent.  
  Example: `/brick/infrared/s2/distance` -> `/brick/infrared/s2/distance/is 80` distance is 80%
