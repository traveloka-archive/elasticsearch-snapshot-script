# elasticsearch-snapshot-script
Repo to store python script to call elasticsearch snapshot service from aws bastion



# Sample call
GET
```
./get 'https://es-endpoint/_search'
```

Post
```
./post 'https://es-endpoint/_search' '{
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
./put 'https://es-endpointm/_snapshot/migration-repo' '{
  "type": "s3",
  "settings": {
    "bucket": "srstest-migrationbucket-123456789123-12345678",
    "region": "ap-southeast-1",
    "role_arn": "arn:aws:iam::123456789123:role/ElasticsearchRole_srs_elasticsearchmigration"
  }
}'
```

Trigger Snapshot
```
./snapshot '{
 "landmark" : "https://endpoint-1/",   
 "geo" : "https://endpoint-2/"   
}' 'srstest-migrationbucket-oldaccountid-12345678' 'arn:aws:iam::oldaccountid:role/ElasticsearchRole_srs_elasticsearchmigration'
```

Trigger Restore
```
./restore '{
 "landmark" : "https://new-es-endpoint-1/",   
 "geo" : "https://new-es-endpoint-2/"   
}' 'srstest-migrationbucket-newaccountid-12345678' 'arn:aws:iam::newaccountid:role/ElasticsearchRole_srs_elasticsearchmigration'
```

# Passing single quotes on the argument
you need to add $ char before the argument
sample : 
```
./post 'https://es-domain.com/link' $'{
  "script": {
    "source": "ctx._source.type=\'LandmarkType\'",
    "lang": "painless"
  }
}'
```

# Error permission
if error happen something like this
```
bash: ./xxxx: Permission denied
```
allow execution by run this command
```
chmod +x xxxx
```
