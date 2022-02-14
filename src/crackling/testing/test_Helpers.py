import nose.tools
import sys, io, datetime
from crackling.Helpers import *
from subprocess import CalledProcessError, TimeoutExpired

################
## Testing rc ##
################
def test_rc_onPalindromicSeq():
    result = rc('ACGTACGTACGTACGTACGT')
    expected = 'ACGTACGTACGTACGTACGT'
    nose.tools.eq_(expected, result, f'\nExpected:\t{expected}\nActually:\t{result}')


#####################
## Testing printer ##
#####################
def test_printer_output():
    # Setting up stdout capture
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    # Generate phrase
    expectedPhrase = 'This is a test phrase: a86a3a279afd9beb2d4e9b202318b58ac65552ddfba5901f24b870153b7b44e6'
    # Run printer function
    printer(expectedPhrase)
    # Reset stdout
    sys.stdout = old_stdout
    # Get caputed stdout value
    result = mystdout.getvalue()
    # Extract phrase
    resultPhrase = result[32:]
    nose.tools.eq_(expectedPhrase.strip(), resultPhrase.strip(), f'\nExpected:\t{expectedPhrase}\nActually:\t{resultPhrase}')

def test_printer_timestamp():
    # Setting up stdout capture
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    # Generate time
    expectedDateTime = datetime.datetime.now()
    # Run printer function
    printer('')
    # Reset stdout
    sys.stdout = old_stdout
    # Get caputed stdout value
    result = mystdout.getvalue()
    # Extract date and time
    testDate = list(map(int, result[4:14].split("-")))
    testTime = list(map(int, result[15:30].split(":")))
    resultDateTime = datetime.datetime(
        testDate[0], testDate[1], testDate[2],
        testTime[0], testTime[1], testTime[2], testTime[3]
        )
    nose.tools.eq_(expectedDateTime, resultDateTime, f'\nExpected:\t{expectedDateTime}\nActually:\t{resultDateTime}')


####################
## Testing runner ##
####################
def test_runner_output():
    # Setting up stdout capture
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    # Generate expected result
    expected = [
        "| Calling: ('exit 0',)",
        '',
        '| Finished',
        '',
        ''
    ]
    # Run runner function
    runner('exit 0', shell=True)
    # Reset stdout
    sys.stdout = old_stdout
    # Get caputed stdout value
    result = mystdout.getvalue().split('\n')
    # Strip time stamps
    result[0] = result[0][32:]
    result[2] = result[2][32:]
    nose.tools.eq_(expected, result, f'\nExpected:\t{expected}\nActually:\t{result}')

@nose.tools.raises(CalledProcessError)
def test_runner_errorChecking():
    # Should raise exception
    runner('exit 1', shell=True, check=True)

@nose.tools.raises(TimeoutExpired)
def test_runner_timeout():
    # Should raise exception
    runner('sleep 0.001', shell=True, check=True, timeout=0.0001)


if __name__ == '__main__':
    nose.run()