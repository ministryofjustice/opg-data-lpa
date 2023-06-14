package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	// "path/filepath"
	"strings"
	"time"
	"flag"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials/stscreds"
	"github.com/aws/aws-sdk-go/aws/session"
	v4 "github.com/aws/aws-sdk-go/aws/signer/v4"
)

func makeRequest(url string, chRespTime chan<-float64, chRespBody chan<-string, chStatus chan<-int, signer *v4.Signer, cfg aws.Config, id string) {

	req, _ := http.NewRequest(http.MethodGet, url, nil)
	req.Header.Set("Content-Type", "application/json")

	_, err := signer.Sign(req, nil, "execute-api", *cfg.Region, time.Now())
	if err != nil {
		fmt.Printf("failed to sign request: (%v)\n", err)
	}
	start := time.Now()
	res, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Printf("failed to call remote service: (%v)\n", err)
	}
	secs := time.Since(start).Seconds()

	defer res.Body.Close()
	respBody, _ := ioutil.ReadAll(res.Body)

	chRespTime <- secs
	chRespBody <- string(respBody)
	chStatus <- res.StatusCode

}

func makeRequests(url string, idsToAction []string,
	signer *v4.Signer, cfg aws.Config, chRespTime chan float64, chRespBody chan string,
	chStatus chan int) {
	var fullUrl string
	for _,id := range idsToAction {
		fullUrl = url + "/" + id
		go makeRequest(fullUrl, chRespTime, chRespBody, chStatus, signer, cfg, id)
	}
}


func idsToTest(filePath string, totalAllowed int) []string {

	content, err := ioutil.ReadFile(filePath)
	if err != nil {
			fmt.Println(err)
	}
	lines := strings.Split(string(content), "\n")

	var codesToValidate []string
	totalCount := 0

	for totalCount < totalAllowed {
		for _,line := range lines {
			if totalCount < totalAllowed {
				if len(line) > 0 {
					totalCount++
					codesToValidate=append(codesToValidate, line)
				}
			}
		}
	}

	return codesToValidate
}

func getFilePath(urlSuffix string) string {
	var filePath string
	if urlSuffix == "lpa-online-tool/lpas" {
		filePath = "./lpa_ids.txt"
	} else if urlSuffix == "use-an-lpa/lpas" {
		filePath = "./lpa_uids.txt"
	} else {
		filePath = ""
	}

	return filePath
}

func main() {
	baseUrl := flag.String("base_url", "fix-tf-data-lpa.dev.lpa.api.opg.service.justice.gov.uk/v1", "a string")
	urlSuffix := flag.String("url_suffix", "lpa-online-tool/lpas", "a string")
	batchSize := flag.Int("batch_size", 1, "an int")
	numberOfBatches := flag.Int("number_of_batches", 2, "an int")
	waitBetweenBatches := flag.Int("wait_between_batches", 2, "an int")
	flag.Parse()

	roleToAssume := "arn:aws:iam::288342028542:role/operator"
	mySession := session.Must(session.NewSession())
	creds := stscreds.NewCredentials(mySession, roleToAssume)
	cfg := aws.Config{Credentials: creds,Region: aws.String("eu-west-1")}
	sess := session.Must(session.NewSession(&cfg))
	signer := v4.NewSigner(sess.Config.Credentials)

	filePath := getFilePath(*urlSuffix)

	idsToTest := idsToTest(filePath, *batchSize)
	url := "https://" + *baseUrl + "/" + *urlSuffix
	chRespTime := make(chan float64)
	chRespBody := make(chan string)
	chStatus := make(chan int)

	fmt.Printf("===== Starting %v batches of %v requests with a wait time of %v secs between each of them =====\n\n", *numberOfBatches, *batchSize, *waitBetweenBatches)
	start := time.Now()
	for i := 0; i < *numberOfBatches; i++ {
		fmt.Printf("Processing batch %v of %v\n\n", i+1, *numberOfBatches)
		makeRequests (url, idsToTest, signer, cfg, chRespTime, chRespBody, chStatus)
		time.Sleep(time.Duration(*waitBetweenBatches)*time.Second )
	}
	var listOfRespBodies []string
	var listOfRespTimes []float64
	okCount := 0
	failCount := 0
	for z := 0; z < (*numberOfBatches * *batchSize); z++ {
		listOfRespTimes = append(listOfRespTimes, <-chRespTime)
		listOfRespBodies = append(listOfRespBodies, <-chRespBody)
		if <-chStatus <= 399 {
			okCount++
		} else {
			failCount++
		}
	}

	fmt.Printf("===== Total run finished in %.2fs =====\n\n", time.Since(start).Seconds())

	var sumTime float64 = 0
	var cnt float64 = 0
	var lowTime float64 = 100
	var highTime float64 = 0
	for _,time := range listOfRespTimes {
		sumTime = sumTime + time
		cnt = cnt + 1
		if time < lowTime {
			lowTime = time
		}
		if time > highTime {
			highTime = time
		}
	}

	fmt.Printf("Total failed: %v, Total success: %v\n", failCount, okCount)
	fmt.Printf("Average response time: %.2fs\n", sumTime/cnt)
	fmt.Printf("Fastest response time: %.2fs\n", lowTime)
	fmt.Printf("Slowest response time: %.2fs\n", highTime)

}
