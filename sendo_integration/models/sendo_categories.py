import requests
import json
from odoo import fields, models, api


class SendoCategories(models.Model):
    _name = "sendo.categories"
    _description = "Update Categories Sendo"

    category_id = fields.Integer(string='Category ID')
    name = fields.Text(string='Name')
    level = fields.Integer(string='Level')
    sendo_parent_id = fields.Char(string='Sendo Parent ID')
    has_called = fields.Boolean(default=False)

    parent_id = fields.Many2one(comodel_name='sendo.categories', string='Parent Category')

    # count_category = fields.Integer(default=0)
    # count_category_child = fields.Integer(default=0)

    # product_get_token = fields.Many2many('sendo.connect.wizard')
    # token_sendo = fields.Char(related='product_get_token.token_connection')

    #       Add To Module Sendo Integration
    def get_categories_sendo(self):
        # if self.count_category < 1:
        current_seller = self.env['sendo.seller'].sudo().search([])[0]

        url = "https://open.sendo.vn/api/partner/category/0"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + current_seller.token_connection
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        result_category = response.json()
        categories = result_category["result"]
        val = {}
        if categories:
            for cate in categories:
                try:
                    if ('id' and 'name' and 'level') in cate:
                        val['category_id'] = cate['id']
                        val['name'] = cate['name']
                        val['sendo_parent_id'] = cate['parent_id']
                        val['level'] = cate['level']
                        val['has_called'] = False
                except Exception as e:
                    print(e)
                existed_category = self.env['sendo.categories'].search([('category_id', '=', cate['id'])], limit=1)
                if len(existed_category) < 1:
                    self.env['sendo.categories'].create(val)
                else:
                    existed_category.write(val)
        # self.count_category = self.count_category + 1

    # else:
    #     pass
    # return self.count_category

    #       Add To Module Sendo Integration
    def get_child_categories_sendo(self):
        # if self.count_category_child < 2:
        current_seller = self.env['sendo.seller'].sudo().search([])[0]
        has_not_called_api = self.env['sendo.categories'].sudo().search(
            [('has_called', '=', False), ('level', '!=', 4)])
        # has_not_called_api = self.env['sendo.categories'].sudo().search([('has_called', '=', False), ('attribute', '!=', True)])
        for a in has_not_called_api:
            url = 'https://open.sendo.vn/api/partner/category/' + str(a['category_id'])

            payload = {}
            headers = {
                'Authorization': 'Bearer ' + current_seller.token_connection
            }

            response_raw = requests.request("GET", url, headers=headers, data=payload)

            result_child_cate = response_raw.json()
            response = result_child_cate["result"]
            val = {}
            if response:
                for res in response:
                    try:
                        if ('id' and 'name' and 'level') in res:
                            val['category_id'] = res['id']
                            val['name'] = res['name']
                            val['level'] = res['level']
                            val['sendo_parent_id'] = a.category_id
                            val['parent_id'] = a.id
                            val['has_called'] = False
                            self.env['sendo.categories'].create(val)
                    except Exception as e:
                        print(e)
            a.has_called = True

    #     self.count_category_child = self.count_category_child + 1
    # else:
    #     pass
    # return self.count_category_child

    #       Add To Module Sale
    def get_categories_sendo_to_product_template(self):
        current_seller = self.env['sendo.seller'].sudo().search([])[0]

        url = "https://open.sendo.vn/api/partner/category/0"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + current_seller.token_connection
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        result_category = response.json()
        categories = result_category["result"]
        val = {}
        if categories:
            for cate in categories:
                try:
                    if ('id' and 'name' and 'level') in cate:
                        val['sendo_cate_id'] = cate['id']
                        val['name'] = cate['name']
                        val['sendo_parent_id'] = cate['parent_id']
                        val['sendo_level'] = cate['level']
                        val['sendo_has_called'] = False
                except Exception as e:
                    print(e)
                existed_category = self.env['product.category'].search([('sendo_cate_id', '=', cate['id'])], limit=1)
                if len(existed_category) < 1:
                    self.env['product.category'].create(val)
                else:
                    existed_category.write(val)

    #       Add To Module Sale
    def get_child_categories_sendo_to_product_template(self):
        current_seller = self.env['sendo.seller'].sudo().search([])[0]
        has_not_called_api = self.env['product.category'].sudo().search(
            [('sendo_has_called', '=', False), ('sendo_level', '!=', 4)])
        for a in has_not_called_api:
            url = 'https://open.sendo.vn/api/partner/category/' + str(a['sendo_cate_id'])

            payload = {}
            headers = {
                'Authorization': 'Bearer ' + current_seller.token_connection
            }

            response_raw = requests.request("GET", url, headers=headers, data=payload)

            result_child_cate = response_raw.json()
            response = result_child_cate["result"]
            val = {}
            if response:
                for res in response:
                    try:
                        if ('id' and 'name' and 'level') in res:
                            val['sendo_cate_id'] = res['id']
                            val['name'] = res['name']
                            val['sendo_level'] = res['level']
                            val['sendo_parent_id'] = a.sendo_cate_id
                            val['parent_id'] = a.id
                            val['sendo_has_called'] = False
                            self.env['product.category'].create(val)
                    except Exception as e:
                        print(e)
            a.sendo_has_called = True

