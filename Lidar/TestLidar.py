import serial
import numpy as np
import math
import pygame

class Lidar:
	
	# Data structures
	angle_info_dt = np.dtype([
					('intensity', '<u2'),					# reflected intensity (0 if not seen)
					('dist_m', '<u2'),						# in mm (0 if not seen)
					('reserved', '<u2')])					# unknown?
	packet_dt = np.dtype([
					('angle_index', np.uint8),				# angle index 0xA0=0degs to 0xDB=59*6degs
					('rpm', '<u2'),							# Speed in 0.1rpm units
					('angle_offset', angle_info_dt,(6))]) 	# 6 readings at 1-degree intervals
					
	def __init__(self):
		# Open the comms port
		self.port = serial.Serial('/dev/ttyS0', 230400, timeout=0.1)
		
	def start(self):
		self.port.write(b'b')
		self.port.reset_input_buffer()
		
	def stop(self):
		self.port.write(b'e')
		#self.port.close()             # close port
		
	def read40(self):
		# Ignore anything that's not 0xFA
		b = self.port.read(size=1)
		while(len(b) == 0 or b[0] != 0xFA):
			b = self.port.read(size=1)
			# To do - some form of timeout...
			
		# Read next 39 bytes + the 2 byte checksum
		b = self.port.read(size=41)
		#print(f"{b}")
		if len(b) != 41:
			print(f"wrong number of bytes read: {len(b)}")
			return None
			
		# Do checksum
		check = sum(b[:40]) + 0xFA
		#print(f"check: {check:04x}, received: {b[39]:02x}{b[40]:02x}")
		if check & 0xff != 0xff:
			print(f"Checksum error")
			return None

		# Deocde the received data structure
		out = np.frombuffer(b[:39], dtype=Lidar.packet_dt)
		#print(out)
		
		# Calculate (x,y) coordinates from the angle and distances
		base_angle = (out[0]['angle_index'] - 0xA0) * 6
		coords = []
		for a in range(6):
			angle = base_angle + a
			d = out[0]['angle_offset'][a]['dist_m']
			#print(f"angle: {angle}, dist_m: {d}mm")
			# Calculate x/y coords
			angle_rads = angle / 180.0 * math.pi
			xy = (d * math.sin(angle_rads), d * math.cos(angle_rads))
			coords.append(xy)

		#print(coords)
		return coords
			

class Plot:
	def __init__(self, lidar, win_width = 640, win_height = 480):
		pygame.init()
		self.lidar = lidar
		self.width = win_width 
		self.height = win_height

		self.screen = pygame.display.set_mode((win_width, win_height))
		pygame.display.set_caption("Lidar Display")
		
		self.lineColor = (255,255,255)
		
	def run(self):
		font = pygame.font.SysFont('Arial', 12)
		self.xy = []
		
		# Main Loop
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return 0

			# Clear current image
			self.screen.fill((64,64,64))

			# Read the next position from input to front of list
			for sect in range(60):
				six_values = lidar.read40()
				if six_values != None:
					for v in six_values:
						self.xy.insert(0, v)
						if len(self.xy) > 720:
							self.xy.pop()
			
			# Draw the positions
			pointlist = []
			for p in range(len(self.xy)):
				x,y = self.xy[p]
				if x == 0 and y == 0:
					if len(pointlist) > 1:
						pygame.draw.lines(self.screen, self.lineColor, False, pointlist, 2)
						pointlist = []
				else:
					pointlist.append((self.width/2 - x/10, y/10 + self.height/2))
			if len(pointlist) > 1:
				pygame.draw.lines(self.screen, self.lineColor, False, pointlist, 2)

			pygame.display.flip()
			pygame.time.wait(50)
			
lidar = Lidar()
plot = Plot(lidar)
lidar.start()
plot.run()
lidar.stop()
