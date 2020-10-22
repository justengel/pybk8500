import time
import pybk8500


with pybk8500.CommunicationManager(com='COM1', baudrate=38400) as ser:
    # Set to remote (Must start with this command for running remote)
    cmd = pybk8500.SetRemoteOperation(operation=1)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    # Set the load
    cmd = pybk8500.LoadSwitch(operation=1)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    print('Waiting!')
    time.sleep(1)

    # Set the load
    cmd = pybk8500.LoadSwitch(operation=0)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    # Set to Local
    cmd = pybk8500.SetRemoteOperation(operation=0)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    print('Exiting!')
    time.sleep(1)
