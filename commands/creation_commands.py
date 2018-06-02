import sublime_plugin

from .base_class import CommandBaseClass


class CreateBaseCommand(sublime_plugin.TextCommand, CommandBaseClass):
    indt = 0
    steps = -3
    snippet_path = (
        'Packages/PythonNiceToHaveFeatures/snippets/{}.sublime-snippet')

    def _snippet(self):
        return self.snippet_path.format(self.snippet)

    def is_enabled(self):
        return self._is_python() and self._one_word_selected()

    def _insert(self, symbol, position):
        content = self.text_type.format(
            base_indentation='' if not self.indt else '    ' * self.indt,
            symbol=symbol,
        )
        self._reset_position(position, 0)
        self.view.settings().set('auto_indent', False)
        self.view.run_command('insert', {'characters': content})
        self.view.run_command('insert_snippet', args={'name': self._snippet()})
        self.view.settings().set('auto_indent', True)

    def run(self, edit):
        original_position = self.view.sel()[0]
        symbol = self.view.substr(
            self.view.word(original_position.begin())
        )

        target_position = self._get_target_position()

        self._insert(symbol, target_position)


class CreateFunctionCommand(CreateBaseCommand):
    text_type = '{base_indentation}def  {symbol}'
    method_text = '{base_indentation}def  {symbol}'
    snippet = 'nth_function'
    blank_lines = 2

    def _get_target_position(self):
        symbols = sorted(
            filter(
                lambda x: x >= 0,
                [
                    self.view.find('^class ', 0).begin(),
                    self.view.find('^def ', 0).begin(),
                    self.view.find('^for ', 0).begin(),
                    self.view.find('^while ', 0).begin()
                ]
            )
        )

        return symbols[0] if symbols else 0


class CreateClassCommand(CreateBaseCommand):
    text_type = 'class {symbol}'
    snippet = 'nth_class'
    blank_lines = 2

    def _get_target_position(self):
        symbols = ['^def ', '^class ', '^for ', '^while ']
        symbols = filter(
            lambda x: x >= 0,
            [self.view.find(st, 0).begin() for st in symbols]
        )
        symbols = sorted(symbols)

        return symbols[0] if symbols else 0


class CreateMethodCommand(CreateBaseCommand):
    text_type = 'def  {symbol}'
    snippet = 'nth_method'
    indt = 1
    steps = -2
    blank_lines = 1

    def _startswith_def(self, temp_pos):
        return self.view.substr(temp_pos).startswith('    def')

    def _get_target_position(self):
        symbols = self.view.find_all('^class ')
        symbols = filter(
            lambda x: x < self.view.sel()[0].begin(),
            [self.view.line(pos).end() for pos in symbols]
        )
        symbols = sorted(symbols, reverse=True)

        if symbols:
            temp_pos = self.view.line(symbols[0] + 1)

            counter = 0
            while not self._startswith_def(temp_pos) and counter < 1000:
                temp_pos = self.view.line(temp_pos.end() + 1)

            return temp_pos.begin() + 4
        return 0
