import requests
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api, _


class SendoSeller(models.Model):
    _name = "sendo.seller"
    _description = "Seller"

    shop_key = fields.Char(string='My Shop Key')
    secret_key = fields.Char(string='My Secret Key')
    token_connection = fields.Char(string='My Token')

