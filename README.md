# D4 Detector Software
### BME 547: Medical Software Design
### Final Version is tagged as `v1.0.0`
### Jason Liu, Nate Watson, Jason Cooper


## D4 Detector Application:

[![Build Status](https://travis-ci.org/nate-watson80/BME547Final.svg?branch=master)](https://travis-ci.org/nate-watson80/BME547Final)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


## Documentation:

[D4 Detector Software Documentation]
(file:///Users/nww5/repos/BME547Final/docs_build/html/index.html)

<file:///Users/nww5/repos/BME547Final/docs_build/html/index.html>

## Contents of Project

* `final_server.py`: Flask server application. Contains all of the server modules.

* `encodedUI.py`: Contains the encoded User Interface (UI) features written in
the pyqt framework.

* `GUI-test.py`: File for deploying the UI application.

* `launch_dialog.py`: Interface for initial application launch.

* `freshRequirements.txt`: Contains all of the required packages necessary for
building the project.

* `LICENSE`: Licensing information for the project.

* `logfile.log`: Debugging log for tasks run on the server.

* `\docs`: Sphinx generated documentation for all modules.

* `\example imgs`: Example images for testing spot finding functionalities.

## Instructions to Run:

* First it is necessary to deploy the server file. If the server is to run
locally, run the following command in the base directory:
    `$ FLASK_APP=final_server.py flask run`

* If server has been deployed to Duke University virtual machine it has the following
information associated with it:

  * Hostname: `vcm-9091.vm.duke.edu`
  * Port: `5000`
  * Operating System: `Ubuntu18 Server`
  * URL of root directory: `http://vcm-9091.vm.duke.edu:5000/`

* You'll need to download mongo db community edition to run the server locally, but otherwise this should work

* Begin a virtual environment and install dependencies:
      `$ pip install -r freshRequirements.txt`

## Server Functionality:

* `GET /`: Initial server root to determine if the server is up and running.

* `GET /pullAllData`: This route is utilized to pull all of the image data that
is currently on the database.


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
