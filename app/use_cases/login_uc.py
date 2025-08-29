from fastapi import Depends
from starlette.responses import Response

from app.schemas.login_request import LoginRequest
from app.use_cases.usecase import UseCase
from app.utils.password import verify_password


class LoginUC(UseCase):
    def __init__(self, response=Depends(Response)):
        self.response = response
        pass

    async def action(self, *args, **kwargs):
        data: LoginRequest = args[0]
        
        # Example of how to use the password utility for login verification
        # In a real implementation, you would:
        # 1. Find the user by username from the database
        # 2. Get the stored hashed password
        # 3. Use verify_password to check if the provided password matches
        # 
        # Example:
        # user = await user_repository.find_by_username(data.username)
        # if user and verify_password(data.password, user.password):
        #     # Login successful
        #     return {"success": True, "message": "Login successful"}
        # else:
        #     # Login failed
        #     return {"success": False, "message": "Invalid credentials"}

        self.response.headers.add('Access-Control-Allow-Origin', '*')

