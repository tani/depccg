
import argparse
from depccg.tools.reader import read_trees_guess_extension
from depccg.printer import print_
from depccg.tokens import japanese_annotator
from depccg.download import SEMANTIC_TEMPLATES
import logging

logger = logging.getLogger(__name__)

LANG = 'ja'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PATH',
                        help='path to either of *.auto, *.xml, *.jigg.xml, *.ptb')
    parser.add_argument('--annotator',
                        default='janome',
                        choices=japanese_annotator.keys(),
                        help='annotate POS, named entity, and lemmas using this library')
    parser.add_argument('-f',
                        '--format',
                        default='jigg_xml',
                        choices=['prolog', 'jigg_xml', 'jigg_xml_ccg2lambda', 'json'],
                        help='output format')
    parser.add_argument('--semantic-templates',
                        help='semantic templates used in "ccg2lambda" format output')
    args = parser.parse_args()

    annotate_fun = japanese_annotator[args.annotator]
    doc, trees = [], []
    for _, tokens, tree in read_trees_guess_extension(args.PATH, lang='ja'):
        doc.append([token.surf for token in tokens])
        trees.append([(tree, 0)])
    tagged_doc = annotate_fun(doc, tokenize=False)

    semantic_templates = args.semantic_templates or SEMANTIC_TEMPLATES[LANG]
    print_(trees,
           tagged_doc,
           format=args.format,
           lang=LANG,
           semantic_templates=semantic_templates)