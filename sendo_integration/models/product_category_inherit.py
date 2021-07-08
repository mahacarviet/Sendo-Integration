from odoo import fields, models, api


#       Class Inherit Product Category
class ApiSendoProductCategoryInherit(models.Model):
    _inherit = "product.category"

    sendo_cate_id = fields.Integer(string='Category ID')
    sendo_level = fields.Integer(string='Level')
    sendo_parent_id = fields.Char(string='Sendo Parent ID')
    sendo_has_called = fields.Boolean(default=False)

