# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import admob_utils

sample = """{'row': {'dimensionValues': {'DATE': {'value': '20240220'}, 'APP': {'value':                          
 'ca-app-pub-2122146556116316~8497268021', 'displayLabel': 'ez빠른키보드 - 한글 키보드'}}, 'metricValues':              
 {'ESTIMATED_EARNINGS': {'microsValue': '13032842'}, 'AD_REQUESTS': {'integerValue': '100013'}, 'MATCHED_REQUESTS':     
 {'integerValue': '28208'}}}}"""


def generate_network_report(service, publisher_id):
  """Generates and prints a network report.

  Args:
    service: An AdMob Service Object.
    publisher_id: An ID that identifies the publisher.
  """

  # [START main_body]
  # Set date range. AdMob API only supports the account default timezone and
  # "America/Los_Angeles", see
  # https://developers.google.com/admob/api/v1/reference/rest/v1/accounts.networkReport/generate
  # for more information.
  import datetime

  # Get the current date
  current_date = datetime.date.today()

  # Extract year, month, and day from the current date
  current_year = current_date.year
  current_month = current_date.month
  current_day = current_date.day - 1
  date_range = {
    'start_date': {'year': current_year, 'month': current_month, 'day': current_day},
    'end_date': {'year': current_year, 'month': current_month, 'day': current_day}
  }

  # Set dimensions.
  dimensions = ['DATE', 'APP', 'PLATFORM', 'COUNTRY']
  dimensions = ['DATE', 'APP']

  # Set metrics.
  metrics = ['ESTIMATED_EARNINGS', 'AD_REQUESTS', 'MATCHED_REQUESTS']

  # Set sort conditions.
  sort_conditions = {'dimension': 'DATE', 'order': 'DESCENDING'}

  # Set dimension filters.
  dimension_filters = {
    'dimension': 'COUNTRY',
    'matches_any': {
      'values': ['US', 'CA']
    }
  }

  # Create network report specifications.
  report_spec = {
    'date_range': date_range,
    'dimensions': dimensions,
    'metrics': metrics,
    'sort_conditions': [sort_conditions],
    # 'dimension_filters': [dimension_filters]
  }

  # Create network report request.
  request = {'report_spec': report_spec}

  # Execute network report request.
  response = service.accounts().networkReport().generate(
    parent='accounts/{}'.format(publisher_id), body=request).execute()

  # Display responses.
  for report_line in response:
    print(report_line)
  print()
  print(str(int(response[1]['row']['metricValues']['ESTIMATED_EARNINGS']['microsValue']) / 1000 / 1000) + '$')
  # [END main_body]


def main():
  service = admob_utils.authenticate()
  generate_network_report(service, admob_utils.PUBLISHER_ID)


if __name__ == '__main__':
  main()
