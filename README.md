# Programming with Python: Beyond the Basics Live Training
_How to Write a Web Scraper in Python_

This is the code for the *Safari Live Training* - **Programming with Python: Beyond the Basics** presented by Arianne Dee

Before the class, please follow these instructions:
1. [Install Python](#1-install-python-36-or-higher)
2. [Choose an IDE](#2-choose-an-ide)
3. [Download the code](#3-download-the-course-files)
4. [Setup before class](#4-setup-before-class)
5. [At the start of class](#5-at-the-start-of-class)

## Set up instructions
### 1. Install Python 3.6 or higher
Go to https://www.python.org/downloads/

Click the yellow button at the top to download the latest version of Python.

#### On Mac or Linux
Follow the prompts and install using the default settings.

#### On Windows
The default settings don't add Python to your PATH 
so your computer doesn't know where to look for it when Python runs 
(for some inexplicable reason).

##### If you're just installing Python now
Follow the instructions here: [Windows Python installer instructions](docs/WININSTALL.md)

##### If you've already installed Python with the default settings
Follow the instructions here: [Add Python to PATH variable in Windows](docs/WINSETPATH.md)

#### Make sure that Python is properly installed
1. Open the *Command Prompt* application in Windows
or *Terminal* on Mac or Linux

1. Type `python --version` and press enter

1. Type `python3 --version` and press enter

1. Type `py --version` and press enter

1. One of those commands should print 
a Python version of 3.6 or higher 
(whichever version you just downloaded).
 If it doesn't, you have to follow instructions to
 [add Python to your PATH variable](docs/WINSETPATH.md).

**Note:** 
You can now type just the `python`, `python3`, or `py` command
in *Command Prompt* or *Terminal* 
to run the Python interpreter.
You can also run a *.py* file by running 
`python filename.py`

### 2. Choose an IDE
An IDE is the program that you write code in.
In this class, I will be using PyCharm (Community Edition).
I highly recommend it for writing Python code,
but you are free to follow along in your IDE of choice.

Download here: https://www.jetbrains.com/pycharm/download/

Install, open, and use the default settings.

### 3. Download the course files
If you're viewing this on GitHub already, stay on this page.
Otherwise, go to the GitHub repository: https://github.com/ariannedee/python-level-2

#### If you know git:
Clone the repository.

#### If you don't know git:
1. Click the "Code" (green) button at the top-right of the page
2. Click "Download ZIP"
3. Unzip it and move the **python-level-2-master** folder to a convenient location

### 4. Setup before class
Open your IDE and load the course files.
Run the file `python-level-2-master/Examples/example_1_review.py` and make sure it runs properly.

### 5. At the start of class
Download the PDF of the slides and reference material.
These should be in the **Resources** widget

## FAQs
### Can I use Python 2?

Yes, but I highly recommend using Python 3. 
If you are using Python 2, a few commands will be different and you can't use [f-strings](https://realpython.com/python-f-strings/) to format strings.
Please see the accompanying resource PDF (page 5) for a list of differences you'll see in this class.

### Can I use a different code editor besides PyCharm?

Yes, but it is only recommended if you are already know it and are comfortable navigating to different files and running commands in the command line. 
If it has syntax highlighting for Python, that is ideal.

### PyCharm can't find Python 3

On a Mac:
- Go to **PyCharm** > **Preferences**

On a PC:
- Go to **File** > **Settings**

Once in Settings:
1. Go to **Project: python-level-2** > **Project Interpreter**
1. Look for your Python version in the Project Interpreter dropdown
1. If it's not there, click **gear icon** > **Add...**
1. In the new window, select **System Interpreter** on the left, and then look for the Python version in the dropdown
1. If it's not there, click the **...** button and navigate to your Python location
   - To find where Python is located, [look in these directories](docs/PATH_LOCATIONS.md)
   - You may have to search the internet for where Python gets installed by default on your operating system

### Do you offer private Python help?
Yes, email **arianne.dee.studios at gmail.com** if you have any questions
or would like to set up some remote training.
