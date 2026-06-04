# -*- coding: utf-8 -*-
with open('E:/myresume/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find ALL occurrences of bg and probes sections
import re

# First, let's identify the structure by finding key markers
rag_end = html.find('id="tab-rag"')
rag_close = html.find('</div>', html.find('</section>', rag_end))

# Find bg sections
bg_starts = [m.start() for m in re.finditer(r'<section id="bg">', html)]
probes_starts = [m.start() for m in re.finditer(r'<section id="probes">', html)]

print(f"Found {len(bg_starts)} bg sections, {len(probes_starts)} probes sections")

# Strategy:
# 1. Extract the FIRST bg+probes content (the real one)
# 2. Remove ALL bg+probes sections
# 3. Create a new tab with the extracted content

# Find the first bg section (should be the real one, inside or near tab-rag)
bg1_start = bg_starts[0]

# Find where the content ENDS - look for the closing of the probes section
# We need to find the </section> of probes and then what comes after
# The probes section ends at either the next section start or </main>

for probes_start in probes_starts:
    probes_close = html.find('</section>', probes_start)
    # Check if probes_close has another section after it
    next_section = html.find('<section ', probes_close)
    next_div = html.find('<div class="tab-content"', probes_close)
    next_main = html.find('</main>', probes_close)

    # The probes section ends at the earliest of <section, <div class="tab-content, </main>
    possible_ends = [e for e in [next_section, next_div, next_main] if e > 0]
    if possible_ends:
        probes_end = min(possible_ends)
    else:
        probes_end = next_main

    # Extract the content from bg_start to probes_end
    probes_end = html.rfind('</div></div>', probes_close, probes_close + 2000)
    if probes_end < 0:
        probes_end = html.find('</section>', probes_close) + len('</section>')
    else:
        probes_end += len('</div></div>')

print(f"First bg starts at: {bg1_start}")
print(f"Probes content ends near: {probes_end}")
