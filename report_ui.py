import requests
import appsecrets
import auth
import json
import time

### The following code is for testing purposes only. Please do you use this API to generate reports.

class ReportUI:
  def __init__(self, env='prod'):
    self._set_endpoints(env)
    self.authorization_header = {'Authorization': 'Bearer ' + auth.get_token(env)}
    self.channel_xid = "x1xgv67"
    self.channel_xid = appsecrets.get_secret('PARENT_XID')
    self.organization_xid = appsecrets.get_secret('ORG_XID')

  def _set_endpoints(self, env):
    if env == 'stage':
      env_base = appsecrets.get_secret('STAGE_URL')
    else:
      env_base = 'https://partner.api.dailymotion.com/'
    self.report_url = env_base + 'graphql'

  def create_report(self, name, metrics, dimensions, start_date, end_date, product, filters={}):
    print("==>> Sending report creation request")
    
    reportRequest = """
      mutation CREATE_REPORT($input: AnalyticsReportCreateInput!) {
        analyticsReportCreate(input: $input) {
          report {
            organizationXid
            channelXid
            createdAt
            hasRevenueInfo
            name
            reportToken
            status
          }
        }
      }
    """

    payload = {
        'query': reportRequest,
        'operationName': 'CREATE_REPORT',
        'variables': {
            'input': {
              'channelXid': self.channel_xid,
              'organizationXid': "x6eh",
              'name': name,
              'notify': False,
              'metrics': metrics,
              'dimensions': dimensions,
              'startDate': start_date,
              'endDate': end_date,
              'product': product,
            }
        }
    }

    response = requests.post(
      self.report_url,
      json=payload,
      headers=self.authorization_header
    )

    if response.status_code != 200 or 'data' not in response.json() or 'errors' in response.json():
      print(response)
      print(json.dumps(response.json(), indent=2))
      raise Exception('Invalid response')

    self.report_token = response.json()['data']['analyticsReportCreate']['report']['reportToken']
    print("<<== Request sent successfully")

  def _update_report_status(self):
    report_request_status_check = """
    query GET_REPORTS_QUERY($channelXid: String) {
      me {
        organizations {
          edges {
            node {
              analysis {
                reports(channelXid: $channelXid) {
                  edges {
                    node {
                      reportToken
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
          "query": report_request_status_check,
          "operationName": "GET_REPORTS_QUERY",
          "variables": { 
            "channelXid": self.channel_xid 
          }
      },
      headers=self.authorization_header
    )

    if response.status_code != 200 or 'data' not in response.json() or 'errors' in response.json():
      print(response)
      print(json.dumps(response.json(), indent=2))
      raise Exception('Invalid response')

    # Find the report node that matches our token
    report_edges = response.json()['data']['me']['organizations']['edges']
    for org_edge in report_edges:
      reports = org_edge['node']['analysis']['reports']['edges']
      for report in reports:
        if report['node']['reportToken'] == self.report_token:
          self.report_status = report['node']['status']
          self.download_links = [link_edge['node']['link'] for link_edge in report['node']['downloadLinks']['edges']]
          return

    raise Exception(f"Report with token {self.report_token} not found.")

  def get_download_links_when_ready(self):
    print ("==>> Polling report status...")
    self._update_report_status()
    time_passed = 0
    while (self.report_status != 'FINISHED'):
      print('  Time: ' + str(time_passed) + ' seconds - Status: ' + self.report_status)
      time.sleep(5)
      time_passed = time_passed + 5
      self._update_report_status()

    print ("<<== Report is ready")
    if (self.report_status == 'FINISHED'):
      print ("==>> Download links:")
      print(self.download_links)