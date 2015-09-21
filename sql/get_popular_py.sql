#  sql to get most popular python open source projects from githubarchive:year data
#  see https://github.com/igrigorik/githubarchive.org/tree/master/bigquery
SELECT repository_url, MAX(repository_watchers) as watchers FROM [githubarchive:year.2014] WHERE repository_language='Python' AND repository_has_wiki=TRUE GROUP BY repository_url ORDER BY watchers DESC LIMIT 500
