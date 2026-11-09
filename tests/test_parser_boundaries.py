"""Run from the repository root: python3 -B -m unittest discover -s tests -v."""

import unittest

from Lexer import Lexer, Token, TokenT
from parser import Parser


def lex(source, include_eof=False):
    lexer = Lexer(source)
    tokens = []
    while True:
        token = lexer.next_token()
        if token.type == TokenT.EOF:
            if include_eof:
                tokens.append(token)
            return tokens
        tokens.append(token)


SAMPLE = """! Convert Fahrenheit into Celsius. !
function convert (fahr integer)
{
    return 5 * (fahr - 32) / 9;
}
@
integer low, high, step;
@
get(low, high, step);
while (low <= high)
{
    put(low);
    put(convert(low));
    low = low + step;
}
"""


class ParserBoundaryTests(unittest.TestCase):
    def assert_valid(self, source):
        for include_eof in (False, True):
            with self.subTest(source=source, include_eof=include_eof):
                parser = Parser(lex(source, include_eof))
                parser.rat26f()
                self.assertEqual(parser.current_token.type, TokenT.EOF)
                self.assertEqual(parser.token_index, len(parser.tokens))

    def assert_invalid(self, source):
        for include_eof in (False, True):
            with self.subTest(source=source, include_eof=include_eof):
                with self.assertRaises(SyntaxError):
                    Parser(lex(source, include_eof)).rat26f()

    def test_boolean_global_declarations(self):
        self.assert_valid('@ boolean flag; @ flag=true;')
        self.assert_valid('@ integer x; boolean flag; real y; @ flag=false;')

    def test_boolean_function_parameters_and_locals(self):
        self.assert_valid('function f(flag boolean){return flag;} @ @ return;')
        self.assert_valid('function f(a,b boolean,c integer) boolean flag; {flag=true; return flag;} @ @ return;')

    def test_official_sample(self):
        self.assert_valid(SAMPLE)

    def test_all_statement_forms(self):
        self.assert_valid('@ integer x,y; @ get(x,y); {x=1+2*3;} if(x>=y) put(x); else return; fi while(x!=y) x=x-1; return x;')

    def test_trailing_tokens_are_rejected(self):
        for suffix in ('@', '$', 'else', 'fi', '}', ';', '123', 'boolean', '! unfinished comment'):
            self.assert_invalid('@ @ x=1; ' + suffix)

    def test_unknown_tokens_inside_program(self):
        for source in ('@ @ x=$;', '@ @ $ x=1;', '@ integer $; @ return;'):
            self.assert_invalid(source)

    def test_empty_or_truncated_programs(self):
        for source in (
            '', ' ', '! comment !', '@', '@ @', 'function', 'function f',
            'function f(', 'function f(a', 'function f(a,',
            'function f(a boolean', 'function f() boolean',
            'function f(){', 'function f(){return;',
            '@ boolean', '@ boolean flag', '@ boolean flag,',
            '@ @ x', '@ @ x=', '@ @ x=1', '@ @ x=1+',
            '@ @ x=(1', '@ @ x=f(', '@ @ x=f(a', '@ @ x=f(a,',
            '@ @ get', '@ @ get(', '@ @ get(x', '@ @ get(x)',
            '@ @ put(', '@ @ put(1', '@ @ put(1)',
            '@ @ return', '@ @ return 1', '@ @ { return;',
            '@ @ if(x==1) return;', '@ @ if(x==1) return; else',
            '@ @ while', '@ @ while(x', '@ @ while(x<1',
            '@ @ while(x<1)', '@ @ while(x<1) x=1',
        ):
            self.assert_invalid(source)

    def test_missing_required_parts(self):
        for source in (
            '@ @ x=;', '@ @ put();', '@ @ if() return; fi',
            '@ @ while() return;', '@ @ get();', '@ @ x=f();',
            '@ @ x=f(1);', '@ @ x=f(x+1);', '@ @ {}',
        ):
            self.assert_invalid(source)

    def test_eof_is_stable_after_exhaustion(self):
        for include_eof in (False, True):
            parser = Parser(lex('@ @ return;', include_eof))
            parser.rat26f()
            for _ in range(3):
                self.assertEqual(parser.next_token().type, TokenT.EOF)

    def test_empty_stream_returns_eof(self):
        parser = Parser([])
        self.assertEqual(parser.current_token.type, TokenT.EOF)
        self.assertEqual(parser.next_token().type, TokenT.EOF)
        self.assertEqual(parser.next_token().type, TokenT.EOF)

    def test_input_list_is_not_modified(self):
        for include_eof in (False, True):
            tokens = lex('@ @ return;', include_eof)
            original = list(tokens)
            Parser(tokens).rat26f()
            self.assertEqual(tokens, original)

    def test_premature_eof_does_not_hide_tokens(self):
        for tail in (lex('x=2;'), [Token(TokenT.EOF, '')]):
            with self.assertRaises(SyntaxError):
                Parser(lex('@ @ return;', True) + tail).rat26f()


if __name__ == '__main__':
    unittest.main()
