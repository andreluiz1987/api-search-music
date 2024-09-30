import yaml
from elasticsearch import Elasticsearch


class ElasticsearchConnection:

    def __init__(self, config_file="config.yaml"):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            self.client = Elasticsearch(
                cloud_id=config['cloud_id'],
                # api_key=config['api_key'],
                basic_auth=("elastic", config['elastic_password'])
            )

    def get_client(self):
        return self.client
