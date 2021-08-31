import subprocess
import json


def parse(text):
    # command = ['node', '../latex-utensils/out/src/bin/luparse.js', 'tmp.tex']
    # with open('tmp.tex', 'w') as f:
    #     f.write(text)

    if ' \\ % ' in text:
        text = text.replace(' \\ % ', ' \\% ')
    # with open('tmp.tex', 'w') as f:
    #     f.write(text)

    command = ['node', '../latex-utensils/out/src/bin/parse.js', text]
    result = subprocess.check_output(command)

    result = json.loads(result)
    return result


_SCRIPT_OP = {
    'superscript': '^',
    'subscript': '_',
}

_SPECIAL_CHARS = {
    'space': ' ',
    'softbreak': '\n',
    'activeCharacter': '~',
    'alignmentTab': '\t',
}


class LatexDoc():

    def __init__(self, text, obj):
        super(LatexDoc, self).__init__()
        self.text = text
        self.obj = obj
        self.flat_tokens = []
        self.flat_token_char_indices = []
        self.flatten(obj)
        self.align()

    def 

    def flatten(self, obj):
        kind = obj['kind']
        arg = obj['arg'] if 'arg' in obj else None
        args = obj['args'] if 'args' in obj else None
        name = obj['name'] if 'name' in obj else None
        content = obj['content'] if 'content' in obj else None
        # print(kind)
        # print(content)

        if kind == 'ast.root':
            for child in content:
                self.flatten(child)

        elif kind == 'displayMath':
            for child in content:
                self.flatten(child)

        elif kind in ['text.string', 'math.character']:
            self.flat_tokens.append(content)

        elif kind in _SPECIAL_CHARS:
            self.flat_tokens.append(_SPECIAL_CHARS[kind])

        elif kind == 'linebreak':
            self.flat_tokens.append(name)

        elif kind in _SCRIPT_OP:
            self.flat_tokens.append(_SCRIPT_OP[kind])
            if arg:
                self.flatten(arg)

        elif kind == 'inlineMath':
            self.flat_tokens.append('$')
            for child in content:
                self.flatten(child)
            self.flat_tokens.append('$')

        elif kind == 'arg.group':
            self.flat_tokens.append('{')
            for child in content:
                self.flatten(child)
            self.flat_tokens.append('}')

        elif kind == 'command':
            self.flat_tokens += ['\\', name]
            for child in args:
                self.flatten(child)

        elif kind == 'command.label':
            if name == 'ref':
                self.flat_tokens += ['\\', 'ref', '{', obj['label'], '}']

        elif kind == 'command.text':
            self.flat_tokens += ['\\', 'text']
            self.flatten(obj['arg'])

        elif kind == 'command.href':
            self.flat_tokens += ['\\', name, '{', obj['url'], '}', '{']
            for child in content:
                self.flatten(child)
            self.flat_tokens.append('}')

        elif kind == 'command.url':
            self.flat_tokens += ['\\', name, '{', obj['url'], '}']

        elif kind == 'env':
            self.flat_tokens += ['\\', 'begin', '{', name, '}']
            if args:
                for child in args:
                    self.flatten(child)
            if content:
                for child in content:
                    self.flatten(child)
            self.flat_tokens += ['\\', 'end', '{', name, '}']

        elif kind == 'arg.optional':
            self.flat_tokens.append('[')
            for child in content:
                self.flatten(child)
            self.flat_tokens.append(']')

        elif kind == 'math.math_delimiters':
            lcommand = obj['lcommand']
            rcommand = obj['rcommand']
            left = obj['left']
            right = obj['right']
            self.flat_tokens.append(left)
            for child in content:
                self.flatten(child)
            self.flat_tokens.append(right)

        elif kind == 'math.matching_delimiters':
            left = obj['left']
            right = obj['right']
            self.flat_tokens.append(left)
            for child in content:
                self.flatten(child)
            self.flat_tokens.append(right)

        elif kind == 'env.math.align' or kind == 'env.math.aligned':
            name = name
            self.flat_tokens += ['\\', 'begin', '{', name, '}']
            if args:
                for child in args:
                    self.flatten(child)
            if content:
                for child in content:
                    self.flatten(child)
            self.flat_tokens += ['\\', 'end', '{', name, '}']
        else:
            print('Unknown kind: ', kind)
            print(obj)

    def align(self):
        offset = 0
        for token in self.flat_tokens:
            i = self.text[offset:].find(token)
            if i > -1:
                offset += i
                self.flat_token_char_indices.append((offset, offset + len(token)))
                offset += len(token)
            else:
                print('Cannot find: ', token, offset, self.text[offset:30])
                self.flat_token_char_indices.append((None, None))


def realignment(text, flat_tokens):


def test_all():
    import glob
    for json_file in glob.glob('../data/train/*.json'):

        with open(json_file) as f:
            data = json.load(f)
        for k, v in data.items():
            # try:
            print(k)
            json_obj = parse(v['text'])
            d = LatexDoc(v['text'], json_obj)
        # except:
        #     pass


def test_one():
    import glob
    for json_file in glob.glob('../data/train/*.json'):

        with open(json_file) as f:
            data = json.load(f)
        for k, v in data.items():
            if k == '1807.09728v2.Adaptive_locally_linear_models_of_complex_dynamics/paragraph_30':
                json_obj = parse(v['text'])
                with open('tmp.json', 'w') as f:
                    json.dump(json_obj, f, indent=2)

                d = LatexDoc(v['text'], json_obj)

                realignment(d.text, d.flat_tokens)


if __name__ == '__main__':
    # test_all()
    test_one()
