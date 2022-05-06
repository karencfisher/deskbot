# deskbot version 1

Project developing an interactive robot. "Deskbot" for now as it would be on your desk, tracking your movement and able to interact with 
you. It could also be adapted for a variety of use cases.

Currently, it performs:
* Face detection (Viola-Jones method AKA HAAR Cascade)
* Face tracking. It adjust keeping you in the center of the visual field, allowing it to be responsive.
* Speech recognition (using Google speech recognition).
* Speech synthesis.
* Some chatbot ability (at present an implementation of Eliza)

### Basic Bot (basic_bot.py)

This is a very basic implementation. It will keep you in its gaze, and will repeat anything you say. It
will also play a kind of "I see you game" -- if you cover your face, for example, it will ask where you
are. When it sees you it says "I see you!"

[![Demonstration](https://img.youtube.com/vi/Y8LBQDt7BbPYE/0.jpg/)](https://www.youtube.com/watch?v=8LBQDt7BbPY "Demonstration")

### Eliza Bot (eliza_bot.py)

This implementation integrates a Python implementation of the classic chabot "Eliza," based on the
original chatbot published by Joseph Weizenbaum in 1966. It is supposed to interact with the user as a Rogerian therapist. The Python version is Copyright (c) 2019 Wade Brainerd under MIT license. 

[![Eliza Repository](https://github.com/wadetb/eliza)](https://github.com/wadetb/eliza/commit/cecbb5b06ca256ee67bf49d251537ad2cbd06eff)

## Hardware Configuration

Raspberry PI 4 2b
Raspberry PI camera
Sunfounder PCA9685 servo controller
SG90 Micro Servos
Adafruit Mini Tilt/Pan stand
USB microphone

