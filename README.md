# elasticsearch-snapshot-script
Repo to store python script to call elasticsearch snapshot service from aws bastion



# Sample call
GET
```
./get 'https://vpc-srsdata-exp-cff4a49ef13eb7d4-dqr6sihwsue7zphopb5ul4drwi.ap-southeast-1.es.amazonaws.com/geo_area_test_2018_10_09_19_00/_search'
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

Put
```
./put 'https://search-ism-usr-c3l7hkbggsr4nmcl6sib56j6jy.ap-southeast-1.es.amazonaws.com/_snapshot/migration-repo' '{
  "type": "s3",
  "settings": {
    "bucket": "srstest-migrationbucket-517530806209-12345678",
    "region": "ap-southeast-1",
    "role_arn": "arn:aws:iam::517530806209:role/ElasticsearchRole_srs_elasticsearchmigration"
  }
}'
```

Trigger Snapshot
```
./snapshot '{
 "landmark" : "https://endpoint-1/",   
 "geo" : "https://endpoint-2/"   
}' 'srstest-migrationbucket-517530806209-12345678' 'arn:aws:iam::517530806209:role/ElasticsearchRole_srs_elasticsearchmigration'
```

Trigger Restore
```
./restore '{
 "landmark" : "https://new-es-endpoint-1/",   
 "geo" : "https://new-es-endpoint-2/"   
}' 'srstest-migrationbucket-newaccountid-12345678' 'arn:aws:iam::newaccountid:role/ElasticsearchRole_srs_elasticsearchmigration'
```
