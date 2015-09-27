import os
from tokenize_code import analyze_code
from collections import Counter
from collections import defaultdict
import urllib
import json


def scan_dir(repo_path, func):
    name_counter = Counter()
    dir_list = [repo_path]
    while dir_list:
        dir_path = dir_list.pop()
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.split('.')[-1] != 'py':
                    continue

                filepath = os.path.join(root, f)
                variable_set, class_set, method_set, name_freq = func(filepath)
                name_counter += name_freq

            dir_list += dirs

    return name_counter


def scan_repo(repo_path):
    word_freq_by_files = defaultdict(list)
    for root, dirs, files in os.walk(repo_path):
        for f in files:
            if f.split('.')[-1] != 'py':
                continue
            filepath = os.path.join(root, f)
            variable_set, class_set, method_set, name_freq = analyze_code(filepath)
            _, _, _, name_freq = analyze_code(filepath)
            for name, freq in name_freq.items():
                relpath = os.path.relpath(filepath, repo_path)
                word_freq_by_files[name].append((relpath, freq))

    return word_freq_by_files


def not_found_on_github(repo_info):
    return "message" in repo_info and repo_info["message"] == "Not Found"


# example output:
# {'code': [('data/urllib2.py', 23)], 'chain': [('data/urllib2.py', 2)], 'skip': [('data/urllib2.py', 4)], 'set_debuglevel': [('data/urllib2.py', 1)]}
def crawl_repo(repo_link):
    repo_api_url = repo_link.replace('github.com', 'api.github.com/repos')
    print "crawling from %s" % repo_api_url
    repo_info = json.loads(urllib.urlopen(repo_api_url).read())

    if not_found_on_github(repo_info):
        print repo_link, 'not found'
        return None
    return repo_info


if __name__ == "__main__":
    print scan_repo("/tmp/clonedir")
    # repo_link = sys.argv[1]
    # print scan_dir("/tmp/exp_dir", analyze_code)
    # crawl_repo(repo_link)
