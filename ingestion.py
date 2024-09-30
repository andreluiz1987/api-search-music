import asyncio
import json

import yaml
from elasticsearch import helpers, AsyncElasticsearch


def get_async_client():
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
        return AsyncElasticsearch(
            cloud_id=config['cloud_id'],
            basic_auth=("elastic", config['elastic_password']),
            request_timeout=240)


def partition_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


async def index_data():
    global partitions
    with open('files/musics.json', 'r') as file:
        data_json = json.load(file)
    documents = []
    for doc in data_json:
        documents.append(
            {
                "_index": "music-vector",
                "_source": doc,
            }
        )

        partitions = partition_list(documents, 500)

    for i, partition in enumerate(partitions):
        print(f"partition {i + 1}")
        await async_bulk_indexing(get_async_client(), partition)


async def async_bulk_indexing(client, documents):
    success, failed = await helpers.async_bulk(client, documents)
    print(f"Successfully indexed {success} documents. Failed to index {failed} documents.")


async def main():
    await index_data()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
