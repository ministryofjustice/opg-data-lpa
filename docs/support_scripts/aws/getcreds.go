package main

import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials/stscreds"

)

func main() {

    roletoassume := "arn:aws:iam::288342028542:role/code-artifact-development"

	mysession := session.Must(session.NewSession())
	creds := stscreds.NewCredentials(mysession, roletoassume)
	cfg := aws.Config{Credentials: creds,Region: aws.String("eu-west-1")}
	sess := session.Must(session.NewSession(&cfg))
	sessionstring, err := sess.Config.Credentials.Get()

	if err != nil {
		fmt.Println(err)
	}

	accesskey := "export AWS_ACCESS_KEY_ID=" + sessionstring.AccessKeyID
	secret := "export AWS_SECRET_ACCESS_KEY=" + sessionstring.SecretAccessKey  // pragma: allowlist secret
	session := "export AWS_SESSION_TOKEN=" + sessionstring.SessionToken
	fmt.Println(accesskey)
	fmt.Println(secret)
	fmt.Println(session)

}


