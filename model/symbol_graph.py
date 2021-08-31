import json
import subprocess
from anytree import Node, RenderTree

def parse(latex_code):
    cmd  = 'rm tmp.tex'
    subprocess.call(cmd.split(' '))

    subprocess.call('pwd')
    with open('tmp.tex','w') as f:
        f.write(latex_code)

    result = subprocess.check_output('./latex-utensils/bin/luparse tmp.tex'.split(' '))
    data = json.loads(result)

    return data

def make_anytree(json_obj, parent=None):
    if 'content' in json_obj:
        if isinstance(json_obj['content'], str):
            node_name= json_obj['content']
        else:
            node_name=json_obj['kind']
    else:
        node_name = json_obj['kind']
    new_node = Node(node_name, parent=parent)
    if 'content' in json_obj:
        for child in json_obj['content']:
            if 'kind' in child:
                child_node = make_anytree(child, new_node)
    return new_node




if __name__ == '__main__':
    json_obj = parse('$S\'=(\cdots,[MASK],w_{k_i},\cdots,w_{k_i+M},[MASK],\cdots)$')
    tree = make_anytree(json_obj)
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))