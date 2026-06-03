with open('E:/myresume/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix agent-shop closing: add missing </section>
old = '迭代周期从3天变成3周。</p></div></div>\n\t</div>\n\t</main>'
new = '迭代周期从3天变成3周。</p></div></div>\n\t</section>\n\t</div>\n\t</main>'

if old in html:
    html = html.replace(old, new, 1)
    with open('E:/myresume/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('OK - fixed agent-shop closing')
else:
    # Try without tabs
    old2 = '迭代周期从3天变成3周。</p></div></div>\n</div>\n</main>'
    if old2 in html:
        html = html.replace(old2, '迭代周期从3天变成3周。</p></div></div>\n</section>\n</div>\n</main>', 1)
        with open('E:/myresume/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('OK - fixed with no-tabs version')
    else:
        print('Pattern not found')
        # Debug: show surrounding chars
        idx = html.find('迭代周期从3天变成3周')
        if idx >= 0:
            print(repr(html[idx:idx+100]))
