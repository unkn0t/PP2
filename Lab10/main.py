from model import ContactInfo, Contacts

from textual import on
from textual.app import App, ComposeResult 
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Button, Static

class NewContactScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="First name", id="first-name")
        yield Input(placeholder="Last name", id="last-name")
        yield Input(placeholder="Phone number", id="phone")
        yield Button("Add phone")
        yield Button.success("OK", id="confirm")

    def on_mount(self) -> None:
        self.contacts = Contacts()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            first_name = self.query_one("#first-name", expect_type=Input).value
            last_name = self.query_one("#last-name", expect_type=Input).value
            phone = self.query_one("#phone", expect_type=Input).value
            self.contacts.add(ContactInfo(
                first_name,
                last_name,
                phones=[phone]
            )) 
            self.app.pop_screen()

class PhonebookApp(App):
    SCREENS = {"new_contact": NewContactScreen()}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Provide name, phone or id", max_length=255, id="query")
        yield Button.success("New", id="new")
        yield DataTable()

    def on_mount(self) -> None:
        self.contacts = Contacts()

        self.title = "PHONEBOOK"
        self.sub_title = "App to manage your contacts"

        table = self.query_one(DataTable)
        table.add_columns("id", "first name", "last name", "phones")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new":
            self.push_screen("new_contact")

    @on(Input.Changed)
    def update_table(self, event: Input.Changed) -> None:
        if event.input.id != "query":
            return

        query = event.value

        table = self.query_one(DataTable)
        table.clear()

        if len(query) == 0:
            return 
        
        res = []
        if query.startswith('@'):
            try:
                id = int(query[1:])
                contact = self.contacts.search_by_id(id)
                if contact:
                    res.append(contact)
            except Exception as error:
                # do logging
                pass
        elif query.startswith('+'):
            phone = query[1:]
            res.extend(self.contacts.search_by_phone(phone))
        else:
            words = query.split(' ')
            first_name = words[0]
            last_name = words[1] if len(words) > 1 else ''
            res.extend(self.contacts.search_by_name(first_name, last_name))

        for contact in res:
            table.add_row(contact.id, contact.first_name, 
                          contact.last_name, contact.phones)

if __name__ == "__main__":
    app = PhonebookApp()
    app.run()
