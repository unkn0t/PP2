
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
