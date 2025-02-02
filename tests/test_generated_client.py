import json

import pytest
from httpx import Response
from respx import MockRouter

from .test_client import client, config, http, schemas

BASE_URL = config.api_base_url()


@pytest.mark.respx(base_url=BASE_URL)
def test_simple_request_simple_request_get(respx_mock: MockRouter):
    # Given
    mocked_response = {"status": "hello world"}
    mock_path = "/simple-request"
    respx_mock.get(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    response = client.simple_request_simple_request_get()
    # Then
    assert isinstance(response, schemas.SimpleResponse)
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_simple_request_simple_request_get_raises_exception(respx_mock: MockRouter):
    # Given
    mocked_response = {"bad": "response"}
    mock_path = "/simple-request"
    respx_mock.get(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=404)
    )
    # Then
    with pytest.raises(http.APIException) as raised_exception:
        client.simple_request_simple_request_get()
    assert isinstance(raised_exception.value, http.APIException)
    # Make sure we have the response on the exception
    assert raised_exception.value.response.status_code == 404
    assert raised_exception.value.reason == "An unexpected status code was received"
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_optional_parameters_request_optional_parameters_get(respx_mock: MockRouter):
    # Given
    mocked_response = {"optional_parameter": None, "required_parameter": "Hello"}
    mock_path = "/optional-parameters"
    respx_mock.get(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    response = client.optional_parameters_request_optional_parameters_get()
    # Then
    assert isinstance(response, schemas.OptionalParametersResponse)
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_parameter_request_simple_request(respx_mock: MockRouter):
    # Given
    your_input = "hello world"
    mocked_response = {"your_input": your_input}
    mock_path = f"/simple-request/{your_input}"
    respx_mock.get(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    response = client.parameter_request_simple_request(your_input=your_input)
    # Then
    assert isinstance(response, schemas.ParameterResponse)
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_query_request_simple_query_get(respx_mock: MockRouter):
    # Given
    your_input = "hello world"
    mocked_response = {"your_query": your_input}
    mock_path = "/simple-query?your_input=hello+world"
    respx_mock.get(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    response = client.query_request_simple_query_get(your_input=your_input)
    # Then
    assert isinstance(response, schemas.SimpleQueryParametersResponse)
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_query_request_optional_query_get(respx_mock: MockRouter):
    # Given
    your_input = None
    mocked_response = {"your_query": "test"}
    # NOTE: omits None query parameter
    mock_path = "/optional-query"
    respx_mock.get(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    response = client.query_request_optional_query_get(your_input=your_input)
    # Then
    assert isinstance(response, schemas.OptionalQueryParametersResponse)
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_complex_model_request_complex_model_request_get(respx_mock: MockRouter):
    # Given
    mocked_response = {
        "a_dict_response": {"dict": "response"},
        "a_enum": "ONE",
        "a_list_of_enums": ["ONE", "TWO"],
        "a_list_of_numbers": [1, 2, 3],
        "a_list_of_other_models": [{"key": "first"}],
        "a_list_of_strings": ["hello", "world"],
        "a_number": 13,
        "a_string": "hello world",
        "another_model": {"key": "value"},
    }
    mock_path = "/complex-model-request"
    respx_mock.get(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    response = client.complex_model_request_complex_model_request_get()
    # Then
    assert isinstance(response, schemas.ComplexModelResponse)
    # Get around the enums
    json.loads(json.dumps(response.model_dump())) == mocked_response
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_request_data_request_data_post(respx_mock: MockRouter):
    # Given
    mocked_response = {"my_input": "test"}
    mock_path = "/request-data"
    respx_mock.post(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    data = schemas.RequestDataRequest(my_input="test")
    response = client.request_data_request_data_post(data=data)
    # Then
    assert isinstance(response, schemas.RequestDataResponse)
    assert response.model_dump() == mocked_response
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_request_data_request_data_put(respx_mock: MockRouter):
    # Given
    mocked_response = {"my_input": "test"}
    mock_path = "/request-data"
    respx_mock.put(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    data = schemas.RequestDataRequest(my_input="test")
    response = client.request_data_request_data_put(data=data)
    # Then
    assert isinstance(response, schemas.RequestDataResponse)
    assert response.model_dump() == mocked_response
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_request_data_path_request_data(respx_mock: MockRouter):
    # Given
    path_parameter = "param"
    mocked_response = {"my_input": "test", "path_parameter": path_parameter}
    mock_path = f"/request-data/{path_parameter}"
    respx_mock.post(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    data = schemas.RequestDataRequest(my_input="test")
    response = client.request_data_path_request_data(path_parameter, data=data)
    # Then
    assert isinstance(response, schemas.RequestDataAndParameterResponse)
    assert response.model_dump() == mocked_response
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_request_delete_request_delete_delete(respx_mock: MockRouter):
    # Given
    mocked_response = {}
    mock_path = "/request-delete"
    respx_mock.delete(mock_path).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    response = client.request_delete_request_delete_delete()
    # Then
    assert isinstance(response, schemas.DeleteResponse)
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path


@pytest.mark.respx(base_url=BASE_URL)
def test_header_request_header_request_get(respx_mock: MockRouter):
    # Given
    input_header = "foo"
    mocked_response = {"x_test": input_header}
    mock_path = "/header-request"
    respx_mock.get(mock_path, headers={"x-test": input_header}).mock(
        return_value=Response(json=mocked_response, status_code=200)
    )
    # When
    headers = schemas.HeaderRequestHeaderRequestGetHeaders(x_test=input_header)
    response = client.header_request_header_request_get(headers=headers)
    # Then
    assert isinstance(response, schemas.HeadersResponse)
    assert response.model_dump() == mocked_response
    assert len(respx_mock.calls) == 1
    call = respx_mock.calls[0]
    assert call.request.url == BASE_URL + mock_path
