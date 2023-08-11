from ice.paper import Paragraph
from ice.utils import map_async
from ice.recipe import recipe
from ice.paper import Paper

from fvalues import F


async def classify_paragraph_by_text(paragraph: Paragraph, question: str, model: str) -> float:
    prompt = F(
f"""Here is a paragraph from a research paper: "{paragraph}"

Question: Does this paragraph answer the question '{question}'? Say Yes or No.
Answer:"""
        ).strip()
    
    choice_probs, _ = await recipe.agent(
        model
    ).classify(
        prompt=prompt,
        choices=(" Yes", " No"),
    )
    return choice_probs.get(" Yes", 0.0)


async def classify_paragraph_by_vector(paragraph: Paragraph, question: str) -> float:
    relevance = await recipe.agent("embedding-ada").relevance(
        context=str(paragraph),
        question=question,
    )
    return relevance


async def classify_paragraph(paragraph: Paragraph, question: str, method: str = 'text', model: str = None) -> float:
    if method == 'text':
        return await classify_paragraph_by_text(paragraph, question, model)
    elif method == 'vector':
        return await classify_paragraph_by_vector(paragraph, question)
    else:
        raise NotImplementedError(f"Unknown method: {method}")


async def get_relevant_paragraphs(
        paper: Paper, question: str, top_n: int = 3, relevance_method: str = 'text', relevance_model: str = None, return_all: bool = False, **kwargs
    ) -> list[Paragraph]:
    probs = await map_async(paper.paragraphs, lambda par: classify_paragraph(par, question, relevance_method, relevance_model))
    sorted_pairs = sorted(zip(paper.paragraphs, probs), key=lambda x: x[1], reverse=True)
    
    # if binary classification with chatgpt is used, remove paragraphs with prob != 1.0 and apply vector based relevance scoring
    if relevance_method == 'text' and relevance_model == 'chatgpt':
        sorted_pairs = [(par, prob) for par, prob in sorted_pairs if prob == 1.0]
        probs = await map_async([par for par, prob in sorted_pairs], lambda par: classify_paragraph(par, question, 'vector'))
        sorted_pairs = sorted(zip([par for par, prob in sorted_pairs], probs), key=lambda x: x[1], reverse=True)
    
    if not return_all:
        return [par for par, prob in sorted_pairs[:top_n]]
    else:
        return [par for par, prob in sorted_pairs]


recipe.main(get_relevant_paragraphs)