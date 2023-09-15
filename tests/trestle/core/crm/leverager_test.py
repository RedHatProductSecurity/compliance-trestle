# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2020 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import pathlib
from unittest.mock import patch

import pytest

import trestle.oscal.ssp as ossp
import trestle.oscal.common as common
import trestle.core.generators as gens
from trestle.common.model_utils import ModelUtils

from trestle.core.crm.leverager import Leverager, get_system_component  # Replace 'your_module' with the actual module name

logger = logging.getLogger(__name__)

@pytest.fixture
def sample_leveraging_ssp():
    return gens.generate_sample_model(ossp.SystemSecurityPlan)

@pytest.fixture
def sample_leveraged_components():
    return [gens.generate_sample_model(ossp.SystemComponent) for _ in range(3)]

@pytest.fixture
def sample_trestle_root():
    return pathlib.Path("/sample/trestle/root")
'''
def test_get_system_component(sample_trestle_root):
    with patch('trestle.common.model_utils.ModelUtils.load_model_for_class') as mock_load_model:
        mock_load_model.return_value = (gens.generate_sample_model(ossp.SystemSecurityPlan), None)
        result = get_system_component(sample_trestle_root, "sample_leveraged_ssp")
        assert isinstance(result, ossp.SystemComponent)
'''

def test_leverager_init(sample_leveraging_ssp, sample_leveraged_components, sample_trestle_root):
    leverager = Leverager(sample_leveraging_ssp, sample_leveraged_components, "sample_leveraged_ssp", sample_trestle_root)
    assert isinstance(leverager, Leverager)

def test_create_leveraged_authz(sample_leveraging_ssp, sample_leveraged_components, sample_trestle_root):
    leverager = Leverager(sample_leveraging_ssp, sample_leveraged_components, "sample_leveraged_ssp", sample_trestle_root)
    result = leverager._create_leveraged_authz("sample_leveraged_ssp", sample_trestle_root)
    assert isinstance(result, ossp.LeveragedAuthorization)

def test_create_leveraging_components(sample_leveraging_ssp, sample_leveraged_components, sample_trestle_root):
    leverager = Leverager(sample_leveraging_ssp, sample_leveraged_components, "sample_leveraged_ssp", sample_trestle_root)
    result = leverager._create_leveraging_components()
    assert isinstance(result, list)
    assert all(isinstance(comp, ossp.SystemComponent) for comp in result)

def test_add_leveraged_info(sample_leveraging_ssp, sample_leveraged_components, sample_trestle_root):
    leverager = Leverager(sample_leveraging_ssp, sample_leveraged_components, "sample_leveraged_ssp", sample_trestle_root)
    result = leverager.add_leveraged_info()
    assert isinstance(result, ossp.SystemSecurityPlan)
