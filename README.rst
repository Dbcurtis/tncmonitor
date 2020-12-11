.. This is the README file for the tncmonitor Python 3 module.
   From inside a python 3 virtual environment that has spinx installed,
   use "rst2html README.rst readme.html" to convert file to html

############
Overview
############

This module is a tool for detecting when the RMS Packet software has lost communications with the attached TNC.

The problem
___________

The problem has been that the RMS communication with the TNC would stop working after 2-3 months or thereabouts.
Once this happened, the TNC needed to be reset at which point the RMS Packet software would successfully connect.

The RMS Packet Software keeps a logs of various information on disk files in a specific directory.

This program (`tncmonitor.py`) periodically reads that directory, looks for the files that have the communication logging information,
reads backwards through the most current logging file to find records that show if the communication has
been successful, or not.

If everything is ok, the program sleeps for 10 minutes.
If a problem is detected, the program tuns off the power to the TNC for 60 seconds, restores power and checks again.
An email is sent to specific addresses when this happens.

We used the "KNACRO SRD-05VDC-SL-C 2-way 5V Relay Module Free driver USB control switch PC intelligent control" USB
board that we purchased from Amazon.  It comes with a program that will send commands to the board to open and close
relays on the board.  The relay module has a unique *moduleid* that must be included as one of the subsequently described parameters.

The software for Windows and Linux can be found at http://www.giga.co.za/ocart/index.php?route=product/product&product_id=229 .

For windows: 
  The application can be invoked from the cmd command line as CommandApp_USBRelay.exe [device id] [close / open] [relay nr]

  And if you want a GUI interface, use GuiApp_Engilish.exe

Linux instructions can be found at https://github.com/darrylb123/usbrelay . I have not tried a linux implementation of tncmonitor at this time.

To test if you have the software correctly installed on Windows 10:
  a) go to cmd in the same directory as CommandApp_USBRelay.exe and execute ``CommandApp_USBRelay.exe relayid [open|close] NN`` where ``NN`` is a 2 digit number.

  b) go to cmd in the same directory as GuiApp_English.exe and execute it.  It will open a window that is pretty obvious how to use it.
  
Usage to Monitor the TNC Error Logs
======================================
Invoke the program in accordance with::
  usage: ``tncmonitor.py [-h] [-li] [-ld] [-eo] [-ese] [-t] pramfile``

    Required argument :
      `pramfile`
          where `pramfile` is a Parameter file that is a subsequently described ``.json`` file.

    optional arguments : 
      ===== ============= =================================================
      opt    lopt          Description
      ===== ============= =================================================
      -h    --help         show this help message and exit
      -li   --loginfo      enable INFO logging
      -ld   --logdebug     enable DEBUG logging
      -eo   --emailonly    do not unpower the tnc just send email
      -ese  --emstartend   send email when program starts and when it ends
      -t    --testing      use testing data from the ./tests/testLogData dir
      ===== ============= =================================================


Parameter file
==============
The parameters are in the file ``tncprams.json`` which contains::

    {
        "account": "email account",
        "password": "email password",
        "fromemail": "from_email address",
        "toemail": ["person1@gmail.com", "person2@outlook.com", "from_email address"],
        "rmslogdir": "an absolute path to ../RMS/RMS Packet/Logs",
        "program": "CommandApp_USBRelay",
        "powerofftime": 10,
        "moduleid": "3X9XI",
        "relay": "01",
        "emsub": "TNC was reset",
        "age": 0,
        "count": 0,
        "timers": [60,600]
    }

Additional Parameters are added to the dict created by the above file by the program.
These include:

* *emailonly* -- boolean, if True does the email operations without trying to reset the relay
* *testing*  -- boolean, if True, then do not use the "rmslogdir" as the source to the rms logger data (doesn't do anything)

Where:

1. *account, password,* and *fromemail* specify the login information for the mail server.
2. *toemail* is a list of the email addresses that are to receive the email.
3. *rmslogdir* is the absolute path to the RMS logging directory (click on logs in the RMS program to get the path).
4. *program* is the name of the program in that executes the commands to open and close a relay and that was provided with the relay board. **Depending** on the above program, resettnc.py may need to be modified to invoke that program.
5. *powerofftime* is the time in seconds for which the power will be removed from the TNC.
6. *moduleid* is the ID of the relay board if needed for your board.
7. *relay* is the disignator for a specific relay on the board that controls the power to the TNC.
8. *emsub* is the subject line for the email messages.
9. *age* and *count* are for debugging.
10. *timers* is a list of seconds to wait after a power reset before reattempting the checks, and the number of seconds to wait between normal checks.


Starting the program
====================
The program can be manually executed by running ``python -m tncmonitor tncprams.json`` in the tncmonitor directory.
The tncmonitor program maintains a log at ./log/tncMonitor.  The program runs checks the RMS log file directory every 10 minutes
and responds to the communication error as previously specified.

Generally, the program should be executed out of the distribution directory when the computer is restarted, or at least at the same time RMS is started.
