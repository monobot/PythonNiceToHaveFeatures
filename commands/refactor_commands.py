from string import ascii_uppercase

import sublime_plugin

from .base_class import CommandBaseClass


class _RegionBaseClass(sublime_plugin.TextCommand, CommandBaseClass):

    def is_enabled(self):
        return self._selection()

    def run(self, edit):
        for sel in self.view.sel():
            current_text = self.view.substr(sel)
            already_changed = []
            while self.view.find(current_text, 0):
                sub_sel = self.view.find(current_text, 0)
                if sub_sel not in already_changed:
                    already_changed.append(sub_sel)
                else:
                    break
                self.view.replace(
                    edit,
                    sub_sel,
                    text=self.converter(current_text)
                )


class RefactorCamelcaseCommand(_RegionBaseClass):

    def converter(self, txt):
        response_txt = txt.lstrip().lstrip('_')
        if response_txt:
            normalized_txt = self._normalize_text(txt)

            response_txt = ''
            cap_next = False
            for char in normalized_txt:
                if cap_next:
                    char = char.capitalize()
                    cap_next = False

                if char != '|':
                    response_txt += char
                else:
                    cap_next = True

        return response_txt


class RefactorClassCaseCommand(_RegionBaseClass):

    def converter(self, txt):
        response_txt = txt.lstrip().lstrip('_')
        if response_txt:
            normalized_txt = self._normalize_text(txt)

            response_txt = ''
            cap_next = True
            for char in normalized_txt:
                if cap_next:
                    char = char.capitalize()
                    cap_next = False

                if char != '|':
                    response_txt += char
                else:
                    cap_next = True

        return response_txt


class RefactorUnderscoreCommand(_RegionBaseClass):

    def converter(self, txt):
        response_txt = txt.lstrip()
        if txt:
            response_txt = txt[0].lower()
            for char in txt[1:]:
                if char in ascii_uppercase:
                    char = '_' + char.lower()
                response_txt += char

        return response_txt
        return txt[::-1]


class RefactorCapfirstCommand(_RegionBaseClass):

    def converter(self, txt):
        if txt:
            txt = txt[0].capitalize() + txt[1:]
        return txt
