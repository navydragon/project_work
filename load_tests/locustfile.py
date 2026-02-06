from locust import HttpUser, task, between
import os
import uuid
from typing import List

from dotenv import load_dotenv


# Загружаем переменные окружения из .env в корне проекта
load_dotenv()


def _parse_team_ids(env_value: str) -> List[str]:
    """
    Разбирает строку вида 'id1,id2,...' в список строк UUID.
    Некорректные значения игнорируются.
    """
    if not env_value:
        return []

    result: List[str] = []
    for raw in env_value.split(","):
        value = raw.strip()
        if not value:
            continue
        try:
            # валидация UUID, но храним как строку
            uuid.UUID(value)
            result.append(value)
        except ValueError:
            # пропускаем некорректное значение, чтобы не падать
            continue
    return result


def _load_team_ids() -> List[str]:
    """
    Пытается прочитать LOCUST_TEAM_IDS из окружения/.env.
    Если переменная не задана или пуста — возвращает пустой список.
    """
    env_value = os.getenv("LOCUST_TEAM_IDS", "")
    ids = _parse_team_ids(env_value)
    if ids:
        print(f"[Locust] TEAM_IDS from env ({len(ids)}): {ids}")
    else:
        print("[Locust] LOCUST_TEAM_IDS не задана или пуста, список команд пуст")
    return ids


TEAM_IDS: List[str] = _load_team_ids()


class TeamsUser(HttpUser):
    """
    Пользователь Locust, который запрашивает эндпоинт GET /api/teams/<id>/.

    Базовый host задаётся при запуске Locust (ключ --host или через веб‑интерфейс).
    Список ID команд задаётся переменной окружения LOCUST_TEAM_IDS
    (через запятую: LOCUST_TEAM_IDS=id1,id2,...).
    """

    wait_time = between(1, 5)

    @task
    def get_team_detail(self):
        if not TEAM_IDS:
            # если ID не заданы, сразу выходим, чтобы не долбить /api/teams/ без id
            return

        # простой круговой перебор ID
        team_id = TEAM_IDS[self.environment.runner.user_count % len(TEAM_IDS)] if self.environment.runner else TEAM_IDS[0]
        url = f"/api/teams/{team_id}/"
        with self.client.get(url, name="/api/teams/:id/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code {response.status_code}")
            else:
                # простая проверка структуры ответа
                try:
                    data = response.json()
                    if "id" not in data:
                        response.failure("Field 'id' is missing in response")
                except ValueError:
                    response.failure("Response is not valid JSON")

