# gbg-field-status-bot

https://twitter.com/gbgplanstatus

- Twitter bot that tweets unavailable football fields in the Gothenburg area.
- Deployed as an AWS Lambda
- Tweets updates daily at 10am, 12am and 3pm (GMT +2)

## Deployment using Terraform and Github Actions
This repo contains a POC/MVP for how to use IaC (Terraform) with Github Actions. In the `configuration.tf`, the required infrastructure is defined. The deployment workflow looks like this: 

1. For a new change, create a `PR` to `main`. This will trigger the `.github/workflows/plan.yml`, which mainly runs `terraform plan`. The plan is shown as a comment on the `PR` and it becomes straightforward to see the infrastructure changes that a merge of this PR creates.
2. When the `PR` merged, the `.github/workflows/deploy.yml` will be triggered. This workflow mainly runs `terraform apply` which executes the plan of infrastructure changes. This workflow also checks in the `terraform.tfstate` file so that the state stays up-to-date.


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
