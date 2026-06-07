from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.loop_agent import LoopAgent

search_agent = Agent(
    name='search_agent',
    model='gemini-2.5-flash',
    instruction='Ти збираєш інформацію з відкритих джерел.'
)

db_agent = Agent(
    name='db_agent',
    model='gemini-2.5-flash',
    instruction='Ти витягуєш статистику з внутрішньої бази даних.'
)

parallel_gather = ParallelAgent(
    name='data_gatherer',
    sub_agents=[search_agent, db_agent]  # Виправлено тут
)

process_agent = Agent(
    name='processor',
    model='gemini-2.5-flash',
    instruction='Оброби та відфільтруй сирі дані.'
)

analyze_agent = Agent(
    name='analyzer',
    model='gemini-2.5-flash',
    instruction='Проаналізуй відфільтровані дані та знайди закономірності.'
)

report_agent = Agent(
    name='reporter',
    model='gemini-2.5-flash',
    instruction='Напиши фінальний звіт на основі аналізу.'
)

sequential_pipeline = SequentialAgent(
    name='main_pipeline',
    sub_agents=[parallel_gather, process_agent, analyze_agent, report_agent] # Виправлено тут
)

reviewer_agent = Agent(
    name='reviewer',
    model='gemini-2.5-flash',
    instruction='Перевір звіт. Якщо він не ідеальний, вимагай покращення.'
)

root_agent = LoopAgent(
name='quality_control_loop',
sub_agents=[sequential_pipeline, reviewer_agent],
max_iterations=3
)