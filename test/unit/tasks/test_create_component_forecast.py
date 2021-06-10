from unittest import TestCase
from unittest.mock import MagicMock, patch

from openstf.tasks.create_components_forecast import create_components_forecast_task

from test.utils import TestData

FORECAST_MOCK = "forecast_mock"


class TestCreateComponentForecastTask(TestCase):
    def setUp(self) -> None:
        self.pj = TestData.get_prediction_job(pid=307)

    @patch(
        "openstf.tasks.create_components_forecast.create_components_forecast_pipeline",
        MagicMock(return_value=FORECAST_MOCK),
    )
    def test_create_basecase_forecast_task_happy_flow(self):
        # Test happy flow of create forecast task
        context = MagicMock()
        context.database.get_predicted_load.return_value = [1, 0]
        context.database.get_energy_split_coefs.return_value = [1, 0]

        create_components_forecast_task(self.pj, context)
        self.assertEqual(context.mock_calls[3].args[0], FORECAST_MOCK)

    @patch(
        "openstf.tasks.create_components_forecast.create_components_forecast_pipeline"
    )
    def test_create_basecase_forecast_task_no_input(self, pipeline_mock):
        # Test pipeline is not called when no input data is available
        context = MagicMock()
        context.database.get_predicted_load.return_value = []
        context.database.get_energy_split_coefs.return_value = [1, 0]
        pipeline_mock.return_value = FORECAST_MOCK
        create_components_forecast_task(self.pj, context)
        self.assertEqual(pipeline_mock.call_count, 0)

    @patch(
        "openstf.tasks.create_components_forecast.create_components_forecast_pipeline"
    )
    def test_create_basecase_forecast_task_no_coefs(self, pipeline_mock):
        # Test pipeline is not called when no coeficients are available
        context = MagicMock()
        context.database.get_predicted_load.return_value = [1, 0]
        context.database.get_energy_split_coefs.return_value = []
        pipeline_mock.return_value = FORECAST_MOCK
        create_components_forecast_task(self.pj, context)
        self.assertEqual(pipeline_mock.call_count, 0)

    @patch(
        "openstf.tasks.create_components_forecast.create_components_forecast_pipeline"
    )
    def test_create_basecase_forecast_task_no_train_components(self, pipeline_mock):
        # Test pipeline is not called when no coeficients are available
        context = MagicMock()
        context.database.get_predicted_load.return_value = [1, 0]
        context.database.get_energy_split_coefs.return_value = [1.0]
        pipeline_mock.return_value = FORECAST_MOCK
        self.pj["train_components"] = 0
        create_components_forecast_task(self.pj, context)
        self.assertEqual(pipeline_mock.call_count, 0)
