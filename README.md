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
graph LR;
  asset--> requirements.txt;
  asset--> src --> portfolio_manager.py;
  asset--> src --> grabber --> Asset.py;
  asset--> src --> grabber --> Binance.py;
  asset--> src --> grabber --> Cathy.py;
  asset--> src --> grabber --> Ctbc.py;
  asset--> src --> grabber --> Firstrade.py;
  asset--> src --> grabber --> Ipost.py;
  asset--> src --> grabber --> Taishin.py;
  asset--> src --> grabber --> Woox.py;
  asset--> src --> grabber --> config --> info.ini;
```

### Github Actions
- run automatically (hourly)
