# Comparison of paragraph relevance ranking using three approaches

Here I compare three approaches to finding relevant paragraphs for a given question:

1. "vector" approach: Each paragraph gets vectorized and the paragraph vectors are sorted by their cosine similarity with the vector from the given question
2. "text" approach: Each paragraph is input to text-davinci-002 which outputs a probability for yes (relevant) or no (not relevant). The paragraphs are then sorted by descending probability for relevance
3. "chatgpt" approach: Each paragraph is input to gpt-3.5-turbo which outputs yes (relevant) or no (not relevant) without probabilities. The relevant paragraphs are then vectorized and get sorted by their cosine similarity with the vector from the given question

I do this experiment because I always used approach 1 for question answering and never really thought of approach 2 until I read through the factored cognition primer. The goal of the experiment is to find out if there are clear and consistent advantages / disadvantages of any of the approaches.

The experiment should get performed using different questions on papers with a few dozen paragraphs.

Ideally this experiment would get evaluated according to the following metrics:

1. How much overlap is there between the first 5 / 10 spots of the returned paragraph list between all three approaches
2. How consistent is the ordering of the paragraphs on these spots across all three approaches
3. How expensive is each approach

The splitting of papers into paragraphs is done by the ICE paper loading component. The splitting method has a direct impact on the vector approach i.e. if each sentence is vectorized and used in the ranking then the vector approach probably picks up much finer nuances in the text that might be picked up by the text and chatgpt approaches already.

The results are to be understood as follows: In e.g. "Order vector and text", the position of the results (list of relevant paragraphs) from text in the vector result list are given. -1 if they are not present. E.g. if the text approach returns a list of four relevant paragraphs and we mark them by consecutive numbers [0, 1, 2, 3] then "Order vector and text" = [1, 0, -1, 3] means that the first paragraph from the text approach is on index 0 in the vector approach, text index 0 is on vector index 1, the fourth paragraph is the same in both approaches and text index 2 is not present in the vector approach results.
Overlap means how many of the same paragraphs are present across approaches.

The traces can be found in the traces folder.

The experiment used the recipes from `recipes/relevance_comparison.py`

## Run 1

-   Paper: 2023_Touvron (114 paragraphs)
-   Question: How many parameters are used in the model?
-   Top 10 paragraphs are considered
-   Traces: 01H7FDRTT7G889YSZPEMVNRAJR, 01H7FF82163D371WD8DCW4QFJ8
-   Answer is generated from the top 3 paragraphs of each approach, using chatgpt

Results 
1. Overlap between vector and text: 3
2. Overlap between text_chatgpt and vector: 2
3. Overlap between text_chatgpt and text: 3
4. Total overlap: 2
5. Order vector and text: [-1, 4, 0, 6, -1, -1, -1, -1, -1, -1]
6. Order text_chatgpt and vector: [0, -1, -1, -1, 1, -1, -1, -1, -1, -1]
7. Order text_chatgpt and text: [2, 1, 0, -1, -1, -1, -1, -1, -1, -1]
8. Kendall tau vector and text: -0.3111111111111111
9. Kendall tau text_chatgpt and vector: -0.2
10. Kendall tau text_chatgpt and text: -0.5333333333333333
11. Answer vector: The model uses 13 billion parameters.
12. Answer text: The model uses a range of parameters from 7B to 65B.
13. Answer text_chatgpt: The model uses a range of parameters from 7B to 65B. 
14. text_chatgpt length: 3

We find that there is only a 30% overlap between the vector and text and only 2 overlapping paragraphs in the vector and chatgpt approach. The chatgpt and text approaches are quite similar, only that the chatgpt approach uses the reverse ordering (and the chatgpt approach identifies only 3 important paragraphs while the text approach returns the top 10 results).

From one human judging, the text approach has the most reasonable paragraph that answers the question on index 0 while that one is not even present in the vector approach. Vector and chatgpt approaches return a somewhat reasonable paragraph on index 0 while the chatgpt approach catches up delivering two more important ones.

