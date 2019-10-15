import unittest
import docsredirector

def gen_event(req):
  event = dict()
  event['Records'] = list()
  record = dict()
  record['cf'] = dict()
  record['cf']['request'] = req
  event['Records'].append(record)
  return event

def gen_request(uri, method):
  request = dict()
  request['uri'] = uri
  request['method'] = method
  return request

class MyTestCase(unittest.TestCase):

  def test_process_uri(self):
    expected_results = {
      '/python/index.html': ('python', 'index.html'),
      '/python': ('python', ''),
      '/python/': ('python', ''),
      '/r/index.html': ('r', 'index.html'),
      '/rest/index.html': ('rest', 'index.html'),
      '/articles/annotation_and_query.html': ('userguide', 'articles/annotation_and_query.html')
    }
    for t in expected_results:
      self.assertEquals(expected_results[t], docsredirector.process_uri(t))

  def test_handler(self):
    expected_results =  {
      '/articles/annotation_and_query.html': {'status': '302', 'statusDescription': 'Found', 'headers': {'location': [{'key': 'Location', 'value': 'https://user-guides.synapse.org/articles/annotation_and_query.html'}]}},
      '/python': {'status': '302', 'statusDescription': 'Found', 'headers': {'location': [{'key': 'Location', 'value': 'https://python-docs.synapse.org/build/html/'}]}},
      '/rest/POST/accessApproval/group.html': {'uri': '/rest/POST/accessApproval/group.html', 'method': 'GET'},
      '/r/reference/synStore.html': {'status': '302', 'statusDescription': 'Found', 'headers': {'location': [{'key': 'Location', 'value': 'https://r-docs.synapse.org/reference/synStore.html'}]}},
      '/python/index.html#wikis': {'status': '302', 'statusDescription': 'Found', 'headers': {'location': [{'key': 'Location', 'value': 'https://python-docs.synapse.org/build/html/index.html#wikis'}]}}
    }
    for tu in expected_results:
      test_event = gen_event(gen_request(tu, 'GET'))
      self.assertEquals(expected_results[tu], docsredirector.lambda_handler(test_event, None))

if __name__ == '__main__':
  unittest.main()
