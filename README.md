## Asset

### Goal
- Build an system to fetch personal total assets

### Method
- API
- crawler

### Install dependencies
```
pip install -r requirements.txt
```

### Directories
```mermaid
graph TD;
  asset
  asset --> requirements.txt
  asset --> src
  src --> portfolio_manager.py
  src --> grabber
  grabber --> config
  config --> info.ini
  grabber --> Asset.py
  grabber --> Binance.py
  grabber --> Cathy.py
  grabber --> Ctbc.py
  grabber --> Firstrade.py
  grabber --> Ipost.py
  grabber --> Taishin.py
  grabber --> Woox.py
```

### Github Actions
- run automatically (hourly)

### Credentials
- keep credentials (ini file) under settings

### Follow Up
1. create a db or google sheets to store the data
2. consider more error scenarios
   - exchange/bank maintenance
   - pop up message bug
   - use more try-except blocks to ensure the process runs smoothly
3. create a dashboard to record asset changes
4. Binance APIs won't work due to legal restrictions.
5. Add usd/twd exchange rate api
6. Reduce duplicate code
