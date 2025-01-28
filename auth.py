from requests import Response
from mosip_auth_sdk import MOSIPAuthenticator
from mosip_auth_sdk.models import DemographicsModel
from dynaconf import Dynaconf


class AuthHandler:
    def __init__(self):
        config = Dynaconf(settings_files=["./env/config.toml"])
        self.authenticator = MOSIPAuthenticator(config=config)

    def yesno(self, uid: str, demographic_data: DemographicsModel) -> bool:
        response: Response = self.authenticator.auth(  # type: ignore
            individual_id=uid,
            individual_id_type="uid",
            consent=True,
            demographic_data=demographic_data,
        )

        response_body: dict[str, str] = response.json()
        response_proper: dict = response_body.get("response")
        return response_proper.get("auth_status")
