
def test_names_to_values():
    import pybk8500

    cmd = pybk8500.CommandStatus(status=0x90)
    assert cmd.status == 'Checksum incorrect'
    assert cmd[3] == 0x90
    cmd = pybk8500.CommandStatus(status='Parameter incorrect')
    assert cmd.status == 'Parameter incorrect'
    assert cmd[3] == 0xA0

    cmd = pybk8500.SetRemoteOperation(operation=0)
    assert cmd.operation == 'Front Panel'
    assert cmd[3] == 0
    cmd = pybk8500.SetRemoteOperation(operation='Remote')
    assert cmd.operation == 'Remote'
    assert cmd[3] == 1

    cmd = pybk8500.LoadSwitch(value=0)
    assert cmd.value == 'Off'
    assert cmd[3] == 0
    cmd = pybk8500.LoadSwitch(value='On')
    assert cmd.value == 'On'
    assert cmd[3] == 1

    cmd = pybk8500.SetMode(value=0)
    assert cmd.value == 'CC'
    assert cmd[3] == 0
    cmd = pybk8500.SetMode(value='CV')
    assert cmd.value == 'CV'
    assert cmd[3] == 1

    cmd = pybk8500.SelectListOperation(operation=0)
    assert cmd.value == 'CC'
    assert cmd[3] == 0
    cmd = pybk8500.SelectListOperation(operation='CV')
    assert cmd.value == 'CV'
    assert cmd[3] == 1

    cmd = pybk8500.SetHowListsRepeat(repeat=0)
    assert cmd.value == 'Once'
    assert cmd[3] == 0
    cmd = pybk8500.SetHowListsRepeat(repeat='Repeat')
    assert cmd.value == 'Repeat'
    assert cmd[3] == 1

    cmd = pybk8500.SetMemoryPartition(scheme=1)
    assert cmd.value == '1 file of 1000 list steps'
    assert cmd[3] == 1
    cmd = pybk8500.SetMemoryPartition(scheme='2 files of 500 list steps')
    assert cmd.value == '2 files of 500 list steps'
    assert cmd[3] == 2

    cmd = pybk8500.SetTimerStateLoadOn(state=0)
    assert cmd.value == 'disabled'
    assert cmd[3] == 0
    cmd = pybk8500.SetTimerStateLoadOn(state='enabled')
    assert cmd.value == 'enabled'
    assert cmd[3] == 1


if __name__ == '__main__':
    test_names_to_values()
