========
pybk8500
========

Python library for the BK Precision 8500 SERIES DC ELECTRONIC LOADS

Models 8500, 8502, 8510, 8512, 8514, 8518, 8520,
8522, 8524 & 8526

Protocol found at https://bkpmedia.s3.amazonaws.com/downloads/manuals/en-us/85xx_manual.pdf
in the "Command details" section.


Command Line Interface
======================

I added some command line interface utilities that use python's "-m" module switch.


Install
-------

.. code-block:: bash

    pip install pybk8500[all]


Requirements
------------

  * pyserial>=3.4
  * continuous-threading>=2.0.0


Send Command
------------

Send a command to a serial port and wait for a response.

.. code-block:: bash

    python -m pybk8500.send_cmd "COM1" 9600 "RemoteOn" --address 1
    # will send the command down a serial port and wait for a response

The command ID can be the string NAME or integer ID.

.. code-block:: bash

    # cmd_id as str
    python -m pybk8500.send_cmd "COM1" 9600 "SetRemote" --value 1 --address 1

    # cmd_id as hex
    python -m pybk8500.send_cmd "COM1" 9600 0x20 --value 1 --address 1

    # cmd_id as decimal
    python -m pybk8500.send_cmd "COM1" 9600 32 --value 1 --address 1


Parser
======

The parser is used to parse incoming messages. It can be used with to parse single messages,
parse messages with an iterator, or parse using a callback function.


Parse Iterator Example
----------------------

Use a for loop to iterate through parsed messages.

.. code-block:: python

    import pybk8500

    with open('saved_messages.txt', 'rb') as f:
        p = pybk8500.Parser()

        for msg in p.parse_iter(f.read()):
            print(msg.NAME)
            for field, value in msg.fields().items():
                print('\t{} = {}'.format(field, value))


Parse Callback Example
----------------------

Use a callback function to handle parsed messages. This is useful for GUI's with a serial port.

.. code-block:: python

    import sys
    import pybk8500

    def print_error(error):
        print('{}: {}'.format(type(error).__name__, str(error)), file=sys.stderr)

    def print_msg(msg):
        print(msg.NAME)
        for field, value in msg.fields().items():
            print('\t{} = {}'.format(field, value))

    p = pybk8500.Parser()
    p.error = print_error

    with open('saved_messages.txt', 'rb') as f:
        p.parse(f.read(), print_msg)


Parse Single Message Example
----------------------------

Parse a single message at a time.

.. code-block:: python


    import sys
    import pybk8500

    def print_error(error):
        print('{}: {}'.format(type(error).__name__, str(error)), file=sys.stderr)


    with open('saved_messages.txt', 'rb') as f:
        p = pybk8500.Parser()

        byts = f.read()
        while True:
            msg, error, byts = self.parse_msg(byts)
            if msg is not None:
                print(msg.NAME)
                for field, value in msg.fields().items():
                    print('\t{} = {}'.format(field, value))
            elif error is not None:
                print_error(error)
            else:
                break


Commands
========

Generate commands and send them down a serial port


Requirements
------------

  * pyserial

`pip install pyserial`


Use Commands
------------

Create and use command easily.

Commands can be found at https://bkpmedia.s3.amazonaws.com/downloads/manuals/en-us/85xx_manual.pdf
in the "Command details" section.


.. code-block:: python

    import pybk8500
    import serial

    ser = serial.Serial('COM1', 9600)

    cmd = pybk8500.SetRemoteOperation(address=1, operation='Remote')
    ser.write(bytes(cmd))

    # Most commands have a value alias
    cmd = pybk8500.SetRemoteOperation(address=1, value='Remote')
    ser.write(bytes(cmd))


Commands are bytearrays which can be used as bytes. When you change a value a flag is set to indicate that the
checksum must be recalculated. Calling `bytes(cmd)` will recalculate the checksum before converting to bytes.


Profile
=======

Custom profile CSV runner.


CSV
---

