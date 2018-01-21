# coding: utf-8
import re
text = 'sydvbwns<"pmid">3479264<"najs>'
PMID = r'pmid">(\d+)<'
res = re.search(PMID, text)
print(res.group(1))