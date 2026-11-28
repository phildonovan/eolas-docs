"""Tidy the rendered HTML before mkdocs-llmstxt turns it back into markdown.

Two things get lost without this:

* Material's content tabs ("Python", "R", "curl"): the labels are dropped, so the
  code blocks end up one after another with nothing saying which is which.
* A "|" inside a table cell ends the cell, so a cell like "json | csv | arrow"
  was cut after its first value.
"""


def preprocess(soup, output):  # noqa: ARG001
    for tabset in soup.select("div.tabbed-set"):
        labels = [label.get_text(strip=True) for label in tabset.select("div.tabbed-labels > label")]
        blocks = tabset.select("div.tabbed-content > div.tabbed-block")
        for label, block in zip(labels, blocks):
            heading = soup.new_tag("p")
            strong = soup.new_tag("strong")
            strong.string = label
            heading.append(strong)
            block.insert(0, heading)

    for cell in soup.select("td, th"):
        for node in list(cell.find_all(string=True)):
            if "|" in node:
                node.replace_with(node.replace("|", "/"))

    # What the plugin's autoclean would have removed (minus the tab labels, handled above).
    for tag in soup.find_all(["img", "svg"]):
        parent = tag.parent
        tag.decompose()
        if parent is not None and parent.name == "a" and not parent.get_text(strip=True):
            parent.decompose()
    for tag in soup.select("a.headerlink, .twemoji, div.tabbed-labels"):
        tag.decompose()
