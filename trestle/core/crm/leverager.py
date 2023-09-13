# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2020 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Reference authorizations and components from a leveraged SSP in a leveraging SSP."""



import logging
import pathlib

import trestle.oscal.ssp as ossp
import trestle.core.generators as gens
import trestle.common.const as const
from trestle.common.model_utils import ModelUtils

logger = logging.getLogger(__name__)

class Leverager:
    
    def __init__(self, ssp: ossp.SystemSecurityPlan, leveraged_ssp: str, trestle_root: pathlib.Path) -> None:
        """Initialize the Leverager class."""
        logger.debug("Initializing Leverager.")
        self._ssp = ssp
        self._leveraged_authz = {}
        self._leveraged_authz = self._get_system_component(trestle_root, leveraged_ssp)
            

    def _get_system_component(self, trestle_root: pathlib.Path, leveraged_ssp: str) -> ossp.SystemComponent:
        """Get the system component from the leveraged SSP."""
        logger.debug(f"Fetching system component from {leveraged_ssp}.")
        leveraged = {}

        try:
            leveraged, _ = ModelUtils.load_model_for_class(trestle_root, leveraged_ssp, ossp.SystemSecurityPlan)  # type: ignore
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return {}

        if leveraged.system_implementation.components[0].type != const.THIS_SYSTEM_AS_KEY:
            logger.error(f'Expected {const.THIS_SYSTEM_AS_KEY} as the first component in the leveraged SSP. No leveraged information found')
            return {}
        else:
            logger.debug("Successfully fetched system component.")
            return leveraged.system_implementation.components[0]

    def _create_leveraged_authz(self):
        """Create leveraged authorizations."""
        logger.debug("Creating leveraged authorizations.")
        # TODO: Implement this method
        pass

    def _add_props(self):
        """Add properties to the leveraged authorizations."""
        logger.debug("Adding properties to leveraged authorizations.")
        # TODO: Implement this method
        pass

    def add_leveraged_info(self):
        """Add leveraged information to the SSP."""
        logger.debug("Adding leveraged information.")
        # TODO: Implement this method
        pass