# 1. universal Markdown element
[uniersalMarkdown.py](uniersalMarkdown.py)

main code is supplied by sonnygeorge on https://github.com/zauberzeug/nicegui/discussions/696, thank you.

I am too lazy to split markdown text into various elements. What I am dreaming is a universal Markdown element which can support as many features as https://support.typora.io/ does. But at least the following features

| feature               | support?                                                     |
| --------------------- | ------------------------------------------------------------ |
| heading               | yes                                                          |
| in-line formula       | yes                                                          |
| block formula         | yes                                                          |
| table                 | yes                                                          |
| code highlight        | yes                                                          |
| pie chart via mermaid | yes<br> I know nicegui support matplotlib                    |
| flowchart via mermaid | yes but not a good one<br>Mermaid uses curve instead of straight line |

[uniersalMarkdown.py](uniersalMarkdown.py) is what I get currently. Please note
- I use JavaScripts which is stored on my local disk due to my internet connection problem
- the official `md_mermaid` extension have 2 bugs
      - it deletes all unicode char
      - it inserts html head later, which is not supported by NiceGUI
- if I comment out the call of `ui.markdown`, some of the `mermaid` strings can not be plotted in my code
- the code uses `~~~mermaid ... ~~~` to define `mermaid` block which is valid syntax in some markdown parser, however it could be better if
<pre>
```mermaid
  something
``` 
</pre>
is supportted
