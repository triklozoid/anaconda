# -*- encoding: utf8 -*-

# Copyright (C) 2012-2016 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import sys
sys.path.insert(0, '../anaconda_server')
sys.path.append('../anaconda_lib')

import jedi

src = 'def test_src():\n\t"""Test String\n\t"""\n\ntest_src('
src_escape = 'def test_src():\n\t"""<strong>&nbsp;Espa&nacute;a currency €</strong>"""\n\ntest_src('  # noqa


class TestDoc(object):
    """Doc test suite
    """

    def test_doc_command(self):

        from commands.doc import Doc

        cmd = Doc(self._check_html, 0, jedi.Script(src), True)
        cmd.run()

        cmd = Doc(self._check_plain, 0, jedi.Script(src), False)
        cmd.run()

        cmd = Doc(self._check_html_escape, 0, jedi.Script(src_escape), True)
        cmd.run()

        cmd = Doc(self._check_no_definition, 0, jedi.Script('nothing'), False)
        cmd.run()

    def test_doc_handler(self):

        from handlers.jedi_handler import JediHandler

        data = {'source': src, 'line': 5, 'offset': 9, 'html': True}
        handler = JediHandler('doc', data, 0, 0, self._check_handler)
        handler.run()

    def _check_html(self, kwrgs):

        self._common_assertions(kwrgs)
        assert kwrgs['doc'].strip() == (
            "test_src\ntest_src()<br><br>Test String<br>"
        )

    def _check_plain(self, kwrgs):

        self._common_assertions(kwrgs)
        assert kwrgs['doc'].strip() == "Docstring for {0}\n{1}\n{2}".format(
            'test_src',
            '=' * 40,
            'test_src()\n\nTest String'
        )

    def _check_html_escape(self, kwrgs):

        self._common_assertions(kwrgs)
        assert kwrgs['doc'].strip() == 'test_src\ntest_src()<br><br>&lt;strong&gt;\xa0Espańa currency €&lt;/strong&gt;'  # noqa

    def _check_no_definition(self, kwrgs):

        assert kwrgs['success'] is False
        assert kwrgs['uid'] == 0
        assert kwrgs['doc'] == ''

    def _check_handler(self, kwrgs):

        self._check_html(kwrgs)

    def _common_assertions(self, kwrgs):

        assert kwrgs['success'] is True
        assert kwrgs['uid'] == 0