from typing import List
import requests
import qrcode
import io
import click
from requests.sessions import RequestsCookieJar

from kraftringen import BankIDAuthorizer, API
from sys import stderr


def format_cookies(cookies: RequestsCookieJar) -> str:
    # example output format
    # .example.com TRUE / FALSE 1560211200 MY_VARIABLE MY_VALUE
    cookie_strings: List[str] = []
    # example attributes (note: the value has been randomly generated to provide an example):
    # {'version': 0, 'name': 'ASP.NET_SessionId', 'value': 'lI4Ea7mSgtgP08i4Kq97Mwyz', 'port': None, 'port_specified': False, 'domain': 'mittkraftringen.kraftringen.se', 'domain_specified': False, 'domain_initial_dot': False, 'path': '/', 'path_specified': True, 'secure': False, 'expires': None, 'discard': True, 'comment': None, 'comment_url': None, 'rfc2109': False, '_rest': {'HttpOnly': None, 'SameSite': 'Lax'}}
    for _, cookies in cookies._cookies.items():
        for _, group in cookies.items():
            for _, attributes in group.items():
                cookie_strings.append(
                    f"{attributes.domain}\tFALSE\t{attributes.path}\t{'TRUE' if attributes.secure else 'FALSE'}\t{0 if attributes.expires is None else attributes.expires}\t{attributes.name}\t{attributes.value}")
    return "\n".join(cookie_strings)


def authorize() -> requests.Session:
    session = requests.session()
    authorizer = BankIDAuthorizer(session)
    authorizer.request_api_key()
    authorizer.request_start_token()
    url = authorizer.format_bankid_url()
    qr = qrcode.QRCode()
    qr.add_data(url)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read(), file=stderr)
    authorizer.wait_for_signature()
    authorizer.login()
    return session


@click.group()
def main():
    pass


@click.command(help="Login to Kraftringen")
def login():
    session = authorize()
    cookies = format_cookies(session.cookies)
    print(cookies)


main.add_command(login)

if __name__ == "__main__":
    main()
