import requests
tokenUrl="http://localhost:8080/realms/test/protocol/openid-connect/token"

client_id="flaskapp"
client_secret = "UP0iZlLHiIyG6r2mNBeZA2UvWFq6PWHr"

accessTokenResp = requests.post(url=tokenUrl,
              data={
                  "grant_type":"client_credentials",
                  "client_id":client_id,
                  "client_secret":client_secret,
                  "scope":"test_api_access"
              },
              headers={
                  'content-type':"application/x-www-form-urlencoded"
              })

if not accessTokenResp.ok:
    print("Server Token response status not ok")
    quit()
accessTokenRespJson = accessTokenResp.json()

if not "access_token" in accessTokenRespJson:
    print(" access_token not found in token response")
    quit() 
accessToken = accessTokenRespJson["access_token"]

apiUrl = "http://localhost:5000/"
apiResp = requests.get(url=apiUrl,headers={
    'authorization':f"Bearer {accessToken}",
    'content-type': "application/json"
})

if not apiResp.ok:
    print("ok response not received from resource API call")
    quit()

#print(apiResp.json())  # Print the response content


print("execution complete...")