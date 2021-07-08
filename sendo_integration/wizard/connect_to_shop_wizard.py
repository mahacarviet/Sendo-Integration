import requests
import json
from odoo import fields, models, api, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError


class SellerConnectWizard(models.TransientModel):
    _name = 'sendo.connect.wizard'
    _description = 'Connect to Sendo Integration'

    shop_key = fields.Char(string='My Shop key')
    secret_key = fields.Char(string='My Secret Key')
    token_connection = fields.Char()

    def get_token_sendo(self):
        url = "https://open.sendo.vn/login"
        payload = json.dumps({
            "shop_key": self.shop_key,
            "secret_key": self.secret_key
        })
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.json()["success"]:
            token_connection = response.json()["result"]["token"]
            val = {
                'shop_key': self.shop_key,
                "secret_key": self.secret_key,
                'token_connection': token_connection
            }
            existed_secret = self.env['sendo.seller'].search([('secret_key', '=', self.secret_key)], limit=1)
            if len(existed_secret) < 1:
                self.env['sendo.seller'].create(val)
            else:
                existed_secret.write(val)
            # raise ValidationError(_('Connecting My Shop In Sendo Successful.'))
        else:
            raise ValidationError(_('My Shop Key or Secret Key is wrong.'))

