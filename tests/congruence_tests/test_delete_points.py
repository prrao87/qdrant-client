from qdrant_client.http.models import NamedVector
from tests.congruence_tests.test_common import (
    COLLECTION_NAME,
    compare_client_results,
    compare_collections,
    generate_fixtures,
)


def test_delete_points(local_client, remote_client):
    records = generate_fixtures(100)
    vector = records[0].vector["image"]

    local_client.upload_records(COLLECTION_NAME, records)
    remote_client.upload_records(COLLECTION_NAME, records)

    compare_client_results(
        local_client,
        remote_client,
        lambda c: c.search(COLLECTION_NAME, query_vector=NamedVector(name="image", vector=vector)),
    )

    found_ids = [
        scored_point.id
        for scored_point in local_client.search(
            COLLECTION_NAME, query_vector=NamedVector(name="image", vector=vector)
        )
    ]

    local_client.delete(COLLECTION_NAME, found_ids)
    remote_client.delete(COLLECTION_NAME, found_ids)

    compare_collections(local_client, remote_client, 100)

    compare_client_results(
        local_client,
        remote_client,
        lambda c: c.search(COLLECTION_NAME, query_vector=NamedVector(name="image", vector=vector)),
    )
