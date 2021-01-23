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
        * threats (we're a static site, don't care about random scrappers)
        """
        query="""
        query {
            viewer {
                zones(filter: {zoneTag: "%s"} ) {
                    httpRequests1dGroups(limit: %i, filter:{date_lt: "%s", date_gt: "%s"}) {
                        dimensions { date }
                        sum {
                            browserMap {
                                pageViews
                                uaBrowserFamily
                            }
                            bytes
                            cachedBytes
                            cachedRequests
                            contentTypeMap {
                                bytes
                                requests
                                edgeResponseContentTypeName
                            }
                            clientSSLMap {
                                requests
                                clientSSLProtocol
                            }
                            countryMap {
                                bytes
                                requests
                                threats
                                clientCountryName
                            }
                            encryptedBytes
                            encryptedRequests
                            ipClassMap {
                                requests
                                ipType
                            }
                            pageViews
                            requests
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
        return r
