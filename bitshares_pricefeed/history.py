from elasticsearch_dsl import connections, Search, Q, A
from bitshares.price import Price

class ElasticSearchLoader:
    def __init__(self, es_config):
        connections.create_connection(**es_config)
    
    def load(self, asset_id, witness_id, n_days):
        s = Search(index="bitshares-*")
        s = s.extra(size=1000)
        s = s.query('bool', filter = [
                Q('term', operation_type=19),
                Q("range", block_data__block_time={'gte': 'now-{}d'.format(n_days)}),
                Q('term', account_history__account=witness_id),
                Q('term', operation_history__op_object__asset_id=asset_id)
            ])
        s = s.params(clear_scroll=False) # Avoid calling DELETE on ReadOnly apis.
    
        result = []
        for hit in s.scan():
            op = hit.operation_history.op_object
            price = op["feed"]["settlement_price"]
            result.append(float(Price(price.to_dict())))
        return result

if __name__ == '__main__':
    from bitshares.asset import Asset
    from bitshares.account import Account
    from statistics import mean 

    usd = Asset("USD")
    witness = Account("zapata42-witness")

    es_config = {
        'hosts': 'https://elasticsearch.bitshares-kibana.info/'
    }

    loader = ElasticSearchLoader(es_config)
    feeds = loader.load(usd["id"], witness["id"], 2)
    print(feeds)
    print(mean(feeds))