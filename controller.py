import logging
from model import GeneralModel


class Controller:
    def __init__(self):
        self.model = GeneralModel()

    async def getGender(self, id):
        data = {
            "1": "Male",
            "2": "Female",
            "3": "Others",
            "4": "Unknown"
        }

        if (str(id) or int(id)) in data:
            return data[str(id)]
        else:
            return data['4']

    async def getGenderCode(self, id):
        data = {
            "Male": "1",
            "Female": "2",
            "Others": "3",
            "Unknown": "4"
        }

        if (str(id)) in data:
            return data[str(id)]
        else:
            return data['Unknown']

    async def getMessage(self, keyword, result):
        exist_msg = keyword + " information already exists. Please check your input."
        failed_msg = keyword + " creation failed. Please check your input."
        success_msg = "Successfully created a new information."

        message = exist_msg if result == "exist" else (failed_msg if result == "failed" else success_msg)

        return message

    async def get_author_list(self):
        try:
            return await self.model.get_author_list()
        except Exception as e:
            logging.exception("Error in get_author_list")
            raise e

    async def get_book_list(self):
        try:
            return await self.model.get_book_list()
        except Exception as e:
            logging.exception("Error in get_book_list")
            raise e

    async def get_client_list(self):
        try:
            return await self.model.get_client_list()
        except Exception as e:
            logging.exception("Error in get_client_list")
            raise e

    async def get_all_borrowed_information(self):
        try:
            return await self.model.get_all_borrowed_information()

        except Exception as e:
            logging.exception("Error in get_all_borrowed_information")
            raise e

    async def get_borrowed_information_by_client(self,client_name):
        try:
            data= await self.model.get_borrowed_information_by_client(client_name)
            if data:
                return {
                    "status":"ok",
                    "data":data,
                }
            else:
                return {
                    "status":"Not-Found",
                    "message":"No book borrower information found for this client."
                }

        except Exception as e:
            logging.exception("Error in get_borrowed_information_by_client")
            raise e



    async def find_book_information_in_details(self,book_title,author_name):
        try:
            data= await self.model.find_book_information_in_details(book_title,author_name)
            if data:
                return {
                    "status":"ok",
                    "data":data,
                }
            else:
                return {
                    "status":"Not-Found",
                    "message":"Your keyword does not match any book name or author name in our system."
                }

        except Exception as e:
            logging.exception("Error in find_book_information_in_details")
            raise e


    async def save_author_information(self, full_name, gender):
        try:
            gender_code= await self.getGenderCode(gender)
            result = await self.model.create_authors(full_name, gender_code, status=1)
            data = {
                "status": "ok" if isinstance(result, int) else str(result),
                "message": await self.getMessage("Author", str(result)),
                "data": {
                    "id": result if isinstance(result, int) else "",
                    "name": full_name,
                    "gender": gender,
                }
            }

            return data

        except Exception as e:
            logging.exception("Error in save_author_information")
            raise e

    async def save_book_information(self, data):

        try:
            author_name = data['author']['author_name']
            gender = await self.getGenderCode(data['author']['gender'])
            book_data = data['books']
            result = await self.model.create_book_info(book_data, author_name, gender, status=1)

            return_data = {
                "status": "ok" if isinstance(result, int) else str(result),
                "message": await self.getMessage("Book", str(result)),
                "data": {
                    "id": result if isinstance(result, int) else "",
                    "author_name": author_name,
                    "gender": gender,
                    "books": book_data,

                }
            }

            return return_data


        except Exception as e:
            logging.exception("Error in save_book_information")
            raise e

    async def save_client_information(self, full_name, dob, gender):
        try:
            gender_code=await self.getGenderCode(gender)
            result = await self.model.create_clients(full_name, dob, gender_code, status=1)
            data = {
                "status": "ok" if isinstance(result, int) else str(result),
                "message": await self.getMessage("Client", str(result)),
                "data": {
                    "id": result if isinstance(result, int) else "",
                    "name": full_name,
                    "dob": dob,
                    "gender": gender,
                }
            }

            return data

        except Exception as e:
            logging.exception("Error in save_client_information")
            raise e

    async def save_borrowed_book_information(self, data):
        try:
            created_id = 1
            result = await self.model.create_borrowed_book_information(data, created_id, status=1)

            if result == "notfound":
                message = "This Book or Client information does not found!"
            elif result == "exist":
                message = "This client has already borrowed this book. First return that book then you can."
            elif result == "failed":
                message = "Something is wrong! Please try again."
            else:
                message = "Successfully accepted borrow request."

            return_data = {
                "status": "ok" if isinstance(result, int) else str(result),
                "message": message,
                "data": {
                    "id": result if isinstance(result, int) else "",
                    "data": data if isinstance(result, int) else "",
                }
            }

            return return_data

        except Exception as e:
            logging.exception("Error in save_borrowed_book_information")
            raise e


    async def update_borrowed_book_information(self, data):
        try:
            borrowed_status = 2
            result = await self.model.update_borrowed_book_information(data, borrowed_status)

            if result == "notfound":
                message = "This Book or Client information does not found!"
            elif result == "exist":
                message = "This book has already been returned by the client."
            elif result == "failed":
                message = "Something is wrong! Please try again."
            else:
                message = "Successfully return this book."

            return_data = {
                "status": "ok" if isinstance(result, int) else str(result),
                "message": message,
                "data": {
                    "id": result if isinstance(result, int) else "",
                    "data": data if isinstance(result, int) else "",
                }
            }

            return return_data

        except Exception as e:
            logging.exception("Error in update_borrowed_book_information")
            raise e


    async def update_author_book_information(self, current_book_name,current_author_name,new_book_name,new_author_name,new_author_gender):
        try:

            new_author_gender_code = await self.getGenderCode(new_author_gender)
            result = await self.model.update_author_book_information(current_book_name,current_author_name,new_book_name,new_author_name,new_author_gender_code)

            if result == "notfound":
                message = "Book and Author information not found !"
            elif result == "notMatch":
                message = "This author does not currently have this book"
            elif result == "exist":
                message = "Book information already updated"
            elif result == "failed":
                message = "Something is wrong! Please try again."
            elif result == "duplicate":
                message = "The new book is already associated with another author"
            else:
                message = "Book information updated successfully"

            return_data = {
                "status": "ok" if isinstance(result, int) else str(result),
                "message": message,
                "data": {
                    "id": result if isinstance(result, int) else "",
                    "book-name": current_author_name if isinstance(result, int) else "",
                    "author-name": new_author_name if isinstance(result, int) else "",
                }
            }

            return return_data

        except Exception as e:
            logging.exception("Error in update_borrowed_book_information")
            raise e
