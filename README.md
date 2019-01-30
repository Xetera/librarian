# Librarian

An elasticsearch instance for querying data found in https://github.com/manami-project/anime-offline-database

**Public API**: https://api.weebsearch.com/search/title:new%20game

## Querying
Response format 
```
{
  count: number,
  max_score: number,
  total: number,
  hits: [{
    _score: number,
    _source: AnimeResponse
  }]
}
```
AnimeResponse is the same format given in the original repo

### GET **/search/query** 
querying all fields in general (/search/death note)
### GET **/search/key:value** 
querying specific fields (/search/title:konosuba) or (/search/sources:anilist)

querying `title` also matches the `synonyms` fields

### Query Params
**limit**: limit search results (max 25)


## Refreshing
To refresh the ES data hit up the /reload endpoint

### POST **/reload**
Headers: { Authorization: LIBRARIAN_KEY }