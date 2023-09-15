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
from typing import List

import trestle.oscal.ssp as ossp
import trestle.oscal.common as common

import trestle.core.generators as gens
import trestle.common.const as const
from trestle.common.model_utils import ModelUtils

logger = logging.getLogger(__name__)

def get_system_component(trestle_root: pathlib.Path, leveraged_ssp: str) -> ossp.SystemComponent:
    """Get the leveraged system components from the leveraged SSP."""
    logger.debug(f"Fetching system component from {leveraged_ssp}.")
    leveraged = {}

    try:
        leveraged, _ = ModelUtils.load_model_for_class(trestle_root, leveraged_ssp, ossp.SystemSecurityPlan)  # type: ignore
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return {} # type: ignore

    if leveraged.system_implementation.components[0].type != const.THIS_SYSTEM_AS_KEY:
        logger.error(f'Expected {const.THIS_SYSTEM_AS_KEY} as the first component in the leveraged SSP. No leveraged information found')
        return {} # type: ignore
    else:
        logger.debug("Successfully fetched system component.")
        return leveraged.system_implementation.components[0]


class Leverager:
    
    def __init__(self, leveraging_ssp: ossp.SystemSecurityPlan, leveraged_components: List[ossp.SystemComponent], leveraged_ssp: str, trestle_root: pathlib.Path) -> None:
        """Initialize the Leverager class."""
        logger.debug("Initializing Leverager.")
        self._leveraging_ssp:  ossp.SystemSecurityPlan = leveraging_ssp
        self._leveraged_components: List[ossp.SystemComponent] = leveraged_components
        self._leveraged_authz: ossp.LeveragedAuthorization = self._create_leveraged_authz(leveraged_ssp, trestle_root)
        self._leveraging_components: List[ossp.SystemComponent] = self._create_leveraging_components()


    def _create_leveraged_authz(self, leveraged_ssp: str, trestle_root: pathlib.Path) -> ossp.LeveragedAuthorization:
        """Create leveraged authorizations."""
        logger.debug("Creating leveraged authorizations.")
        leveraged_authz = gens.generate_sample_model(ossp.LeveragedAuthorization)
        # Insert the relative leveraged ssp path as a link
        leveraged_authz.links = []

        href: pathlib.Path = ModelUtils.get_model_path_for_name_and_class(trestle_root, leveraged_ssp, ossp.SystemSecurityPlan) # type: ignore
        if href is None:
            logger.error("Failed to get model path.")
            return leveraged_authz# Handle the error appropriately, perhaps by raising an exception or returning
        else:
            link: common.Link = common.Link(href=href) # type: ignore
            leveraged_authz.links.append(link) # type: ignore
            return leveraged_authz

    def _create_leveraging_components(self) -> List[ossp.SystemComponent]:
        """Create leveraging components."""
        self._leveraging_components = []
        # For each leveraged component, create a leveraging component
        logger.debug("Creating leveraging components.")
        for comp in self._leveraged_components:
            
            leveraging_comp = gens.generate_sample_model(ossp.SystemComponent)
            leveraging_comp.type = comp.type
            leveraging_comp.title = comp.title
            leveraging_comp.description = comp.description
            leveraging_comp.status = comp.status

            leveraging_comp.props = []
            leveraging_comp.props.append(common.Property(name="implementation-point", value="external")) # type: ignore
            leveraging_comp.props.append(common.Property(name="leveraged-authorization-uuid", value=self._leveraged_authz.uuid)) # type: ignore
            leveraging_comp.props.append(common.Property(name="inherited-uuid", value=comp.uuid)) # type: ignore
            # Add the leveraging component to the leveraging components list
            self._leveraging_components.append(leveraging_comp)

        return self._leveraging_components
        


    def add_leveraged_info(self) -> ossp.SystemSecurityPlan:
        """Add leveraged information to the SSP."""
        logger.debug("Adding leveraged information.")
        # Add the leveraged authorization to the leveraging SSP
        self._leveraging_ssp.system_implementation.leveraged_authorizations = []
        self._leveraging_ssp.system_implementation.leveraged_authorizations.append(self._leveraged_authz)
        # Add the leveraging components to the leveraging SSP
        self._leveraging_ssp.system_implementation.components = []
        self._leveraging_ssp.system_implementation.components = self._leveraging_components

        return self._leveraging_ssp

