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
            infos = read_from_csv(Path(selected_file.value))
            wrong = self.contacts.add_many(infos)
            self.notify(f"Wrong data: {wrong}", severity='error')
            self.app.pop_screen()
