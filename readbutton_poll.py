#!/usr/bin/env python
 
import os
import signal
import sys
from time import sleep
import RPi.GPIO as GPIO

BUTTON_PIN=25
LED_PIN=24

def init_GPIO():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup( BUTTON_PIN, GPIO.IN)
  GPIO.setup( LED_PIN, GPIO.OUT)
 
  return

def cleanup():
  GPIO.output( LED_PIN, False ) ;
  sys.exit(1)


def exit_cleanly(signum, frame):
  # restore the original signal handler as otherwise evil things will happen
  # in raw_input when CTRL+C is pressed, 
  #our signal handler is not re-entrant
  signal.signal(signal.SIGINT, original_sigint)

  try:
    # if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
      cleanup() ;

  except KeyboardInterrupt:
    cleanup() ;

  #  this is here in case in the try block the user said they
  #  did not want to quit

  # restore the exit gracefully handler here    
  signal.signal(signal.SIGINT, exit_gracefully)

# main program entry point - runs continuously updating our datastream with the
def run_program():
  init_GPIO()

  while True:
    if( GPIO.input(BUTTON_PIN) == False ):
      print "False"
      GPIO.output( LED_PIN, False ) ;
    else:
      print "True"
      GPIO.output( LED_PIN, True ) ;
      sleep(2);
    sleep(1);

  return

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_cleanly)
    run_program() 

