import re

from markdown import Markdown
from nicegui import ui, app

app.add_static_files('/js', 'js')

HIGHLIGHT_STYLE = "background: #f5f5f5; border-radius: 0.2rem;"
HIGHLIGHT_STYLE += "padding: 0.2rem 0.3rem 0.2rem 0.3rem;"


def markdown_to_html_with_math(markdown_text: str) -> str:
    md_parser = Markdown(
        extensions=[
            "pymdownx.superfences",
            "pymdownx.highlight",
            "pymdownx.arithmatex",
            "pymdownx.inlinehilite",
            'pymdownx.extra',
            'md_mermaid', # 需要修改源码
        ],
        extension_configs={
            "pymdownx.inlinehilite": {
                "style_plain_text": True,
            },
            "pymdownx.highlight": {
                "guess_lang": False,
                "noclasses": True,
            },
            "pymdownx.arithmatex": {
                "smart_dollar": False,
                "preview": True,
                "generic": True,
            },
            'pymdownx.extra': {
                'markdown.extensions.tables': {
                    'use_align_attribute': True
                }
            },
            #~ 'md_mermaid.md_mermaid':{},


        },
    )
    return md_parser.convert(markdown_text)


def apply_tailwind(html: str) -> str:  # Borrowed from NiceGUI's ui.markdown
    rep = {
        "<h1": '<h1 class="text-5xl mb-4 mt-6"',
        "<h2": '<h2 class="text-4xl mb-3 mt-5"',
        "<h3": '<h3 class="text-3xl mb-2 mt-4"',
        "<h4": '<h4 class="text-2xl mb-1 mt-3"',
        "<h5": '<h5 class="text-1xl mb-0.5 mt-2"',
        "<a": '<a class="underline text-blue-600 hover:text-blue-800 visited:text-purple-600"',  # noqa: E501
        "<ul": '<ul class="list-disc ml-6"',
        "<p>": '<p class="mb-2">',
    }
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], html)


def apply_custom_highlight_style(html: str) -> str:  # Would be better w/ re
    classes_to_highlight = ["highlight"]
    for class_name in classes_to_highlight:
        html = html.replace(
            f'class="{class_name}"',
            f'class="{class_name}" style="{HIGHLIGHT_STYLE}"',
        )
    return html


def markdown(text: str) -> ui.html:
    html = markdown_to_html_with_math(text)
    html = apply_tailwind(html)
    html = apply_custom_highlight_style(html)
    for key, value in {
        "<table": "<table border=1",
        '<th>': '<th style="border:1px solid red;">',   # 因为有<thread
        '<th ': '<th style="border:1px solid red;"',   # 因为有<th align
        '<td>': '<td style="border:1px solid red;">',
        '<td ': '<td style="border:1px solid red;"',   # 因为有 <td align

        # a quick&dirty solution
        '​~~~mermaid': '<div class="mermaid">',
        '\n~~~\n': '\n</div>\n',

    }.items():
        html = html.replace(key, value)
    return ui.html(html)


if __name__ in {"__main__", "__mp_main__"}:
    # The presence of these scripts in page body is necessary for MathJax to render
    #~ mathjax_scripts = """
    #~ <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    #~ <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    #~ """

    mathjax_scripts = """
    <script src="./js/polyfill.min.js?features=es6"></script>
    <script src="./js/tex-chtml.js"></script>
    """

    ui.add_body_html(mathjax_scripts)

    mermaid_scripts = r'''
    <script src="./js/mermaid.min.js"></script>
    <script>
                    function initializeMermaid() {
                        mermaid.initialize({startOnLoad:true})
                    }

                    if (document.readyState === "complete" || document.readyState === "interactive") {
                        setTimeout(initializeMermaid, 1);
                    } else {
                        document.addEventListener("DOMContentLoaded", initializeMermaid);
                    }
            </script>
    '''

    ui.add_body_html(mermaid_scripts)

    # Raw string is important for parser to not remove '\b', '\t', etc. from math
    example_md_text = r"""
This is inline code: `hello world`

This is block code:

(add your own since putting backticks here would confuse GitHub)

This is inline math: $\text{det}(A)$

This is block math:

$$ A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} $$


$c = \pm\sqrt{a^2 + b^2}$

This is a gif:

![silly cat](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)


| x    | y    | mean        |
| ---- | ---- | ------------: |
| 1    | 234  | hello |
| 2    | 234  | world       |
| 3    | 234  | hello world       |

```python
for i in range(10):
    print(i)
```
下面的未指定语言
```
for i in range(10):
    print(i)
```

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

\[3 < 4\]

\begin{align}
    p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
    p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
\end{align}


\begin{equation}
  x = a_0 + \frac{1}{\displaystyle a_1
          + \frac{1}{\displaystyle a_2
          + \frac{1}{\displaystyle a_3 + a_4}}}
\end{equation}


\(\frac{1}{(\sqrt{\phi \sqrt{5}}-\phi) e^{\frac{2}{5} \pi}}=1+\frac{e^{-2 \pi}}{1+\frac{e^{-4 \pi}}{1+\frac{e^{-6 \pi}}{1+\frac{e^{-8 \pi}}{1+\cdots}}}}\)
# Title

Some text.



~~~mermaid
graph LR;
    A --> B;
    A --> C;
~~~

~~~mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D结束;
    C-->D结束;
~~~

~~~mermaid
timeline
    title History of Social Media Platform
    2002 : LinkedIn
    2004 : Facebook
         : Google
    2005 : Youtube
    2006 : Twitter
~~~

the following demos can't be rendered as expected

~~~mermaid
flowchart TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
~~~


~~~mermaid
pie showData
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" :  5
~~~
"""


    markdown(example_md_text)

    ui.separator()
    ui.label('Following use ui.mermaid')


    #~ ui.mermaid('''
#~ ---
#~ title: Hello Title
#~ config:
  #~ theme: base
  #~ themeVariables:
    #~ primaryColor: "#00ff00"
#~ ---
#~ flowchart
	#~ Hello --> World
#~ ''')

    #~ ui.mermaid('''flowchart TD
    #~ A[Start] --> B{Is it?}
    #~ B -- Yes --> C[OK]
    #~ C --> D[Rethink]
    #~ D --> B
    #~ B -- No ----> E[End]''')


    #~ ui.mermaid('''
#~ mindmap
  #~ root((mindmap))
    #~ Origins
      #~ Long history
      #~ ::icon(fa fa-book)
      #~ Popularisation
        #~ British popular psychology author Tony Buzan
    #~ Research
      #~ On effectiveness<br/>and features
      #~ On Automatic creation
        #~ Uses
            #~ Creative techniques
            #~ Strategic planning
            #~ Argument mapping
    #~ Tools
      #~ Pen and paper
      #~ Mermaid
#~ ''')

    #~ ui.mermaid('''
#~ %%{init: {"pie": {"textPosition": 0.8}, "themeVariables": {"pieOuterStrokeWidth": "5px"}} }%%
#~ pie showData
    #~ title Key elements in Product X
    #~ "Calcium" : 42.96
    #~ "Potassium" : 50.05
    #~ "Magnesium" : 10.01
    #~ "Iron" :  5
#~ ''')



    ui.run()


