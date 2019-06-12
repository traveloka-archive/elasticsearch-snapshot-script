# elasticsearch-snapshot-script
Repo to store python script to call elasticsearch snapshot service from aws bastion



# Sample call
GET
```
./get "https://vpc-srsdata-exp-cff4a49ef13eb7d4-dqr6sihwsue7zphopb5ul4drwi.ap-southeast-1.es.amazonaws.com/geo_area_test_2018_10_09_19_00/_search"
```

Post
```
./post 'https://vpc-srsdata-exp-cff4a49ef13eb7d4-dqr6sihwsue7zphopb5ul4drwi.ap-southeast-1.es.amazonaws.com/geo_area_test_2018_10_09_19_00/_search' '{
    "query" : {
        "bool" : {
            "must" : [
                {
                    "term" : {
                        "pC" : "geo_area"
                    }
                }
            ]
        
        }
    }
}'
```
