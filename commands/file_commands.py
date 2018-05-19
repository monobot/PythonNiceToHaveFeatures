import os
import sublime
import sublime_plugin


class _FileBaseClass(sublime_plugin.TextCommand):

    def get_minimal_path(self):
        minimal_path = min(
            (
                os.path.relpath(self.view.file_name(), folder)
                for folder in self.view.window().folders()
            ),
            key=len,
        )
        return '.'.join(minimal_path.split('.')[:-1])


class CopyRelativePathCommand(_FileBaseClass):

    def run(self, edit):
        minimal_path = self.get_minimal_path()
        sublime.set_clipboard(minimal_path)


class CopyPackageRelativePathCommand(_FileBaseClass):

    def run(self, edit):
        trim_file_extension = self.get_minimal_path()
        sublime.set_clipboard(trim_file_extension.replace('/', '.'))


class CopyReferenceCommand(_FileBaseClass):

    def is_enabled(self):
        return len(self.view.sel()) == 1

    def run(self, edit):
        minimal_path = self.get_minimal_path()
        reference = self.view.sel()[0]
        if reference.begin() == reference.end():
            reference = self.view.word(reference)

        minimal_path += '.' + self.view.substr(reference)
        sublime.set_clipboard(minimal_path.replace('/', '.'))


class CopyFilenameCommand(_FileBaseClass):

    def run(self, edit):
        trim_file_extension = self.get_minimal_path()
        sublime.set_clipboard(trim_file_extension.replace('/', '.'))


class CreatePackageDirectoryCommand(_FileBaseClass):

    def run(self, edit):
        def on_done(input_string):
            if input_string:
                target_dir = os.path.join(
                    os.path.dirname(self.view.file_name()),
                    input_string
                )
                os.makedirs(target_dir)

                init_filename = os.path.join(target_dir, '__init__.py')
                os.open(init_filename, os.O_CREAT).close()
            else:
                on_cancel()

        def on_change(input_string):
            if input_string:
                print('Creating sub-package "%s"' % input_string)

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
