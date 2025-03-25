from requests import Response
from mosip_auth_sdk import MOSIPAuthenticator
from mosip_auth_sdk.models import DemographicsModel
from dynaconf import Dynaconf
from dotenv import load_dotenv
import os

class AuthHandler:
    def __init__(self):
        load_dotenv()
        config_path = os.environ["CONFIG_PATH"]
        assert(config_path is not "")
        print(config_path)
        config = Dynaconf(settings_files=[config_path])
        self.authenticator = MOSIPAuthenticator(config=config)

    def yesno(self, uid: str, demographic_data: DemographicsModel) -> tuple[bool, str, str]:
        response: Response = self.authenticator.auth(  # type: ignore
            individual_id=uid,
            individual_id_type="UIN",
            consent=True,
            demographic_data=demographic_data,
        )

        response_body: dict[str, str] = response.json()
        response_time = response_body.get("responseTime", "")
        response_errors = response_body.get("errors", [])

        response_proper: dict = response_body.get("response")
        assert response_proper is not None
        response_status = response_proper.get("authStatus")
        assert response_status is not None
        final_response = (response_status, response_time, str(response_errors))

        return final_response
    
    def otp_request(self, uid: str) -> str:
        response: Response = self.authenticator.genotp(
            individual_id=uid,
            individual_id_type="UIN",
            phone=True
        )

        response_body: dict[str, str] = response.json()

        print(response_body)

        errors = response_body.get("errors") or []
        if errors:
            raise Exception(errors)
        txn_id: str = response_body.get("transactionID")
        assert txn_id is not None
        return txn_id
    
    def otp_verify(self, uid: str, txn_id: str, otp_value: str) -> bool:
        response: Response = self.authenticator.kyc(
            individual_id=uid,
            individual_id_type="UIN",
            otp_value=otp_value,
            consent=True,
            txn_id=txn_id
        )

        response_body: dict[str, str] = response.json()
        response_proper: dict = response_body.get("response")
        assert response_proper is not None
        final_response = response_proper.get("kycStatus")
        assert final_response is not None
        return final_response


def main():
    auth = AuthHandler()
    demo: DemographicsModel = DemographicsModel(dob="1992/04/29")
    print(auth.yesno("2047631038", demo))


if __name__ == "__main__":
    main()
