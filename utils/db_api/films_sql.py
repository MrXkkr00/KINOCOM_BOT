from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database_Film:

    def __init__(self) -> None:
        self.pool: Union[Pool, None] = None

    async def create(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        except Exception as e:
            print(f"Error creating connection pool: {e}")

    async def disconnect(self):

        try:
            if self.pool:
                await self.pool.close()
        except Exception as e:
            print(f"Error closing connection pool: {e}")

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):

        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_films(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Films (
            id SERIAL PRIMARY KEY,
            film_number varchar(255),
            film_cod varchar(255),
            name varchar(255), 
            tili varchar(255),
            hajmi varchar(255),
            sifati varchar(255),
            janri varchar(255),
            korish_yoshi varchar(255),
            davomiyligi varchar(255)
            );
"""
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_film(self, film_number: str = None, film_cod: str = None, name: str = None, tili: str = None,
                       hajmi: str = None, sifati: str = None, janri: str = None, korish_yoshi: str = None,
                       davomiyligi: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Films(film_number, film_cod, name, tili, hajmi, sifati, janri, 
        korish_yoshi, davomiyligi) 
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) returning *
        """
        return await self.execute(sql, film_number, film_cod, name, tili, hajmi, sifati, janri,
                                  korish_yoshi, davomiyligi, fetchrow=True)

    async def select_all_users(self):
        sql = """
        SELECT * FROM Films
        """
        return await self.execute(sql, fetch=True)

    async def select_film(self, **kwargs):
        sql = "SELECT * FROM Films WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_films(self):
        return await self.execute("SELECT COUNT(*) FROM Films", fetchval=True)

    async def drop_films(self):
        await self.execute("DROP TABLE Films", execute=True)

    async def update_film(self, film_number: str, **kwargs):
        # Ensure that there are fields to update
        if not kwargs:
            return "No fields provided to update."

        # Start building the SQL command
        sql = "UPDATE Films SET "

        # Format the SQL command to update fields dynamically
        sql += ", ".join([f"{item} = ${num}" for num, item in enumerate(kwargs.keys(), start=1)])
        sql += " WHERE film_number = $" + str(len(kwargs) + 1)  # Append the 'WHERE' condition to update by film_number

        # Create the parameters for the query
        parameters = tuple(kwargs.values()) + (film_number,)

        # Execute the command
        return await self.execute(sql, *parameters, execute=True)


# await db.update_film("F123", name="Updated Film Name", sifati="HD")

