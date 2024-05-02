from dataclasses import dataclass
from typing import List, Optional
from . import ModelManager
from . import phone

@dataclass
class Contact:
    id: int
    first_name: str
    last_name: str
    phones: List[phone.Phone]

@dataclass
class ContactForCreate:
    first_name: str
    last_name: str
    phone_num: str

@dataclass
class ContactForUpdate:
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    phones_c: List[str]
    phones_d: List[int]
    phones_u: List[phone.Phone]

@dataclass
class GetManyFilters:
    limit: int 
    offset: int
    pattern: str = ""
    inc: bool = True

class ModelError(Exception):
    pass

class EntityNotExist(ModelError):
    def __init__(self, entity: str, id: int) -> None:
        super().__init__(f"{entity} with id {id} does not exist")

class EntityAlreadyExist(ModelError):
    def __init__(self, entity: str, value, other_id: int) -> None:
        super().__init__(f"{entity} with value {value} already exists at id {other_id}")

def create(mm: ModelManager, contact: ContactForCreate) -> int:
    with mm.db.cursor() as curs:
        curs.execute("""
            INSERT INTO contacts(first_name, last_name)
            VALUES (%s, %s)
            RETURNING id;
        """, (contact.first_name, contact.last_name))
        row = curs.fetchone()
        contact_id = row[0]
    
    phone.create(mm, phone.PhoneForCreate(
        contact.phone_num,
        contact_id
    ))

    mm.db.commit()
    return contact_id

def create_or_replace(mm: ModelManager, contact: ContactForCreate) -> int:
    if phone.exist(mm, contact.phone_num):
        raise EntityAlreadyExist("phone", contact.phone_num, 0) 
    
    curs = mm.db.cursor()
    curs.execute("""
        call create_or_replace_contact(
            row(%s, %s, %s)::contact_for_create,
            null 
        )
    """, (contact.first_name, contact.last_name, contact.phone_num))
    row = curs.fetchone()
    contact_id = row[0]

    curs.close()
    mm.db.commit()

    return contact_id

def get(mm: ModelManager, id: int) -> Contact:
    curs = mm.db.cursor()
    curs.execute("""
        SELECT first_name, last_name
        FROM contacts
        WHERE id = %s
    """, (id,))
    row = curs.fetchone()
    first_name, last_name = row
    phones = phone.get_by_contact(mm, id)
    curs.close()
    return Contact(id, first_name, last_name, phones)

def get_many(mm: ModelManager, filters: GetManyFilters) -> List[Contact]:
    res = []

    sql = "SELECT * FROM contacts\n"
    
    pattern = filters.pattern.replace('%', '').replace('_', '')
    pattern = pattern.lower()
    params = {}
    if len(pattern) > 0:
        sql += "WHERE LEVENSHTEIN(LOWER(first_name), %(pattern)s, 2, 1, 2) < 12\n"
        sql += "ORDER BY SIMILARITY(LOWER(first_name), %(pattern)s) DESC\n"
        params['pattern'] = f'%{pattern}%'
    else:
        if filters.inc:
            sql += "ORDER BY id ASC\n"
        else:
            sql += "ORDER BY id DESC\n"

    sql += f"LIMIT {filters.limit} OFFSET {filters.offset}\n"

    curs = mm.db.cursor()
    curs.execute(sql, params)
    for row in curs.fetchall():
        id, first_name, last_name = row
        phones = phone.get_by_contact(mm, id)
        res.append(Contact(id, first_name, last_name, phones))

    curs.close()
    return res 

def update(mm: ModelManager, contact: ContactForUpdate) -> None:
    sql = "UPDATE contacts\n"
    params = []
    
    if contact.first_name is not None:
        sql += "SET first_name = %s\n"
        params.append(contact.first_name)
    if contact.last_name is not None:
        sql += "SET last_name = %s\n"
        params.append(contact.last_name)

    for phone_num in contact.phones_c:
        phone.create(mm, phone.PhoneForCreate(phone_num, contact.id))

    for phone_id in contact.phones_d:
        phone.delete(mm, phone_id)
    
    for phone_u in contact.phones_u:
        phone.update(mm, phone_u)
    
    if len(params) > 0:
        sql += "WHERE id = %s"
        params.append(contact.id)

        curs = mm.db.cursor()
        curs.execute(sql, params)
        curs.close()

    mm.db.commit()

def delete(mm: ModelManager, id: int) -> None:
    phone.delete_by_contact(mm, id)

    with mm.db.cursor() as curs:
        curs.execute("DELETE FROM contacts WHERE id = %s", (id,))

        if curs.rowcount == 0:
            raise EntityNotExist("contact", id) 

    mm.db.commit()

