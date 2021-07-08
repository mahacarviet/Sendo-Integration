from odoo import fields, models, api


#       Class Inherit Product Attribute
class ApiSendoProductAttributeInherit(models.Model):
    _inherit = "product.attribute"

    sendo_attribute_id = fields.Integer(string='Sendo Attribute ID')
    sendo_attribute_code = fields.Char(string='Sendo Attribute Code')
    check_sendo_attribute = fields.Boolean(string='Sendo Attribute', compute='_compute_check_sendo_attribute', store=True)

    def _compute_check_sendo_attribute(self):
        for rec in self:
            if rec.sendo_attribute_id:
                if rec.sendo_attribute_code:
                    rec.check_sendo_attribute = True
            else:
                rec.check_sendo_attribute = False

