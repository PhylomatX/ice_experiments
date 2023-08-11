from utils.summarization import summarize_paragraphs
from ice.recipe import recipe
from ice.paper import Paper


async def summarize_paper(
        paper: Paper, 
        summary_length: int = 3,
        model: str = 'chatgpt',
        context: str = None
):
    answer = await summarize_paragraphs(
        paper.paragraphs,
        summary_length,
        context=context,
        model=model
    )

    return answer


recipe.main(summarize_paper)
