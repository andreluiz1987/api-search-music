from elasticsearch_connection import ElasticsearchConnection

client = ElasticsearchConnection().get_client()


def create_pipeline_vector():
    pipeline_id = "vector_pipeline"
    pipeline_body = {
        "description": "Create embedding lyrics",
        "processors": [
            {
                "inference": {
                    "model_id": "sentence-transformers__all-minilm-l6-v2",
                    "input_output": [
                        {
                            "input_field": "text_field",
                            "output_field": "lyrics_embedding"
                        },
                        {
                            "input_field": "lyrics_sentiment_analysis",
                            "output_field": "lyrics_sentiment_analysis_embedding"
                        }
                    ]
                }
            }
        ]
    }

    response = client.ingest.put_pipeline(id=pipeline_id, body=pipeline_body)

    print(response)


def create_index():
    response = client.indices.create(
        index="music-vector",
        settings={"index": {"default_pipeline": "vector_pipeline"}},
        mappings={
            "properties": {
                "artist": {
                    "type": "text",
                },
                "song": {
                    "type": "text",
                },
                "photo_album": {
                    "type": "keyword",
                },
                "text_field": {
                    "type": "text",
                },
                "lyrics_sentiment_analysis": {
                    "type": "text",
                },
                "lyrics_embedding": {
                    "type": "dense_vector",
                    "dims": 384
                },
                "lyrics_sentiment_analysis_embedding": {
                    "type": "dense_vector",
                    "dims": 384
                }
            }
        }
    )
    print(response)


if __name__ == '__main__':
    # print(client.info())
    create_pipeline_vector()
    create_index()
