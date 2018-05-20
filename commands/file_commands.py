import os
import sublime

from .base_class import CommandBaseClass


class CopyRelativePathCommand(CommandBaseClass):

    def run(self, edit):
        minimal_path = self._get_minimal_path()
        sublime.set_clipboard(minimal_path)


class CopyPackageRelativePathCommand(CommandBaseClass):

    def run(self, edit):
        trim_file_extension = self._get_minimal_path()
        sublime.set_clipboard(trim_file_extension.replace('/', '.'))


class CopyReferenceCommand(CommandBaseClass):

    def is_enabled(self):
        return self._one_word_selected()

    def run(self, edit):
        minimal_path = self._get_minimal_path()
        reference = self.view.sel()[0]
        if reference.begin() == reference.end():
            reference = self.view.word(reference)

        minimal_path += '.' + self.view.substr(reference)
        sublime.set_clipboard(minimal_path.replace('/', '.'))


class CopyFilenameCommand(CommandBaseClass):

    def run(self, edit):
        trim_file_extension = self._get_minimal_path()
        sublime.set_clipboard(trim_file_extension.replace('/', '.'))


class CreatePackageDirectoryCommand(CommandBaseClass):

    def run(self, edit):
        def on_done(input_string):
            if input_string:
                target_dir = os.path.join(
                    os.path.dirname(self.view.file_name()),
                    input_string
                )
                os.makedirs(target_dir)

                init_filename = os.path.join(target_dir, '__init__.py')
                os.open(init_filename, os.O_CREAT)
            else:
                on_cancel()

        def on_change(input_string):
            pass

        def on_cancel():
            print('User cancelled the input')

        window = self.view.window()
        window.show_input_panel(
            'SubPackage name:',
            '',
            on_done,
            on_change,
            on_cancel
        )
