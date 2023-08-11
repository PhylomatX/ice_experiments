# Recursive Paragraph summarization

This (very simple) experiment was a short test of how well papers can be summarized by recursively summarizing small groups of paragraphs. 

The experiment used the recipes from `recipes/summarize_paper.py`.

The papers used can be found in `papers/train`.

## Run 1

2023_Touvron.pdf: 01H7J1J63QR8E05HXK5QC0AHZF

Summary: The text introduces LLaMA, a collection of large language models that outperform other models on benchmarks. It discusses modifications made to the transformer architecture and training method used. The text also mentions the examination of biases and toxicity encoded in the models. The LLaMA model achieves state-of-the-art performance on Natural Questions and TriviaQA benchmarks. It also outperforms other models in reading comprehension, mathematical reasoning, and code writing tasks. The text addresses the challenges of evaluating toxicity and biases in language models. It discusses the use of LLaMA-I for generating conversations and provides instructions for making HTTP requests. The text includes information on popular chess openings, Julius Caesar's criticism of Napoleon, and suggests sending an email to request responsible use of language models. It encourages users to explore new tools responsibly, consider ethical implications, and seek advice from experts. The significance of Abraham Lincoln and Albert Einstein is highlighted, praising their contributions to history.


The last few sentences of the summary got mixed up by some experiments that were discussed in the appendix of the paper. With this in mind I adjusted the prompt with an additional context and the instruction to skip a paragraph group if it doesn't seem relevant with respect to the context.


2023_Touvron.pdf: 01H7J1GRZJC1560F3KQBCPHKE4 (with context: "This is from a scientific article about a new large language model")

Summary: LLaMA is a collection of large language models that surpass GPT-3 in various benchmarks. It focuses on transformer architecture modifications and training methods. The article addresses biases and toxicity in the models and achieves impressive performance in zero-shot and few-shot tasks. LLaMA-65B and LLaMA-13B excel in reading comprehension, surpassing GPT-3. LLaMA-65B also outperforms Minerva-62B in mathematical reasoning. The article highlights the importance of evaluating biases and toxic content in large language models, as well as measuring their energy consumption and carbon emissions. The architecture and scaling of language models are also explored.


## Run 2

2022_Peng.pdf: 01H7J1JJ71ZRS2Y1QE3GE8W9C8 (no context)

Summary: The text introduces GODEL, a large pretrained language model for dialog that outperforms other models in few-shot finetuning setups. It discusses the importance of utility in dialog models and proposes automated evaluation criteria based on the model's ability to fulfill user goals. The authors provide code and baselines for future research and discuss the impact of large pre-trained language models in Conversational AI. The text also describes the training and evaluation process of GODEL models, including their performance in knowledge-grounded response generation, task-oriented dialog, and conversational QA. Various evaluation datasets and metrics are used to assess the model's performance. GODEL is found to be superior in terms of usefulness, human-likeness, and safety compared to other models. It performs well in knowledge-grounded generation tasks and achieves better utility scores than baseline methods. The text also discusses the challenges of ensuring safe and inoffensive responses in dialog systems, including social bias and toxicity. Different versions of GODEL are mentioned, with GODEL B performing well in evaluation results and GODEL XL having lower BLEU scores compared to GODEL and GODEL L. GODEL GPT-J XL is introduced as a substitute for GPT-3. The contributions of the Microsoft


2023_Touvron.pdf: 01H7J1MTE6VP3W5N4769WMS0JZ (with context: "This is from a scientific article about a new large language model")

Summary: The text discusses the development and evaluation of a new large language model called GODEL for dialog. GODEL outperforms other models in few-shot finetuning setups and emphasizes the importance of utility in a dialog model. The model is trained in three phases and uses external knowledge from various datasets. Evaluation involves metrics like F R 1, F K 1, Inform, Success, and Combined score. The text also discusses a human evaluation setup comparing GODEL to other models and analyzing the correlation between human and automated evaluation. It addresses the challenges of ensuring safe and inoffensive responses and mentions the release of GODEL XL as a substitute for GPT-3.


## Discussion

These kind of summaries are very sequential and documentary in nature. A human generated abstract captures the core ideas much more precise. In the Factored Cognition Primer there is a paper recommendation that might be an interesting further reading for how to improve this: https://arxiv.org/abs/2109.10862