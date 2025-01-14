import sys
import time

import pytest
from fido2.ctap import CtapError
from fido2.utils import hmac_sha256, sha256
from tests.utils import *


@pytest.mark.skipif(
    "--sim" in sys.argv or '--nfc' in sys.argv,
    reason="Simulation doesn't care about user presence"
)
class TestUserPresence(object):
    def test_user_presence_instructions(self, MCRes, GARes):
        print()
        print()
        print("Starting User Presence (UP) tests.")
        time.sleep(1)
        print()
        print(
            "Follow instructions.  You will have to give UP or not give UP to pass the tests."
        )
        time.sleep(2)

    def test_user_presence(self, device, GARes):
        print("ACTIVATE UP ONCE")
        device.sendGA(*FidoRequest(GARes).toGA())

    def test_no_user_presence(self, device, MCRes, GARes):
        print("DO NOT ACTIVATE UP")
        with pytest.raises(CtapError) as e:
            device.sendGA(*FidoRequest(GARes, timeout=2).toGA())
        assert e.value.code == CtapError.ERR.INVALID_COMMAND

    def test_user_presence_option_false_on_get_assertion(self, device, MCRes, GARes):
        print("DO NOT ACTIVATE UP")
        time.sleep(1)
        device.sendGA(*FidoRequest(GARes, options = {'up': False}, timeout=2).toGA())

    def test_user_presence_option_false_on_make_credential(self, device, MCRes):
        print("DO NOT ACTIVATE UP")
        time.sleep(1)
        with pytest.raises(CtapError) as e:
            device.sendMC(*FidoRequest(MCRes, options = {'up': False}, timeout=1).toMC())
        assert e.value.code == CtapError.ERR.INVALID_OPTION
        with pytest.raises(CtapError) as e:
            device.sendMC(*FidoRequest(MCRes, options = {'up': True}, timeout=1).toMC())
        assert e.value.code == CtapError.ERR.INVALID_OPTION


    def test_user_presence_permits_only_one_request(self, device, MCRes, GARes):
        print("ACTIVATE UP ONCE")
        device.sendGA(*FidoRequest(GARes).toGA())

        with pytest.raises(CtapError) as e:
            device.sendGA(*FidoRequest(GARes, timeout=1).toGA())
        assert e.value.code == CtapError.ERR.INVALID_COMMAND
