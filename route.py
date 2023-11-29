# route.py
from fastapi import APIRouter, Depends, HTTPException,Path,Body
from pydantic import ValidationError
from security import verify_token
from validation import *
from controller import Controller
import logging



#router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_token)])
obj = Controller()  # Create an instance of the Controller class


@router.get("/authorList")
async def author_list():
    try:
        result = await obj.get_author_list()
        return result
    except Exception as e:
        logging.exception("Error in author_list")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/bookList")
async def book_list():
    try:
        result = await obj.get_book_list()
        return result
    except Exception as e:
        logging.exception("Error in book_list")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/clientList")
async def client_list():
    try:
        result = await obj.get_client_list()
        return result
    except Exception as e:
        logging.exception("Error in client_list")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/allBorrowedInformation")
async def all_borrowed_information():
    try:
        result = await obj.get_all_borrowed_information()
        return result
    except Exception as e:
        logging.exception("Error in all_borrowed_information")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

async def validate_client_name(client_name: str = Path(..., title="Client Name", description="You have to enter the same client name")):
    return client_name

async def validate_book_title(book_title: str = Path(..., title="Book Title", description="You have to enter the minimum The first letter of the book's title")):
    return book_title

async def validate_author_name(author_name: str = Path(..., title="Author Name", description="You have to enter the minimum The first letter of the author name")):
    return author_name

@router.get("/borrowedInformationByClient/{client_name}")
async def borrowed_information_by_client(client_name:str = Depends(validate_client_name)):
    try:
        result = await obj.get_borrowed_information_by_client(client_name)
        return result
    except Exception as e:
        logging.exception("Error in borrowed_information_by_client")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/findBookInformation/{book_title}/{author_name}")
async def find_book_information(book_title:str = Depends(validate_book_title),author_name:str = Depends(validate_author_name)):
    try:
        result = await obj.find_book_information_in_details(book_title,author_name)
        return result

    except Exception as e:
        logging.exception("Error in find_book_information")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e



@router.post("/addAuthor")
async def add_author(author: Author):
    try:
        # Validate the request parameters using the Validation model
        valid_dict = author.dict()
        # If validation is successful, call the controller method with the parameters
        result = await obj.save_author_information(valid_dict["author_name"], valid_dict["gender"])
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/addBook")
async def add_books(books: ValidaitonBooks):
    try:
        data = books.dict()
        result = await obj.save_book_information(data)
        return result

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/addClient")
async def add_client(client: ClientValidation):
    try:
        # Validate the request parameters using the Validation model
        valid_dict = client.dict()
        # If validation is successful, call the controller method with the parameters
        result = await obj.save_client_information(valid_dict["client_name"], valid_dict["dob"], valid_dict["gender"])
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/borrowedBook")
async def borrowed_book(data: borrowedBookValidation):
    try:
        # Validate the request parameters using the Validation model
        valid_dict = data.dict()
        # If validation is successful, call the controller method with the parameters
        result = await obj.save_borrowed_book_information(data)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/bookReturn")
async def return_book(data: returnBookValidation):
    try:
        # Validate the request parameters using the Validation model
        valid_dict = data.dict()
        # If validation is successful, call the controller method with the parameters
        result = await obj.update_borrowed_book_information(data)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/updateBookInfo")
async def update_book_info(update_info: UpdateBookInfo):
    try:

        result = await obj.update_author_book_information(
            update_info.current_book_name,
            update_info.current_author_name,
            update_info.new_book_name,
            update_info.new_author_name,
            update_info.new_author_gender
        )
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
