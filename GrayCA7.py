# Casey Gray
# Assignment 7
# ITEC 4270 Section 01
# Due 7/15

# Note: All other Python files were provided by the Freenove Car Kit. All code in this file is my own. I played around with
# different features over the weekend and came up with this routine

import time
import sys
import os
from datetime import datetime

# Import classes
from rover_modules.motor import Ordinary_Car
from rover_modules.ultrasonic import Ultrasonic
from rover_modules.led import Led
from rover_modules.buzzer import Buzzer
from rover_modules.infrared import Infrared
from rover_modules.camera import Camera

# Main class that manages the rover's actions
class Rover:
    # Constructor method
    def __init__(self):
        
        # Print a message that shows that the rover is starting
        print("Initializing Rover")
        
        # Create an instance of the ordinary car class for motor control
        self.car = Ordinary_Car()
        
        # Create an instance of the ultrasonic sensor setting its max distance
        self.ultrasonic = Ultrasonic(max_distance=60.0)
        
        # Create an instance of the led class for LED control
        self.led = Led()
        
        # Create an instance of the buzzer class
        self.buzzer = Buzzer()
        
        # Create an instance of the infrared class for line sensors
        self.infrared = Infrared()
        
        # Create an instance of the camera class that flips horizontally/vertically as needed
        self.cam = Camera(hflip=True, vflip=True)
        
        # Set distance (in centimeters) at which an obstacle is detected
        self.obstacle_distance = 30
        
        # Set a distance threshold (in centimeters) to determine if the rover is clear to move forward after turning
        self.clear_path = 50
        
        # Define motor speed for moving forward
        self.forward_speed = 1000
        
        # Define motor speed for turning
        self.turn_speed = 1000
        
        # Set expected infrared sensor value when the rover is on the cardboard box
        # Gotten by setting rover on box and reading sensor value
        self.box_ir_value = 7
        
        # Initialize variable for storing video file
        self.video_filename = None
        
        # Print message stating that the rover is finished initializing
        print("Rover Initialized.")
        
    # Method to make the rover move forward
    def move_forward(self):
        
        # Print message stating rover is moving forward
        print("Moving forward...")
        
        # Stop any LEDs from blinking
        self.led.colorBlink(state=0)
        
        # Activate rainbow effect on LEDs to signify the rover is moving
        self.led.rainbowCycle(20)
        
        # Set all four motors to move forward at the defined speed
        self.car.set_motor_model(self.forward_speed, self.forward_speed,self.forward_speed,self.forward_speed)
        
    # Method to stop the rover
    def stop_rover(self):
        
        # Print message stating the rover is stopping
        print("Stopping rover.")
        
        # Set all motor duties to 0 to stop them
        self.car.set_motor_model(0, 0, 0, 0)
        
        # Make LEDs blink to indicate a stop
        self.led.colorBlink(state=1)
        
        # Sound buzzer for a short beep
        self.buzzer.set_state(True)
        time.sleep(0.2)
        self.buzzer.set_state(False)
        
        # Stop LED blinking
        self.led.colorBlink(state=0)
        
    # Method to make the rover turn right until able to move forward, with a max duration as a backup
    def turn_right(self, max_duration = 2.0):
        
        # Print message stating the rover is turning right
        print(f"Turning right until clear path ahead (max {max_duration})")
        
        # Set motors to turn right (left motors forward, right motors backward)
        self.car.set_motor_model(self.turn_speed, self.turn_speed, -self.turn_speed, -self.turn_speed)
        
        # Record the start time of the turn
        turn_start = time.time()
        
        # Loop continues as long as maximum turn duration isn't reached
        while time.time() - turn_start < max_duration:
            
            # Get current distance from the ultrasonic sensor
            distance = self.ultrasonic.get_distance()
            
            # If valid reading is obtained
            if distance is not None:
                
                # If a clear path is found
                if distance > self.clear_path:
                    
                    # Print message stating that a clear path has been found
                    print(f"Clear path detected ({distance:.1f} cm). Stopping turn.")
                    
                    # Exit loop
                    break
                
            # Pause to prevent fast sensor reading
            time.sleep(0.05)
            
        # Stop the rover after the turn
        self.stop_rover()
        
        # Pause after stopping the turn
        time.sleep(0.2)
        
    # Method to make the rover turn left until able to move forward, with a max duration as a backup
    def turn_left(self, max_duration = 2.0):
        
        # Print message stating the rover is turning left
        print(f"Turning left until clear path ahead (max {max_duration})")
        
        # Set motors to turn left (left motors backward, right motors forward)
        self.car.set_motor_model(-self.turn_speed, -self.turn_speed, self.turn_speed, self.turn_speed)
        
        # Record the start time of the turn
        turn_start = time.time()
        
        # Loop continues as long as maximum turn duration isn't reached
        while time.time() - turn_start < max_duration:
            
            # Get current distance from the ultrasonic sensor
            distance = self.ultrasonic.get_distance()
            
            # If valid reading is obtained
            if distance is not None:
                
                # If a clear path is found
                if distance > self.clear_path:
                    
                    # Print message stating that a clear path has been found
                    print(f"Clear path detected ({distance:.1f} cm). Stopping turn.")
                    
                    # Exit loop
                    break
                
            # Pause to prevent fast sensor reading
            time.sleep(0.05)
            
        # Stop the rover after the turn
        self.stop_rover()
        
        # Pause after stopping the turn
        time.sleep(0.2)
        
    # Method to avoid obstacle
    def avoid_obstacle(self):
        
        # Print message stating an obstacle was detected
        print("Obstacle detected! Beginning avoidance maneuver...")
        
        # Stop the rover when an obstacle is detected
        self.stop_rover()
        
        # Turn the buzzer on as an alert
        self.buzzer.set_state(True)
        time.sleep(0.5)
        self.buzzer.set_state(False)
        
        # Make LEDs blink
        self.led.colorBlink(state=1)
        
        # Avoidance sequence
        # Step 1: Turn right until path is clear
        self.turn_right()
        
        # Step 2: Move forward for a set duration
        self.move_forward()
        time.sleep(1.5)
        self.stop_rover()
        
        # Step 3: Turn left until a clear path is detected
        self.turn_left()
        
        # Step 4: Move forward to ensure obstacle is avoided
        self.move_forward()
        time.sleep(0.5)
        self.stop_rover()
        
        # Print message stating the obstacle has been avoided
        print("Obstacle has been avoided.")
        
        # Stop LEDs blinking
        self.led.colorBlink(state=0)
        
    # Main method for rover
    def rover_run(self):
        
        # Print message stating that the run is beginning
        print("Beginning Rover Run")
        
        # Try block to handle any potential errors
        try:
            
            # Generate video filename using current date/time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.video_filename = f"rover_run_{timestamp}.mp4"
            
            # Print message stating that a video is being recorded
            print(f"Starting video recording to {self.video_filename}...")
            
            # Start recording video
            self.cam.start_stream(filename=self.video_filename)
            
            # Pause to allow camera to initialize
            time.sleep(1)
            
            # Start the rover by moving forward
            self.move_forward()
            
            # Initialize a flaf to track if the obstacle has been avoided yet
            obstacle_avoided = False
            
            # Loop that continues until a stop condition is met
            while True:
                
                # Get the current distance reading from the ultrasonic sensor
                distance = self.ultrasonic.get_distance()
                
                # Check if reading is valid
                if distance is not None:
                    
                    # If an obstacle is detected AND it hasn't been avoided yet
                    if distance < self.obstacle_distance and not obstacle_avoided:
                        
                        # Execute obstacle avoidance
                        self.avoid_obstacle()
                        
                        # Set the flag to true
                        obstacle_avoided = True
                        
                        # Resume moving forward after avoiding the obstacle
                        self.move_forward()
                        
                        # Print message
                        print("Resuming movement towards goal.")
                        
                # Read value from ir sensors
                current_ir_value = self.infrared.read_all_infrared()
                
                # If the current value matches the value of the cardboard box
                if current_ir_value == self.box_ir_value:
                    
                    # Print status
                    print("Cardboard box reached! Stopping.")
                    
                    # Stop the rover
                    self.stop_rover()
                    
                    # Set all LEDs to green
                    self.led.ledIndex(0xFF, 0, 255, 0)
                    
                    # Turn the buzzer on
                    self.buzzer.set_state(True)
                    time.sleep(1)
                    self.buzzer.set_state(False)
                    
                    # Exit the loop
                    break
                
                # Pause to allow good sensor readings
                time.sleep(0.1)
                
        # Catch keyboard interrupt exception
        except KeyboardInterrupt:
            print("\nRoutine interrupted by user.")
            
        # Catch any other unexpected exceptions
        except Exception as e:
            print(f"An error has occurred: {e}")
            
        # Clean up rover resources
        print("Cleaning up rover resources...")
        
        # Make sure motors are stopped
        self.stop_rover()
        
        # Make sure camera has stopped recording
        if self.cam.streaming:
            print(f"Stopped recording of {self.video_filename}...")
            self.cam.stop_stream()
            
        # Release resources used by rover
        self.car.close()
        self.ultrasonic.close()
        self.infrared.close()
        self.cam.close()
        self.led.ledIndex(0xFF, 0, 0, 0)
        self.buzzer.close()
        
        print("Rover resources cleaned.")
        
if __name__ == '__main__':
    
    # Create an instance of the rover class
    controller = Rover()
    
    # Call the rover run method
    controller.rover_run()