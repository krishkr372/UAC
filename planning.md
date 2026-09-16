##### To make this project completely manageable, we are going to break this down into a long-term plan.





# **🗺️ UAC Project Master Roadmap**





###### Phase 1: Local AI Engine (The Core)



Task 1.1: Build a Python script to collect and save 3D hand landmarks using MediaPipe.

Task 1.2: Train a Random Forest model on 100% of your data and save it as a .pkl file.

Task 1.3: (Optional future step) Gather data for Indian Sign Language (ISL) letters using the exact same script from Task 1.1, so your model can support both ASL and ISL later.



###### Phase 2: Web Server Skeleton - Setting up your local web framework so your computer can run the website locally.



Task 2.1: Create your clean UAC folder structure (core\_assets/, uac\_web/, etc.).

Task 2.2: Install web libraries (flask, flask-socketio, eventlet).

Task 2.3: Write the basic uac\_web/app.py server script to route pages.

Task 2.4: Build the basic index.html (Homepage) and meeting.html (Room Page) layouts. Launch it and verify you can open http://127.0.0.1:5000 in your browser.



###### Phase 3: Model Conversion (Bridging Python to the Web)Translating your working Python model into something a web browser can read directly.



Task 3.1: Create a Python script to convert your asl\_model.pkl file into an asl\_model.onnx file.

Task 3.2: Export your asl\_scaler.pkl parameters (mean and scale arrays) into a simple scaler\_params.json file.

Task 3.3: Move both the .onnx and .json files into your website's static asset folder.



###### Phase 4: Frontend "Edge" Sign Interpreter (For Mute Users)Running the computer vision tracking completely inside the user's web browser.



Task 4.1: Include the MediaPipe JavaScript library and ONNX Runtime Web library via script tags in meeting.html.

Task 4.2: Write JavaScript code to open the webcam and display the live tracking landmarks on the screen.

Task 4.3: Write a JavaScript function that uses the values from scaler\_params.json to scale the coordinates.

Task 4.4: Write the JavaScript code to pass those scaled numbers into your asl\_model.onnx file to get the live predicted text character.



###### Phase 5: Voice Systems (For Blind \& Standard Users)Building the two-way audio communication module.



Task 5.1: Set up the Web-based Text-to-Speech engine. (Good news: Web browsers have a built-in voice tool called the JavaScript SpeechSynthesis API, so you don't even need pyttsx3 on the website!).

Task 5.2: Build the Web-based Speech-to-Text listener using the browser's built-in JavaScript Web Speech API so it listens to a user's microphone and converts it to text text boxes natively.



###### Phase 6: WebSockets Linking \& Chat Core (The Google Meet Bridge)Gluing it all together so users can actually send their text to each other.



Task 6.1: Use Flask-SocketIO to write a "Message Broker". When a Mute user's browser predicts a letter, send that text over the socket connection.

Task 6.2: Set up the receiver logic. If a user is marked as Deaf, display that incoming socket text as captions. If they are marked as Blind, trigger the browser's audio engine to speak it out loud.



###### Phase 7: The Visual Avatar (For Deaf Users)Adding the sign language output module.



Task 7.1: Create a folder containing short animation clips or GIFs named after words/letters (e.g., a.gif, hello.gif).

Task 7.2: Write a JavaScript listener on the meeting page that watches incoming text. If a text message comes in, look up the word in your dictionary and play the matching video/GIF right next to the video frame.

