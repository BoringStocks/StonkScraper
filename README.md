# __StonkScraper__
[See a live implementation here!](https://boringstocks.live/)

`StonkScraper` is a lightweight API built off the robin_stock API.

## Usage

Primary endpoint: `http://api.boringstocks.live/v2`

### Index Data
Request `https://api.boringstocks.live/v2/<stock_index>`<br>
`StonkScraper` returns a JSON containing:

Data | Key | Type
---- | --- | ----
Current price | `"current"` | float
Market cap | `"market_cap"` | float
Market status (closed/open) | `"market_status"` | int (0 & 1) 
Index name | `"name"` | string
Points/Percent change | `"points_change"` | dict
Price ranges (date/high/low/open) | `"range"` | dict
Index symbol | `"symbol"` | string
Timestamp | `"timestamp"` | string
Average volume | `"avg_volume"` | float
Volume | `"volume"` | float


### Historical Data
`StonkScraper` can also return historical data terminating on the current date.<br>
Request `https://api.boringstocks.live/v2/<stock_index>/historical/<data_range>`

Desired Range | <data_range> | Increment size
------------- | ------------ | --------------
Today | `1_day` | 5 mins
5 days | `5_days` | 1 hour
3 months | `3_months` | 1 day
1 year | `1_year` | 1 day
5 years | `5_years` | 1 week

JSON format:
```javascript
{
  "historical": [
    {
      "close": "622.625600", 
      "date": "2021-03-25T14:00:00Z"
    },
    ...
}
```

## Examples
Requesting `https://api.boringstocks.live/v2/TSLA`:
```javascript
{
  "avg_volume": 39377741.1, 
  "current": 667.93, 
  "market_cap": 661020996284.5, 
  "market_status": 0, 
  "name": "Tesla", 
  "points_change": {
    "percent": 5.08, 
    "points": 32.31
  }, 
  "range": {
    "date": "2021-03-31", 
    "high": 672.0, 
    "low": 641.12, 
    "open": 646.25
  }, 
  "symbol": "TSLA", 
  "timestamp": "22:05:25", 
  "volume": 33255670.0
}
```
<br>Requesting `https://api.boringstocks.live/v2/tsla/historical/5_days`:
```python
{
  "historical": [
    {
      "close": "622.625600", 
      "date": "2021-03-25T14:00:00Z"
    }, 
    {
      "close": 631.99500, 
      "date": "2021-03-25T15:00:00Z"
    }, 
    ...
  ]
}
```

### License
`StonkScraper` is available under the MIT license. See the [LICENSE](https://github.com/BoringStocks/StonkScraper/blob/dev/LICENSE) for more info.

### Disclaimer
`StonkScraper` uses robin_stocks. No copyright infringement intended.
