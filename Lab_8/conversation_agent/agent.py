from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from tools.common_tools import format_text, count_words

def save_user_preference(tool_context: ToolContext, preference_type: str, value: str) -> dict:
    """
    Зберігає вподобання користувача.

    Args:
        preference_type: тип вподобання (улюблений_колір, хобі, тощо)
        value: значення вподобання

    Returns:
        dict: підтвердження збереження
    """
    existing_state = tool_context.state.get(preference_type, [])
    tool_context.state[preference_type] = existing_state + [value]
    print(f"[Added to {preference_type}] {value}")
    return {
        "status": "success",
        "message": f"Збережено: {preference_type} = {value}"
    }

def recall_preference(tool_context: ToolContext, preference_type: str) -> dict:
    """
    Згадує вподобання користувача.

    Args:
        preference_type: тип вподобання для пошуку

    Returns:
        dict: збережене вподобання або повідомлення про відсутність
    """
    # Примітка: історія зберігається автоматично в ADK
    preferences = tool_context.state.get(preference_type, [])
    if preferences:
        return {
            "status": "success",
            "message": f"Згадано: {preference_type} = {', '.join(preferences)}"
        }
    else:
        return {
            "status": "error",
            "message": f"Не знайдено вподобань типу: {preference_type}"
        }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='conversation_agent',
    description="Розмовний агент який памʼятає користувача.",
    instruction="""
    Ти дружелюбний асистент який веде розмову з користувачем.

    Важливо:
    - Памʼятай що користувач розповідає про себе та зберігай цю інформацію як вподобання за допомогою інструменту save_user_preference
    - Використовуй цю інформацію у подальшій розмові використовуючи інструмент recall_preference
    - Стався уважно до деталей, які користувач розповідає про себе, це допоможе тобі краще його розуміти та підтримувати цікаву розмову
    - Будь ввічливим та цікавим співрозмовником
    - Звертайся до користувача по імені, якщо він його назве, та намагайся запамʼятати його інтереси та вподобання для подальшого використання у розмові

    Відповідай українською мовою.
    """,
    tools=[save_user_preference, recall_preference],
)
