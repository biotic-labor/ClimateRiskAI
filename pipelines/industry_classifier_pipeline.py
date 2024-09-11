from helper import load_env
from haystack import Pipeline
from haystack_integrations.components.embedders.cohere.text_embedder import CohereTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack_integrations.document_stores.pinecone import PineconeDocumentStore
from haystack_integrations.components.retrievers.pinecone import PineconeEmbeddingRetriever
import json

load_env()

def classify_industry(industry_info:str):
    document_store = PineconeDocumentStore(
		index="industries",
		namespace="Classification",
        dimension=1024,
        spec={"serverless": {"region": "us-east-1", "cloud": "aws"}},
    )

    prompt = """
    Answer the question based on the provided context.
    Context:
    {% for doc in documents %}
    {{ doc.content }} 
    {% endfor %}
    Question: {{ query }}
    """

    query_embedder = CohereTextEmbedder(model="embed-english-v3.0")
    retriever = PineconeEmbeddingRetriever(document_store=document_store)
    prompt_builder = PromptBuilder(template=prompt)
    generator = OpenAIGenerator()
    query_pipeline = Pipeline()
    query_pipeline.add_component("query_embedder", query_embedder)
    query_pipeline.add_component("retriever", retriever)
    query_pipeline.add_component("prompt", prompt_builder)
    query_pipeline.add_component("generator", generator)

    query_pipeline.connect("query_embedder.embedding", "retriever.query_embedding")
    query_pipeline.connect("retriever.documents", "prompt.documents")
    query_pipeline.connect("prompt", "generator")

    industry_question = industry_info+ ": What industry and subindustry would this company be classified as? Provide in the json format {\"industry\":\"\", \"industry_id\":\"\", \"subindustry\":\"\", \"subindustry_id\":\"\"}"

    industries_result = query_pipeline.run(
        {
            "query_embedder": {"text": industry_question},
            "retriever": {"top_k": 1},
            "prompt": {"query": industry_question},
        }
    )
    # print(industries_result["generator"]["replies"][0])
    industry = json.loads(industries_result["generator"]["replies"][0])
    print(industry['subindustry_id'])
    return industry