For actually answering the question, the vector approach draws an only partially true conclusion (based on the first paragraph which is not as good as the first paragraph from the text approach), while chat_gpt and text approach come to the same true and more informative conclusion.

The cost of the text approach is 0.29$ while the costs of the other two approaches are negligible.

The results are consistent over multiple runs.

## Run 2

-   Paper: 2023_Touvron (114 paragraphs)
-   Question: What is the climate impact of the model training?
-   Top 10 paragraphs are considered
-   Traces: 01H7FG1AHQ8TDQG0DEYET1VX2B
-   Answer is generated from the top 3 paragraphs of each approach, using chatgpt

Results (e.g. in "Order vector and text", the position of the results from text in the vector result list are given. -1 if they are not present)
1. Overlap between vector and text: 3
2. Overlap between text_chatgpt and vector: 3
3. Overlap between text_chatgpt and text: 3
4. Total overlap: 3
5. Order vector and text: [0, -1, -1, 2, -1, -1, -1, -1, 1, -1]
6. Order text_chatgpt and vector: [0, 1, 2, -1, -1, -1, -1, -1, -1, -1]
7. Order text_chatgpt and text: [0, -1, -1, 2, -1, -1, -1, -1, 1, -1]
8. Kendall tau vector and text: -0.08888888888888889
9. Kendall tau text_chatgpt and vector: -0.4
10. Kendall tau text_chatgpt and text: -0.08888888888888889
11. Answer vector: The climate impact of the model training is the emission of carbon dioxide, with a total of 1,015 tCO2 eq.
12. Answer text: The climate impact of the model training is the emission of carbon dioxide (CO2) due to the energy consumption involved in the training process.
13. Answer text_chatgpt: The climate impact of the model training is the emission of carbon dioxide, with a total of 1,015 tCO2 eq. 
14. text_chatgpt length: 3

Three paragraphs are resulting from all approaches, using the same ordering in case of chatgpt and vector while they are distributed over the full range in case of the text approach. The first paragraph is the same in all approaches.

The text approach seems to get confused my some artefact paragraphs without much content and puts the crucial paragraph for answering the question on index 3 which is not input to the answering recipe. That's why the text answer falls short of the concrete number for the climate impact which is present in both other approaches which have the crucial context on index 2 which is seen by the answering recipe which in turn includes it in the answer.

The cost of the text approach is 0.29$ while the costs of the other two approaches are negligible.

## Run 3

-   Paper: 2019_Zhang (73 paragraphs)
-   Question: What was the training corpus used?
-   Top 10 paragraphs are considered
-   Traces: 01H7FJ04BPQSX8Q0HNG3PDNAJ0
-   Answer is generated from the top 3 paragraphs of each approach, using chatgpt

Results (e.g. in "Order vector and text", the position of the results from text in the vector result list are given. -1 if they are not present)
1. Overlap between vector and text: 1
2. Overlap between text_chatgpt and vector: 2
3. Overlap between text_chatgpt and text: 2
4. Total overlap: 1
5. Order vector and text: [0, -1, -1, -1, -1, -1, -1, -1, -1, -1]
6. Order text_chatgpt and vector: [0, -1, -1, -1, -1, -1, 1, -1, -1, -1]
7. Order text_chatgpt and text: [0, 3, -1, -1, -1, -1, -1, -1, -1, -1]
8. Kendall tau vector and text: -0.2
9. Kendall tau text_chatgpt and vector: -0.1111111111111111
10. Kendall tau text_chatgpt and text: -0.3333333333333333
11. Answer vector: The training corpus used was English Wikipedia.
12. Answer text: The training corpus used was English Wikipedia.
13. Answer text_chatgpt: The training corpus used was the English Wikipedia.
14. text_chatgpt length: 5

The one crucial paragraph is present in the results of all approaches and is always on index 0. Correspondingly all answers are the same. None of the answers include Wikidata as an additional data source, even so it is present in the crucial paragraph and the text approach even puts another crucial paragraph about this on index 1. The vector approach misses this paragraph completely while it is present in the chatgpt approach on index 3 which is not included in the answer recipe.

