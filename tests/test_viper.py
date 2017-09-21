# NOTE: We are testing the process but not the details of each form
#       request. Due to the fragility of the form interactions the most
#       likely issue is going to be an upstream change, locking the current
#       process in with tests just makes adapting slower and more annoying.
#       A basic functional test is sufficient to ensure that the forms are
#       appropriate.

import pytest
from viper import Viper
from requests import Response
import requests
import requests_mock

def test_creation():
    # Initialisation basically takes login password details
    # Multiple creation options to try and leverage default SES values

    # Default options, id number & ses password
    t1 = Viper(ses_id='23', ses_password='alphabet')
    assert(type(t1) is Viper)
    assert(t1.ses_username == 'ses_23')
    assert(t1.ses_password == 'alphabet')
    assert(t1.viper_username == '23')
    assert(t1.viper_password == '023')

    # Explicit options
    t2 = Viper(ses_username='foo', ses_password='car', viper_username='flubble', viper_password='duck')
    assert(type(t2) is Viper)
    assert(t2.ses_username == 'foo')
    assert(t2.ses_password == 'car')
    assert(t2.viper_username == 'flubble')
    assert(t2.viper_password == 'duck')


    # Override some defaults
    t3 = Viper(ses_id='23', ses_password='alphabet', viper_username='donald', ses_username='duck')
    assert(type(t3) is Viper)
    assert(t3.ses_username == 'duck')
    assert(t3.ses_password == 'alphabet')
    assert(t3.viper_username == 'donald')
    assert(t3.viper_password == '023')

    # Override different defaults
    t4 = Viper(ses_id='23', ses_password='alphabet', viper_password='foo', viper_username='raffy')
    assert(type(t4) is Viper)
    assert(t4.ses_username == 'ses_23')
    assert(t4.ses_password == 'alphabet')
    assert(t4.viper_username == 'raffy')
    assert(t4.viper_password == 'foo')

    # Try missing ses_password
    with pytest.raises(TypeError) as e5:
        t5 = Viper(ses_id='23')
    assert('ses_password' in str(e5))

    # Try missing ses_username
    with pytest.raises(TypeError) as e6:
        t6 = Viper(ses_password='car', viper_username='flubble', viper_password='duck')
    assert('ses_username' in str(e6))
    assert('ses_id' in str(e6))

    # Try missing viper_username
    with pytest.raises(TypeError) as e7:
        t7 = Viper(ses_username='my', ses_password='car', viper_password='duck')
    assert('viper_username' in str(e7))
    assert('ses_id' in str(e7))

    # Try missing viper_password
    with pytest.raises(TypeError) as e8:
        t8 = Viper(ses_username='my', ses_password='car', viper_username='flubble')
    assert('viper_password' in str(e8))
    assert('ses_id' in str(e8))

