# reconsider
A module for cloning RethinkDB DBs/Tables from one server to another

## Introduction

I needed a way to copy a DB in it's entirety from one host to another without having to worry about file access or versions. I looked around for anything similar and couldn't find it so I decided to build my own. It's meant strictly for copying within a closed network and thus provides no additional security. It does however use the official [RethinkDB API](http://rethinkdb.com/api/python/ "RethinkDB API") which provides options to use SSL when connecting.

## Installing

You can install the latest version using pip

```sudo pip install reconsider```

## Methods

The Reconsider module contains one method, clone, which takes 4 arguments

#### clone(source, destination, dbs = None, verbose = False)

- **source** *dict* : A dictionary matching the arguments passed to the [RethinkDB connect](http://rethinkdb.com/api/python/#connect "RethinkDB connect") method. This connection will be used as the source to clone the data from.
- **destination** *dict* : Set exactly the same as **source**, this connection will be used as the destination to clone the data to.
- **dbs** *list|dict* : This optional argument can be sent as either a list, in which each item is the name of a DB on the source to be cloned to the destination, or a dictionary, in which the key is the name of the DB, and the value is a list of tables in that DB which will be copied. If left unset, all DBs with all their tables will be copied from the source to the destination.
- **verbose** *bool* : Used primarily for the cli script in order to give feedback while the data is being cloned. Depending on the size of the DBs cloning can take quite some time and knowing how much is done can be a real benefit.

## CLI

Provided for ease of use is a cli script which can be found in the root of the repo. It does not allow for individual table selection when cloning, but does allow for picking which DBs will be cloned from the source to the destination.

To get a full list of arguments to the script, run it with no arguments, or with ```--help```

```./reconsider.py --help```

### Copyright

All code belongs to [OuroborosCoding](http://ouroboroscoding.com "OuroborosCoding"), see LICENSE for more details
