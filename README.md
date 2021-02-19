# __StonkScraper__
[See a live implementation here!](https://boringstocks.live/)

`StonkScraper` is a lightweight API that scrapes Yahoo's financial pages for a defined stock index. It is minimal by design but returns most of the data that the average daytrader would require to decide whether to buy or sell GME.

## Usage

Primary endpoint: `http://api.boringstocks.live/`

### Current Index Data
Request `http://api.boringstocks.live/v1/<stock_index>`<br>
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
Request `http://api.boringstocks.live/v1/<stock_index>/historical/<data_range>`
Desired Range | <data_range>
------------- | ------------
5 days | 5_days
1 month | 1_month
6 months | 6_months
1 year | 1_year
All historical data | max

## Examples
Requesting `http://api.boringstocks.live/v1/GOOG`:
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
<br>Requesting `http://api.boringstocks.live/v1/GOOG/historical/5_days`:
```python
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
```

## [License](https://github.com/BoringStocks/StonkScraper/blob/dev/LICENSE)
Copyright © 2021 BoringStocks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
