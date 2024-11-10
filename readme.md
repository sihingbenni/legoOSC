A Wrapper for https://pybricks.com/ev3-micropython to control via [OSC](https://opensoundcontrol.stanford.edu/)
- needs WLAN

uses modified https://github.com/SpotlightKid/micropython-osc 

## How to use
1. import this as a Lego-Micropython Projekt (https://pybricks.com/ev3-micropython/startrun.html)
2. run it on the EV3-Brick
3. use the Routes to control the Brick

# Routes:
Placeholder can be:
- `ID` for `IP-Address` or `Name`  
- `PORT` for `a`, `b`, `c`, `d`, `s1`, `s2`, `s3` or `s4` 
- `PORTs` for a group of `PORT`, e.g. `ab`, `bcd`  
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
- `/ID/light/off`  
  disables the brick lights


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
- `/ID/say/language [language as string]`  
  sets the speaker language. see [here ](https://pybricks.com/ev3-micropython/hubs.html#pybricks.hubs.EV3Brick.speaker.set_speech_options) for available ones 
- `/ID/say/voice [voice as string]`  
  sets the speaker voice. see [here ](https://pybricks.com/ev3-micropython/hubs.html#pybricks.hubs.EV3Brick.speaker.set_speech_options) for available ones 
- `/ID/say/speed [speed as int]`  
  sets the speaker speed in words per minute
- `/ID/say/pitch [pitch as int]`  
  sets the speakers pitch from 0 to 99
- `/ID/say/volume [percentage as int]`  
  sets the brick speech volume to the given percentage  
  Example: `/brick/say/volume 50` -> 50% volume

## Music



## Motor  
- `/ID/motor/PORTs/stop`
- `/ID/motor/PORTs/brake`
- `/ID/motor/PORTs/hold`
- `/ID/motor/PORTs/angle` -> sends `/ID/motor/PORT/angle/at [int]`
- `/ID/motor/PORTs/angle [int]` -> sends `/ID/motor/PORT/angle/at [int]`
- `/ID/motor/PORTs/run [int]`
- `/ID/motor/PORTs/run/until_stalled [int]` -> sends `/ID/motor/PORT/stalled [int]`
- `/ID/motor/PORTs/run/until_stalled [int, MOTOR_ACTION, int]` -> sends `/ID/motor/PORT/stalled [int]`
- `/ID/motor/PORTs/run/target [int, int]` -> sends `/ID/motor/PORT/reached/target [int]`
- `/ID/motor/PORTs/run/target [int, int, MOTOR_ACTION]` -> sends `/ID/motor/PORT/reached/target [int]`
- `/ID/motor/PORTs/multirun/target [int, ints]` -> sends per `/ID/motor/PORT/reached/target [int]`
- `/ID/motor/PORTs/multirun/target [int, ints, MOTOR_ACTION]` -> sends per `/ID/motor/PORT/reached/target [int]`


## Colorsensor
- `/ID/color/PORT` replies with `/ID/color/PORT/is [color as string]`
- `/ID/color/PORT/ambient` replies with `/ID/color/PORT/ambient/is [percentage as int]`
- `/ID/color/PORT/reflection` replies with `/ID/color/PORT/reflection/is [percentage as int]`
- `/ID/color/PORT/rgb` replies with `/ID/light/PORT/rgb/is [r as int, g as int, b as int]`


##  UltrasonicSensor
- `/ID/ultrasonic/PORT/distance` replies with `/ID/ultrasonic/PORT/distance/is [distance as int]`
- `/ID/ultrasonic/PORT/distance/silent` replies with `/ID/ultrasonic/PORT/distance/is [distance as int]`
- `/ID/ultrasonic/PORT/others` replies with `/ID/ultrasonic/PORT/others/exist [value as boolean]`


##  TouchSensor
- `/ID/touch/PORT` replies with `/ID/touch/PORT/pressed [value as bool]`
- `/ID/touch/PORT/onchange` replies with `/ID/touch/PORT/changed/pressed [value as bool]`

##  UltrasonicSensor
- `/ID/infrared/PORT/distance` replies with `/ID/infrared/PORT/distance/is [distance as int]`
