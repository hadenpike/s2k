#!/usr/bin/env python
# s2k --- Send files to your Kindle email
#
# Author: Haden Pike <haden.pike@gmail.com>
#
# Copyright (c) 2017 Haden Pike
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import smtplib
import sys

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from os.path import basename

__all__ = ['send_to_kindle']

def _prepare_msg(sender, rcpt, convert = False, files = None):
    """Format the message to be sent to Kindle.

    @param sender: Email to send from.
    @type sender: str
    @param rcpt: Your Kindle email address.
    @type rcpt: str
    @param convert: Whether or not to have the Kindle service convert files to Kindle's internal format
    @type convert: bool
    @param files: The files to attach to the message.
    @type files: list
    @return msg: The email message
    @rtype msg: MIMEMultipart
    """

    assert(isinstance(files, list))
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = rcpt
    msg['Date'] = formatdate(localtime = True)
    if convert:
        msg['Subject'] = 'convert'

    for f in files:
        fname = basename(f)
        with open(f, 'rb') as fil:
            attachment = MIMEApplication(fil.read(),
                                         name = fname)
            attachment['Content-Disposition'] = "attachment; filename={0}".format(fname)
            msg.attach(attachment)

    return msg

def _send_msg(msg, username, password, server, port):
    """Send an email message.
    @param msg: The message to send.
    @type msg: MIMEMultipart
    @param username: The username to authenticate the SMTP server
    @type usernAme: str
    @param password: The password to authenticate the SMTP server.
    @type password: str
    @param server: The SMTP server to send from.
    @type server: str
    @param port: The port the SMTP server is listening on.
    @type port: int
    """

    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.close()

def send_to_kindle(sender, rcpt, username, password, server, port, files = None):
    msg = _prepare_msg(sender, rcpt, convert = False, files = files)
    _send_msg(msg, username, password, server, port)

def main():
    send_to_kindle(*sys.argv[1:7], files = sys.argv[7:])

if __name__ == '__main__':
    main()
