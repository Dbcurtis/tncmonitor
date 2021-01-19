.. This is the README file for the tncmonitor Python 3 module.
  From inside a python 3 virtual environment that has spinx installed,
  use "makehtml.py" to convert file to html
  decided I didn't know how to rebase on 20210119 so it was not done

####################
TNCMONITOR Overview
####################

This module is a tool for detecting when the RMS Packet 
software has lost communications with the attached TNC.

The problem
___________

The problem has been that the RMS communication with the 
TNC would stop working after 2-3 months or thereabouts.
Once this happened, the TNC needed to be reset at which 
point the RMS Packet software would successfully connect.

The RMS Packet Software keeps a logs of various information
on disk files in a specific directory.

This program (``tncmonitor.py``) periodically reads that directory, 
looks for the files that have the communication logging information,
reads backwards through the most current logging file 
to find records that show if the communication has
been successful, or not.

If everything is ok, the program sleeps for 10 minutes.
If a problem is detected, the program tuns off the power 
to the TNC for 60 seconds, restores power and checks again.
An email is sent to specific addresses when this happens.

We used the "KNACRO SRD-05VDC-SL-C 2-way 5V Relay Module 
Free driver USB control switch PC intelligent control" USB
board that we purchased from Amazon.  It comes with a program 
that will send commands to the board to open and close
relays on the board.  
The relay module has a unique *moduleid* that must be 
included as one of the subsequently described parameters.

The software for Windows and Linux 
can be found 
at http://www.giga.co.za/ocart/index.php?route=product/product&product_id=229 .

For windows:
  The application can be invoked from the cmd command line 
  as CommandApp_USBRelay.exe [moduleid] [close | open] [relay-id]

  And if you want an English GUI interface, use GuiApp_Engilish.exe

Linux instructions can be found 
at https://github.com/darrylb123/usbrelay . 
I have not yet tried a linux implementation of tncmonitor.

To test if you have the software correctly installed on Windows 10:

a) go to cmd in the same directory as CommandApp_USBRelay.exe and
   execute ``CommandApp_USBRelay.exe relayid [open|close] NN`` 
   where ``NN`` is a 2 digit number.

b) go to cmd in the same directory as GuiApp_English.exe 
   and execute it.  
   It will open a window that is pretty obvious how to use it.

Python version
---------------
I have tested this on windows 10 using python version 3.8.0 
using a virtual environment.
I do not expect it to work using Python 2 or Python 3 
prior to 3.7. It "could" work on 3.7, but I have not tried it.

Use a virtual Python envrionment that has installed the modules listed in
``requirements.txt``.  Run the program from a ``cmd`` shell after every reboot 
of the computer.  It should start executing after RMS has started.

Usage to Monitor the TNC Error Logs
======================================

Invoke the program in accordance with:
  usage: ``tncmonitor.py [-h] [-li] [-ld] [-eo] [-ese] [-t] pramfile``

  Required argument:
    ``pramfile``
          where ``pramfile`` is a Parameter file that is a 
          subsequently described ``.yaml`` file.

  Optional arguments: 
    ===== ============= ==================================================
    opt    lopt          Description
    ===== ============= ==================================================
    -h    --help        show this help message and exit
    -li   --loginfo     enable INFO logging
    -ld   --logdebug    enable DEBUG logging
    -eo   --emailonly   do not unpower the tnc just send email
    -ese  --emstartend  send email when program starts and when it ends
    -t    --testing     use testing data from the ./tests/testLogData dir
    ===== ============= ==================================================


Parameter file
==============
The parameters are described in the 
file ``prototypetncprams.yaml``.  This file should be 
copied into ``./tests/tncprams.yaml`` and the values provided.

In addition, the tncprams.yaml should be copied to the tests directory 
with any changes that may be needed for testing.

Additional Parameters are added to the dict created by 
the above file by the program.
These include:

* *emailonly* -- boolean, if True does the email operations 
  without trying to reset the relay
* *testing*  -- boolean, if True, then do not use 
  the "rmslogdir" as the source to the rms logger data 
  (doesn't do anything)

In addition, if a value or key in the ``yaml`` file
includes ``--comment--``, that key and 
value will removed when the file is processed.
Not removed from the file, but no corrsponding dict 
value will be passed to the program.

Starting the program
====================
After the python virtual envionment is configured and activated
(search for python virtual envionment for Windows 10) 
the program can be manually executed in ``cmd`` by 
running ``python -m tncmonitor tncprams.yaml`` in the tncmonitor 
directory.
The tncmonitor program maintains a 
log at ``./log/tncMonitor``.  The tncmonitor program
checks the RMS log file directory every 10 minutes
and responds to the communication error as previously specified.

Generally, the program should be executed out of the 
distribution directory when the computer is restarted, 
or at least at or after the same time RMS is started.

First Time Configuration
========================
1. activate the python virtual environment.

#. run tncmonitor with a command line. 
   For windows: ``python -m tncmonitor -h``. 
   For linux: ``python3 -m tncmonitor -h``.
   Both executed in the tncmonitor directory.
   This verifies that the help switch works 
   as it and the starting message should be the only output.

#. edit test_resettnc.py at approx. line 75 and enter your values for the relay
   module id and relay number in the ``argdic`` Dict 
   for ``test_01instant``.
   This is needed because the test program does not use the .yaml 
   configuration file.

#. run the test, you should hear the relay clicking.  
   I ran the test from visual studio code, 
   using launch.json of:

   .. code-block::

    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "args": [ ],
      "justMyCode": true,
      "console": "integratedTerminal"
    }

#. create a ``./tests/testtncprams.yaml`` file based off 
   of ``prototypetncprams.yaml`` 
   and in the same directory with the currect ``SMTPServer`` 
   information including the 
   account and password as well as  valid email addresses 
   in the ``fromemail`` 
   and ``toemail`` fields.  In addition, 
   ``rmslogdir`` needs to point to a directory with captured log data 
   for testing (For
   example, data files in the tncmonitor/test/testLogData distribution 
   dirctory).

#. create a ``tncprams.yaml`` based off of ``testtncprams.yaml`` 
   with real email addresses and ``rmslogdir`` being an absolute 
   path to the actual RMS log directory.

Testing Sequence
========================
Testing process from the start:
(I have not verified that you have enough information here to 
do the tests)

#. verify that test_loadprams.py passes.  
   If it does not, nothing will work.

#. verify that test_resettnc.py passes.  
   You should hear the relay click.

#. verify that test_myemail passes.  
   Check that you actually receive some test messages.

#. verify that test_findlogfile.py passes. 

#. verify that test_check4noinit.py passes.


How do I make the requirements.txt file?
=========================================

See: 
https://blog.jcharistech.com/2020/11/02/how-to-create-requirements-txt-file-in-python/

Read about ``Pipreqs``.


How do I make the html for this file?
=====================================
run ``makehtml.py`` in the same directory wherein this file is located.

It will generate the .html file in the same directory.
