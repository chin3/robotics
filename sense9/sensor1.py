import ev3dev.ev3 as ev3

button = ev3.Button()   # object to access EV3 buttons

leftTouch = ev3.TouchSensor('in4')
rightTouch = ev3.TouchSensor('in1')


ev3.Sound.beep()  # beep to indicate loop starting
while not button.any():
#	LTvar = leftTouch.is_pressed
#	RTvar = rightTouch.is_pressed
#   print(LTvar, RTvar)
    if leftTouch.is_pressed and rightTouch.is_pressed:
        ev3.Sound.play_song([('E4', 'e')]).wait()
        ev3.Sound.speak("Stop touching me").wait()
    elif leftTouch.is_pressed:
        ev3.Sound.play_song([('C4', 'e')]).wait()
        ev3.Sound.speak("Ouch my left arm").wait()
    elif rightTouch.is_pressed:
        ev3.Sound.play_song([('G4', 'e')]).wait()
        ev3.Sound.speak("WAAAAAAAAAAAAAAAAAAAAAAAAAAAH").wait()

ev3.Sound.speak("Autobots lets roll")