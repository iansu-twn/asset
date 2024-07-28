## asset

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
