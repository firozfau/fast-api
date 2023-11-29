# model.py
from sqlalchemy.orm import Session
from datetime import datetime

from db import DB


class GeneralModel(DB):
    def __init__(self):
        super().__init__()
        self.DB = self.engine

    async def get_author_list(self):
        sql_query = "SELECT * FROM authors"
        result = self.DB.execute(sql_query)
        data = result.fetchall()
        return {"data": data}

    async def get_book_list(self):
        sql_query = "SELECT * FROM book_information"
        result = self.DB.execute(sql_query)
        data = result.fetchall()
        return {"data": data}

    async def get_client_list(self):
        sql_query = "SELECT * FROM client_information"
        result = self.DB.execute(sql_query)
        data = result.fetchall()
        return {"data": data}

    async def get_all_borrowed_information(self):
        sql_query = "SELECT borrowed_information.id, borrowed_information.borrowed_date, borrowed_information.created_at, borrowed_information.return_date, borrowed_information.comments, book_information.title, authors.full_name AS author_name, client_information.full_name AS client_name, client_information.dob AS client_date_of_birth, CASE WHEN authors.gender = 1 THEN 'Male' WHEN authors.gender = 2 THEN 'Female' WHEN authors.gender = 3 THEN 'Others' ELSE 'Unknown' END AS authors_gender, CASE WHEN client_information.gender = 1 THEN 'Male' WHEN client_information.gender = 2 THEN 'Female' WHEN client_information.gender = 3 THEN 'Others' ELSE 'Unknown' END AS client_gender, CASE WHEN borrowed_information.status = 1 THEN 'Lend' WHEN borrowed_information.status = 2 THEN 'Return' WHEN borrowed_information.status = 3 THEN 'Lost' ELSE 'Unknown' END AS status FROM borrowed_information INNER JOIN book_information ON borrowed_information.book_id = book_information.id INNER JOIN client_information ON borrowed_information.client_id = client_information.id INNER JOIN authors ON book_information.author_id = authors.id"

        result = self.DB.execute(sql_query)
        data = result.fetchall()
        return {"data": data}

    async def get_borrowed_information_by_client(self, client_name):
        sql_query = "SELECT borrowed_information.id, borrowed_information.borrowed_date, borrowed_information.created_at, borrowed_information.return_date, borrowed_information.comments, book_information.title, authors.full_name AS author_name, client_information.full_name AS client_name, client_information.dob AS client_date_of_birth, CASE WHEN authors.gender = 1 THEN 'Male' WHEN authors.gender = 2 THEN 'Female' WHEN authors.gender = 3 THEN 'Others' ELSE 'Unknown' END AS authors_gender, CASE WHEN client_information.gender = 1 THEN 'Male' WHEN client_information.gender = 2 THEN 'Female' WHEN client_information.gender = 3 THEN 'Others' ELSE 'Unknown' END AS client_gender, CASE WHEN borrowed_information.status = 1 THEN 'Lend' WHEN borrowed_information.status = 2 THEN 'Return' WHEN borrowed_information.status = 3 THEN 'Lost' ELSE 'Unknown' END AS status FROM borrowed_information INNER JOIN book_information ON borrowed_information.book_id = book_information.id INNER JOIN client_information ON borrowed_information.client_id = client_information.id INNER JOIN authors ON book_information.author_id = authors.id  WHERE client_information.full_name =%s"

        result = self.DB.execute(sql_query, (client_name))
        data = result.fetchall()
        if data:
            return data
        else:
            False

    async def find_book_information_in_details(self,book_title,author_name):
        sql_query = "SELECT book_information.*,authors.full_name AS author_name, CASE WHEN authors.gender = 1 THEN 'Male' WHEN authors.gender = 2 THEN 'Female' WHEN authors.gender = 3 THEN 'Others' ELSE 'Unknown' END AS authors_gender FROM book_information  INNER JOIN authors ON book_information.author_id = authors.id   WHERE book_information.title like %s or authors.full_name like %s"

        result = self.DB.execute(sql_query,(f"%{book_title}%", f"%{author_name}%"))
        data = result.fetchall()
        if data:
            return data
        else:
            False


    async def checkExistData(self, table_name, query_data, details=False):
        sql_query = "SELECT * FROM " + table_name + " where " + query_data

        result = self.DB.execute(sql_query)
        data = result.fetchone()
        if details:
            return data if data else False
        else:
            return data['id'] if data else False

    async def create_authors(self, full_name, gender, status, optionAction=False):
        full_name = full_name.strip()

        check_whr = f" full_name = '{full_name}' AND gender = {gender}"
        isExisit = await self.checkExistData("authors", check_whr)
        if (isExisit == False):

            sql_query = "INSERT INTO authors (full_name, gender, status) VALUES (%s, %s, %s) RETURNING id"
            result = self.DB.execute(sql_query, (full_name, gender, status))
            last_insert_id = result.fetchone()
            return last_insert_id[0] if last_insert_id else "failed" if optionAction == True else False
        else:
            return isExisit if optionAction == True else "exist"

    async def create_book_info(self, book_data, author_name, gender, status):
        author_name = author_name.strip()

        author_id = await self.create_authors(author_name, gender, status, True)

        if author_id is not None:

            if isinstance(author_id, (int)):

                insert_stack = []

                # Assuming self.DB is an instance of SQLAlchemy's create_engine
                engine = self.DB

                # Create a database session
                with Session(engine) as session:
                    # Start a transaction
                    transaction = session.begin()

                    try:
                        for item in book_data:
                            book_title = item['title'].strip()
                            check_whr = f" title = '{book_title}' AND author_id = {author_id}"
                            is_exist = await self.checkExistData("book_information", check_whr)

                            if not is_exist:
                                sql_query = "INSERT INTO book_information (title, author_id, status) VALUES (%s, %s, %s) RETURNING id"
                                result = self.DB.execute(sql_query, (book_title, author_id, status))
                                last_insert_id = result.fetchone()

                                if last_insert_id:
                                    insert_stack.append(last_insert_id[0])
                                else:
                                    insert_stack.append("failed")
                            else:
                                insert_stack.append("exist")

                        # Commit the transaction if there are successful insertions
                        if any(isinstance(item, int) for item in insert_stack):
                            # Commit the transaction
                            transaction.commit()
                            insert_status = int(insert_stack[0])
                        else:
                            # Rollback the transaction
                            transaction.rollback()
                            insert_status = "failed" if "failed" in insert_stack else "exist"

                    except Exception as e:
                        # Handle exceptions, log the error, etc.
                        # print(f"Error during transaction: {e}")

                        # Rollback the transaction on error
                        transaction.rollback()
                        insert_status = "failed"

                    # Return the final status
                    return insert_status


            else:
                return "failed"
        else:
            return "failed"

    async def create_clients(self, full_name, dob, gender, status, optionAction=False):
        full_name = full_name.strip()

        check_whr = f" full_name = '{full_name}' AND gender = {gender}"
        is_exist = await self.checkExistData("client_information", check_whr)
        if not is_exist:
            sql_query = "INSERT INTO client_information (full_name, dob, gender, status) VALUES (%s, %s, %s, %s) RETURNING id"
            result = self.DB.execute(sql_query, (full_name, dob, gender, status))
            last_insert_id = result.fetchone()
            return last_insert_id[0] if last_insert_id else "failed" if optionAction == True else False
        else:
            return is_exist if optionAction == True else "exist"

    async def isBookAndClientExist(self, data, type="book"):

        client_name = data.client_name.strip()
        book_title = data.book_title.strip()

        if type == "book":
            check_book_whr = f" title = '{book_title}' AND status = 1"
            is_book_exist = await self.checkExistData("book_information", check_book_whr)
            if is_book_exist:
                return is_book_exist
            else:
                return False
        elif type == "client":
            check_client_whr = f" full_name = '{client_name}' AND status = 1"
            is_client_exist = await self.checkExistData("client_information", check_client_whr)
            if is_client_exist:
                return is_client_exist
            else:
                return False

    async def create_borrowed_book_information(self, data, created_id, status):

        book_id = await self.isBookAndClientExist(data, "book")
        client_id = await self.isBookAndClientExist(data, "client")

        if book_id and client_id:

            check_whr = f" client_id = '{client_id}' AND book_id = {book_id} and status=1"
            is_exist = await self.checkExistData("borrowed_information", check_whr)
            if not is_exist:
                borrowed_date = data.borrowed_date  # datetime.strptime(data.borrowed_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                expected_return_date = data.expected_return_date  # datetime.strptime(data.expected_return_date, '%d-%m-%Y').strftime('%Y-%m-%d')

                sql_query = "INSERT INTO borrowed_information (book_id,client_id,borrowed_date,expected_return_date,comments,status,created_id) VALUES (%s, %s, %s, %s,%s, %s, %s) RETURNING id"
                result = self.DB.execute(sql_query, (
                    book_id, client_id, borrowed_date, expected_return_date, data.comments, status, created_id))
                last_insert_id = result.fetchone()
                return last_insert_id[0] if last_insert_id else "failed"
            else:
                return "exist"

        else:
            return "notfound"

    async def update_borrowed_book_information(self, data, borrowed_status):

        book_id = await self.isBookAndClientExist(data, "book")
        client_id = await self.isBookAndClientExist(data, "client")

        if book_id and client_id:

            check_whr = f" client_id = '{client_id}' AND book_id = {book_id} and status=2"
            is_exist = await self.checkExistData("borrowed_information", check_whr)
            if not is_exist:
                sql_query = "UPDATE borrowed_information SET status = %s, return_date = %s WHERE book_id = %s AND client_id = %s AND status IN (1, 3)  RETURNING id"
                result = self.DB.execute(sql_query, (borrowed_status, data.return_date, book_id, client_id))
                last_insert_id = result.fetchone()
                return last_insert_id[0] if last_insert_id else "failed"
            else:
                return "exist"
        else:
            return "notfound"

    async def isCurrentBookNameWillUpdate(self, new_book_name, author_id, new_author_id):
        check_book_whr = f" title = '{new_book_name}'"
        new_book_data = await self.checkExistData("book_information", check_book_whr, True)

        if new_book_data != False:
            if new_book_data.author_id == new_author_id:
                return True
            else:
                if new_book_data.author_id == author_id:
                    return True
                else:
                    return False
        else:
            return True

    async def update_author_book_information(self, current_book_name, current_author_name, new_book_name,
                                             new_author_name, new_author_gender):

        check_authors_whr = f" full_name = '{current_author_name}'"
        author_id = await self.checkExistData("authors", check_authors_whr)

        if author_id:
            check_book_whr = f" title = '{current_book_name}' AND author_id = '{author_id}'"
            book_id = await self.checkExistData("book_information", check_book_whr)

            if book_id:
                new_author_name_solid = new_author_name.strip()

                new_author_id = await self.create_authors(new_author_name_solid, new_author_gender, 1, True)
                if new_author_id is not None:
                    if isinstance(new_author_id, (int)):
                        new_book_name = new_book_name.strip()

                        isUpdate = await self.isCurrentBookNameWillUpdate(new_book_name, new_author_id, author_id)
                        if isUpdate:

                            sql_query = "UPDATE book_information SET title = %s, author_id = %s WHERE id = %s  RETURNING id"
                            result = self.DB.execute(sql_query, (new_book_name, new_author_id, book_id))
                            last_insert_id = result.fetchone()
                            return last_insert_id[0] if last_insert_id else "failed"
                        else:
                            return "duplicate"

                    else:
                        return "failed"
                else:
                    return "failed"

            else:
                return "notMatch"
        else:
            return "notfound"
