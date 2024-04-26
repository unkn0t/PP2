import psycopg2
import config

from typing import List, Tuple

# Contact:
#     id: int
#     first_name: str
#     last_name: str
#     phones: List[str]
class Contact:
    def __init__(self, id: int, first_name: str, last_name: str, phones: List[str]):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phones = phones

# ContactInfo:
#     first_name: str
#     last_name: str
#     phones: List[str]
class ContactInfo:
    def __init__(self, first_name: str, last_name: str, phones: List[str]):
        self.first_name = first_name
        self.last_name = last_name
        self.phones = phones

class Error:
    pass 

class Dublicate(Error):
    def __init__(self, phone: str, contact: Contact):
        self.phone = phone
        self.contact = contact

    def __str__(self) -> str:
        return f'Phone {self.phone} already owned by [ID:{self.contact.id}] {self.contact.first_name} {self.contact.last_name}'

class NotFound(Error):
    def __init__(self, id: int):
        self.id = id

    def __str__(self) -> str:
        return f'Contact with [ID:{self.id}] not found'

def escape_sql_like(s):
    return s.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')

# Model:
#     add_contact/
#         - contact_info
#         + id
#         ? error (phone owned by another contact) 
#     search_by_name/
#         - first_name
#         - last_name
#         + list[contact]
#     search_by_phone/
#         - phone
#         + list[contact]
#     search_by_id/
#         - id
#         + contact or none
#     delete_contact/
#         - id
#         ? error (no such contact) 
#     update_contact/
#         - id
#         - contact_info
#         ? error (no such contact)
#         ? error (phone owned by another contact) 

class Contacts:
    def __init__(self):
        cfg = config.load()
        self.db = psycopg2.connect(**cfg)
        
        TABLES_SQL = (
            """
            CREATE TABLE IF NOT EXISTS contacts(
                id SERIAL PRIMARY KEY,
                first_name varchar(255) NOT NULL,
                last_name varchar(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phones(
                phone_number varchar(11) PRIMARY KEY,
                contact_id integer REFERENCES contacts
            )
            """
        )

        try:
            with self.db:
                with self.db.cursor() as curs:
                    for sql in TABLES_SQL:
                        curs.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def search_by_name(self, first_name: str, last_name: str) -> List[Contact]:
        GET_IDS_SQL = """
            SELECT id
            FROM contacts
            WHERE 
                first_name LIKE %s AND last_name LIKE %s
        """

        with self.db:
            with self.db.cursor() as curs:
                first_name = escape_sql_like(first_name)
                last_name = escape_sql_like(last_name)
                curs.execute(GET_IDS_SQL, (f'%{first_name}%', f'%{last_name}%'))
                ids = curs.fetchall()
                ids = list(map(lambda row: row[0], ids))
        
        res = []
        for id in ids:
            contact = self.search_by_id(id)
            if contact:
                res.append(contact)
        return res

    def search_by_phone(self, phone: str) -> List[Contact]:
        GET_IDS_SQL = """
            SELECT contact_id
            FROM phones
            WHERE phone_number LIKE %s
            GROUP BY contact_id
        """

        with self.db:
            with self.db.cursor() as curs:
                curs.execute(GET_IDS_SQL, (f'%{phone}%',))
                ids = curs.fetchall()
                ids = list(map(lambda row: row[0], ids))

        res = []
        for id in ids:
            contact = self.search_by_id(id)
            if contact:
                res.append(contact)
        return res

    def search_by_id(self, id: int) -> Contact | None:
        GET_CONTACT_SQL = """
            SELECT 
                first_name, last_name
            FROM contacts
            WHERE id = %s
        """
        GET_PHONES_SQL = """
            SELECT phone_number
            FROM phones
            WHERE contact_id = %s
        """

        with self.db:
            with self.db.cursor() as curs:
                curs.execute(GET_CONTACT_SQL, (id,))
                name = curs.fetchone()
                if name:
                    curs.execute(GET_PHONES_SQL, (id,))
                    phones = curs.fetchall()
                    phones = list(map(lambda row: row[0], phones))
                    return Contact(id, *name, phones=phones)

        return None

    def add(self, info: ContactInfo) -> Tuple[int, Error | None]:
        CONTACT_SQL = """ 
            INSERT INTO 
                contacts
                (first_name, last_name)
            VALUES (%s, %s)
            RETURNING id
        """
        PHONE_SQL = """ 
            INSERT INTO 
                phones
                (phone_number, contact_id)
            VALUES (%s, %s)
        """
        UNIQUE_SQL = """
            SELECT * FROM phones WHERE phone_number = %s 
        """
        ID_SQL = """
            SELECT * FROM contacts WHERE id = %s;
        """

        with self.db:
            with self.db.cursor() as curs:
                curs.execute(CONTACT_SQL, (info.first_name, info.last_name))
                contact_id = curs.fetchone()[0]
                for phone in set(info.phones):
                    curs.execute(UNIQUE_SQL, (phone,))
                    row = curs.fetchone()
                    if row:
                        phone, id = row
                        curs.execute(ID_SQL, (id,))
                        contact = Contact(*curs.fetchone(), phones=[])
                        self.db.rollback()
                        return (-1, Dublicate(phone, contact)) 
                    
                    curs.execute(PHONE_SQL, (phone, contact_id))

        return (contact_id, None)

    def update(self, id: int, info: ContactInfo) -> Error | None:
        UPDATE_CONTACT_SQL = """
            UPDATE contacts
            SET 
                first_name = %s,
                last_name = %s 
            WHERE id = %s
        """
        GET_PHONES_SQL = """
            SELECT phone_number
            FROM phones
            WHERE contact_id = %s
        """
        ADD_PHONE_SQL = """ 
            INSERT INTO 
                phones
                (phone_number, contact_id)
            VALUES (%s, %s)
        """
        DELETE_PHONE_SQL = "DELETE FROM phones WHERE phone_number = %s"
        
        new_phones = set(info.phones)
        
        with self.db:
            with self.db.cursor() as curs:
                curs.execute(GET_PHONES_SQL, (id,))
                old_phones = curs.fetchall()
                old_phones = set(map(lambda row: row[0], old_phones))
                deleted = old_phones.difference(new_phones)
                added = new_phones.difference(old_phones)

                for phone in deleted:
                    curs.execute(DELETE_PHONE_SQL, (phone,))
                for phone in added:
                    curs.execute(ADD_PHONE_SQL, (phone, id))

                curs.execute(UPDATE_CONTACT_SQL, (info.first_name, info.last_name, id))

        return None

    def delete(self, id: int) -> Error | None:
        PHONES_SQL = "DELETE FROM phones WHERE contact_id = %s"
        CONTACT_SQL = "DELETE FROM contacts WHERE id = %s"
        
        with self.db:
            with self.db.cursor() as curs:
                curs.execute(PHONES_SQL, (id,))
                curs.execute(CONTACT_SQL, (id,))
                rows_deleted = curs.rowcount
        return None if rows_deleted > 0 else NotFound(id) 

    def __del__(self):
        self.db.close()

