# __StonkScraper__
This API is a WIP. Check back often for new features!<br>
[See a live implementation here!](https://boringstocks.live/)

`StonkScraper` is a lightweight API that scrapes Yahoo's financial pages for a defined stock index. It is minimal by design but returns most of the data that the average daytrader would require to decide whether to buy or sell GME.

## Usage

Primary endpoint: `http://api.boringstocks.live/`

### Current Index Data
Request `https://api.boringstocks.live/v1/<stock_index>`<br>
`StonkScraper` returns a JSON containing these data points:
  - Current price
  - Range of historical data (not including the current day)
  - Market cap
  - Market status (open/close)
  - Opening price
  - Price change (points & percent)
  - Day's range (date, high, low, & close)
  - Index
  - Timestamp
  - Average volume
  - Volume

### Historical Index Data
`StonkScraper` can also return the historical data ending on the current date.<br>
Request `https://api.boringstocks.live/v1/<stock_index>/historical/<data_range>`
Desired Range | <data_range>
------------- | ------------
5 days | 5_days
1 month | 1_month
6 months | 6_months
1 year | 1_year
All historical data | max

## Examples
Requesting `https://api.boringstocks.live/v1/GOOG`:
```javascript
{
  "avg_volume": 1571006.0, 
  "current": 2117.2, 
  "historical": [
    {
      "close": 2104.11, 
      "date": "2021-02-12"
    }, 
    {
      "close": 2121.9, 
      "date": "2021-02-16"
    }, 
    {
      "close": 2128.31, 
      "date": "2021-02-17"
    }, 
    {
      "close": 2117.2, 
      "date": "2021-02-18"
    }
  ], 
  "market_cap": "1.424T", 
  "market_status": 0, 
  "name": "Alphabet Inc.", 
  "open": 2110.39, 
  "points_change": {
    "percent": -0.52, 
    "points": -11.11
  }, 
  "range": {
    "close": 2117.2, 
    "date": "2021-02-18", 
    "high": 2132.74, 
    "low": 2104.28
  }, 
  "symbol": "GOOG", 
  "timestamp": "03:58:01", 
  "volume": 1121855.0
}
```
<br>Requesting `https://api.boringstocks.live/v1/GOOG/historical/5_days`:
```python
{ "historical": 
  [
    {
      "close": 2104.11, 
      "date": "2021-02-12"
    }, 
    {
      "close": 2121.9, 
      "date": "2021-02-16"
    }, 
    {
      "close": 2128.31, 
      "date": "2021-02-17"
    }, 
    {
      "close": 2117.2, 
      "date": "2021-02-18"
    }
  ]
}
```

### License
`StonkScraper` is available under the MIT license. See the [LICENSE](https://github.com/BoringStocks/StonkScraper/blob/dev/LICENSE) file for more info.

### Disclaimer
`StonkScraper` uses Yahoo Finance to aggregate its data. No copyright infringement intended.