The CSV of profile commands is defined by "Command", "Value", "Run Time (s)".

  * Command - Name of the command you want to send.

   * Runs any command registered in "pybk8500.Parser.lookup" as well as predefined custom internal commands.

   * Commands can be a name "SetRemote", hex value "0x20", or decimal value 32.

  * Value - Value to pass into the command.

   * The Command needs the "value" alias or custom internal command.

   * Accepts units! "1 mW" will be parsed and converted to "0.001 W"

  * Run Time (s) - Turn on the load and run for the given amount of time.

   * Accepts Units "1 h" or "1:00:00" will be parsed and converted to "3600 s"


Commands
--------

 * Comment line by starting the line with "#" or ";"
 * Internal Commands

  * "SetupRemote,," - Turn On Remote, Turn Off Load
  * "TeardownRemote,," - Turn Off Load, Turn Off Remote
  * "Run,,10 s" - Run the current mode by turning on the load and reading the input for the run time.
  * "Connect,," - Connect the serial port.
  * "SampleRate,40," - Set the read input time sample rate (1/value delay after each read).
  * "SampleTime,0.1," - Set the read input time (value delay after each read).
  * "BaudRate,38400," - Set the serial port baud rate.
  * "Com,COM1," - Set the serial com port.
  * "Port,COM1," - Set the serial com port.
  * "Output,my_file.csv," - Set the output file for any subsequent runs.

   * "Output,," - Print the results for subsequent runs.

  * "Print,===== Print =====," - Print the value ("===== Print =====") to stdout.
  * "Sleep,0.1 s," - Sleep the given amount of time

   * "Sleep,,0.1 s" - Sleep with timeout also works

  * "Stop,," - Stop running the program here. This is a hard stop that can be useful for debugging.

 * All defined commands in "pybk8500.commands.py" can be used

  * "CC,3 A,100 ms" - Set Constant Current of value (3 A).

   * If "Run Time (s)" is given run this mode for the given amount of time.

  * "CV,12 V,1" - Set Constant Voltage of value (12 V).

   * If "Run Time (s)" is given run this mode for the given amount of time.

  * "CW,1,08:00" - Set Constant Power of value (1 W).

   * If "Run Time (s)" is given run this mode for the given amount of time.

  * "CR,1,1" - Set Constant Resistance of value (1 Ohm).

   * If "Run Time (s)" is given run this mode for the given amount of time.


Example
-------

.. code-block:: text

    # profile.txt
    Command,Value,Run Time (s)
    Print,===== Setup Coms =====
    SampleTime,0.1,
    BaudRate,38400,
    Com,COM1,

    SetupRemote,,
    # "SetupRemote,," does the following
    # RemoteOn,,
    # LoadOff,,

    Print,========== Setup Max Values ==========,
    SetMaxCurrent,4.600 A,0
    SetMaxVoltage,25.000,0
    SetMaxPower,30.000,0

    Print,========== CC ==========,
    Output,CC_test1.csv,
    CC,1mA,0.100
    # Continue saving output for next run
    CC,3 W,100 ms

    Output,CC_test2.csv,
    CC,1.600,19.8

    # Stop output. Print results
    Output,,
    SampleRate,1.000,0
    CW,20.000,60.000

    Print,===== Finished =====,
    TeardownRemote,,
    # "TeardownRemote,," does the following
    # LoadOff,,
    # RemoteOff,,


Run with the command line

.. code-block:: bash

    python -m pybk8500.run_profile "./profile.txt"


Run with python script

.. code-block:: python

    from pybk8500.run_profile import main

    # python -m pybk8500.run_profile "./profile.txt"
    main('./profile.txt')


Plot the results

.. code-block:: python

    from pybk8500 import parse_csv, plot_csv_file, plot_csv_files

    # python -m pybk8500.plot_csv "./profile_results.csv"
    plot_csv_files('./profile_results.csv', './profile_results2.csv')

Combine csv files.

.. code-block:: python

    from pybk8500 import combine_csv_files

    # python -m pybk8500.combine_csv "./profile_results.csv" "./profile_results2.csv"
    combine_csv_files('./profile_results.csv', './profile_results2.csv')
