import requests
import appsecrets
import json

def get_auth_endpoint(env):
  if env == 'stage':
    env_base = appsecrets.get_secret('STAGE_URL')
  else:
    env_base = 'https://partner.api.dailymotion.com/'
  return (env_base + 'oauth/v1/token')

def get_token(env='prod'):
  response = requests.post(
    get_auth_endpoint(env),
    data={
      'client_id': appsecrets.get_secret('API_KEY'),
      'client_secret': appsecrets.get_secret('API_SECRET'),
      'grant_type': 'client_credentials',
      'scope': 'access_ads access_revenue create_reports delete_reports'
    },
    headers={
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  )

  if response.status_code != 200 or not 'access_token' in response.json():
      print(response)
      print(json.dumps(json.loads(response.content), indent=2))
      raise Exception('Invalid authentication response')
  
  return response.json()['access_token']
