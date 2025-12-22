from .base_page import BasePage


class IndexPage(BasePage):
    path = "/"

    def go_to_index(self):
        if not self.is_in_current_page:
            self.goto_path(self.path)
        else:
            return
