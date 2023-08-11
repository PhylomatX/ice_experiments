from ice.recipe import recipe
from ice.paper import Paper
from utils.paragraph_ranking import get_relevant_paragraphs

from fvalues import F


async def answer(
    context: str, question: str, answer_model: str = "chatgpt", **kwargs
) -> str:
    
    prompt = F(
f"""Background text: "{context}"

Answer the following question about the background text above:

Question: "{question}"
Answer: """
    ).strip()

    answer = await recipe.agent(answer_model).complete(prompt=prompt, stop='"')
    return answer


async def answer_for_paper(
    paper: Paper, question: str, **kwargs
):
    relevant_paragraphs = await get_relevant_paragraphs(paper, question, **kwargs)
    relevant_str = F("\n\n").join(str(p) for p in relevant_paragraphs)
    response = await answer(context=relevant_str, question=question, **kwargs)
    return paper.document_id, response


recipe.main(answer_for_paper)