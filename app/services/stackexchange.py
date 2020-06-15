import itertools
import requests
import logging
from .stack_conf import API_URL


class StackOverFlow():

    def shuffle_tags(self, tags):
        return list(itertools.combinations(tags, len(tags) - 1))

    def request_results(self, args):
        splitted = ' '.join(map(str, args))
        url = API_URL + splitted
        results = requests.get(url)
        return results.json()

    def get_posts(self, in_title):
        if in_title is None:
            return 0
        try:
            if (len(in_title) > 2):
                urls_args = self.shuffle_tags(in_title)
                list_of_args = [list(args) for args in urls_args]
                try:
                    listed_results = [self.request_results(
                        args) for args in list_of_args]
                    results_with_content = [
                        res for res in listed_results if len(res) > 0]
                    return results_with_content
                except Exception as e:
                    return {}
            results = self.request_results(in_title)
            return results
        except Exception as e:
            return {}

    @staticmethod
    def map_posts(posts, tags):
        if (not isinstance(posts, list)):
            posts = [posts]
        items = []
        for post in posts:
            if 'items' in post and len(post['items']) > 0:
                items.extend(post['items'])
        mapped = []
        answered_posts = [post for post in items if post['is_answered']]
        for post in answered_posts:
            temp = {}
            accuracy = find_relevant(post['tags'], tags)
            len_given_tags = len(tags)
            if accuracy >= len_given_tags:
                temp['title'] = post['title']
                temp['link'] = post['link']
                temp['tags'] = post['tags']
                mapped.append(temp)
        return mapped


def find_relevant(posts_tags, tags):
    relevancy = 0
    if tags and len(tags) > 0 and posts_tags and len(posts_tags) > 0:
        for post_tags in posts_tags:
            for tag in tags:
                if tag.lower() in post_tags.lower() or post_tags.lower() in tag.lower():
                    relevancy += 1
        return relevancy
