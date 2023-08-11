## ICE experiments

This repository documents some of my experiments to get familiar with the Interactive Composition Explorer (ICE) by Ought.

-   primer: Contains the code snippets from the [Factored Cognition Primer](https://primer.ought.org/) by Ought.
-   recipes: Contains code snippets for my own introductory experiments.


## Usage

I added some additional functionality to ICE, so this repository is based on my own ICE fork: https://github.com/PhylomatX/ice. See that repository for installation instructions.


## Experiments

So far I conducted 3 introductory experiments. All of them are documented in the `documentation` folder.

-   Experiment 1: Test to reproduce some of the rows of a comparison of transformer models from the [Open Research Knowledge Graph](https://orkg.org/comparison/R595154/)
-   Experiment 2: A comparison of paragraph relevance ranking using three approaches: 1) classification by text-davinci-002, 2) ranking by vector similarity between text-embedding-ada-002 embeddings, 3) binary classification by gpt-3.5-turbo with consecutive ranking by vectory similarity between text-embedding-ada-002 embeddings.
-   Experiment 3: Recursive text summarization using gpt-3.5-turbo.
