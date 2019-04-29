# D4 Detector Software
### BME 547: Medical Software Design
### Final Version is tagged as `v1.0.0`
### Jason Liu, Nate Watson, Jason Cooper


## D4 Detector Application:

[![Build Status](https://travis-ci.org/nate-watson80/BME547Final.svg?branch=master)](https://travis-ci.org/nate-watson80/BME547Final)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

* GRADING NOTE: As we discussed in class, Nate's computer did not interface well
with the computer vision package. I have been using the Hudson machine to work
on this project. For some reason, all of my commits are not coming in as from my
GitHub. So when looking under collaborators it will say that I have only made
one commit. If you look at the full list of commits you will see my commits as
"Nate Watson", however, not linked to my GitHub. Thanks.


## Documentation:

* Sphinx generated documentation:

Open the html located on the following path in repository:

    * `BME547Final/docs/_build/html/index.html`


## Contents of Project

* `final_server.py`: Flask server application. Contains all of the server modules.

* `encodedUI.py`: Contains the encoded User Interface (UI) features written in
the PyQt framework.

* `GUI-test.py`: File for deploying and controlling the flow of the
UI application.

* `launch_dialog.py`: Interface for initial application launch. Instructs user
to manually enter their name, the D4 batch number, the data group, and the
location that the sample was obtained.  

* `config.py`: Python file containing the window information.

* `requirements.txt`: Contains all of the required packages necessary for
building the project. pip is utilized as a package manager for this project.

* `LICENSE`: Licensing information for the project. MIT Open Source

* `logfile.log`: Debugging log for tasks run on the server.

* `\docs`: Sphinx generated documentation for all modules.

* `\example imgs`: Example images for testing spot finding functionalities.

* `.travis.yml`: Continuous integration file.


## Instructions to Run:

* Begin a virtual environment and install dependencies:

      `$ pip install -r requirements.txt`

* First it is necessary to deploy the server file. If the server is to run
locally, run the following command in the base directory:

    `$ python final_server.py`

* If server has been deployed to Duke University virtual machine it has the
following information associated with it:

  * Hostname: `vcm-9091.vm.duke.edu`
  * Port: `5000`
  * Operating System: `Ubuntu18 Server`
  * URL of root directory: `http://vcm-9091.vm.duke.edu:5000/`

* MongoDB has been deployed to the virtual machine and should be functional
remotely.

*  To run this application run the file: `GUI_test.py`

      `$ python GUI_test.py`


## GUI Overview and Functionality:

* GUI functionality has been distributed into three main python files:

      * `launch_dialog.py`
      * `encodedUI.py`
      * `GUI_test.py`

* `GUI_test.py` functions as the main driver and functions as the "controller"
for the user interface. `GUI_test.main()` is the module that goes through the
various windows of the program as such:

      * First, the launch window is deployed (contained in the file
        `launch_dialog.py`). Launch window prompts the user to enter their
        username, the D4 batch number, the data group, and the location that
        the sample was obtained.

      * Next, the user presses "ok" and if all fields have inputs, the window
        changed to the main functional window (contained in the files:
        `encodedUI.py` and `GUI_test.py`). This window contains five main
        buttons for image processes tasks.

              - "Open Image": Import a .tiff file into the application.

              - "Upload Image to Server": Send image to server. Server will
              respond with spots identified, their mean intensities, the
              background noise associated with the signal, and the dimensions
              of the pixel image.

              - "View entered filename from server": Command to find an image
              that has been stored on the server.

              - "Test Server!": Test to see if the server is functional.

              - "Pull Data to outputData.csv": Pull all of the data to a local
              csv file.


## Server Overview and Functionality:

* `GET /`: Initial server root to determine if the server is up and running.

* `GET /pullAllData`: This route is utilized to pull all of the data that
is currently on the database. The return payload associated with this server
request is a JSON file containing the filename, individual spot intensities,
and the background signal.

* `POST /imageUpload`: This route is used to upload image files onto the server.
The server in return will run spot finding algorithms, analyze each spot, and
calculate the background intensities of the image. This will be returned to the
client in a JSON payload containing the processed image as well as these
calculations.

* `GET /pullImage/<qFileName>`: This route is utilized in order to pull
specific images from the MongoDB database and return it back to the client
program.


## Database Overview and Functionality:

* 


## License:

MIT License

Copyright (c) 2019 Nate Watson, Jason Liu, Jason Cooper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
