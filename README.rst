========
pybk8500
========

Python library for the BK Precision 8500 SERIES DC ELECTRONIC LOADS

Models 8500, 8502, 8510, 8512, 8514, 8518, 8520,
8522, 8524 & 8526

Protocol found at https://bkpmedia.s3.amazonaws.com/downloads/manuals/en-us/85xx_manual.pdf
in the "Command details" section.


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