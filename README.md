# data-tracker

# How to run this app
1. Initialize the virtual env 
`python3 -m venv env`
2. Activate the virtual env
`source env/bin/activate`
3. Install dependencies
`pip install -r requirements.txt`
4. From the project root, start the price ingester
`python ./data-tracker/run_price_ingester.py`
5. Start the server
```
export FLASK_APP=data-tracker
export FLASK_ENV=development
flask run
```
6. Send test requests
```
> curl http://127.0.0.1:5000/price-l24h/btcjpy
{
  "result": [
    {
      "price": 4385854, 
      "symbol": "btcjpy", 
      "timestamp": 1623726097
    }, 
    {
      "price": 4385854, 
      "symbol": "btcjpy", 
      "timestamp": 1623726157
    }
  ]
}

> curl -X POST http://127.0.0.1:5000/rank -d '{"symbols": ["btcusd", "btceur", "btcjpy"]}' -H "Content-Type: Application/Json"
{
  "result": [
    {
      "rank": 1, 
      "stdev": 10461.451485329088, 
      "symbol": "btcjpy"
    }, 
    {
      "rank": 2, 
      "stdev": 51.05111402688678, 
      "symbol": "btcusd"
    }, 
    {
      "rank": 3, 
      "stdev": 37.357079324558164, 
      "symbol": "btceur"
    }
  ]
}

> curl http://127.0.0.1:5000/currency-dropdown
{
  "result": [
    {
    "symbol": "minausd"
    }, 
    {
    "symbol": "minabtc"
    }, 
    {
    "symbol": "minagbp"
    }
  ]
}
```

# Scalability
To improve the scalability of this app, I would focus on 3 areas:
- Price Ingester: The price ingester is essentially a python script that runs on a loop and queries the cryptocurrency api. In a production system, I would like to rewrite this to run as a separate service with a task scheduler/worker model. Each task would query the current price for a single symbol.
- Datastore: Due to time constraints, this app uses a sqlite database. However, I don't think this is the best choice for a production app. A typical relational databse is not the right choice because (1) that data is not relational in nature and (2) our primary concern is handling a large number of concurrent reads/writes. As such, I think Cassandra of Amazon DynamoDB are both better options for a production system.
- API: The API, as written, is relatively light on business logic and should be able to handle a large number of requests as long as we scale horizontally. That being said, we could get some performance imporovements by switching to a language like Java or Go. However, I do not believe this is necessary.

# Testing
Due to time constraints, I was unable to write tests for this app. In a production system, I would test as follows:
- Unit tests w/ at least 90% coverage to test the handlers, clients, dal, etc. The purpose of these tests is to verify the functionality of individual components of the app (not e2e).
- CI/CD job to run unit tests on all pull requests on creation.
- CI/CD job to test master after a PR is merged.

In addition, we could run blackbox integration tests which query our api and check that the response is as expected. Because of the constantly changing nature of the data, we would need to identify some other source of truth with which to compare the response.

# Feature Request
Requirement: For all currencies, push alert to users when its value is 3x the l1h average.

Proposal:
- Every time our price ingester updates a currency's price, it emits a "price-updated" event
- A separate alerting service ingests the event and compares the latest price vs. the l1h average
- If the current_price >= 3 * avg_price, the alerting service sends a notification to the users. For example, this notification could take the form of an email.

Potential drawbacks:
- Creates a new service which may add complexity. It is possible to house this logic in the price ingester. However, for long-term scalability and maintainability, I think it makse sense to have a separate alerting service
- Users may get a lot of alerts for currencies that are volatile. However, this should be rare because even the most volatile currencies are unlikely to change 3X in 1 hour.
- This approach checks all currencies for every update. Depending on our feature requirements, we may be able to cut this down and only check once every X minutes. 

# Additional Work
In addition to what has already been discussed above, if I had additional time I would:
- Rewrite the ranking endpoint to automatically pick "comparable" currencies. As written today, the endpoint requires the caller to pass in a list of currencies they want to rank/compare
- Add input validation to check request parameters
- Logging/metrics to track the performance of all endpoints, clients, etc.
- Better error handling throughout the app. For example, in the ranking endpoint we do not handle errors returned from the stdev() function.
