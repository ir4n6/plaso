#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 The Plaso Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This file contains a unit test for the xchatscrollback parser in plaso."""

import os
import pytz
import unittest

# pylint: disable-msg=unused-import
from plaso.formatters import xchatscrollback as xchatscrollback_formatter
from plaso.lib import eventdata
from plaso.lib import preprocess
from plaso.parsers import xchatscrollback as xchatscrollback_parser
from plaso.parsers import test_lib


__author__ = 'Francesco Picasso (francesco.picasso@gmail.com)'


class XChatScrollbackUnitTest(unittest.TestCase):
  """A unit test for the XChatScrollback Parser."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    pre_obj = preprocess.PlasoPreprocess()
    pre_obj.zone = pytz.timezone('UTC')
    self._parser = xchatscrollback_parser.XChatScrollbackParser(pre_obj, None)

  def testParse(self):
    """Tests the Parse function."""
    test_file = os.path.join('test_data', 'xchatscrollback.log')

    events = test_lib.ParseFile(self._parser, test_file)

    self.assertEquals(len(events), 10)

    self.assertEquals(events[0].timestamp, 1232074579000000)
    self.assertEquals(events[1].timestamp, 1232074587000000)
    self.assertEquals(events[2].timestamp, 1232315916000000)
    self.assertEquals(events[3].timestamp, 1232315916000000)
    self.assertEquals(events[4].timestamp, 1232959856000000)
    self.assertEquals(events[5].timestamp, 0)
    self.assertEquals(events[7].timestamp, 1232959862000000)
    self.assertEquals(events[8].timestamp, 1232959932000000)
    self.assertEquals(events[9].timestamp, 1232959993000000)

    self._TestText(events[0], u'[] * Speaking now on ##plaso##')
    self._TestText(events[1], u'[] * Joachim \xe8 uscito (Client exited)')
    self._TestText(events[2], u'[] Tcl interface unloaded')
    self._TestText(events[3], u'[] Python interface unloaded')
    self._TestText(events[6], u'[] * Topic of #plasify \xe8: .')
    self._TestText(events[8], u'[nickname: fpi] Hi Kristinn!')
    self._TestText(events[9],
      u'[nickname: Kristinn] GO AND WRITE PARSERS!!! O_o')

  def _TestText(self, evt, text):
    msg, _ = eventdata.EventFormatterManager.GetMessageStrings(evt)
    self.assertEquals(msg, text)


if __name__ == '__main__':
  unittest.main()
