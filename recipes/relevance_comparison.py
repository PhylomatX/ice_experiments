import os
from pathlib import Path
from ice.utils import map_async
from ice.recipe import recipe
from ice.paper import Paper
from utils.paragraph_ranking import get_relevant_paragraphs
from utils.question_answering import answer

from fvalues import F


def kendall_tau(list1, list2):
    """Compute the Kendall tau rank correlation coefficient between two lists to test the order consistency."""
    if len(list1) != len(list2):
        raise ValueError("Input lists must have the same length")

    concordant = 0
    discordant = 0

    for i in range(len(list1)):
        for j in range(i + 1, len(list1)):
            a = list1[i] - list1[j]
            b = list2[i] - list2[j]

            if a * b > 0:
                concordant += 1
            elif a * b < 0:
                discordant += 1

    total_pairs = len(list1) * (len(list1) - 1) // 2  # n choose 2

    kendall_tau_coefficient = (concordant - discordant) / total_pairs
    return kendall_tau_coefficient


async def test_paragraph_relevance_methods_on_paper(
        paper: str, 
        question: str, 
        top_n: int = 10
):
    paper = Paper.load(Path(paper))

    kwargs_list = [
        (paper, question, top_n, 'vector'),
        (paper, question, top_n, 'text'),
        (paper, question, top_n, 'text', 'chatgpt'),
    ]

    results = await map_async(kwargs_list, lambda kwargs: get_relevant_paragraphs(*kwargs))
    answers = await map_async(results, lambda result: answer(context=F("\n\n").join(str(p) for p in result[:3]), question=question))

    vector_based_ranking, text_based_ranking, text_chatgpt_based_ranking = results
    vector_based_answer, text_based_answer, text_chatgpt_based_answer = answers

    # check how much overlap there is between the three rankings (i.e. how many papers that are in one ranking are also in the others)
    overlap_vector_text = len(set(vector_based_ranking).intersection(set(text_based_ranking)))
    overlap_vector_text_chatgpt = len(set(vector_based_ranking).intersection(set(text_chatgpt_based_ranking)))
    overlap_text_text_chatgpt = len(set(text_based_ranking).intersection(set(text_chatgpt_based_ranking)))
    total_overlap = len(set(vector_based_ranking).intersection(set(text_based_ranking).intersection(set(text_chatgpt_based_ranking))))

    # check if the order of the papers in the rankings is the same
    order_vector_text = [vector_based_ranking.index(par) if par in vector_based_ranking else -1 for par in text_based_ranking]
    order_text_chatgpt_vector = [text_chatgpt_based_ranking.index(par) if par in text_chatgpt_based_ranking else -1 for par in vector_based_ranking]
    order_text_chatgpt_text = [text_chatgpt_based_ranking.index(par) if par in text_chatgpt_based_ranking else -1 for par in text_based_ranking]

    kendall_tau_vector_text = kendall_tau(order_vector_text, list(range(len(order_vector_text))))
    kendall_tau_text_chatgpt_vector = kendall_tau(order_text_chatgpt_vector, list(range(len(order_text_chatgpt_vector))))
    kendall_tau_text_chatgpt_text = kendall_tau(order_text_chatgpt_text, list(range(len(order_text_chatgpt_text))))

    return [
        f"Overlap between vector and text: {overlap_vector_text}",
        f"Overlap between text_chatgpt and vector: {overlap_vector_text_chatgpt}",
        f"Overlap between text_chatgpt and text: {overlap_text_text_chatgpt}",
        f"Total overlap: {total_overlap}",
        f"Order vector and text: {order_vector_text}",
        f"Order text_chatgpt and vector: {order_text_chatgpt_vector}",
        f"Order text_chatgpt and text: {order_text_chatgpt_text}",
        f"Kendall tau vector and text: {kendall_tau_vector_text}",
        f"Kendall tau text_chatgpt and vector: {kendall_tau_text_chatgpt_vector}",
        f"Kendall tau text_chatgpt and text: {kendall_tau_text_chatgpt_text}",
        f"Answer vector: {vector_based_answer}",
        f"Answer text: {text_based_answer}",
        f"Answer text_chatgpt: {text_chatgpt_based_answer}",
        f"text_chatgpt length: {len(text_chatgpt_based_ranking)}",
    ]


recipe.main(test_paragraph_relevance_methods_on_paper)
