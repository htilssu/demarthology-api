from fastapi import Depends
from starlette.responses import Response

from app.schemas.login_request import LoginRequest
from app.use_cases.usecase import UseCase


class LoginUC(UseCase):
    def __init__(self, response=Depends(Response)):
        self.response = response
        pass

    async def action(self, *args, **kwargs):
        data: LoginRequest = args[0]


        self.response.headers.add('Access-Control-Allow-Origin', '*')

