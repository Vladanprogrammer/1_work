from google.adk.agents.llm_agent import Agent
from tools.common_tools import format_text, count_words

def explain_concept(concept: str, level: str = "beginner") -> dict:
    """
    Пояснює концепцію програмування.
    
    Args:
        concept: назва концепції для пояснення
        level: рівень складності (beginner, intermediate, advanced)
    
    Returns:
        dict: пояснення та приклади
    """
    explanations = {
        "beginner": f"Базове пояснення концепції {concept}",
        "intermediate": f"Поглиблене пояснення концепції {concept}",
        "advanced": f"Експертне пояснення концепції {concept}"
    }
    return {
         "status": "success",
         "concept": concept,
         "level": level,
         "explanation": explanations.get(level, "Невідомий рівень")
    }

def check_syntax(code: str, language: str = "python") -> dict:
    """
    Перевіряє синтаксис коду (базова перевірка).
    
    Args:
        code: код для перевірки
        language: мова програмування
    
    Returns:
        dict: результат перевірки
    """
    # Проста перевірка для демонстрації
    if not code.strip():
        return {"status": "error", "message": "Код порожній"}
    return {"status": "success", "message": "Синтаксис виглядає коректно", "language": language}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='student_helper',
    description="Помічник для студентів які вивчають програмування.",
    instruction="""
    Ти досвідчений викладач з ООП програмування який допомагає студентам.
    
    Твої обов'язки:
    - Пояснювати складні концепції простими словами
    - Наводити приклади коду
    - Перевіряти синтаксис коду
    - Давати поради щодо best practices
    - Бути терплячим та підтримуючим
    - За замовчуванням використовувати Python для прикладів, якщо не вказано іншу мову
    
    Завжди відповідай українською мовою.
    Використовуй форматування Markdown для коду.
    """,
    tools=[explain_concept, check_syntax],
)