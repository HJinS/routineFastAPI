from pydantic import BaseModel, Field, ValidationError, validator, EmailStr
import re


class UserRegistrationSchema(BaseModel):

    email: EmailStr = Field(...)
    first_name: str = Field(..., max_length=15)
    last_name: str = Field(..., max_length=15)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @validator('confirm_password', always=True)
    def password_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValidationError('password does not match')
        return v

    @validator('password', always=True)
    def password_rule(cls, v):
        if not re.findall('[()[\]{}|`~!@#$%^&*_\-+=;:\'",<>./?]', v):
            raise ValidationError('The password must contain at least 1 symbol: ' + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?")
        if len(v) < 8:
            raise ValidationError('The length should be greater than 8')

    class Config:
        validate_all = True


class UserLoginSchema(BaseModel):

    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
