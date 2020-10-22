import time
import pybk8500


def print_received(msg):
    print('Reading:', msg)


with pybk8500.CommunicationManager(com='COM1', baudrate=38400) as ser:
    # Set to remote (Must start with this command for running remote)
    cmd = pybk8500.SetRemoteOperation(operation=1)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    # Set constant current
    cmd = pybk8500.SetCCModeCurrent(current=1)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    # Set the load
    cmd = pybk8500.LoadSwitch(operation=1)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    timeout = 5
    print('Waiting {} sec ...\n'.format(timeout))
    # time.sleep(timeout)
    start = time.time()
    read_values = pybk8500.ReadInputVoltageCurrentPowerState()
    with ser.change_message_parsed(print_received):
        while (time.time() - start) < timeout:
            ser.write(read_values)
            time.sleep(0.1)

    # Set the load
    print()
    cmd = pybk8500.LoadSwitch(operation=0)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    # Set to remote (Must start with this command for running remote)
    cmd = pybk8500.SetRemoteOperation(operation=0)
    ser.send_wait(cmd, timeout=1, print_recv=True)

    print('Exiting!')
    time.sleep(1)
