## Curl Request

```
curl --request POST \
  --url http://localhost:5000/generate \
  --header 'Content-Type: application/json' \
  --data '{
    "question": "what is cricket?",
	"streaming": true
  }' \
  --no-buffer
```