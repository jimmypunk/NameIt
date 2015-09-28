from django.core.management.base import BaseCommand
from smart_naming.models import Repo, RepoWordCountView
from name_extractor.scan_repo import scan_repo, crawl_repo
import git
import shutil
import traceback
TEMP_REPO_DIR = "/tmp/clonedir"


class Command(BaseCommand):
    help = 'Load repo to db'

    def add_arguments(self, parser):
        parser.add_argument('repo_url', nargs='+', type=str)

    def handle(self, *args, **options):
        for repo_url in options['repo_url']:
            # check if repo info is already in REPO TABLE
            if True or not Repo.objects.filter(repo_url=repo_url).exists():
                repo_info = crawl_repo(repo_url)
                r = Repo.objects.create(repo_url=repo_url, repo_info=repo_info)
                self.update_repo_word_count_view(r, repo_url)

    def update_repo_word_count_view(self, repo_ref, repo_url):
        # download repo from repo_url
        # scan & analyze repo from the local repo_path
        print "cloning repo from %s" % repo_url
        self.clean_clone_dir()
        git.Repo.clone_from(repo_url, TEMP_REPO_DIR)
        word_freq_by_files = scan_repo(TEMP_REPO_DIR)
        for word in word_freq_by_files:
            files, counts = zip(*word_freq_by_files[word])
            total_freq = sum(counts)
            v = RepoWordCountView(repo=repo_ref, word=word, total=total_freq, counts=counts, files=files, count_in_files=word_freq_by_files[word])
            v.save()
        # remove downloaded repo
        self.clean_clone_dir()

    def clean_clone_dir(self):
        try:
            shutil.rmtree(TEMP_REPO_DIR)
        except OSError:
            print(traceback.format_exc())
