# Trek

A simple tool that graphs your daily steps using information from HealthBox

![Trek Logo](https://v0lttech.com/assets/img/treklogo.png)
![Works with HealthBox](https://v0lttech.com/assets/img/workswithhealthbox.png)


## Usage

Trek is designed to work with HealthBox, and requires it to function. If you don't already have HealthBox, make sure to download and set it up before setting up Trek. It should also be noted that the following instructions assume you are on GNU/Linux. However, the same directions can be loosly followed for MacOS as well.

1. Download Trek, either from the V0LT website, or by cloning the git repository using this command: `git clone https://github.com/connervieira/Trek`
2. Install Trek's python dependencies using the following commands.
    `pip3 install requests`
    `pip3 install matplotlib`
3. Change into the newly downloaded Trek directory using the following command: `cd Trek`
4. Open the 'main.py' file with a text editor of your choice. For example, you may use the following command to open the file in a graphical text editor: `gedit main.py`
5. After opening the file, look for the section labled *Configuration*. This section stores the values you should change before running HealthBox.
6. Change the `default_apikey` variable to an API key generated in HealthBox for Trek. This API key should be an *app* key, and have permission to access metric A1 (Steps).
7. Change the `default_server` variable to the server host address and port number for your HealthBox instance. If you're running HealthBox locally, on the default port, this will likely be `localhost:5050`. However, if you're running HealthBox remotely, you may enter something more like `192.168.0.28:5050`.
8. Save and close the file.
9. Run `main.py` using Python 3, by running the following command: `python3 main.py`

You can now view information about how many steps you took on a particular date using Trek! Every time you'd like to re-run Trek, simply navigate to the Trekfolder and run `main.py`. After the initial set up, you shouldn't need to edit `main.py` again, unless you'd like to make changes to your configuration.


## Features


### Quick

Trek is a command line program, making it easy to quickly enter the start and end dates of the span of time you'd like to graph.


### Easy

Trek uses a simply terminal user interface that doesn't require you have an extensive knowledge of the command line. Using the instructions above, even inexperienced command line users should be able to work out how to use Trek.


### Completely Open Source

Just like HealthBox itself, Trek is completely open source from top to bottom, ensuring your privacy and security.


### Well Documented

The source code of Trek is clearly laid out and well documented, making it easy to modify for other uses.


### Cross Platform

Trek uses cross platform Python modules that can be installed on several different operating systems, allowing you to generate charts on any device you choose.


### Works With HealthBox

Trek works with HealthBox, the easy way to keep all of your health information in one secure, easy to access location!
