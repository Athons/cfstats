import CloudFlare


class CFStats:
    """
    Wrapper around the cloudflare API library to provide a nice interface for
    fetching statistics.
    """

    def __init__(self, token):
        self.token = token
        self.cf = CloudFlare.CloudFlare(token=token)


    def zones(self):
        """
        Quick wrapper to get the zones
        """
        return self.cf.zones.get()

    def stats(self, zone_id, start_date, end_date, limit=100):
        """
        Our query for getting statistics from the CF GraphQL api.

        For more info on that, check:
        https://developers.cloudflare.com/analytics/graphql-api

        We're currently looking at the `httpRequests1dGroups` table, which
        covers mostly what we'd want to make public (general request numbers
        countries, etc)

        Based on:
        https://developers.cloudflare.com/analytics/migration-guides/zone-analytics

        But with the following removed:
        * threats. we're a static site, don't care about random scrappers.
        * SSL. Really not that interesting to know the 90% is TLSv1.3
        * ipclassmap. it's mostly unknown / no record.

        But for what we do include:
        * Browser Usage Stats
        * Requests per country.
        * cached / vs non cached requests.
        * Content types being requested.
        * Status code info
        """
        query="""
        query {
            viewer {
                zones(filter: {zoneTag: "%s"} ) {
                    httpRequests1dGroups(limit: %i, filter:{date_lt: "%s", date_gt: "%s"}) {
                        dimensions { date }
                        sum {
                            pageViews
                            bytes
                            requests

                            cachedBytes
                            cachedRequests

                            browserMap {
                                pageViews
                                uaBrowserFamily
                            }
              
                            contentTypeMap {
                                bytes
                                requests
                                edgeResponseContentTypeName
                            }
                            countryMap {
                                bytes
                                requests
                                threats
                                clientCountryName
                            }

                            responseStatusMap {
                                requests
                                edgeResponseStatus
                            }
                        }

                        uniq {
                            uniques
                        }
                    }
                }
            }
        }
        """ % (zone_id, limit, start_date, end_date)
        r = self.cf.graphql.post(data={'query':query})
        # Skipping the API filler stuff
        # Only 1 zone would be included, so zero indexing should be fine.
        return r['data']['viewer']['zones'][0]['httpRequests1dGroups']
