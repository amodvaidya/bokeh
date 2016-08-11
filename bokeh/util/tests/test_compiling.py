from __future__ import absolute_import

from bokeh.util.compiling import nodejs_compile

def test_nodejs_compile_coffeescript():
    assert nodejs_compile("""(a, b) -> a + b""", "coffeescript", "some.coffee") == \
        dict(code="""(function(a, b) {\n  return a + b;\n});\n""", deps=[])

    assert nodejs_compile("""some = require 'some/module'""", "coffeescript", "some.coffee") == \
        dict(code="""var some;\n\nsome = require('some/module');\n""", deps=["some/module"])

    assert nodejs_compile("""(a, b) -> a + b +""", "coffeescript", "some.coffee") == \
        dict(error=dict(
            message="unexpected end of input",
            text="some.coffee:unexpected end of input"))

    assert nodejs_compile("""some = require some/module'""", "coffeescript", "some.coffee") == \
        dict(error=dict(
            line=1,
            column=27,
            message="missing '",
            text="some.coffee:1:27:missing '",
            extract="some = require some/module'",
            annotated="some.coffee:1:27:missing '\n  some = require some/module'\n                            ^"))

    assert nodejs_compile("""(a, b) -> a + b +""", "coffeescript", "some.coffee") == \
        dict(error=dict(
            message="unexpected end of input",
            text="some.coffee:unexpected end of input"))

    assert nodejs_compile("""some = require some/module'""", "coffeescript", "some.coffee") == \
        dict(error=dict(
            line=1,
            column=27,
            message="missing '",
            text="some.coffee:1:27:missing '",
            extract="some = require some/module'",
            annotated="some.coffee:1:27:missing '\n  some = require some/module'\n                            ^"))

def test_nodejs_compile_javascript():
    assert nodejs_compile("""function f(a, b) { return a + b; };""", "javascript", "some.js") == \
        dict(code="""function f(a, b) { return a + b; };""", deps=[])

    assert nodejs_compile("""var some = require('some/module');""", "javascript", "some.js") == \
        dict(code="""var some = require('some/module');""", deps=["some/module"])

    assert nodejs_compile("""function f(a, b) { eturn a + b; };""", "javascript", "some.js") == \
        dict(error=dict(
            line=1,
            column=25,
            message="Unexpected token",
            text="some.js:1:25:Unexpected token"))

def test_nodejs_compile_less():
    assert nodejs_compile(""".bk-some-style { color: green; }""", "less", "some.less") == \
        dict(code=""".bk-some-style{color:green}""")

    assert nodejs_compile(""".bk-some-style color: green; }""", "less", "some.less") == \
        dict(error=dict(
            line=1,
            column=21,
            message="Unrecognised input",
            text="some.less:1:21:Unrecognised input",
            extract=".bk-some-style color: green; }",
            annotated="some.less:1:21:Unrecognised input\n  .bk-some-style color: green; }"))
