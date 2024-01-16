from data import letters
import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 56       # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
SCROLL_SPEED = 5      # How many columns per second the message moves.
STRIP_LENGTH = 8      # Number of LEDS per line

def dotGridConversion(string):
    "Converts a string to a 7 row grid format."
    grid = [" " * STRIP_LENGTH for i in range(7)]
    for char in string:
            translation = letters[char]
            for i in range(7):
                grid[i] += translation[i] + "  "
    return grid


def getCurrentDisplay(completeMessage, start):
    "Retrieves a slice of the message that fits the display"
    output = ["" for i in range(7)]
    for i in range(7):
        output[i] = completeMessage[i][start: start + LED_COUNT//7]
        output[i] += ' ' * (STRIP_LENGTH - len(output[i])) #fills remaining space with blanks when reaching the end of the message
    return output


def updateDisplay(ledStrip, message):
    "Sets LEDS to display specified grid."
    flattenedMessage = ""
    lineN = 0
    for line in message:
        if not (lineN % 2):
            reversedLine = ''.join(line[i] for i in range(len(line) -1, -1, -1))
            flattenedMessage += reversedLine #reverses odd numbered lines
        else:
            flattenedMessage += line
        lineN += 1
        
    for i in range(len(flattenedMessage)):
        if flattenedMessage[i] == ' ':
            ledStrip.setPixelColor(i, Color(0,0,0,0))
        elif flattenedMessage[i] == '.':
            ledStrip.setPixelColor(i, Color(255, 255, 255, 1))
        else:
            print(flattenedMessage)
            raise "Incorrect character encoding. Check data.py"
        
    print(flattenedMessage, len(flattenedMessage))

    strip.show()


def wipeDisplay(ledStrip):
    "Clears the LED strip."
    for i in range(LED_COUNT):
        ledStrip.setPixelColor(i, Color(0, 0, 0, 0))
    ledStrip.show();
        

if __name__ == "__main__":
    message = "HELLO WORLD"
    grid = dotGridConversion(message)
    startIndex = 0
    currentGrid = getCurrentDisplay(grid, startIndex)

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    while True:
        sleep = 1.0/SCROLL_SPEED
        time.sleep(sleep)
        
        updateDisplay(strip, currentGrid)
        
        startIndex += 1
        currentGrid = getCurrentDisplay(grid, startIndex)

        if startIndex >= len(grid[0]):
            startIndex = 0
            
        for line in currentGrid:
            print(line)
        print()