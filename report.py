from flask import current_app as app

from math import ceil


def sell_report(username, since):
    return 'TEST\nTEXT\nHERE'
    output = ""
    collection = _build_collection_index(username)
    plays = _build_plays_set(username, since)
    sell_count = 0
    output += f'Games with no logged plays since {since}:\n\n'
    for k, v in collection.items():
        if k not in plays:
            sell_count += 1
            output += f'{v}\n'
    output += f'\n{sell_count} of {len(collection)} games in your collection'
    return output

def _add_plays(setobj, plays):
    for play in plays.plays.play:
        setobj.add(int(play.item.objectid))

def _build_plays_set(username, since):
    has_plays = set()
    plays = app.bgg.get_plays(min_date=since, username=username)
    _add_plays(has_plays, plays)

    last_page = ceil(int(plays.plays.total) / 100)
    remaining_pages = range(2, last_page)
    for page in remaining_pages:
        plays = app.bgg.get_plays(
            min_date=since,
            username=username,
            page=page)
        _add_plays(has_plays, plays)
    return has_plays

def _build_collection_index(username):
    coll = app.bgg.get_collection(username, own=1)
    coll_index = {
        int(c['objectid']): c['name']['TEXT']
        for c in coll['items']['item']}
    return coll_index
