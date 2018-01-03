#!/usr/bin/env python
from db.graph_collection_manager import GraphCollectionManager
from constants import BLOCK_RUNNING_STATUS_MAP
from web.common import *
from utils.common import to_object_id, JSONEncoder
from collections import defaultdict, OrderedDict
import random

SAMPLE_SIZE = 10
graph_collection_manager = GraphCollectionManager()


@app.route("/graphs/<graph_id>")
def get_pool(graph_id):
    return render_template('base.html')
    graph_id = to_object_id(graph_id)
    src_images = pcoll.getSampleOfImages(graph_id, 1000, previewOnly=True)
    class_images = defaultdict(list)
    neg_images = []
    for img in src_images:
        if 'valid_image' not in img or not img['valid_image']:
            continue
        #pos_images.append(img)
        pool_info = [p for p in img['pools'] if p['poolId'] == pool_id][0]
        class_images[pool_info['target']].append(img)

    targets = class_images.keys()
    for k in targets:
        class_len = len(class_images[k])
        class_images[k] = random.sample(class_images[k], min(SAMPLE_SIZE, class_len))

    models = list(mcoll.getModelsByPoolId(pool_id))
    pool = pcoll.getPool(pool_id)[0]

    properties = OrderedDict()
    properties['Pool Size'] = pcoll.getPoolSize(pool_id)
    properties['Pool Size (Valid images)'] = pcoll.getPoolSize(pool_id, valid_only=True)
    properties['Created'] = pool['date_inserted']
    properties['Targets'] = ', '.join(map(str, class_images.keys()))

    app.logger.info(models)
    return render_template('pool.html', pool=pool, class_images=class_images, models=models, properties=properties)


@app.route('/plynx/api/v0/graphs/<graph_id>', methods=['GET'])
def get_graph(graph_id):
    graph = graph_collection_manager.get_db_graph(graph_id)
    for block in graph['blocks']:
        block['block_running_status'] = BLOCK_RUNNING_STATUS_MAP[block['block_running_status']]
    return JSONEncoder().encode({'data': graph_collection_manager.get_db_graph(graph_id), 'status':'success'})
