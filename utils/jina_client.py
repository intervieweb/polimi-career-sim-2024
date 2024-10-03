import requests


class Client:

    def __init__(self, api_key=None):
        if not api_key:
            raise Exception("Please provide an api_key")
        else:
            self.api_key = api_key

        self.url_reranker = "https://api.jina.ai/v1/rerank"
        self.model_reranker = "jina-reranker-v2-base-multilingual"

        self.url_embeddings = "https://api.jina.ai/v1/embeddings"
        self.model_embeddings = "jina-embeddings-v3"

        self.url_segmenter = "https://segment.jina.ai/"
        self.model_segmenter = "cl100k_base"  # technically the tokenizer

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _call(self, url, json):
        response = requests.post(url, headers=self.headers, json=json)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}\n{response.text}."
            )

    def call_reranker(self, query: str, documents: list, top_n: int = 5) -> dict:

        data = {
            "model": self.model_reranker,
            "query": query,
            "documents": documents,
            "top_n": top_n,
        }

        return self._call(self.url_reranker, data)

    def get_embeddings(
        self, input: list, dimensions=1024, downstream_task="text-matching"
    ) -> list:

        data = {
            "model": self.model_embeddings,
            "task": downstream_task,
            "dimensions": dimensions,
            "late_chunking": False,
            "embedding_type": "float",
            "input": input,
        }

        response = self._call(self.url_embeddings, data)

        if "data" in response:
            return [item.get("embedding") for item in response["data"]]

    def get_segmentation(
        self, content, max_chunk_length=1000, remove_new_lines=True
    ) -> list:

        if remove_new_lines:
            content = content.replace("\n", " ")

        data = {
            "content": content,
            "tokenizer": self.model_segmenter,
            "return_chunks": "true",
            "max_chunk_length": max_chunk_length,
        }

        response = self._call(self.url_segmenter, data)

        if "chunks" in response:
            return response["chunks"]
        else:
            return []
