import os
from pathlib import Path
from utils.question_answering import answer_for_paper
from ice.utils import map_async
from ice.recipe import recipe
from ice.paper import Paper


async def question_papers(
        paper_folder: str, 
        question: str, 
        top_n: int = 3, 
        relevance_method: str = 'text', 
        answer_model: str = 'chatgpt', 
        relevance_model: str = None
):
    files = [os.path.join(paper_folder, file) for file in os.listdir(paper_folder)]
    papers = [Paper.load(Path(file)) for file in files]

    answers = await map_async(papers, lambda paper: answer_for_paper(
        paper,
        question, 
        top_n=top_n, 
        relevance_method=relevance_method, 
        answer_model=answer_model, 
        relevance_model=relevance_model
    ))

    return answers


async def question_paper(
        paper: Paper, 
        question: str, 
        top_n: int = 3, 
        relevance_method: str = 'text', 
        answer_model: str = 'chatgpt', 
        relevance_model: str = None
):
    answer = await answer_for_paper(
        paper,
        question, 
        top_n=top_n, 
        relevance_method=relevance_method, 
        answer_model=answer_model, 
        relevance_model=relevance_model
    )

    return answer


recipe.main(question_paper)
