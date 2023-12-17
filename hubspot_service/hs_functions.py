import requests
from utils import getRequestHubspot, postRequestHubspot, getRequestStripe
import stripe

stripe.api_key = 'sk_test_51OOBFcSJbAzAaGwaC6vI6216XAfJwHA48cZtkkfmu8J4YDFYq5Vk7kc3Z01F4lq71Ix2vlSpsrTQtyg6yQTYGThR00nLzAc294'

class HubspotBuilder:
    def __init__(self, email):
        self.email = email
        self.user_vid = None
    
    def fetch_user_vid(self):
        url = f"https://api.hubapi.com/contacts/v1/contact/email/{self.email}/profile"
        resp = getRequestHubspot(url)

        if not resp:
            return {"status": 0, "message": "User not found in contact list."}
        
        if 'driver' not in resp['properties']['jobtitle']['value'].lower():
            return {"status": 0, "message": "User is not driver."}
        
        user_id = resp['vid']
        self.user_vid = user_id

        return {"status": 1, "message": "User Id fetched", "user_vid": self.user_vid}
    
    def fetch_associated_tickets_ids(self):
        # fetch user data if its an existing driver
        if not self.user_vid:
            user_resp = self.fetch_user_vid()
            if not user_resp['status']:
                return user_resp

        url = f"https://api.hubapi.com/crm/v3/objects/tickets"
        body = {
            "associations": [
                    {
                    "to": {
                        "id": self.user_vid
                    },
                    "types": [
                        {
                        "associationCategory": "HUBSPOT_DEFINED",
                        "associationTypeId": 15
                        }
                    ]
                    }
                ]
            }
        
        resp = getRequestHubspot(url, body)

        if not resp:
            return {"status": 0, "message": "No associated tickets Found."}
        
        associated_tickets = resp.get('results', [])
        open_tickets = [ticket for ticket in associated_tickets if ticket.get("properties", {}).get("hs_pipeline_stage") != '4']

        return {"status": 1, "message": "Associated open tickets Fetched", "tickets": open_tickets}
    

    def create_ticket(self, subject):
        # fetch user data if its an existing driver
        if not self.user_vid:
            user_resp = self.fetch_user_vid()
            if not user_resp['status']:
                return user_resp
        
        data = stripe.Customer.list()['data']
        customer_id = [i for i in data if i['email'] == self.email]

        if len(customer_id):
            customer_id = customer_id[0]['id']
            all_payments = stripe.PaymentIntent.list()
            customer_payment = [i for i in all_payments if i['customer'] == customer_id and i['status'] != 'succeeded']

            if len(customer_payment):
                customer_payment = customer_payment[0]
                return {'status': 0, 'message': "Please clear your pending due first.", "secret_token": customer_payment['client_secret']}
    
        # no pending payment so create ticket for issue
        url = 'https://api.hubapi.com/crm/v3/objects/tickets'
        body = {
                    "properties": {
                        "subject": subject,
                        "hubspot_owner_id": "650846798",
                        "hs_pipeline_stage": 1,
                    },
                    "associations": [
                        {
                        "to": {
                            "id": self.user_vid
                        },
                        "types": [
                            {
                            "associationCategory": "HUBSPOT_DEFINED",
                            "associationTypeId": 16
                            }
                        ]
                    }
                ]
            }
        
        resp = postRequestHubspot(url, body)

        return {"status": 1, "message": "Ticket created."}