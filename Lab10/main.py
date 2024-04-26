from pathlib import Path
from typing import Iterable

from textual.coordinate import Coordinate
from model import ContactInfo, Contacts

from textual import on, work
from textual.app import App, ComposeResult 
from textual.screen import Screen
from textual.widgets import DataTable, DirectoryTree, Footer, Header, Input, Button, Label 

import csv

def read_from_csv(path: Path) -> Iterable[ContactInfo]:
    with open(path, newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            phones = row['phones'].split(';')
            yield ContactInfo(row['first_name'], row['last_name'], phones)

class FilterCSVDirTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        def csv_or_dir(path: Path) -> bool:
            if path.name.startswith('.'):
                return False
            return path.is_dir() or (path.is_file() and path.suffix == ".csv") 
        return filter(csv_or_dir, paths)

class ImportCSVScreen(Screen):
    def compose(self) -> ComposeResult:
        yield FilterCSVDirTree(Path.home())
        yield Label("Selected file:")
        yield Input(disabled=True)
        yield Button.success("OK", id="confirm")
    
    def on_mount(self) -> None:
        self.contacts = Contacts()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        selected_file = self.query_one(Input)
        selected_file.value = str(event.path)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            selected_file = self.query_one(Input)
            for info in read_from_csv(Path(selected_file.value)):
                self.contacts.add(info)
            self.app.pop_screen()

class NewContactScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="First name", id="first-name")
        yield Input(placeholder="Last name", id="last-name")
        yield Input(placeholder="Phone number", id="phone")
        yield Button("Add phone")
        yield Button.success("Ok", id="confirm")
        yield Button.error("Cancel", id="cancel")

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
        elif event.button.id == "cancel":
            self.app.pop_screen()

class UpdateContactScreen(Screen[bool]):
    def __init__(self, id: int, first_name, last_name, phones) -> None:
        super().__init__()
        self.contact_id = id
        self.first_name = first_name
        self.last_name = last_name 
        self.phones = phones

    def compose(self) -> ComposeResult:
        yield Input(placeholder="First name", id="first-name")
        yield Input(placeholder="Last name", id="last-name")
        yield Input(placeholder="Phone number", id="phone")
        yield Button("Add phone")
        yield Button.success("Ok", id="confirm")
        yield Button.error("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.contacts = Contacts()
        self.query_one("#first-name", expect_type=Input).value = self.first_name
        self.query_one("#last-name", expect_type=Input).value = self.last_name
        self.query_one("#phone", expect_type=Input).value = self.phones[0]
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            first_name = self.query_one("#first-name", expect_type=Input).value
            last_name = self.query_one("#last-name", expect_type=Input).value
            phone = self.query_one("#phone", expect_type=Input).value
            self.contacts.update(self.contact_id, ContactInfo(
                first_name,
                last_name,
                phones=[phone]
            )) 
            self.dismiss(True)
        elif event.button.id == "cancel":
            self.dismiss(False)

class PhonebookApp(App):
    SCREENS = {
        "new_contact": NewContactScreen(),
        "import": ImportCSVScreen()
    }

    BINDINGS = [
        ("d", "delete_row", "Delete contact"),
        ("u", "update_row", "Update contact")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Provide name, phone or id", max_length=255, id="query")
        yield Button.success("New", id="new")
        yield Button.success("Import", id="import")
        yield DataTable(cursor_type='row')
        yield Footer()
    
    @work
    async def action_update_row(self) -> None:
        table = self.query_one(DataTable)
        key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        id, first_name, last_name, phones = table.get_row(key)
        update_screen = UpdateContactScreen(id, first_name, last_name, phones)
        
        if await self.push_screen_wait(update_screen):
            coord = Coordinate(table.cursor_row, 0)
            contact = self.contacts.search_by_id(id)
            
            for value in contact.__dict__.values():
                table.update_cell_at(coord, value, update_width=True)
                coord = coord.right()
        else:
            self.notify("Canceled")

    def action_delete_row(self) -> None:
        table = self.query_one(DataTable)
        key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        id = table.get_row(key)[0]
        self.contacts.delete(id)
        table.remove_row(key)

    def on_mount(self) -> None:
        self.contacts = Contacts()

        self.title = "PHONEBOOK"
        self.sub_title = "App to manage your contacts"

        table = self.query_one(DataTable)
        table.add_columns("id", "first name", "last name", "phones")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new":
            self.push_screen("new_contact")
        elif event.button.id == "import":
            self.push_screen("import")

    @on(Input.Changed)
    def update_table(self, event: Input.Changed) -> None:
        if event.input.id != "query":
            return

        query = event.value

        table = self.query_one(DataTable)
        table.clear()
        
        res = []
        if query.startswith('@'):
            try:
                id = int(query[1:])
                contact = self.contacts.search_by_id(id)
                if contact:
                    res.append(contact)
            except Exception as error:
                self.notify(str(error), severity='error')
                pass
        elif query.startswith('+'):
            phone = query[1:]
            res.extend(self.contacts.search_by_phone(phone))
        else:
            words = query.split(',')
            first_name = words[0]
            last_name = words[1] if len(words) > 1 else ''
            if len(first_name) > 0 or len(last_name) > 0: 
                res.extend(self.contacts.search_by_name(first_name, last_name))

        for contact in res:
            table.add_row(contact.id, contact.first_name, 
                          contact.last_name, contact.phones)

if __name__ == "__main__":
    app = PhonebookApp()
    app.run()
