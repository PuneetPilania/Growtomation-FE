# third party imports here
from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api, reqparse
import json

# create Restful api object and Blueprint object
hs_bp = Blueprint('hs_api', __name__)
hs_api = Api(hs_bp)

# local imports
from hubspot_service.hs_functions import HubspotBuilder


class FetchLeadAssociatedTickets(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('lead_email', type=str, required=True)
            args = parser.parse_args(strict=True)
            lead_email = args['lead_email']
            
            # call builder
            hs_builder = HubspotBuilder(lead_email)
            resp = hs_builder.fetch_associated_tickets_ids()

            return jsonify(resp)
        except:
            raise

class CreateTicket(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('lead_email', type=str, required=True)
            parser.add_argument('subject', type=str, required=True)
            args = parser.parse_args(strict=True)
            lead_email = args['lead_email']
            subject = args['subject']
            
            # call builder
            hs_builder = HubspotBuilder(lead_email)
            resp = hs_builder.create_ticket(subject)

            return jsonify(resp)
        except:
            raise

hs_api.add_resource(FetchLeadAssociatedTickets, '/lead/associated/tickets')
hs_api.add_resource(CreateTicket, '/ticket/create')