from http import HTTPStatus

from tests.conftest import NovelistFactory


def test_create_novelist(client, token):
    response = client.post(
        '/romancista/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Test Novelist',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'test novelist',
    }


def test_create_duplicate_novelist(client, novelist, token):
    response = client.post(
        '/romancista/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': novelist.name,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_delete_novelist(client, novelist, token):
    response = client.delete(
        f'/romancista/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado no MADR'}


def test_delete_novelist_error(client, token):
    response = client.delete(
        f'/romancista/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_patch_novelist(client, novelist, token):
    response = client.patch(
        f'/romancista/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test!'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'Test!'


def test_patch_novelist_error(client, novelist, token):
    response = client.patch(
        f'/romancista/{10}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test!'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_get_novelist_by_id(client, novelist):
    response = client.get(
        f'/romancista/{novelist.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'name': 'Name Test 4'}


def test_get_novelist_by_params(client, session):
    expected_novelists = 2

    session.bulk_save_objects(
        NovelistFactory.create_batch(1, name='Test Name 1')
    )

    session.bulk_save_objects(
        NovelistFactory.create_batch(1, name='Test Name 2')
    )
    session.commit()

    response = client.get(
        '/romancista/?name=Test',
    )

    assert len(response.json()['romancistas']) == expected_novelists


def test_get_novelist_by_id_error(client):
    response = client.get(f'/romancista/{9999}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}
