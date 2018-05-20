import os


class CommandBaseClass:
    # selection methods

    def _reset_position(self, position, offset):
        self.view.sel().clear()
        self.view.sel().add(position + offset)

    def _one_word_selected(self):
        selection = self.view.sel()
        one_word = self.view.word(selection[0].begin()) == selection[0]
        return len(selection) == 1 and one_word

    def _selection(self):
        return bool(self.view.sel())

    # helper methods
    @staticmethod
    def _normalize_text(txt):
        return txt.replace('_', '|').replace('-', '|').replace(' ', '|')

    def _get_minimal_path(self):
        minimal_path = min(
            (
                os.path.relpath(self.view.file_name(), folder)
                for folder in self.view.window().folders()
            ),
            key=len,
        )
        return '.'.join(minimal_path.split('.')[:-1])
