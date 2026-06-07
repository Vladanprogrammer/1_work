import json
from pathlib import Path
from google.adk.agents.llm_agent import Agent

STATE_FILE = Path("stateful_agent/user_state.json")

def load_state() -> dict:
    """Завантажує стан з файлу"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_state(data: dict) -> dict:
    """Зберігає стан у файл"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return {"status": "saved", "data": data}

def remember_fact(key: str, value: str) -> dict:
    """Запамʼятовує факт про користувача"""
    state = load_state()
    state[key] = value
    return save_state(state)

def recall_fact(key: str) -> dict:
    """Згадує факт про користувача"""
    state = load_state()
    value = state.get(key)
    if value:
        return {"key": key, "value": value, "found": True}
    return {"key": key, "value": None, "found": False}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='stateful_agent',
    description="Агент який памʼятає користувача між сесіями.",
    instruction="""
    Ти персональний асистент який памʼятає інформацію про користувача.
    
    Коли користувач розповідає щось про себе, використовуй remember_fact.
    Коли потрібно згадати щось, використовуй recall_fact.
    
    Будь уважним та корисним. Відповідай українською мовою.
    """,
    tools=[remember_fact, recall_fact],
)