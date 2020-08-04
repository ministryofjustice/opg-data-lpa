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

func main() {

	account := flag.String("account", "288342028542", "a string")
	role := flag.String("role", "operator", "a string")
	branch := flag.String("branch", "in322.", "a string")
	domain := flag.String("domain", "lpa", "a string")
	version := flag.String("version", "v1", "a string")
	path := flag.String("path", "healthcheck", "a string")

	flag.Parse()

  roleToAssume := "arn:aws:iam::" + *account + ":role/" + *role
	url := "https://" + *branch + "dev." + *domain + ".api.opg.service.justice.gov.uk/" + *version + "/" + *path
	mysession := session.Must(session.NewSession())
	creds := stscreds.NewCredentials(mysession, roleToAssume)
	cfg := aws.Config{Credentials: creds,Region: aws.String("eu-west-1")}
	sess := session.Must(session.NewSession(&cfg))
	signer := v4.NewSigner(sess.Config.Credentials)
	req, _ := http.NewRequest(http.MethodGet, url, nil)

	_, err := signer.Sign(req, nil, "execute-api", *cfg.Region, time.Now())
	if err != nil {
		fmt.Printf("failed to sign request: (%v)\n", err)
	}

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Printf("failed to call remote service: (%v)\n", err)
	}

	defer res.Body.Close()

	buffer := new(bytes.Buffer)
	buffer.ReadFrom(res.Body)
	responseBody := buffer.String()

	fmt.Println(responseBody)
	fmt.Println(res.Status)
	fmt.Println(res.StatusCode)
}
