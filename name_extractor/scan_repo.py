import os
import urllib
import json
import shelve
from collections import Counter

from tokenize_code import analyze_code

CACHE_FILE = "/tmp/nameit.cache"


def scan_dir(dirpath, func):

    name_counter = Counter()
    dir_list = [dirpath]
    variable_set = set()
    class_set = set()
    method_set = set()
    while dir_list:
        dir_path = dir_list.pop()
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if not is_python(f):
                    continue

                filepath = os.path.join(root, f)
                v_set, c_set, m_set, name_freq = func(filepath)

                variable_set = variable_set.union(v_set)
                class_set = class_set.union(c_set)
                method_set = method_set.union(m_set)
                name_counter += name_freq

            dir_list += dirs

    return variable_set, class_set, method_set, name_counter


def scan_repo(repo_path, enable_cache=True):

    cache = shelve.open(CACHE_FILE)
    if repo_path not in cache:
        print 'scan dir %s'%repo_path
        cache[repo_path] = scan_dir(repo_path, analyze_code)
    
    ret = cache[repo_path]
    cache.close()
    return ret


def is_python(f):
    return f.split('.')[-1] == 'py'


def not_found_on_github(repo_info):
    return "message" in repo_info and repo_info["message"] == "Not Found"


# example output:
# {'code': [('data/urllib2.py', 23)], 'chain': [('data/urllib2.py', 2)], 'skip': [('data/urllib2.py', 4)], 'set_debuglevel': [('data/urllib2.py', 1)]}
def crawl_repo_info(repo_link):
    repo_api_url = repo_link.replace('github.com', 'api.github.com/repos')
    print "crawling from %s" % repo_api_url
    repo_info = json.loads(urllib.urlopen(repo_api_url).read())

    if not_found_on_github(repo_info):
        print repo_link, 'not found'
        return None
    return repo_info


if __name__ == "__main__":
    print scan_repo("/tmp/clonedir")
    
