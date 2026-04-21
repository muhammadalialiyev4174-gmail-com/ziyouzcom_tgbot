import aiosqlite
import logging


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    async def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        
        async with aiosqlite.connect(self.path_to_db) as connection:
            # uncomment this to log SQL queries
            # await connection.set_trace_callback(logger)
            cursor = await connection.cursor()
            data = None
            await cursor.execute(sql, parameters)

            if commit:
                await connection.commit()
            if fetchall:
                data = await cursor.fetchall()
            if fetchone:
                data = await cursor.fetchone()
            return data

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
        """
        await self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        if parameters:
            sql += " AND ".join([
                f"{item} = ?" for item in parameters
            ])
            return sql, tuple(parameters.values())
        return sql, ()

    async def add_user(self, id: int, name: str, username: str = None, email: str = None, language: str = 'uz'):
        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        await self.execute(sql, parameters=(id, name, email, language), commit=True)
    
    async def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return await self.execute(sql, fetchall=True)
    
    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters=parameters, fetchone=True)

    async def count_users(self):
        return await self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    async def update_user_email(self, email, id):
        sql = """
        UPDATE Users SET email=? WHERE id=?
        """
        return await self.execute(sql, parameters=(email, id), commit=True)
    
    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", commit=True)
    
    async def select_all_category(self):
        sql = """
        SELECT * FROM category
        """
        return await self.execute(sql, fetchall=True)
        
    async def select_category(self, **kwargs):
        sql = "SELECT * FROM category WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters=parameters, fetchone=True)
    
    async def add_category_books(self, id: int, name: str, typ: str):
        sql = """
        INSERT INTO category_books(id, name, typ) VALUES(?, ?, ?)
        """
        await self.execute(sql, parameters=(id, name, typ), commit=True)
    
    async def select_any_category_books(self, **kwargs):
        sql = "SELECT * FROM category_books WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters=parameters, fetchall=True)
        
    async def select_category_books(self, **kwargs):
        sql = "SELECT * FROM category_books WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters=parameters, fetchone=True)
          
    async def select_all_category_books(self):
        sql = """
        SELECT * FROM category_books
        """
        return await self.execute(sql, fetchall=True)

def logger(statement):
    logging.info(f"Executing SQL: {statement}")
