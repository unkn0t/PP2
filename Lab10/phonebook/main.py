from view.app import PhonebookApp

import model
import model.contact
import model.phone

def test():
    mm = model.ModelManager()
    all_contacts = model.contact.get_many(mm, model.contact.GetManyFilters(
        limit=100,
        offset=0,
        pattern="In"
    ))
    for cont in all_contacts:
        print(cont)

def main():
    app = PhonebookApp()
    app.run()

if __name__ == "__main__":
    test()
