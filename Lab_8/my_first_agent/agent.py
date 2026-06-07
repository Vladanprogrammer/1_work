from google.adk.agents.llm_agent import Agent
from tools.common_tools import format_text, count_words

# Визначаємо функцію-інструмент
def get_current_time(city: str) -> dict:
    """
    Повертає поточний час у вказаному місті.
    
    Args:
        city: назва міста
    
    Returns:
        dict: інформація про час у вказаному місті
    """
    # Це mock-реалізація для демонстрації
    import datetime
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return {
        "status": "success",
        "city": city,
        "time": current_time
    }

# Створюємо агента
root_agent = Agent(
    model='gemini-2.5-flash',
    name='time_agent',
    description="Повідомляє поточний час у вказаному місті.",
    instruction="Ти корисний асистент, який повідомляє поточний час у містах. Використовуй функцію 'get_current_time' для цього. Відповідай українською мовою та використовуй подачу дати/часу у форматі HH:MM:SS.",
    tools=[get_current_time],
)

import logging
from google.adk.agents.llm_agent import Agent

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logging_tool(param: str) -> dict:
    """Інструмент з логуванням подій"""
    logger.info(f"Виклик інструменту logging_tool з параметром: {param}")
    return {"result": "success", "processed_param": param}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='logging_agent',
    description="Агент з логуванням.",
    instruction="Використовуй інструмент logging_tool та логуй всі дії.",
    tools=[logging_tool],
)