from typing import List, Optional
from lxml import etree
from depccg.tree import Tree, ScoredTree
from depccg.tokens import Token


def _process_tree(tree: Tree, tokens: Optional[List[Token]] = None) -> etree.Element:

    def rec(node, parent):

        if node.is_leaf:
            leaf_node = etree.SubElement(parent, 'lf')
            start, token = tokens.pop(0)
            leaf_node.set('start', str(start))
            leaf_node.set('span', '1')
            leaf_node.set('cat', str(node.cat))
            for k, v in token.items():
                leaf_node.set(k, v)
        else:
            rule_node = etree.SubElement(parent, 'rule')
            rule_node.set('type', node.op_string)
            rule_node.set('cat', str(node.cat))
            for child in node.children:
                rec(child, rule_node)

    if tokens is None:
        tokens = [
            Token.from_word(word) for word in tree.word.split(' ')
        ]

    tokens = list(enumerate(tokens))
    result = etree.Element("ccg")
    rec(tree, result)

    return result


def xml_of(
    nbest_trees: List[List[ScoredTree]],
    tagged_doc: List[List[Token]],
) -> etree.Element:
    """convert parsing results to a XML etree.Element in a format commonly used by C&C.

    Args:
        nbest_trees (List[List[ScoredTree]]): parsing results
        tagged_doc (List[List[Token]]): corresponding lists of tokens

    Returns:
        etree.Element: XML object
    """

    candc_node = etree.Element('candc')
    for sentence_index, (trees, tokens) in enumerate(zip(nbest_trees, tagged_doc), 1):
        for tree_index, (tree, _) in enumerate(trees, 1):
            out = _process_tree(tree, tokens)
            out.set('sentence', str(sentence_index))
            out.set('id', str(tree_index))
            candc_node.append(out)

    return candc_node