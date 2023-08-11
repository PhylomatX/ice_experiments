from fvalues import F

from ice.recipe import recipe
from ice.utils import map_async

def make_qa_prompt(question: str) -> str:
    return F(
        f"""Answer the following question:

Question: "{question}"
Answer: "
"""
    ).strip()


async def answer(question: str = "What is happening on 9/9/2022?"):
    prompt = make_qa_prompt(question)
    answer = await recipe.agent().complete(prompt=prompt, stop='"')
    return answer

async def dummy(items: list[str]):
    return items


async def answer_mapped(questions: list[str] = ["What is happening on 9/9/2022?", "What is a test?"]):
    answers = await map_async(questions, answer)
    answers = await dummy(answers)
    return list(zip(questions, answers))


recipe.main(answer_mapped)