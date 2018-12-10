import rospy
import signal
import numpy as np
import goToAR as goToAR
from geometry_msgs.msg import Twist

class Instructions():

    # Init method sets base link, home AR tag, and isHome
    def __init__(self):
        rospy.init_node('FASTbot', anonymous=False)
        #base and home are always static because dispatch should never 
        #need to dictate their location.
        self.base = "base_link"
        self.home = "ar_marker_0"
        self.isHome = True


    #Instruction recieved by dispatch. Takes in destination AR tag given by dispatch
    def pickUp(self, ar):
        print("I am picking up at " + ar)
        goToAR.GoForwardAvoid(self.base, ar)
        self.isHome = False        

    #Instruction recieved by dispatch. Takes in destination AR tag given by dispatch
    def dropOff(self, ar):
        print("I am dropping off at " + ar)
        goToAR.GoForwardAvoid(self.base, ar)
        self.isHome = False

    #Bot will return home on its own when no further instructions are recieved.
    #Dispatch should never be instructing the bot to go home. Home is a static var
    def goHome(self):
        print("I am going home")
        if(goToAR.GoForwardAvoid(self.base, self.home).condition):
            self.isHome = True       

    #Bot will request new when it either completes its previous instruction
    #or when it cannot find its destination
    #Dispatch may enter any number of pick ups or dropoffs in the following format:
    #[pickup/pickUp/PICKUP # dropoff/dropOff/DROPOFF #]*
    def requestNew(self):
        print("I am already home and waiting for a request")
        command = raw_input('Please enter request: \n').split()
        return command

    #Bot will request new when it either completes its previous instruction
    #or when it cannot find its destination
    #Dispatch may enter any number of pick ups or dropoffs in the following format:
    #[pickup/pickUp/PICKUP # dropoff/dropOff/DROPOFF #]*
    def requestNewAlarm(self, prompt = 'Please enter request: \n', timeout = 20):
        signal.signal(signal.SIGALRM, alarmHandler)
        signal.alarm(timeout)
        try:
            print("I am not home and waiting for a request")
            command = raw_input(prompt)
            signal.alarm(0)
            return command.split()
        except AlarmException:
            print("I timed out waiting for a command and I am going home")
            self.goHome()
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return ''


class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    raise AlarmException

# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':

  try:
    inst = Instructions()
    #while rospy is running, the bot sits at home and awaits further instruction
    while not rospy.is_shutdown():
        if(inst.isHome):
            print("I am requesting new instruction")
            cmd = inst.requestNew()
        else:
            print("I am requesting new ALARM instruction")
            cmd = inst.requestNewAlarm()

        for i in range(0, len(cmd), 2):
            print("I am parsing the command I was given")
            instruction = cmd[i]
            print(instruction)
            destination = "ar_marker_" + cmd[i + 1]
            print(destination)
            for case in switch(instruction):
                if case("pickup" or "PICKUP" or "pickUp"):
                    inst.pickUp(destination)
                    break
                if case("dropoff" or "dropOff" or "DROPOFF"):
                    inst.dropOff(destination)
                    break
                if case():
                    continue


  except rospy.ROSInterruptException:
    pass