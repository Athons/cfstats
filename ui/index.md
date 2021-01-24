<link rel="stylesheet" href="css/splendor.min.css">
<script src="./js/main.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"></script>

# Athon stats!

These are directly fetched from the cloudflare API and might be a little
inaccurate (from bots to vpns, etc).

## Data

Data is collected by a script which reads the last 30 days worth of data, daily.

We present the data from yesterday, as today isn't over and would show lower
numbers compared to the rest!

### Unique Visitors

<canvas id="uniqueChart" width="400" height="200"></canvas>

### Page Views

<canvas id="pageViewsChart" width="400" height="200"></canvas>

### Requests

<canvas id="requestsChart" width="400" height="200"></canvas>

### Bytes Transfered

<canvas id="bytesChart" width="400" height="200"></canvas>

### Cached Response and Byte Ratios

<canvas id="cachedRequestsChart" width="400" height="200"></canvas>

<canvas id="cachedBytesChart" width="400" height="200"></canvas>

## Tech Details

This page is built from the code in
[athons/cfstats](https://github.com/athons/cfstats), which uses:

* Python for talking to the Cloudflare API and downloading the data.
* [Chart.js](https://www.chartjs.org/docs/latest/) for Graphs
* [Splendor](https://github.com/markdowncss/splendor) for some nice default CSS

Check the code out if this sort of thing interests you, and feel free to submit
patches to make improvements!
