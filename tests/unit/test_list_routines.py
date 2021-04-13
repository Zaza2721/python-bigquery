from .helpers import make_connection, dataset_polymorphic
import pytest


def test_list_routines_empty_w_timeout(client):
    conn = client._connection = make_connection({})

    iterator = client.list_routines("test-routines.test_routines", timeout=7.5)
    page = next(iterator.pages)
    routines = list(page)
    token = iterator.next_page_token

    assert routines == []
    assert token is None
    conn.api_request.assert_called_once_with(
        method="GET",
        path="/projects/test-routines/datasets/test_routines/routines",
        query_params={},
        timeout=7.5,
    )


@dataset_polymorphic
def test_list_routines_defaults(make_dataset, get_reference, client, PROJECT):
    from google.cloud.bigquery.routine import Routine

    project_id = PROJECT
    dataset_id = "test_routines"
    path = f"/projects/{PROJECT}/datasets/test_routines/routines"
    routine_1 = "routine_one"
    routine_2 = "routine_two"
    token = "TOKEN"
    resource = {
        "nextPageToken": token,
        "routines": [
            {
                "routineReference": {
                    "routineId": routine_1,
                    "datasetId": dataset_id,
                    "projectId": project_id,
                }
            },
            {
                "routineReference": {
                    "routineId": routine_2,
                    "datasetId": dataset_id,
                    "projectId": project_id,
                }
            },
        ],
    }

    conn = client._connection = make_connection(resource)
    dataset = make_dataset(client.project, dataset_id)

    iterator = client.list_routines(dataset)
    assert iterator.dataset == get_reference(dataset)
    page = next(iterator.pages)
    routines = list(page)
    actual_token = iterator.next_page_token

    assert len(routines) == len(resource["routines"])
    for found, expected in zip(routines, resource["routines"]):
        assert isinstance(found, Routine)
        assert found.routine_id == expected["routineReference"]["routineId"]
    assert actual_token == token

    conn.api_request.assert_called_once_with(
        method="GET", path=path, query_params={}, timeout=None
    )


def test_list_routines_wrong_type(client):
    with pytest.raises(TypeError):
        client.list_routines(42)