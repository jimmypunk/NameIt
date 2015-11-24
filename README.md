# NameIt
a variable naming suggestion tool

# Idea of NameIt
Learning how to name variable from epic projects on GitHub.
You can stay in the console and seek for inspirations without distraction.

What can Nameit do:

nameit will find popular namings with prefix :

    $ nameit db
    > db                  280                      variable                      
    > dbm                 31                       variable                      
    > db_sort             30                       variable                      
    > db2py               10                       variable                      
    > db_app_name         9                        variable                      
    > db_times            9                        variable                      
    > db_name             8                        variable                      
    > db_manager          8                        variable                      
    > db_create_tables    7                        variable                      
    > db_port             5                        variable

nameit can show context of namings "dbm" without manually diving into sourcecode:

    $ nameit —context dbm 
    > reddit/r2/r2/lib/app_globals.py-        self.startup_timer.intermediate("cassandra")
    > reddit/r2/r2/lib/app_globals.py-
    > reddit/r2/r2/lib/app_globals.py-        ################# POSTGRES
    > reddit/r2/r2/lib/app_globals.py:        self.dbm = self.load_db_params()
    > reddit/r2/r2/lib/app_globals.py-        self.startup_timer.intermediate(“postgres")
    > —
    > —
    > reddit/r2/r2/lib/app_globals.py:        dbm = db_manager.db_manager()
    > reddit/r2/r2/lib/app_globals.py-        db_param_names = ('name', 'db_host', 'db_user', 'db_pass', 'db_port',
    > reddit/r2/r2/lib/app_globals.py-                          'pool_size', 'max_overflow')
    > reddit/r2/r2/lib/app_globals.py-        for db_name in self.databases
    > —
    > —
    > reddit/r2/r2/lib/app_globals.py-            if params['max_overflow'] == "*":
    > reddit/r2/r2/lib/app_globals.py-                params['max_overflow'] = self.db_pool_overflow_size
    > reddit/r2/r2/lib/app_globals.py-
    > reddit/r2/r2/lib/app_globals.py:            dbm.setup_db(db_name, g_override=self, **params)
    > reddit/r2/r2/lib/app_globals.py-            self.db_params[db_name] = params

# Usage
-------------------------------------------

    usage: nameit.py [-h] [-t TYPE] [-c CONTEXT] [-l LOAD] [-i]
                     [QUERY [QUERY ...]]
    
    instant python naming suggestion via the command line
    
    positional arguments:
      QUERY                 naming prefix query
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TYPE, --type TYPE  specify naming type 0:variable, 1: class, 2: method
      -c CONTEXT, --context CONTEXT
                            display the code context
      -l LOAD, --load LOAD  load repository
      -i, --interactive     interactive mode
      -C, --clear-cache clear the cache

# Development
-----------------------------------------
1) make it execute from command line
2) server-client version of Nameit
