# Development Environment Setup

## 1. Prerequisites

To run the DRB Rounder software, you must be on a Windows system (32-bit or 64-bit).

You will also need git to clone this repository.

### Clone the drb_rounder repository

Please clone this repository using your preferred git client or by using the command line:

`git clone https://github.com/simsong/drb_rounder.git`

***Developers on the drb_rounder program are to use Unix-style line endings exclusively.***

### Anaconda & 'drb_rounder' environment

First, you must install [Anaconda 3](https://www.anaconda.com/distribution/). After installing, create a new Anaconda environment called `drb_rounder` that will be your development environment. You will also need to install the followings packages:

- [Pyinstaller](https://anaconda.org/anaconda/pyinstaller)
- [Pytest] (https://anaconda.org/anaconda/pytest)
- [OpenPyXl] (https://anaconda.org/anaconda/openpyxl)
- [Xlrd] (https://anaconda.org/anaconda/xlrd)

After installing Anaconda, you should now have a program called `Anaconda Powershell Prompt` in the Application folder located in the Windows Start Menu. Open that now.

## 2. Creating the executable

Change directories to wherever you cloned the repository locally:

`cd /path/to/repo`

For more instructions on creating the drb_rounder executable, look [here](creating_installer.md)

## 3. Running the drb_rounder executable
