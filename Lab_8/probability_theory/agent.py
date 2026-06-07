from google.adk.agents.llm_agent import Agent

def calculate_probability(m: int, n: int) -> dict:
    """
    Розраховує класичну ймовірність.
    
    Args:
        m: кількість сприятливих подій
        n: загальна кількість можливих подій
    """
    if n == 0:
        return {"error": "Ділення на нуль неможливе."}
    if m > n:
        return {"error": "Помилка: сприятливих подій не може бути більше за загальні."}
        
    return {"probability": m / n, "error": None}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Ти розумний калькулятор який вираховує теорію ймовірності',
    instruction=(
        'Ти відповідаєш лише Українською мовою. '
        'Ти розумний калькулятор, який допомагає розрахувати теорію ймовірності. '
        'Обов\'язково використовуй інструмент calculate_probability для отримання результату. '
        'Ти видаєш лише чіткі відповіді на поставлену задачу з теорії ймовірності.'
    ),
    tools=[calculate_probability]
)