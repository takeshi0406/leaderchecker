import twitter
import networkx as nx


class LeaderChecker:

    def __init__(self, auth):
        self.set_client(auth)
        self.graph = nx.DiGraph()
        self.seed_accounts = set()
        self.checked_accounts = set()

    def set_client(self, oauth):
        self.client = twitter.Twitter(auth=oauth)

    def set_seed_accounts(self, accounts):
        self.seed_accounts = set(accounts)

    def update_seed_accounts(self, accounts):
        self.seed_accounts.update(accounts)

    def search_seed_accounts(self, word, count=10, lang=None):
        tweets = self._search_tweets(word, count, lang)
        members = self._find_screen_names(tweets)
        self.set_seed_accounts(members)

    def build_community_structure(self, trials=10, bulk=5):
        self._check_seed_accounts()
        for t in range(trials):
            for target in self._find_next_targets(bulk):
                self._check_target_edge(target)

    def get_members_degree(self):
        degrees = self.graph.in_degree()
        return [self._to_centricity_dict(t, c, 'degree')
                for t, c in degrees.items()]

    def get_members_pagerank(self, alpha=0.8):
        pageranks = nx.pagerank_numpy(self.graph, alpha=alpha)
        return [self._to_centricity_dict(t, c, 'pagerank')
                for t, c in pageranks.items()]

    def _check_seed_accounts(self):
        for target in self.seed_accounts:
            if target not in self.checked_accounts:
                self._check_target_edge(target)

    def _find_next_targets(self, bulk):
        target_dict = self.graph.in_degree()
        targets = ((target, degree)
                   for target, degree in target_dict.items()
                   if target not in self.checked_accounts)
        target_tuples = sorted(targets, key=lambda x: x[1], reverse=True)
        return (target for target, _degree in target_tuples[0:bulk])

    def _check_target_edge(self, target):
        for source in self._request_rt_sources(target):
            self._add_edge(target, source)

    def _request_rt_sources(self, seed_account):
        tweets = self.client.statuses.user_timeline(
            screen_name=seed_account, count=200)
        members = self._find_retweet_source(tweets)
        return set(members)

    def _add_edge(self, target, source):
        self.graph.add_edge(target, source)
        self.checked_accounts.add(target)

    def _search_tweets(self, word, count, lang):
        if lang is None:
            return self.client.search.tweets(q=word, count=count)
        else:
            return self.client.search.tweets(q=word, count=count, lang=lang)

    def _find_screen_names(self, tweets, func=lambda x: True):
        statuses = filter(func, tweets['statuses'])
        return {t['user']['screen_name'] for t in statuses}

    def _find_retweet_source(self, tweets):
        for t in tweets:
            if 'retweeted_status' in t:
                yield t['retweeted_status']['user']['screen_name']

    def _to_centricity_dict(self, screen_name, centricity, centricity_name):
        return {'screen_name': screen_name, centricity_name: centricity}
