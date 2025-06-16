import requests
import appsecrets
import json
import time

class Report:
  def __init__(self):
    self.auth_url = "https://partner.api.dailymotion.com/oauth/v1/token"
    self.report_url = 'https://partner.api.dailymotion.com/graphql'
    #self.auth_url = 'https://partner.api-staging.dailymotion.com/oauth/v1/token'
    #self.report_url = 'https://partner.api-staging.dailymotion.com/graphql'

    self.token = self._get_token()
    self.authorization_header = {'Authorization': 'Bearer ' + self.token}

  def _get_token(self):
    response = requests.post(
      self.auth_url,
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
    #print(response)
    #print(json.dumps(json.loads(response.content), indent=2))

    if response.status_code != 200 or not 'access_token' in response.json():
        raise Exception('Invalid authentication response')

    return response.json()['access_token']

  def create_report(self, metrics, dimensions, start_date, end_date, product, filters):
    print ("==>> Sending report creation request")
    reportRequest = """
      mutation ($input: AskPartnerReportFileInput!) {
        askPartnerReportFile(input: $input) {
          reportFile {
            reportToken
          }
        }
      }
    """
    response = requests.post(
      self.report_url,
      json={
        'query': reportRequest,
        'variables': {
          'input': {
            'metrics': metrics,
            'dimensions': dimensions,
            'filters': filters,
            'startDate': start_date,
            'endDate': end_date,
            'product': product,
          }
        }
      },
      headers = self.authorization_header
    )

    if response.status_code != 200 or not 'data' in response.json() or 'errors' in response.json():
        print(response)
        print(json.dumps(json.loads(response.content), indent=2))
        raise Exception('Invalid response')

    self.report_token = response.json()['data']['askPartnerReportFile']['reportFile']['reportToken']
    print ("<<== Request sent successfully")

  def _update_report_status(self):
    report_request_status_check = """
      query PartnerGetReportFile ($reportToken: String!) {
        partner {
          reportFile(reportToken: $reportToken) {
            status
            downloadLinks {
              edges {
                node {
                    link
                }
              }
            }
          }
        }
      }
    """
    response = requests.post(
      self.report_url,
      json={
        'query': report_request_status_check,
        'variables': {
          'reportToken': self.report_token
        }
      },
      headers = self.authorization_header
    )

    if response.status_code != 200 or not 'data' in response.json() or 'errors' in response.json():
      print(response)
      print(json.dumps(json.loads(response.content), indent=2))
      raise Exception('Invalid response')

    self.report_response = response
    self.report_status = response.json()['data']['partner']['reportFile']['status'];

  def _get_download_links(self):
    self.download_links = []
    for url in map(lambda edge: edge['node']['link'], self.report_response.json()['data']['partner']['reportFile']['downloadLinks']['edges']):
        self.download_links.append(url)

  def get_download_links_when_ready(self):
    print ("==>> Polling report status...")
    self._update_report_status()
    time_passed = 0
    while (self.report_status == 'IN_PROGRESS'):
      print('  Time: ' + str(time_passed) + ' seconds - Status: ' + self.report_status)
      time.sleep(5)
      time_passed = time_passed + 5
      self._update_report_status()

    print ("<<== Report is ready")
    if (self.report_status == 'FINISHED'):
      download_links = self._get_download_links()
      print ("==>> Download links:")
      print(self.download_links)