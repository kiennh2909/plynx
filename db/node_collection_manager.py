from . import Node
from utils.common import to_object_id
from utils.db_connector import *


class NodeCollectionManager(object):
    """
    """

    @staticmethod
    def get_db_nodes(author, status=None, per_page=20, offset=0, base_node_names=None):
        if status and isinstance(status, basestring):
            status = [status]
        if base_node_names and isinstance(base_node_names, basestring):
            base_node_names = [base_node_names]

        and_query = []
        and_query.append({
            '$or': [
                {'author': author},
                {'public': True}
            ]})
        if base_node_names:
            and_query.append({'base_node_name': {'$in': base_node_names}})
        if status:
            and_query.append({'node_status': {'$in': status}})

        db_nodes = db.nodes.find({
            '$and': and_query
        }).sort('insertion_date', -1).skip(offset).limit(per_page)

        res = []
        for node in db_nodes:
            node['_readonly'] = (author != to_object_id(node['author']))
            res.append(node)
        return res

    @staticmethod
    def get_db_nodes_by_ids(ids):
        db_nodes = db.nodes.find({
            '_id': {
                '$in': list(ids)
                }
            })

        return list(db_nodes)

    @staticmethod
    def get_db_nodes_count(author, status=None, base_node_names=None):
        if status and isinstance(status, basestring):
            status = [status]
        if base_node_names and isinstance(base_node_names, basestring):
            base_node_names = [base_node_names]

        and_query = []
        and_query.append({
            '$or': [
                {'author': author},
                {'public': True}
            ]})
        if base_node_names:
            and_query.append({'base_node_name': {'$in': base_node_names}})
        if status:
            and_query.append({'node_status': {'$in': status}})

        if not status:
            return db.nodes.count({
                '$and': and_query
                })
        else:
            return db.nodes.count({
                '$and': and_query
                })

    @staticmethod
    def get_db_node(node_id, author = None):
        res = db.nodes.find_one({'_id': to_object_id(node_id)})
        if res:
            res['_readonly'] = (author != to_object_id(res['author']))
        return res
