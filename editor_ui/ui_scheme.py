import json


class ColorSheme:
    def __init__(self) -> None:
        super().__init__()
        self.file = "editor_ui/color_schemes.json"
        self.update_color_scheme()

    def update_color_scheme(self):
        self.color_scheme = {}
        with open(self.file, "r") as file:
            self.color_scheme = json.load(file)
        self.color_scheme = self.color_scheme[self.color_scheme["target"]]

    @property
    def ui_fon(self):
        return self.color_scheme["ui_fon"]

    @property
    def ui_widgets(self):
        return self.color_scheme["ui_widgets"]

    @property
    def ui_text(self):
        return self.color_scheme["ui_text"]

    @property
    def editor_fon(self):
        return self.color_scheme["editor_fon"]

    @property
    def editor_lines(self):
        return self.color_scheme["editor_lines"]

    @property
    def editor_target(self):
        return self.color_scheme["editor_target"]

    @property
    def editor_error(self):
        return self.color_scheme["editor_error"]

    @property
    def editor_text(self):
        return self.color_scheme["editor_text"]
