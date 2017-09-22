import re
import requests
import logging


def _str_response(res):
    return 'HTTP/1.1 {status_code}\n{headers}\n\n{body}'.format(
        status_code=res.status_code,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
        body=res.content,
    )


class Viper:
    def __init__(self, ses_id=None, ses_password=None, ses_username=None, viper_username=None, viper_password=None):
        if ses_username is not None:
            self.ses_username = ses_username
        elif ses_id is not None:
            self.ses_username = "ses_{}".format(ses_id)
        else:
            raise(TypeError("missing required argument 'ses_username', provide either 'ses_username' or 'ses_id'"))

        if ses_password is not None:
            self.ses_password = ses_password
        else:
            raise(TypeError("missing required argument 'ses_password'"))

        if viper_username is not None:
            self.viper_username = viper_username
        elif ses_id is not None:
            self.viper_username = ses_id
        else:
            raise(TypeError("missing required argument 'viper_username', provide either 'viper_username' or 'ses_id'"))

        if viper_password is not None:
            self.viper_password = viper_password
        elif ses_id is not None:
            self.viper_password = "0{}".format(ses_id)
        else:
            raise(TypeError("missing required argument 'viper_password', provide either 'viper_password' or 'ses_id'"))

        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()

    def _login_ses(self):
        r = self.session.post(
            "https://viper.ses.vic.gov.au/_yfniecqqxbdycgmvb_login",
            data={
                'httpd_username' : self.ses_username,
                'httpd_password' : self.ses_password,
            },
            allow_redirects=True
        )
        self.logger.debug(_str_response(r))
        return r

    def _login_viper(self):
        r = self.session.post(
            "https://viper.ses.vic.gov.au/ViperWeb/login.do",
            data = {
                'username' : self.viper_username,
                'password' : self.viper_password,
                'rememberme' : "on",
            },
            allow_redirects=False
        )
        self.logger.debug(_str_response(r))
        return r

    def _send_msg(self, to, msg, priority=3):
        r = self.session.post(
            "https://viper.ses.vic.gov.au/ViperWeb/msg/sendMessage.do",
            data = {
                'searchTerm' : to,
                'message' : msg,
                'charCount' : len(msg),
                'messageTypeId' : str(priority), # 3 == admin, 2 == non-emergency
                'charMsg' : "", # Temporary buffer
            },
            allow_redirects=False
        )
        self.logger.debug(_str_response(r))
        return r

    def send(self, to, msg):
        progress = None
        for i in range(5):
            self.logger.info("Sending page")
            r = self._send_msg(to, msg)

            if (r.status_code == 302 and re.match(r"/_\w+_form", r.headers["Location"]) is not None):
                self.logger.info("Logging in to SES network")
                progress = "SES Login"
                self._login_ses()
            elif (r.status_code == 302 and r.headers["Location"] == "https://viper.ses.vic.gov.au/ViperWeb/login.jsp"):
                self.logger.info("Logging in to Viper")
                progress = "Viper Login"
                self._login_viper()
            elif (r.status_code == 200 and re.search(r"<td>Message Accepted</td>", r.text) is not None):
                self.logger.info("Message sent successfully")
                return False
            else:
                self.logger.warn("Unknown response")
                progress = "Unknown response"
                if not self.logger.isEnabledFor(logging.DEBUG):
                    # Already output if debug is enabled
                    self.logger.info(_str_response(r))
        return progress
