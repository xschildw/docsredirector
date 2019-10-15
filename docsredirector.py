import re

# Returns a tuple (subdomain, path) to match in handler
def process_uri(uri):
  pattern_all = re.compile('/(python|rest|r)/?(.*)')

  m = pattern_all.match(uri)
  if (m != None):
    return m.group(1, 2)
  else:
    uri = uri.lstrip('/')
    return ('userguide', uri)

# handler
def lambda_handler(event, context):
  SUBDOMAIN_MAP = {
    'python': 'python-docs.synapse.org/build/html',
    'r': 'r-docs.synapse.org',
    'rest': 'docs.synapse.org',
    'userguide': 'user-guides.synapse.org'
  }

  request = event['Records'][0]['cf']['request']
  uri = request['uri']
  processed_uri = process_uri(uri)

  if processed_uri[0] == 'rest':
    # Just go on
    return request
  else:
    redirect_location = "https://{}/{}".format(SUBDOMAIN_MAP[processed_uri[0]], processed_uri[1])
    response = {
      'status': '302',
      'statusDescription': 'Found',
      'headers': {
        'location': [{
          'key': 'Location',
          'value': redirect_location
        }]
      }
    }
    return response
