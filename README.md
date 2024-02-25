# How to run

## Option 1 - Docker
Clone repository and then run the following to build and run the container:
```
docker compose build && docker compose up
```

## Option 2
Clone repository and then run the following:
```
1 - pipx install poetry==1.7.1
2 - poetry install --no-root
3 - poetry run python manage.py migrate
4 - poetry run python manage.py runserver
```

## Making API requests
### List of funds in the database
```
curl --request GET --url http://localhost:8000/funds/
```

### Filter funds by strategy
```
curl --request GET --url http://localhost:8000/funds/?strategy=REPLACE_WITH_STRATEGY

Strategy options - LSE (Long/Short Equity), GLM (Global Macro), ARB (Arbitrage)
```

### Filter fund by id
```
curl --request GET --url http://localhost:8000/funds/1
```

## Upload CSV file
```
http://localhost:8000/funds-upload/
```

## Fund list
```
http://localhost:8000/fund-list/
```

## Running tests
Run the following command:
```
poetry run python manage.py test -v 2
```
