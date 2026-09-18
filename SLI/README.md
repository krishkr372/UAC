# Sign Language Interpreter (SLI)
This is the one of the most important component of the UAC.

## Introduction & Objective 
The Sign Language Interpreter (SLI) is a computer-vision-based project for the Inspire Award Science Competition made by Krish Kumar.

 It is designed to bridge the communication gap between mute individuals and the general public. The main goal is to create a reliable, real-time system that translates hand gestures into text and then spoken words instantly, allowing them to communicate effectiveely with others.



## How it Works (Methodology)
The application is built using Python and uses webcame or any camera to capture hand gestures and then convert it to text and speech.

### Hand Tracking:
We use MediaPipe and OpenCV to track hand movements and map precise joint landmarks in real time.

### Machine Learning: 
These mapped points are processed by a trained model that instantly translates specific gestures into alphabets or full-word shortcuts to speed up typing and communication.

### Local Processing: 
The system is optimized to run completely offline/locally on the device to keep the software fast and portable.

### User Interface:
The application have simple interface which shows the translated text on the screen.

### Arduino Interface:
This program then send the text to oled screen which make the other people to see the translated word so the other people not need to see on the laptop screen.

This give option to scale this project as industry ready product which can be sold or provided by government to the required people and children in the schools at low cost. This will not demand any computer setup. With the camera integrated and the SLI device people can communicate. This simple device only cost up to 1000 to 2000 rupees if mass produced.

## Economy:
### Subsidized SLI Unit Cost (Mass Production Projections)

| Component / Item | Bulk Specifications (Government Subsidized Plan) | Estimated Wholesale Unit Cost (INR) |
| :--- | :--- | :---: |
| **Microcomputer** | Raspberry Pi Zero (Bulk) | ₹1,000 |
| **Camera Module** | Good ribbon camera | ₹400 |
| **Display** | 0.96" OLED Screen | ₹200 |
| **Storage & OS** | 16GB MicroSD Card (Preloaded with SLI Linux OS {developed after getting some fund as it need software development team}) | ₹200 |
| **Power & Circuitry & Speaker** | 5V Rechargeable battery and circuit | ₹150 |
| **Enclosure** | Mass-produced injection-molded plastic casing | ₹50 |
| **Software Architecture** | Project code is open sourced in Github under MIT open source licence(under Krish Kumar) | ₹0 (Charity to mute community from my side) |
| **Total Production Cost** | **Per-Unit Manufacturing Cost** | **₹2000** |
| **Subsidized Rate** | **Government Subsidized Pricing (e.g., 75% Subsidy for target families)** | **~500** |
<br>
<br>

## Future Scope & Improvements (UAC): 
- Adding text to Sign language Avatar model which can convert the text to avatars for the deaf people who understand the language
- Make a website/app which can be downloaded by the people and communicate to other people from far place through internet
- Making a universal platform for communication for national and international people having disabilities called UAC(universal accessible communication)
- Making operating system and devices for the community.

## Project Repository
The full source code, trained model configurations, and documentation are here:
https://github.com/krishkr372/UAC


# How to Use It?

- Clone the repository to your local machine using:

```bash git clone https://github.com/krishkr372/UAC.git```

- Navigate to the project directory:

```bash cd UAC/SLI```

- Open Arduino IDE and upload the code(in Ardiuno folder) to your Arduino board preesent in the Code for Arduino folder inside the project directory.(Optional if you want to use Arduino for additional features)   **(optional)**

- Get required libraries and extensions by running the following command in your terminal:

```bash run -r requirements.txt```

- Run the main application using:

```bash python arduinoModel.py```

- Now you can use your webcam to capture hand gestures and see the translated text on the screen. The application will also read out the text using the built-in text-to-speech engine.

- If you have connected the Arduino board, you can also see the translated text on the LCD display connected to the board and if not then only in the desktop.
