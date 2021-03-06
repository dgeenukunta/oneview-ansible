#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from ansible.compat.tests import unittest
from oneview_module_loader import EnclosureFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Enclosure",
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test-Enclosure",
    options=['utilization', 'environmentalConfiguration', 'script']
)

PARAMS_GET_UTILIZATION_WITH_PARAMS = dict(
    config='config.json',
    name="Test-Enclosure",
    options=[dict(utilization=dict(fields='AveragePower',
                                   filter=['startDate=2016-06-30T03:29:42.000Z',
                                           'endDate=2016-07-01T03:29:42.000Z'],
                                   view='day',
                                   refresh=True))]
)

PRESENT_ENCLOSURES = [{
    "name": "Test-Enclosure",
    "uri": "/rest/enclosures/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]

ENCLOSURE_SCRIPT = '# script content'

ENCLOSURE_UTILIZATION = {
    "isFresh": "True"
}

ENCLOSURE_ENVIRONMENTAL_CONFIG = {
    "calibratedMaxPower": "2500"
}


class EnclosureFactsSpec(unittest.TestCase,
                         FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, EnclosureFactsModule)
        self.enclosures = self.mock_ov_client.enclosures
        FactsParamsTestCase.configure_client_mock(self, self.enclosures)

    def test_should_get_all_enclosures(self):
        self.enclosures.get_all.return_value = PRESENT_ENCLOSURES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        EnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosures=(PRESENT_ENCLOSURES))
        )

    def test_should_get_enclosure_by_name(self):
        self.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        EnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosures=(PRESENT_ENCLOSURES))

        )

    def test_should_get_enclosure_by_name_with_options(self):
        self.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        self.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        self.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        self.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        EnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosures=PRESENT_ENCLOSURES,
                               enclosure_script=ENCLOSURE_SCRIPT,
                               enclosure_environmental_configuration=ENCLOSURE_ENVIRONMENTAL_CONFIG,
                               enclosure_utilization=ENCLOSURE_UTILIZATION)

        )

    def test_should_get_all_utilization_data(self):
        self.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        self.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        self.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        self.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        EnclosureFactsModule().run()

        self.enclosures.get_utilization.assert_called_once_with(PRESENT_ENCLOSURES[0]['uri'], fields='', filter='',
                                                                view='', refresh='')

    def test_should_get_utilization_with_parameters(self):
        self.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        self.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        self.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        self.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        self.mock_ansible_module.params = PARAMS_GET_UTILIZATION_WITH_PARAMS

        EnclosureFactsModule().run()

        date_filter = ["startDate=2016-06-30T03:29:42.000Z", "endDate=2016-07-01T03:29:42.000Z"]

        self.enclosures.get_utilization.assert_called_once_with(
            PRESENT_ENCLOSURES[0]['uri'], fields='AveragePower', filter=date_filter, view='day', refresh=True)


if __name__ == '__main__':
    unittest.main()
