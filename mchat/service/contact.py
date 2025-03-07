import mchat.data.contact as d_contact
from mchat.helper import db_connect


@db_connect
def get_by_user(curs, user_id):
    db_contacts = d_contact.get_by_user(curs, user_id)
    contacts = []
    for db_contact in db_contacts:
        contact = {
            "username": db_contact["receiver_username"],
            "id": db_contact["receiver_id"],
        }
        if user_id == db_contact["receiver_id"]:
            contact = {
                "username": db_contact["sender_username"],
                "id": db_contact["sender_id"],
            }
        contacts.append(contact)
    return contacts


@db_connect
def get_by_user_and_date(curs, user_id, create_date):
    return d_contact.get_by_user_and_date(user_id, create_date)
