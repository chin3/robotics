import ev3dev.ev3 as ev3
class SturdyRobot(object):
	def __init__(self, lmot, rmot, mmot):
		self.lmot = lmot
		self.rmot = rmot
		self.mmot = mmot
	def forward(self,speed, time = None):
		self.lmot.speed_sp = self.lmot.max_speed*speed
		self.rmot.speed_sp = self.rmot.max_speed*speed
#		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
#		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.run_forever()
		self.rmot.run_forever()
#		self.lmot.wait_until_not_moving()
	def backward(self, speed,time = None):
		self.lmot.speed_sp = -(self.lmot.max_speed*speed)
		self.rmot.speed_sp = -(self.rmot.max_speed*speed)
		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.wait_until_not_moving()
	
	def turnLeft(self, speed, time= None):
		self.lmot.speed_sp = -self.lmot.max_speed*speed
		self.rmot.speed_sp = self.rmot.max_speed*speed
		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.wait_until_not_moving()

	def turnRight(self, speed, time= None):
		self.lmot.speed_sp = self.lmot.max_speed*speed
		self.rmot.speed_sp = -self.rmot.max_speed*speed
#		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
#		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.run_forever()
		self.rmot.run_forever()
#		self.lmot.wait_until_not_moving()
	def stop(self):
		self.lmot.stop(stop_action = 'hold')
		self.rmot.stop(stop_action = 'hold')
	def curve(self,leftSpeed,rightSpeed, time=None):
		self.lmot.speed_sp = self.lmot.max_speed*leftSpeed
		self.rmot.speed_sp = self.rmot.max_speed*rightSpeed
		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.wait_until_not_moving()
	def zeroPointer(self):
		self.mmot.position_sp = 0
		self.mmot.run_to_abs_pos(position_sp = self.mmot.position_sp)
		self.mmot.wait_until_not_moving()

	def leftPointer(self,speed = .25,time = None):

		self.mmot.speed_sp = -(speed*self.mmot.max_speed)
		self.mmot.run_timed(time_sp = time,speed_sp = self.mmot.speed_sp)
		self.mmot.wait_until_not_moving()

	def rightPointer(self,speed = .25, time = None):
		self.mmot.speed_sp = speed*self.mmot.max_speed
		self.mmot.run_timed(time_sp = time,speed_sp = self.mmot.speed_sp)
		self.mmot.wait_until_not_moving()

	def pointerTo(self,angle):
		self.mmot.position_sp = angle
		self.mmot.run_to_abs_pos(position_sp = self.mmot.position_sp)
		self.mmot.wait_until_not_moving()

	def speak(self, words):
		ev3.Sound.speak(words).wait()
	def beep(self):
		ev3.Sound.beep()

def main():

	leftM = ev3.LargeMotor('outC')
	rightM = ev3.LargeMotor('outB')
	flatMot = ev3.MediumMotor('outD')
	cs = ev3.ColorSensor('in2')
	dakota = SturdyRobot(leftM,rightM,flatMot)
	while(cs.color != cs.COLOR_BLACK):
		print("yay")
		dakota.turnRight(.1)
	dakota.stop()

main()