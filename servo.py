import serial

class Servo(object):

  def __init__(self, path_to_serial):
    self.LR, self.UD = 90, 60
    self.con = serial.Serial(path_to_serial,9600,timeout=10)

  def turn(self):
    self.con.write( "U%03dU%03dL%03dL%03d" % (self.UD,self.UD,self.LR,self.LR) )

  def turn_left(self,resolution=10):
    self.LR = self.LR-resolution if self.LR-resolution>0 else 0
    self.turn()

  def turn_right(self,resolution=10):
    self.LR = self.LR+resolution if self.LR+resolution<180 else 180
    self.turn()

  def turn_up(self,resolution=10):
    self.UD = self.UD-resolution if self.UD-resolution>0 else 0
    self.turn()

  def turn_down(self,resolution=10):
    self.UD = self.UD+resolution if self.UD+resolution<180 else 180
    self.turn()

  def turn_front(self):
    self.UD, self.LR = 90,60
    self.turn();
