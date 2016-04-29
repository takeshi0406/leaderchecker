# leaderchecker

Twitterのリツイート関係をネットワーク解析して、オピニオンリーダーを簡単に見つけるためのライブラリです。

Twitterを検索し、その人がリツイートしているユーザー（≒情報源として信頼している:人）のアカウントを辿って、ネットワークとして構成します。
その後各ユーザーのページランクを計算します。

# Description

各ユーザーのページランクをpandasのデータフレームとして格納するサンプルコード。

```
import pandas as pd
import leaderchecker as lc

tw_confing = {
    'token': 'your twitter access token',
    'token_secret': 'your twitter access token secret',
    'consumer_key': 'your twitter consumer key',
    'consumer_secret': 'your twitter consumer secret'
    }
oauth = lc.OAuth(**tw_config)
client = lc.LeaderChecker(oauth)
client.search_seed_accounts(word='pydata')
client.build_community_structure()
result = client.get_members_pagerank()
dataframe = pd.DataFrame(result)
```

# Installation

```
pip install git+https://github.com/takeshi0406/leaderchecker
```