def test_send():
    ses_login_resp = Response()
    ses_login_resp.status_code = 302
    ses_login_resp.headers['Location'] = '/_yfniecqqxbdycgmvb_form?Lw=='

    viper_login_resp = Response()
    viper_login_resp.status_code = 302
    viper_login_resp.headers['Location'] = 'https://viper.ses.vic.gov.au/ViperWeb/login.jsp'

    success_resp = Response()
    success_resp.status_code = 200
    success_resp._content = b'<td>Message Accepted</td>'

    basic_resp = Response()
    basic_resp.status_code = 200

    # POST URLs used by program
    send_url = 'https://viper.ses.vic.gov.au/ViperWeb/msg/sendMessage.do'
    ses_login_url = 'https://viper.ses.vic.gov.au/_yfniecqqxbdycgmvb_login'
    viper_login_url = 'https://viper.ses.vic.gov.au/ViperWeb/login.do'

    responses = []
    def send_handler(request):
        if request.path_url == '/ViperWeb/msg/sendMessage.do':
            try:
                return responses.pop(0)
            except IndexError:
                resp = Response
                resp.status_code = 200
                return resp
        else:
            return None

    adapter = requests_mock.Adapter()
    adapter.register_uri('POST', 'https://viper.ses.vic.gov.au/ViperWeb/login.do')
    adapter.register_uri('POST', 'https://viper.ses.vic.gov.au/_yfniecqqxbdycgmvb_login')
    adapter.add_matcher(send_handler)

    # Standard auth pattern
    t1 = Viper(ses_id='23', ses_password='alphabet')
    responses = [ses_login_resp, viper_login_resp, success_resp]
    with requests_mock.mock() as m1:
        m1._adapter = adapter # Dodgy but nfi how it is meant to be done
        err1 = t1.send('111', 't1 send')
    assert(err1 == False)
    assert(m1.request_history.pop(0).url == send_url)
    assert(m1.request_history.pop(0).url == ses_login_url)
    assert(m1.request_history.pop(0).url == send_url)
    assert(m1.request_history.pop(0).url == viper_login_url)
    assert(m1.request_history.pop(0).url == send_url)
    assert(len(m1.request_history) == 0)
    assert(len(responses) == 0)

    # No auth required
    t2 = Viper(ses_id='23', ses_password='alphabet')
    responses = [success_resp]
    with requests_mock.mock() as m2:
        m2._adapter = adapter # Dodgy but nfi how it is meant to be done
        err2 = t2.send('111', 't1 send')
    assert(err2 == False)
    assert(m2.request_history.pop(0).url == send_url)
    assert(len(m1.request_history) == 0)
    assert(len(responses) == 0)

    # SES auth unsuccessful
    t3 = Viper(ses_id='23', ses_password='alphabet')
    responses = [ses_login_resp, ses_login_resp, ses_login_resp, ses_login_resp, ses_login_resp] 
    with requests_mock.mock() as m3:
        m3._adapter = adapter # Dodgy but nfi how it is meant to be done
        err3 = t3.send('111', 't1 send')
    assert(err3 == "SES Login")
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == ses_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == ses_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == ses_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == ses_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == ses_login_url)
    assert(len(m1.request_history) == 0)
    assert(len(responses) == 0)

    # Viper auth unsuccessful
    t4 = Viper(ses_id='23', ses_password='alphabet')
    responses = [ses_login_resp, viper_login_resp, viper_login_resp, viper_login_resp, viper_login_resp] 
    with requests_mock.mock() as m4:
        m4._adapter = adapter # Dodgy but nfi how it is meant to be done
        err4 = t4.send('111', 't1 send')
    assert(err4 == "Viper Login")
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == ses_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == viper_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == viper_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == viper_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == viper_login_url)
    assert(len(m1.request_history) == 0)
    assert(len(responses) == 0)

    # Garbage out
    t5 = Viper(ses_id='25', ses_password='alphabet')
    responses = [basic_resp, basic_resp, basic_resp, basic_resp, basic_resp] 
    with requests_mock.mock() as m5:
        m5._adapter = adapter # Dodgy but nfi how it is meant to be done
        err5 = t5.send('111', 't1 send')
    assert(err5 == "Unknown response")
    assert(m5.request_history.pop(0).url == send_url)
    assert(m5.request_history.pop(0).url == send_url)
    assert(m5.request_history.pop(0).url == send_url)
    assert(m5.request_history.pop(0).url == send_url)
    assert(m5.request_history.pop(0).url == send_url)
    assert(len(m1.request_history) == 0)
    assert(len(responses) == 0)

    # Weird flow
    t6 = Viper(ses_id='23', ses_password='alphabet')
    responses = [viper_login_resp, basic_resp, ses_login_resp, viper_login_resp, success_resp] 
    with requests_mock.mock() as m6:
        m6._adapter = adapter # Dodgy but nfi how it is meant to be done
        err6 = t6.send('111', 't1 send')
    assert(err6 == False)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == viper_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == ses_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(m3.request_history.pop(0).url == viper_login_url)
    assert(m3.request_history.pop(0).url == send_url)
    assert(len(m1.request_history) == 0)
    assert(len(responses) == 0)

