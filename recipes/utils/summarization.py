from ice.recipe import recipe
from ice.utils import map_async
from ice.paper import Paragraph

from fvalues import F


async def summarize(
    text: str, context: str = None, model: str = "chatgpt"
) -> str:
    if context is None:
        prompt = F(
f"""Summarize the following text:

{text}

Summary:
"""
        ).strip()
    else:
        prompt = F(
f"""You are given the following context:

{context}

Summarize the following text. If the text is not relevant to the context, you may skip it and return an empty string.

{text}

Summary:
"""
        ).strip()
    answer = await recipe.agent(model).complete(prompt=prompt)
    return answer


async def summarize_paragraphs(
    paragraphs: list[Paragraph], summary_length: int = 5, context: str = None, **kwargs
):
    if len(paragraphs) > summary_length:
        # split texts into chunks of size summary_length and recursively summarize
        paragraphs = await map_async(
            [paragraphs[i:i+summary_length] for i in range(0, len(paragraphs), summary_length)],
            lambda chunk: summarize_paragraphs(chunk, summary_length, context, **kwargs)
        )
        summary = await summarize_paragraphs(paragraphs, summary_length, context, **kwargs)
    else:
        # concatenate summaries and summarize again
        summary = await summarize("\n\n".join([str(p) for p in paragraphs]), context, **kwargs)
    return summary


recipe.main(summarize_paragraphs)