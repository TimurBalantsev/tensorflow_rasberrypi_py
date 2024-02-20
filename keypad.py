from gpiozero import LED, Button,DigitalOutputDevice
import time

L1 = DigitalOutputDevice(21)
L2 = DigitalOutputDevice(20)
L3 = DigitalOutputDevice(25)
L4 = DigitalOutputDevice(24)  # this pin might be disconnected

C1 = Button(26, pull_up=False)
C2 = Button(19, pull_up=False)
C3 = Button(13, pull_up=False)
C4 = Button(6, pull_up=False)

current_chain=""

# The readLine function
def readLine(line, characters):
    global current_chain
    prev_chain = current_chain
    line.on()
    if C1.is_pressed:
        current_chain += characters[0]
    if C2.is_pressed:
        current_chain += characters[1]
    if C3.is_pressed:
        current_chain += characters[2]
    if C4.is_pressed:
        current_chain += characters[3]
    
    line.off()

    if not prev_chain == current_chain:
        print(current_chain)

def checkLines():
    readLine(L1, ["1", "2", "3", "A"])
    readLine(L2, ["4", "5", "6", "B"])
    readLine(L3, ["7", "8", "9", "C"])
    readLine(L4, ["*", "0", "#", "D"])

def mainLoop():
    try:
        while True:
            # Call the readLine function for each row of the keypad
            readLine(L1, ["1", "2", "3", "A"])
            readLine(L2, ["4", "5", "6", "B"])
            readLine(L3, ["7", "8", "9", "C"])
            readLine(L4, ["*", "0", "#", "D"])
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nApplication stopped!")

if __name__ == "__main__":
    mainLoop()