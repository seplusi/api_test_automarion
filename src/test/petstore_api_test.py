import unittest
import requests
import jinja2
import json


class TestPetstoreApi(unittest.TestCase):
    """A sample test class to show how page object works"""

    @classmethod
    def setUpClass(cls):
        template_loader = jinja2.FileSystemLoader(searchpath="../main/templates/")
        cls.template_env = jinja2.Environment(loader=template_loader)
        cls.headers = {"accept": "application/json", "Content-Type": "application/json"}

    def setUp(self):
        pass

    def test_add_pet(self):

        add_pet_payload = self.template_env.get_template('add_pet_template.json')
        payload = add_pet_payload.render({'petname': 'bobbie'})
        response = requests.post(url='https://petstore.swagger.io/v2/pet', data=payload, headers=self.headers)
        assert response.status_code == 200
        assert response.ok
        assert response.reason == 'OK'

        response_json = json.loads(response.text)
        payload_json = json.loads(payload)

        assert response_json['name'] == payload_json['name']
        assert response_json['status'] == payload_json['status']
        assert isinstance(response_json['id'], int)

        self.validate_header(response.headers)

    def test_add_pet_with_empty_payload(self):

        response = requests.post(url='https://petstore.swagger.io/v2/pet', data='', headers=self.headers)
        assert response.status_code == 500
        assert not response.ok
        assert response.reason == 'Server Error'

        response_json = json.loads(response.text)

        assert response_json['code'] == 500
        assert response_json['type'] == "unknown"
        assert response_json['message'] == "something bad happened"

        self.validate_header(response.headers)

    def test_login_uer(self):
        response = requests.get(url='https://petstore.swagger.io/v2/user/login?username=seplusi&password=12345678', headers=self.headers)
        assert response.status_code == 200
        assert response.ok
        assert response.reason == 'OK'

        resp_text_items = response.text.split(':')
        assert resp_text_items[0] == 'logged in user session'
        assert resp_text_items[1].isdigit()

    def validate_header(self, response_header):
        assert response_header['content-type'] == 'application/json'
        assert response_header['Access-Control-Allow-Origin'] == '*'
        assert response_header['Access-Control-Allow-Methods'] == 'GET, POST, DELETE, PUT'
        assert response_header['Access-Control-Allow-Headers'] == 'Content-Type, api_key, Authorization'
        assert response_header['connection'] == 'close'



    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
