# gbg-field-status-bot

https://twitter.com/gbgplanstatus

- Twitter bot that tweets unavailable football pitches in the Gothenburg area.
- Deployed as an AWS Lambda
- Tweets updates daily at 10am, 12am and 15am (GMT +2)

## Deployment instructions

1. Create a zip file with the `lambda_handler.py` and all the dependencies.

```bash
zip -r9 lambda.zip * -x "bin/*" requirements.txt setup.cfg
``` 
2. Create an AWS lambda of using the `lambda.zip` and then use `CloudWatcher` for creating scheduled triggers.

## Run it locally

1. Create virtual environment
```bash 
python -m venv venv
source venv/bin/activate
```
2. Install requirements
```bash
pip install -r requirements.txt
```
3. Call the following methods in the `lambda_handler.py`
```python
statuses = collect_statuses_from_webpage()
closed_fields = get_closed_fields(statuses)
tweet_statuses(closed_fields)
```
