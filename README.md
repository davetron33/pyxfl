# PyXFL v2

Is this officially version 2? It's a pretty substantial change. We have classes now! And a lot less crap in the repo. 

PyXFL is a python class that uses the publicly facing XFL api to retrieve player and team statistics and store them into dataframes for easy analysis. 

The code in this repo is meant purely for *extraction* and makes only minimal attempts to transform and normalize data. It is intended to simplify the process of querying the various XFL stat endpoints and make saving large returns of data easy. 

# Demo dashboard:
A (work in progress) dashboard showcasing the use of this data can be found [here](https://app.hex.tech/7c7ec0d1-7123-40af-aa5f-db65e17670f2/app/f4bca27b-b99d-497f-aa93-3d63ea568562/latest). This dashboard is for educational purposes only. 

# Usage:

Install dependencies:

```
$ pip -m install requirements.txt
```

Create a new instance of the XFL class:

```
x = xfl(token)
```

Print all XFL players:

```
players = x.get_players()
```

Because we're using Pandas, all objects returned are stored as dataframes, making it easy to immediately begin manipulating data as you see fit:

```
>>> print(type(players))

<class 'pandas.core.frame.DataFrame'>
```

# FAQ

## What?

An attempt to create a library to query the XFL stats API using python. 

## Why are you doing this?

Why indeed.

## How do I contribute?

Gitops. Write code. Open PR. 

## Who are you?

Space ghost.
![space ghost likes his coffee, so do I](https://pbs.twimg.com/media/Dj7aIfxXcAIKnHs.jpg:large)

## Where do I get an API key?

Not from this repo, that's for starters.

If you know a thing or two about [troubleshooting APIs via the browser](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/request_details/index.html), then you're already halfway there.    
If you don't, then treat this repo like a 'CTF'. Wait..that's a terrible idea.

Use this code responsibly.
