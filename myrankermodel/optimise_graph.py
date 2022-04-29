import os
import tensorflow as tf
sesh = tf.InteractiveSession()

from bert_serving.server.graph import optimize_graph
from bert_serving.server.helper import get_args_parser

# input dir
MODEL_DIR = 'D:/PFE-realisat/myrankermodel/model/uncased_L-12_H-768_A-12/uncased_L-12_H-768_A-12' #@param {type:"string"}
# output dir
GRAPH_DIR = 'D:/PFE-realisat/myrankermodel//model/graph/' #@param {type:"string"}
# output filename
GRAPH_OUT = 'extractor.pbtxt' #@param {type:"string"}

POOL_STRAT = 'REDUCE_MEAN' #@param ['REDUCE_MEAN', 'REDUCE_MAX', "NONE"]
POOL_LAYER = '-2' #@param {type:"string"}
SEQ_LEN = '256' #@param {type:"string"}
do_lower_case = False
# tf.io.gfile.mkdir(GRAPH_DIR)

parser = get_args_parser()
carg = parser.parse_args(args=['-model_dir', MODEL_DIR,
                               '-graph_tmp_dir', GRAPH_DIR,
                               '-max_seq_len', str(SEQ_LEN),
                               '-pooling_layer', str(POOL_LAYER),
                               '-pooling_strategy', str(POOL_STRAT)])
if carg :
    print('True')
    print(carg)
    tmp_name, config = optimize_graph(carg)
    graph_fout = os.path.join(GRAPH_DIR, GRAPH_OUT)

    tf.gfile.Rename(
        tmp_name,
        graph_fout,
        overwrite=True
    )
    print("\nSerialized graph to {}".format(graph_fout))
else:
    print('false')
