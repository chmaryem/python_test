import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from logic import process_data


class TestProcessData:

    @pytest.fixture
    def mock_execute_query(self):
        with patch('logic.execute_query') as mock:
            yield mock

    @pytest.fixture
    def mock_connection(self):
        return Mock()

    @pytest.fixture
    def mock_result(self):
        result = Mock()
        result.fetchall.return_value = [('value1', 'value2'), ('value3', 'value4')]
        result.description = [('col1',), ('col2',)]
        return result

    def test_process_data_with_valid_result_returns_dataframe(self, mock_execute_query, mock_connection, mock_result):
        mock_execute_query.return_value = mock_result
        df = process_data(mock_connection, "SELECT * FROM table")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ['col1', 'col2']

    def test_process_data_with_none_result_returns_empty_dataframe(self, mock_execute_query, mock_connection):
        mock_execute_query.return_value = None
        df = process_data(mock_connection, "SELECT * FROM table")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_process_data_calls_execute_query_with_correct_parameters(self, mock_execute_query, mock_connection, mock_result):
        mock_execute_query.return_value = mock_result
        process_data(mock_connection, "SELECT * FROM users WHERE id = 1")
        mock_execute_query.assert_called_once_with(mock_connection, "SELECT * FROM users WHERE id = 1")

    def test_process_data_with_empty_query_string(self, mock_execute_query, mock_connection, mock_result):
        mock_execute_query.return_value = mock_result
        df = process_data(mock_connection, "")
        mock_execute_query.assert_called_once_with(mock_connection, "")

    def test_process_data_with_none_query_string(self, mock_execute_query, mock_connection, mock_result):
        mock_execute_query.return_value = mock_result
        df = process_data(mock_connection, None)
        mock_execute_query.assert_called_once_with(mock_connection, None)

    def test_process_data_with_exception_in_execute_query(self, mock_execute_query, mock_connection):
        mock_execute_query.side_effect = Exception("Database error")
        with pytest.raises(Exception, match="Database error"):
            process_data(mock_connection, "SELECT * FROM table")

    def test_process_data_with_single_row_result(self, mock_execute_query, mock_connection):
        mock_result = Mock()
        mock_result.fetchall.return_value = [('single_value',)]
        mock_result.description = [('column_one',)]
        mock_execute_query.return_value = mock_result
        df = process_data(mock_connection, "SELECT * FROM table LIMIT 1")
        assert len(df) == 1
        assert df.iloc[0]['column_one'] == 'single_value'

    def test_process_data_with_multiple_columns(self, mock_execute_query, mock_connection):
        mock_result = Mock()
        mock_result.fetchall.return_value = [('a', 'b', 'c', 'd')]
        mock_result.description = [('col1',), ('col2',), ('col3',), ('col4',)]
        mock_execute_query.return_value = mock_result
        df = process_data(mock_connection, "SELECT col1, col2, col3, col4 FROM table")
        assert list(df.columns) == ['col1', 'col2', 'col3', 'col4']
        assert df.iloc[0]['col3'] == 'c'

    def test_process_data_with_special_characters_in_query(self, mock_execute_query, mock_connection, mock_result):
        mock_execute_query.return_value = mock_result
        query = "SELECT * FROM table WHERE name = 'O'Brien'"
        df = process_data(mock_connection, query)
        mock_execute_query.assert_called_once_with(mock_connection, query)

    def test_process_data_with_none_connection(self, mock_execute_query, mock_result):
        mock_execute_query.return_value = mock_result
        df = process_data(None, "SELECT * FROM table")
        mock_execute_query.assert_called_once_with(None, "SELECT * FROM table")