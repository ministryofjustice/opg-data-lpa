### Load testing

You can call the load testing script as follows:

```
aws-vault exec identity -- go run load_testing.go \
-base_url="api.dev.sirius.opg.digital/v1" \
-url_suffix="lpa-online-tool/lpas" \
-batch_size=5 \
-number_of_batches=1 \
-wait_between_batches=0
```

options for url suffixes are:
- lpa-online-tool/lpas
- use-an-lpa/lpas

options for base urls:
- dev.lpa.api.opg.service.justice.gov.uk/v1
- api.dev.sirius.opg.digital/v1

The batch size is the number of concurrent processes to kick off at a time.

The number of batches is how many lots of those concurrent processes you want to kick off.

The wait between batches is how many seconds to wait between kicking off each batch.

You may just want to try a single batch of 500 requests and see how it handles it, or you may
want to make small batches that take longer to come back than the wait time and see how it performs over time.

It should be fairly easy to improve this to add variability and other interesting features into the model.