The text approach again includes a lot of not meaningful artefact paragraphs. The overlap between vector and text is only 1 out of 10. The vector approach includes only meaningful paragraphs but focuses too much on the semantics of "corpora" which may be an insufficiency of our prompting method.

The cost of the text approach is 0.18$ while the costs of the other two approaches are negligible.

## Run 4

-   Paper: 2019_Zhang (73 paragraphs)
-   Question: How does the model extend or use previous work and models?
-   Top 10 paragraphs are considered
-   Traces: 01H7FJWEJJNN2JGRASSJACV2KX
-   Answer is generated from the top 3 paragraphs of each approach, using chatgpt

Results (e.g. in "Order vector and text", the position of the results from text in the vector result list are given. -1 if they are not present)
1. Overlap between vector and text: 4
2. Overlap between text_chatgpt and vector: 8
3. Overlap between text_chatgpt and text: 4
4. Total overlap: 4
5. Order vector and text: [-1, 6, -1, -1, 5, 4, 1, -1, -1, -1]
6. Order text_chatgpt and vector: [0, 1, 2, 3, 4, 5, 6, -1, 7, -1]
7. Order text_chatgpt and text: [-1, 6, -1, -1, 5, 4, 1, -1, -1, -1]
8. Kendall tau vector and text: -0.2222222222222222
9. Kendall tau text_chatgpt and vector: 0.3111111111111111
10. Kendall tau text_chatgpt and text: -0.2222222222222222
11. Answer vector: The model extends or uses previous work and models by incorporating pre-trained language representation models, both feature-based and fine-tuning approaches. It builds upon the work of Mikolov et al., Pennington et al., Peters et al., Dai and Le, Howard and Ruder, Radford et al., and Devlin et al. It also incorporates the use of pre-trained word representations, such as ELMo, to capture complex word features across different linguistic contexts. Additionally, the model recognizes the importance of incorporating extra knowledge information, as demonstrated in recent work on reading comprehension, machine translation, and other NLP applications.
12. Answer text: The model extends or uses previous work and models by adopting micro averaged metrics instead of macro averaged metrics, following the work of Zhang et al. (2017). It also utilizes the results of CNN, PA-LSTM, and C-GCN from the paper by Zhang et al. (2018) as benchmarks. Additionally, the model incorporates the entity mask strategy, which is similar to the proposed pre-training task dEA, and is inspired by the work of Dai and Le (2015) who trained auto-encoders on unlabeled text. The model also mentions the use of pre-trained language representation models such as ULMFiT, GPT, and BERT, and highlights the adoption of masked language model (MLM) and next sentence prediction (NSP) as pre-training tasks, similar to BERT.
13. Answer text_chatgpt: The model extends or uses previous work and models by incorporating pre-trained language representation models, both feature-based and fine-tuning approaches. It builds upon the work of Mikolov et al. (2013), Pennington et al. (2014), Peters et al. (2017, 2018), Dai and Le (2015), Howard and Ruder (2018), Radford et al. (2018), and Devlin et al. (2019). It also mentions the early work of Collobert and Weston (2008) and Turian et al. (2010) in adopting feature-based approaches for word representations. Additionally, it references the use of extra knowledge information in recent work to enhance original models in various NLP applications. 
14. text_chatgpt length: 10

There is a 80% overlap between chatgpt and vector and therefore also a very similar ordering (as chatgpt uses the vector approach to rerank its binary classifications). Therefore the answers of chatgpt and text approaches are almost the same. The overlap to the text approach is also relatively (with respect to previous experiments) high even so the ordering is quite different, especially for the first three paragraphs which are important for question answering which results in different answers between chatgpt / vector and text approaches.

The answers concentrate on related work and miss the intended result (the distillation of the paper by a human researcher for the keyword "extension" as seen in the ORGK comparison table for transformer models). The intended result was something like "Uses BERT for Encoder architecture, but stacks and aggregates two of them for text and entities. This architecture could be understood as BERT for text + knowledge graphs". This is not present in the given answers by all approaches (only the text approach partially includes the dEA pre-training approach). This again is an insufficiency of our prompt as the next experiment run shows.

