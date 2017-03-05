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
  GPIO.cleanup()
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

  return

def flash_LED( channel=BUTTON_PIN ):
  print "Blinking!"
  for x in range(0,4):
    GPIO.output( LED_PIN, True ) 
    sleep(.25);
    GPIO.output( LED_PIN, False ) 
    sleep(.25);
  print "Done Blinking!\n"
  return
  
# main program entry point - runs continuously updating our datastream with the
def run_program():
  init_GPIO()

  # tell the GPIO library to look out for an 
  # event on pin 23 and deal with it by calling 
  # the buttonEventHandler function
  GPIO.remove_event_detect( BUTTON_PIN )

  # Add for interrupt-driven
  #GPIO.add_event_detect(BUTTON_PIN,GPIO.RISING)
  #GPIO.add_event_callback(BUTTON_PIN, flash_LED, 800)

  while True:  
    # Add for Wait approach
    print "Waiting for Button press"
    GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING) ;
    flash_LED()

    # Add for interrupt-driven
    #print "Sleep"
    #sleep(10)

  return

if __name__ == '__main__':
  # store the original SIGINT handler
  original_sigint = signal.getsignal(signal.SIGINT)
  signal.signal(signal.SIGINT, exit_cleanly)

  run_program() 

