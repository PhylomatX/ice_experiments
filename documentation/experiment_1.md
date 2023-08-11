# Comparison of generated comparison tables with human generated ones

The first experiment was to generate some of the rows of https://orkg.org/comparison/R595154/ with simple paper question answering and compare them to the human generated ones. The human generated rows used can be found in the `dataset/train_ORKG_transformer_catalog.csv` file. The corresponding papers can be found in `papers/train`.

ORKG seems like a nice dataset for evaluating ICE recipes and also Elicit.

- paragraph relevance scoring was done by vector similarity between question and paragraph. 
- chatgpt was used as model for answer generation from top 3 paragraphs.

The experiment used the recipes from `recipes/paper_qa.py`


## Results from one example run

training corpus: What was the training corpus used?
=> 01H7DGSQD9BFX1PQJCJF096H7G

number of parameters: How many parameters are used in the model?
=> 01H7DGXQV1T5XCPX3V5CSX1GCK

application: What is the application of the model?
=> 01H7DH0SC86XBWQVDD6BPN6PQM

extension: How does the model extend previous work and models?
=> 01H7DH3R42XR272ZGH2D050DV9

organization: What organization developed the model?
=> 01H7DH8XBV022XR6W2A0P1P3SZ


## Discussion

In most cases the generated answer resembles the human generated entries, but lacks some of the details. The quality of the generated answers seems highly dependent on the quality of the prompt. Often, it is unclear how to evaluate the comparison as the human who created the table was also biased and different humans would probably create different tables. Also there is sometimes meta information (e.g. the organization) which cannot be inferred from the papers directly but must probably be extracted from the journal meta data about the paper. 

It seems very difficult to evaluate the generated results against the human generated ones in a formal setting.


## Further experiments

- There is a need for a clearly defined evaluation framework of LLM generated rows and human generated ones.
- Often, the LLM generates an answer that resembles the human generated entry on a high level but doesn't go as much into detail as the human. Here it would be interesting to write a recipe where one can ask for further details and the LLM then answers that question based on the text and the previsously generated answer.
