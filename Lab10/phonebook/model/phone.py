from dataclasses import dataclass
from typing import List
from . import ModelManager

@dataclass
class Phone:
    id: int
    num: str 
    
@dataclass
class PhoneForCreate:
    num: str 
    contact_id: int

def create(mm: ModelManager, phone: PhoneForCreate) -> int:
    if exist(mm, phone.num):
        raise Exception(f"Contact with phone number {phone.num} already exists.")

    curs = mm.db.cursor()
    curs.execute("""
        INSERT INTO phones (
            phone_num, contact_id
        ) 
        VALUES (%s, %s) 
        RETURNING id
    """, (phone.num, phone.contact_id))
    
    row = curs.fetchone()
    id = row[0]

    curs.close()
    return id

def get_by_contact(mm: ModelManager, contact_id: int) -> List[Phone]:
    curs = mm.db.cursor()
    curs.execute("""
        SELECT id, phone_num
        FROM phones
        WHERE contact_id = %s
    """, (contact_id,))
    rows = curs.fetchall()
    curs.close()
    return list(map(lambda row: Phone(*row), rows))

def exist(mm: ModelManager, num: str) -> bool:
    curs = mm.db.cursor()
    curs.execute("SELECT id FROM phones WHERE phone_num = %s", (num,))
    count = curs.rowcount
    curs.close()
    return count > 0 

def update(mm: ModelManager, phone: Phone) -> None:
    if exist(mm, phone.num):
        raise Exception(f"Contact with phone number {phone.num} already exists.")
    
    curs = mm.db.cursor()
    curs.execute(""" 
        UPDATE phones
        SET phone_num = %s 
        WHERE id = %s 
    """, (phone.num, phone.id))
    curs.close()

def delete(mm: ModelManager, id: int) -> None:
    curs = mm.db.cursor()
    curs.execute("""
        DELETE FROM phones
        WHERE id = %s
    """, (id,))
    curs.close()

def delete_by_contact(mm: ModelManager, contact_id: int) -> None:
    curs = mm.db.cursor()
    curs.execute("""
        DELETE FROM phones
        WHERE contact_id = %s
    """, (contact_id,))
    curs.close()

