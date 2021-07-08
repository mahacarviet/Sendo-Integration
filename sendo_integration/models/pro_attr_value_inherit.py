from odoo import fields, models, api


#       Class Inherit Product Attribute
class ApiSendoProductAttributeValueInherit(models.Model):
    _inherit = "product.attribute.value"

    sendo_attribute_value_id = fields.Integer(string='Sendo Attribute ID')
    check_sendo_attribute_value = fields.Boolean(string='Sendo Attribute Value',
                                                 compute='_compute_check_sendo_attribute', store=True)

    def _compute_check_sendo_attribute(self):
        for rec in self:
            if rec.sendo_attribute_value_id:
                rec.check_sendo_attribute_value = True
            else:
                rec.check_sendo_attribute_value = False
