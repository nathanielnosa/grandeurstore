from django.conf import settings
import requests
from urllib.parse import urljoin

class Paystack:
    PAYSTACK_SECRETE_KEY = settings.PAYSTACK_SECRETE_KEY
    base_url = 'https://api.paystack.co/'

    def verify_payment(self, ref, *args, **kwargs):
        path = f'transaction/verify/{ref}'
        headers = {
            'Authorization': f"Bearer {self.PAYSTACK_SECRETE_KEY}",
            'Content-Type': "application/json"
        }
        url = urljoin(self.base_url, path)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False, str(e)

        response_data = response.json()
        if response.status_code == 200:
            return response_data['status'], response_data['data']
        else:
            return response_data['status'], response_data.get('message', 'An error occurred')

# Example usage
# paystack = Paystack()
# status, data_or_message = paystack.verify_payment('your_reference_here')
# print(status, data_or_message)
