import asyncio

from utils.db_api.films_sql import Database_Film


async def test():
    db = Database_Film()
    await db.create()
    # await db.create_table_films()

    # users = await db.select_all_Tavarlar()
    # print(users)
    # await db.add_Tavar(user_id="23131", t_turi="330", t_soni="2", t_nomer="4", t_narxi="40000")
    # await db.add_Tavar(user_id="23131", t_turi="800", t_soni="2", t_nomer="4", t_narxi="80000")
    # users = await db.select_all_Tavarlar()
    # user1 = await db.update_film("1", name='Ibtido_2')
    # print(user1)


    # await db.delete_Tavar(user_id="23131")
    users = await db.select_all_users()
    user = await db.select_film(name="Ibtido_2")
    print(user)


asyncio.run(test())

#
# soat = "10-11"
# print(soat[:2])
# print(soat[2])
# print(soat[3:5])
