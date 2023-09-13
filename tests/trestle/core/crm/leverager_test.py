import pathlib
from unittest.mock import patch, Mock
from trestle.common.model_utils import ModelUtils
import trestle.oscal.ssp as ossp
from trestle.core.crm.leverager import Leverager
import trestle.common.const as const
import tests.test_utils as testutils


def test_get_system_component(tmp_trestle_dir: pathlib.Path) -> None:
    """Test the _get_system_component method for successful retrieval."""
    leveraging_ssp, _ = ModelUtils.load_model_for_class(testutils.JSON_TEST_DATA_PATH, "leveraging_ssp", ossp.SystemSecurityPlan, 1)
    leverager = Leverager(leveraging_ssp, "leveraged_ssp", tmp_trestle_dir)

    # Call _get_system_component
    result = leverager._get_system_component(tmp_trestle_dir, "leveraged_ssp")

    # Validate the result
    assert result is not None
    assert result.type == 'this-system'

'''
def test_get_system_component_fail(tmp_trestle_dir: pathlib.Path) -> None:
    """Test the _get_system_component method for failure scenario."""
    # Mocking the return value of load_model_for_class
    mock_ssp = Mock()
    mock_ssp.system_implementation.components = [Mock(type='not-this-system')]

    with patch('trestle.common.model_utils.ModelUtils.load_model_for_class') as mock_load_model:
        mock_load_model.return_value = (mock_ssp, None)

        # Initialize Leverager
        ssp = ossp.SystemSecurityPlan()
        leveraged_ssp = 'sample_leveraged_ssp'
        trestle_root = tmp_trestle_dir
        leverager = Leverager(ssp, leveraged_ssp, trestle_root)

        # Call _get_system_component
        result = leverager._get_system_component(trestle_root, leveraged_ssp)

        # Validate the result
        assert result == {}
        '''