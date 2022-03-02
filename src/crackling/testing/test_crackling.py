from crackling import ConfigManager
from crackling.Helpers import printer
from crackling.cracklingClass import Crackling
import hashlib, pytest, os

@pytest.fixture
def crackling_setup():
    # Setup 
    # (Nothing to setup)
    # NOTE: Everything after yeild is considered teardown as per Pytest documentation. (https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization)
    yield 
    # Teardown
    os.remove('data/output/test-guides.txt')
    os.remove('data/output/test-test.errlog')
    os.remove('data/output/test-test.log')

def test_crackling(crackling_setup):
    cm = ConfigManager('data/integration-testing/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    if not cm.isConfigured():
        print('Something went wrong with reading the configuration.')
        exit()
    else:
        printer('Crackling is starting...')

    c = Crackling(cm)   
    c.run()

    result = hashlib.md5(open('data/output/test-guides.txt','rb').read()).hexdigest()
    expected = '244007ec9e5681fa1953b8e83a1072f3'

    assert expected == result