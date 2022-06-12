from pydantic import BaseModel, Field, ValidationError, validator, EmailStr
import re


class UserSchema(BaseModel):

    email: EmailStr = Field(..., min_length=8, max_length=25, unique_items=True)
    first_name: str = Field(..., max_length=15)
    last_name: str = Field(..., max_length=15)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @validator('password2', always=True)
    def password_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValidationError('passwords do not match')
        return v

    @validator('password1', always=True)
    def password_rule(cls, v):
        if not re.findall('[()[\]{}|`~!@#$%^&*_\-+=;:\'",<>./?]', v):
            raise ValidationError('The password must contain at least 1 symbol: ' + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?")