The cost of the text approach is 0.18$ while the costs of the other two approaches are negligible.

## Run 5

-   Paper: 2019_Zhang (73 paragraphs)
-   Question: What are the main contributions?
-   Top 10 paragraphs are considered
-   Traces: 01H7FMB3GERZZN131BXW8RE228
-   Answer is generated from the top 3 paragraphs of each approach, using chatgpt

Results (e.g. in "Order vector and text", the position of the results from text in the vector result list are given. -1 if they are not present)
1. Overlap between vector and text: 0
2. Overlap between text_chatgpt and vector: 2
3. Overlap between text_chatgpt and text: 2
4. Total overlap: 0
5. Order vector and text: [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
6. Order text_chatgpt and vector: [-1, -1, -1, -1, -1, -1, -1, 0, -1, 1]
7. Order text_chatgpt and text: [-1, -1, -1, -1, 2, -1, -1, 8, -1, -1]
8. Kendall tau vector and text: 0.0
9. Kendall tau text_chatgpt and vector: 0.3333333333333333
10. Kendall tau text_chatgpt and text: 0.1111111111111111
11. Answer vector: The main contributions mentioned in the background text are the incorporation of knowledge information into feature-based and fine-tuning language representation models, and the enhancement of original models in various tasks such as reading comprehension and machine translation through the injection of extra knowledge information. Additionally, the architecture of ERNIE and the aggregator for the mutual integration of the input of tokens and entities are also mentioned as contributions.
12. Answer text: The main contributions of the paper are: 1. ERNIE effectively reduces the noisy label challenge in the FIGER dataset by injecting information from knowledge graphs. 2. ERNIE outperforms the baselines on the Open Entity dataset, which has gold annotations. 3. ERNIE significantly outperforms the state-of-the-art model BERT on entity typing and relation classification tasks by utilizing lexical, syntactic, and knowledge information. 4. ERNIE achieves comparable results to BERT on other common NLP tasks. 5. The paper provides the source code and experiment details for ERNIE.
13. Answer text_chatgpt: The main contributions mentioned in the background text are the proposal of ERNIE, a language representation model that incorporates knowledge information, and the proposal of the knowledgeable aggregator and the pre-training task dEA for better fusion of heterogeneous information from both text and knowledge graphs. The experimental results demonstrate that ERNIE has better abilities in denoising distantly supervised data and fine-tuning on limited data compared to BERT. 
14. text_chatgpt length: 10

We encounter a 0% total overlap. 0% overlap between vector and text and only 20% overlap between chatgpt and vector and text respectively (with very different ordering) even so chatgpt marked 10 paragraphs as important.

From one human judging, the chatgpt answer matches the human answer (from the ORKG comparison) best: "Uses BERT for Encoder architecture, but stacks and aggregates two of them for text and entities. This architecture could be understood as BERT for text + knowledge graphs". The vector answer also partially captures this notion while the text answer concentrates too much on the actual outcomes and conclusions of the paper.

This time, the vector approach picks up a lot of paragraph artefacts and includes only one meaningful paragraph in the top 3 from which the answer is generated.

The cost of the text approach is 0.18$ while the costs of the other two approaches are negligible.

## Discussion

Considering that this experiment only includes 5 runs across two papers, the discussion should be taken with caution. With this in mind, our observations seem to indicate:

-   All three approaches are reasonable methods for the task at hand. There are no consistent advantages or disadvantages of any approach (except for the high cost disadvantage of the text approach).
-   All three approaches can result in completely different lists of relevant paragraphs with different orderings. Considering the vector approach vs chatgpt and text this can be understood by the insufficiency of the vectorization model to encode text nuances into the embedding. Comparing the chatgpt with the text approach this can be explained by the fact that the chatgpt model is much different from the old text-davinci-002 used by the text approach.
-   The choice of the approach to answering questions therefore can have a large impact on the performance of the system. Given that the respective approaches all use black boxes, that at the moment are not well understood this is an example where our insufficient knowledge about these models can lead to applications whose behavior is hard to predict and formalize.
