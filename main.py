import logging
import sys
import json
import re

from app.collection.parse import parse_near
from app.processing.graphs import build_graph, build_bar


########################################################################################################################
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='[%(asctime)s]:[%(levelname)s]:[%(filename)s]:[%(lineno)d]: %(message)s',
    )


########################################################################################################################
if __name__ == '__main__':
    logger.info('Start')
    filename_local_json_with_data = parse_near()
    logger.info(f'Parse finish. File with data: "{filename_local_json_with_data}"')

    file_json_with_data = open('app/collection/' + filename_local_json_with_data, 'r', encoding='utf-8')
    data = json.load(file_json_with_data)

    graphs_data = {
        'mainnet': {
            'contributors': [],
            'total_stake': [],
            'fees': [],
            'positions': []
        },
        'shardnet': {
            'contributors': [],
            'total_stake': [],
            'fees': [],
            'positions': []
        }
    }
    total_pattern = re.compile(r'((^(\d|,)*)(\xa0))')
    for i in data["shardnet"]:
        graphs_data['shardnet']['contributors'].append(
            int(i["contributors"].replace('Н/Д', '0')))
        graphs_data['shardnet']['total_stake'].append(
            int(total_pattern.findall(i["total"])[0][1].replace(',', '')))
        graphs_data['shardnet']['fees'].append(
            int(i["fee"].replace('Н/Д', '0').replace('%', '')))
        graphs_data['shardnet']['positions'].append(
            int(i["position"]))
    for i in data["mainnet"]:
        graphs_data['mainnet']['contributors'].append(
            int(i["contributors"].replace('Н/Д', '0')))
        graphs_data['mainnet']['total_stake'].append(
            int(total_pattern.findall(i["total"])[0][1].replace(',', '')))
        graphs_data['mainnet']['fees'].append(
            int(i["fee"].replace('Н/Д', '0').replace('%', '')))
        graphs_data['mainnet']['positions'].append(
            int(i["position"]))

    # total stake to contributors
    mainnet_stake_contr_graph = build_graph(
        graph_name='mainnet_stake_contr_graph',
        x=graphs_data['mainnet']['total_stake'],
        y=graphs_data['mainnet']['contributors'],
    )
    shardnet_stake_contr_graph = build_graph(
        graph_name='shardnet_stake_contr_graph',
        x=graphs_data['shardnet']['total_stake'],
        y=graphs_data['shardnet']['contributors'],
    )

    # fee to contributors
    mainnet_fee_contr_graph = build_bar(
        width=1,
        graph_name='mainnet_fee_contr_graph',
        x=graphs_data['mainnet']['fees'],
        y=graphs_data['mainnet']['contributors'],
    )
    shardnet_fee_contr_graph = build_bar(
        width=1,
        graph_name='shardnet_fee_contr_graph',
        x=graphs_data['shardnet']['fees'],
        y=graphs_data['shardnet']['contributors'],
    )

    # position to contributors
    mainnet_position_contr_graph = build_bar(
        width=1,
        graph_name='mainnet_position_contr_graph',
        x=graphs_data['mainnet']['positions'],
        y=graphs_data['mainnet']['contributors'],
    )
    shardnet_position_contr_graph = build_bar(
        width=1,
        graph_name='shardnet_position_contr_graph',
        x=graphs_data['shardnet']['positions'],
        y=graphs_data['shardnet']['contributors'],
    )

    file_json_with_data.close()


