package main

import (
	"bytes"
	"fmt"
	"net/http"
	"time"
	"flag"

	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/aws"
	v4 "github.com/aws/aws-sdk-go/aws/signer/v4"
	"github.com/aws/aws-sdk-go/aws/credentials/stscreds"

)
// WORKING FIXTURE DATA IDs TO USE IN INTEGRATION:
// lpa-online-tool/lpas/A33718377316
// use-an-lpa/lpas/700000000047
// use-an-lpa/lpas/requestCode ----- payload: {\"case_uid\": 700000000047, \"actor_uid\": 700000000799}
func main() {

	account := flag.String("account", "288342028542", "a string")
	role := flag.String("role", "operator", "a string")
	branch := flag.String("branch", "", "a string")
	domain := flag.String("domain", "lpa", "a string")
	version := flag.String("version", "v1", "a string")
	path := flag.String("path", "", "a string")
	full_url := flag.String("full_url", "", "a string")
    payload := flag.String("payload", "", "a string")

	flag.Parse()

    roleToAssume := "arn:aws:iam::" + *account + ":role/" + *role

	var url string = ""

	if *full_url != "" {
		url = *full_url
	} else {
		url = "https://" + *branch + ".dev." + *domain + ".api.opg.service.justice.gov.uk/" + *version + "/" + *path
	}

	mysession := session.Must(session.NewSession())
	creds := stscreds.NewCredentials(mysession, roleToAssume)
	cfg := aws.Config{Credentials: creds,Region: aws.String("eu-west-1")}
	sess := session.Must(session.NewSession(&cfg))
	signer := v4.NewSigner(sess.Config.Credentials)

	if *payload != "" {
		req, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer([]byte(*payload)))
		if err != nil {
			fmt.Printf("failed to create POST request: %v\n", err)
			return
		}

		_, err = signer.Sign(req, bytes.NewReader([]byte(*payload)), "execute-api", *cfg.Region, time.Now())
		if err != nil {
			fmt.Printf("failed to sign request: %v\n", err)
			return
		}

		req.Header.Set("Content-Type", "application/json")

		res, err := http.DefaultClient.Do(req)
		if err != nil {
			fmt.Printf("failed to call remote service: %v\n", err)
			return
		}

		defer res.Body.Close()

		buffer := new(bytes.Buffer)
		buffer.ReadFrom(res.Body)
		responseBody := buffer.String()

		fmt.Println(responseBody)
		fmt.Println(res.Status)
		fmt.Println(res.StatusCode)
	} else {
		// Perform GET request as before
		req, _ := http.NewRequest(http.MethodGet, url, nil)

		_, err := signer.Sign(req, nil, "execute-api", *cfg.Region, time.Now())
		if err != nil {
			fmt.Printf("failed to sign request: %v\n", err)
			return
		}

		res, err := http.DefaultClient.Do(req)
		if err != nil {
			fmt.Printf("failed to call remote service: %v\n", err)
			return
		}

		defer res.Body.Close()

		buffer := new(bytes.Buffer)
		buffer.ReadFrom(res.Body)
		responseBody := buffer.String()

		fmt.Println(responseBody)
		fmt.Println(res.Status)
		fmt.Println(res.StatusCode)
	}
}
