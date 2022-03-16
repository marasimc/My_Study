# hanlp_trie的用法

作业：提取文本中的关键词

```python
from hanlp_trie import Trie

text = ''

trie_item = {}
trie = Trie(trie_item)
parse_result = trie.parse(text)
```



```python
from hanlp_trie import Trie


trie_item = {}

trie_item['白酒'] = [1,2,3]
trie_item['土木工程'] = ['a', 'b']
trie_item['能源'] = ['h','j']
trie_item['目前'] = ['aa','bb']

trie = Trie(trie_item)

data = {
        "title":"【林洋能源：目前与乌克兰公司合作项目正常履行】",
        "text":"【林洋能源：目前与乌克兰公司合作项目正常履行】财联社2月24日电，财联社记者从林洋能源获悉，截至目前，公司与乌克兰公司的合作项目还在正常履行中。公司持续关注当前局势发展，未来如果受到影响会进行披露。据此前公告，林洋能源子公司2021年12月中标乌克兰DTEK公司智能电能表招标项目。（记者 刘梦然）",
        }

parse_result = trie.parse(data['text'])

print(parse_result)
'''
[(3, 5, ['h', 'j']), (6, 8, ['aa', 'bb']), (41, 43, ['h', 'j']), (48, 50, ['aa', 'bb']), (107, 109, ['h', 
'j'])]
'''


concept_tmp = {}      # 匹配到的所有概念
for item in parse_result: 
    concept_name = text[item[0]: item[1]]
    if concept_name not in concept_tmp:
        concept_tmp[concept_name] = {}
        concept_tmp[concept_name]['stock_code_list'] = item[2]
        concept_tmp[concept_name]['index'] = []
        concept_tmp[concept_name]['index'].append((item[0], item[1]))
    else:
        concept_tmp[concept_name]['index'].append((item[0], item[1]))

print(concept_tmp)
'''
{'能源': {'stock_code_list': ['h', 'j'], 'index': [(3, 5), (41, 43), (107, 109)]}, '目前': {'stock_code_list': ['aa', 'bb'], 'index': [(6, 8), (48, 50)]}}
'''
```

