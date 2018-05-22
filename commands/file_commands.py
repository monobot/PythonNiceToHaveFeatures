import os
import sublime
import sublime_plugin

from .base_class import CommandBaseClass


class CopyRelativePathCommand(sublime_plugin.TextCommand, CommandBaseClass):

    def run(self, edit):
        minimal_path = self._get_minimal_path()
        sublime.set_clipboard(minimal_path)


class CopyPackageRelativePathCommand(
        sublime_plugin.TextCommand, CommandBaseClass):

    def run(self, edit):
        minimal_path = self._get_minimal_path()
        dotted_path = '.'.join(minimal_path.split('.')[:-1])
        sublime.set_clipboard('.'.join(dotted_path.split(os.sep)))


class CopyReferenceCommand(sublime_plugin.TextCommand, CommandBaseClass):

    def is_enabled(self):
        return self._one_word_selected()

    def run(self, edit):
        minimal_path = self._get_minimal_path()
        reference = self.view.sel()[0]
        if reference.begin() == reference.end():
            reference = self.view.word(reference)

        strip_extension = '.'.join(minimal_path.split('.')[:-1])
        strip_extension += '.' + self.view.substr(reference)
        dotted_path = strip_extension.replace(os.sep, '.')
        sublime.set_clipboard(dotted_path)


class CopyFilenameCommand(sublime_plugin.TextCommand, CommandBaseClass):

    def run(self, edit):
        minimal_path = self._get_minimal_path()
        sublime.set_clipboard(minimal_path.split(os.sep)[1])


class CreatePackageDirectoryCommand(
        sublime_plugin.TextCommand, CommandBaseClass):

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
