from flask import Flask, jsonify, request
from flask_cors import CORS

from elasticsearch_connection import ElasticsearchConnection

es_client = ElasticsearchConnection().get_client()
app = Flask(__name__)
CORS(app)


def search_semantic(term):
    result = []
    response = es_client.search(
        index="music-vector",
        size=3,
        source_excludes=["lyrics_embedding", "lyrics_sentiment_analysis_vector"],
        body={
            "knn": {
                "field": "lyrics_sentiment_analysis_embedding",
                "query_vector_builder": {
                    "text_embedding": {
                        "model_id": "sentence-transformers__all-minilm-l6-v2",
                        "model_text": term
                    }
                },
                "k": 10,
                "num_candidates": 50
            },
            "_source": [
                "song", "artist", "photo_album"
            ]
        })

    for hit in response["hits"]["hits"]:
        score = hit["_score"]
        artist = hit["_source"]["artist"]
        song = hit["_source"]["song"]
        photo_album = hit["_source"]["photo_album"]
        result.append({
            'artist': artist,
            'song': song,
            'photo_album': photo_album,
        })
    return result


@app.route('/api/music/search', methods=['GET'])
def get_music():
    query = request.args.get('query')
    results = search_semantic(query)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
