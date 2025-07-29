import requests
from datetime import date, timedelta
from fastapi import status

base_url = "http://localhost:8000/"


def test_get_currency_future_date():
    future_date = date.today() + timedelta(days=1)
    future_date_str = future_date.strftime("%d/%m/%Y")
    response = requests.get(
        f"{base_url}scripts/XML_daily.asp?date_req={future_date_str}"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "выходит за пределы доступного диапазона API." in response.json()["detail"]


def test_get_currency_past_date():
    past_date = date(1515, 10, 10)
    past_date_str = past_date.strftime("%d/%m/%Y")
    response = requests.get(f"{base_url}scripts/XML_daily.asp?date_req={past_date_str}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "выходит за пределы доступного диапазона API." in response.json()["detail"]


def test_get_currency_success_for_today():
    today_date = date.today()

    response = requests.get(f"{base_url}scripts/XML_daily.asp")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/xml"
    assert f"<ValCurs Date=\"{today_date.strftime('%d.%m.%Y')}\"" in response.text


def test_get_currency_invalid_date():
    invalid_date_str = "2025-07-28"
    response = requests.get(
        f"{base_url}scripts/XML_daily.asp?date_req={invalid_date_str}"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_currency_invalid_input():
    invalid_date_str = "invalid_input"
    response = requests.get(
        f"{base_url}scripts/XML_daily.asp?date_req={invalid_date_str}"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_two_same_requests():

    test_date = date(2024, 1, 20)
    test_date_str = test_date.strftime("%d/%m/%Y")

    response1 = requests.get(
        f"{base_url}scripts/XML_daily.asp?date_req={test_date_str}"
    )
    response2 = requests.get(
        f"{base_url}scripts/XML_daily.asp?date_req={test_date_str}"
    )

    assert response1.text == response2.text


def test_500_error():
    response = requests.get(f"{base_url}scripts/XML_daily.asp?simulate_error=true")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
