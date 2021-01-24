# cfstats

Fetching our cloudflare stats and making them public!

Trying to provide as much info as possible without causing privacy risks. (i.e,
no IPs from "threats", only reporting information where the user wouldn't be
unique, etc)



## Usage

This takes a Cloudflare token by the `CF_TOKEN` env var.

The tool will list all stats for the domains it has access to, so make sure to
limit your tokens scope!

The code references a [JSONBin](https://jsonbin.io) that is used to store the
data without having to spam a branch.

The key is called `JSONBIN_KEY`.

`JSONBIN_ID` is the bin id to be updated.
