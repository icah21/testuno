import RPi.GPIO as GPIO
import time

# === GPIO Pin Configuration ===
IR_PIN = 17       # GPIO pin for IR sensor
SERVO_PIN = 18    # GPIO pin for Servo signal

# === Setup GPIO Mode ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# === Setup PWM for Servo ===
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz (standard for servos)
pwm.start(0)

def set_servo_angle(angle):
    duty = (0.05 * angle) + 2.5  # Convert angle to duty cycle
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    print("System is running. Waiting for object detection...")
    while True:
        if GPIO.input(IR_PIN) == 0:  # 0 = Object detected
            print("Object detected!")
            set_servo_angle(0)
            time.sleep(0.5)

            set_servo_angle(90)
            print("Holding at 90° for 15 seconds...")
            time.sleep(15)

            set_servo_angle(180)
            print("Holding at 180° for 10 seconds...")
            time.sleep(10)

            set_servo_angle(0)
            print("Returning to 0° and holding for 10 seconds...")
            time.sleep(10)

        else:
            time.sleep(0.1)  # Polling delay

except KeyboardInterrupt:
    print("Cleaning up...")
    pwm.stop()
    GPIO.cleanup()
