# Pipelines

## Daily steps

```python
pipe = ([
        {
            "$match": {
                "ts": datetime(requested_date.year, requested_date.month, requested_date.day, tzinfo=timezone.utc)
            }
        }, {
            "$sort": {
                "steps": -1
            }
        }, {
            "$limit": 1
        }, {
        '$project': {
            '_id': 0, 
            'ts': 1, 
            'steps': 1
        }
    }
    ])
```

## Daily steps for many (range of days)

```python
pipe = [
    {
        '$match': {
            'ts': {
                '$gte': datetime(begin.year, begin.month, begin.day, tzinfo=timezone.utc), 
                '$lte': datetime(end.year, end.month, end.day, tzinfo=timezone.utc)
            }
        }
    }, {
        '$sort': {
            'steps': -1
        }
    }, {
        '$group': {
            '_id': {
                '$dayOfYear': '$ts'
            }, 
            'ts': {
                '$first': '$ts'
            }, 
            'steps': {
                '$first': '$steps'
            }
        }
    }, {
        '$project': {
            '_id': 0
        }, 
    }, {
        '$sort': {
            'ts': 1
        }
    }
    ]
```