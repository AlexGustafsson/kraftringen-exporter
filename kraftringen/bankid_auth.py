import json
import requests
from requests.auth import AuthBase
from typing import List, TypedDict, Union
from time import sleep

from requests.models import PreparedRequest


class BasicAuth(AuthBase):
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["authorization"] = "Basic " + self.token
        return r


class AuthenticationInitializationeResponse(TypedDict):
    transactionIdField: str
    orderRefField: str
    autoStartTokenField: str


class Attribute(TypedDict):
    nameField: str
    valueField: str


class CollectResponse(TypedDict):
    transactionIdField: str
    attributesField: List[Attribute]
    signatureField: str


class CollectRequestResponse(TypedDict):
    FaultStatus: int
    FaultStatusAsString: Union[str, None]
    ProgressStatusAsString: str
    CollectResponse: CollectResponse


class PinCode(TypedDict):
    PinCode: str
    CustomerId: str
    FullName: str
    CustomerCode: str


class CustomerPinCodeResponse(TypedDict):
    d: str


class BankIDAuthorizer:
    def __init__(self, session: requests.Session) -> None:
        self.__session = session
        self.__api_key: str
        self.__start_token: str
        self.__collect_response: CollectRequestResponse
        pass

    def request_api_key(self) -> str:
        self.__api_key = self.__session.get(
            "https://mittkraftringen.kraftringen.se/api/eid/key").text.strip('"')
        return self.__api_key

    def request_start_token(self) -> str:
        response: AuthenticationInitializationeResponse = self.__session.post("https://mittkraftringen.kraftringen.se/api/eid/InitializeAuthenticationProcess/21175/null", auth=BasicAuth(
            self.__api_key), allow_redirects=False).json(object_hook=lambda d: AuthenticationInitializationeResponse(**d))
        self.__start_token = response["autoStartTokenField"]
        self.__order_reference = response["orderRefField"]
        return self.__start_token

    def format_bankid_url(self) -> str:
        return f'bankid:///?autostarttoken={self.__start_token}&redirect='

    def request_signature(self) -> Union[CollectRequestResponse, None]:
        """
        Returns a response if successful, None if ongoing or raises an exception if unsuccessful.
        """
        response = self.__session.post(f'https://mittkraftringen.kraftringen.se/api/eid/CollectRequest/21175/{self.__order_reference}', auth=BasicAuth(
            self.__api_key), allow_redirects=False).json(object_hook=lambda d: CollectRequestResponse(**d))
        # If completed
        if response["ProgressStatusAsString"] == "COMPLETE":
            # Something happened
            if response["FaultStatus"] != 0:
                raise Exception(response["FaultStatusAsString"])
            return response
        return None

    def wait_for_signature(self) -> CollectRequestResponse:
        response: Union[CollectRequestResponse, None] = None
        for _ in range(15):
            response = self.request_signature()
            if response is not None:
                break
            sleep(3)
        if response is None:
            raise Exception("signature never completed")
        self.__collect_response = response
        return response

    def login(self) -> str:
        serial = ""
        for attributes_field in self.__collect_response["CollectResponse"]["attributesField"]:
            if attributes_field["nameField"] == "Subject.SerialNumber":
                serial = attributes_field["valueField"]
        if serial == "":
            raise Exception("no serial found in collect response")

        pin_response: CustomerPinCodeResponse = self.__session.post(
            "https://mittkraftringen.kraftringen.se/Default.aspx/GetCustomerByPinCode", allow_redirects=False, json={"personalNumber": serial, "transactionId": self.__collect_response["CollectResponse"]["transactionIdField"]}).json(object_hook=lambda d: CustomerPinCodeResponse(**d))

        pin_code: PinCode = json.loads(pin_response["d"])[0]

        self.__session.post(
            "https://mittkraftringen.kraftringen.se/Default.aspx/Login", allow_redirects=False, json={"personalNumber": serial, "customerId": pin_code["CustomerId"], "collectResponse": self.__collect_response["CollectResponse"], "transId": self.__collect_response["CollectResponse"]["transactionIdField"], "signatureField": self.__collect_response["CollectResponse"]["signatureField"]})

        return pin_code["CustomerId"]
