# validation.py
from pydantic import BaseModel, constr, validator
from typing import List,Optional
import re

class Author(BaseModel):
    author_name: constr(min_length=3, max_length=150)

    @validator('author_name')
    def validate_author_name(cls, value):
        # Use a regular expression to check for allowed characters
        if not all(char.isalnum() or char.isspace() or char in "_-' " for char in value):
            raise ValueError("Invalid characters in author_name. Only A-Z, a-z, _, -, and ' are allowed.")
        return value

    gender: constr(max_length=10)

    @validator('gender')
    def validate_gender(cls, value, valid_genders={'Male', 'Female', 'Others', 'Unknown'}):
        if value not in valid_genders:
            raise ValueError(f"Invalid gender value. Must be one of {', '.join(valid_genders)}.")
        return value

class Books(BaseModel):
    title: constr(min_length=3, max_length=250)

    @validator('title')
    def validate_title(cls, value):
        # Use a regular expression to check for allowed characters
        if not all(char.isalnum() or char.isspace() or char in "_-' " for char in value):
            raise ValueError("Invalid characters in title. Only A-Z, a-z, 0-9, _, -, and ' are allowed.")

        return value

class Date(BaseModel):
    date: constr(max_length=10)  # Assuming "dob" is a string in the format 'dd-mm-yyyy'

    @validator('date')
    def validate_date(cls, value):
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # Change the pattern to match 'yyyy-mm-dd'
        if not datePattern.match(value):
            raise ValueError("Invalid date format. Must be in the format 'yyyy-mm-dd'.")
        return value



class ValidaitonBooks(BaseModel):
    author: Author
    books: List[Books]

    class Config:
        orm_mode = True



class ClientValidation(BaseModel):
    client_name: constr(min_length=3, max_length=150)

    @validator('client_name')
    def validate_client_name(cls, value):
        # Use a regular expression to check for allowed characters
        if not all(char.isalnum() or char.isspace() or char in "_-' " for char in value):
            raise ValueError("Invalid characters in client_name. Only A-Z, a-z, _, -, and ' are allowed.")
        return value

    gender: constr(max_length=10)

    @validator('gender')
    def validate_gender(cls, value, valid_genders={'Male', 'Female', 'Others', 'Unknown'}):
        if value not in valid_genders:
            raise ValueError(f"Invalid gender value. Must be one of {', '.join(valid_genders)}.")
        return value

    dob: constr(max_length=10)  # Assuming "dob" is a string in the format 'dd-mm-yyyy'

    @validator('dob')
    def validate_dob(cls, value):
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # Change the pattern to match 'yyyy-mm-dd'
        if not datePattern.match(value):
            raise ValueError("Invalid date format. Must be in the format 'yyyy-mm-dd'.")
        return value


class borrowedBookValidation(BaseModel):
    client_name: constr(min_length=3, max_length=150)

    @validator('client_name')
    def validate_client_name(cls, value):
        # Use a regular expression to check for allowed characters
        if not all(char.isalnum() or char.isspace() or char in "_-' " for char in value):
            raise ValueError("Invalid characters in client_name. Only A-Z, a-z, _, -, and ' are allowed.")
        return value

    book_title: constr(min_length=3, max_length=250)

    @validator('book_title')
    def validate_book_title(cls, value):
        # Use a regular expression to check for allowed characters
        if not all(char.isalnum() or char.isspace() or char in "_-' " for char in value):
            raise ValueError("Invalid characters in book_title. Only A-Z, a-z, 0-9, _, -, and ' are allowed.")

        return value

    borrowed_date: constr(max_length=10)

    @validator('borrowed_date')
    def validate_borrowed_date(cls, value):
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # Change the pattern to match 'yyyy-mm-dd'
        if not datePattern.match(value):
            raise ValueError("Invalid date format. Must be in the format 'yyyy-mm-dd'.")
        return value

    expected_return_date: constr(max_length=10)
    @validator('expected_return_date')
    def validate_expected_return_date(cls, value):
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # Change the pattern to match 'yyyy-mm-dd'
        if not datePattern.match(value):
            raise ValueError("Invalid date format. Must be in the format 'yyyy-mm-dd'.")
        return value

    comments: constr(max_length=250)




class returnBookValidation(BaseModel):
    client_name: constr(min_length=3, max_length=150)

    @validator('client_name')
    def validate_client_name(cls, value):
        # Use a regular expression to check for allowed characters
        if not all(char.isalnum() or char.isspace() or char in "_-' " for char in value):
            raise ValueError("Invalid characters in client_name. Only A-Z, a-z, _, -, and ' are allowed.")
        return value

    book_title: constr(min_length=3, max_length=250)

    @validator('book_title')
    def validate_book_title(cls, value):
        # Use a regular expression to check for allowed characters
        if not all(char.isalnum() or char.isspace() or char in "_-' " for char in value):
            raise ValueError("Invalid characters in book_title. Only A-Z, a-z, 0-9, _, -, and ' are allowed.")

        return value

    return_date: constr(max_length=10)

    @validator('return_date')
    def validate_return_date(cls, value):
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # Change the pattern to match 'yyyy-mm-dd'
        if not datePattern.match(value):
            raise ValueError("Invalid date format. Must be in the format 'yyyy-mm-dd'.")
        return value



class UpdateBookInfo(BaseModel):
    current_book_name: constr(min_length=3, max_length=250)
    current_author_name: constr(min_length=3, max_length=150)
    new_book_name: Optional[constr(min_length=3, max_length=250)] = None
    new_author_name: Optional[constr(min_length=3, max_length=150)] = None

    @validator('new_book_name', 'new_author_name', pre=True, always=True)
    def strip_string(cls, value):
        # Strip leading and trailing whitespaces from optional fields
        return value.strip() if value is not None else value

    new_author_gender: constr(max_length=10)

    @validator('new_author_gender')
    def validate_new_author_gender(cls, value, valid_new_author_gender={'Male', 'Female', 'Others', 'Unknown'}):
        if value not in valid_new_author_gender:
            raise ValueError(f"Invalid gender value. Must be one of {', '.join(valid_new_author_gender)}.")
        return value