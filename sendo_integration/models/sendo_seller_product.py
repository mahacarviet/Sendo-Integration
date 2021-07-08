import requests
import json
from datetime import *
from odoo import fields, models, api
from urllib.request import urlopen
import base64
import pandas as pd
import re


class SendoSellerProduct(models.Model):
    _name = "sendo.seller.product"
    _description = "Seller Product Sendo"

    seller_product_id = fields.Char(string='Product ID', store=True)
    # category_for_name = fields.Char(string='Category', store=True)
    name = fields.Char(string='Product Name', store=True)
    # final_price_min = fields.Float(string='Price', store=True)
    # stock_quantity = fields.Integer(string='Available Product', store=True)
    # sku = fields.Char('SKU', store=True)
    # category_for_id = fields.Integer(store=True, string='Category ID')
    # store_name = fields.Char(store=True)
    # image = fields.Binary(store=True)

    date_from = fields.Char(store=True, default='')
    date_to = fields.Char(store=True, default=(datetime.today()).strftime("%Y-%m-%d"))

    # product_get_token = fields.Many2many('sendo.connect.wizard')
    # token_sendo = fields.Char(related='product_get_token.token_connection')

    categories = fields.Many2one(comodel_name='sendo.categories', string='Product Categories')

    # @api.onchange('date_from')
    def get_date_to(self):
        self.date_to = (datetime.today()).strftime("%Y-%m-%d")

        # Function get list product
        self.get_seller_product_sendo()

        self.date_from = self.date_to

    #       Add To Module Sendo Integration
    def get_seller_product_sendo(self):
        try:
            current_seller = self.env['sendo.seller'].sudo().search([])[0]

            url = "https://open.sendo.vn/api/partner/product/search/"

            payload = json.dumps({
                "page_size": 50,
                "product_name": "",
                "date_from": self.date_from or None,
                "date_to": self.date_to or None
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + current_seller.token_connection
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            seller_products = response.json()
            list_products = seller_products["result"]["data"]

            val = {}
            for product in list_products:
                if 'id' in product:
                    val['seller_product_id'] = product['id']
                    # val['category_for_name'] = product['category_4_name']
                    val['name'] = product['name']
                    # val['final_price_min'] = product['final_price_min']
                    # val['stock_quantity'] = product['stock_quantity']
                    # val['sku'] = product['sku']
                    # val['category_for_id'] = product['cate_4_id']
                    # val['store_name'] = product['store_name']
                    # val['image'] = base64.b64encode(urlopen(product["image"]).read())
                    existed_seller_product = self.env['sendo.seller.product'].search(
                        [('seller_product_id', '=', product['id'])], limit=1)
                    #   Link To Sendo Categories
                    # existed_categories_product = self.env['sendo.categories'].search(
                    #     [('category_id', '=', product['cate_4_id'])], limit=1)
                    # val['categories'] = existed_categories_product.id
                    #   Check Product In Database
                    if len(existed_seller_product) < 1:
                        self.env['sendo.seller.product'].create(val)
                    else:
                        existed_seller_product.write(val)

        except Exception as e:
            print(e)

    #       Add To Module Sale
    def get_product_sendo_to_product_template(self):
        try:
            current_seller = self.env['sendo.seller'].sudo().search([])[0]

            url = "https://open.sendo.vn/api/partner/product/search/"

            payload = json.dumps({
                "page_size": 50,
                "product_name": "",
                "date_from": self.date_from or None,
                "date_to": self.date_to or None
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + current_seller.token_connection
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            seller_products = response.json()
            list_products = seller_products["result"]["data"]

            val = {}
            for product in list_products:
                if 'id' in product:
                    #   Link To Sendo Categories
                    existed_categories_product = self.env['product.category'].search(
                        [('sendo_cate_id', '=', product['cate_4_id'])], limit=1)
                    val['categ_id'] = existed_categories_product.id
                    val['sendo_product_id'] = product['id']
                    val['sendo_category_id'] = existed_categories_product.sendo_cate_id
                    val['type'] = 'product'
                    val['name'] = product['name']
                    val['taxes_id'] = None
                    val['is_published'] = True
                    val['list_price'] = product['final_price_min']
                    # val['qty_available'] = product['stock_quantity']
                    val['default_code'] = product['sku']
                    # val['category_for_id'] = product['cate_4_id']
                    # val['store_name'] = product['store_name']
                    val['sale_ok'] = True
                    val['purchase_ok'] = False
                    val['image_1920'] = base64.b64encode(urlopen(product["image"]).read())
                    #   Field Sendo Add To Core
                    # val['sendo_stock_availability'] = product['stock_availability']
                    val['sendo_height'] = float(product['height'])
                    val['weight'] = float(product['weight'] / 1000)
                    val['sendo_length'] = float(product['length'])
                    val['sendo_width'] = float(product['width'])
                    val['sendo_unit_id'] = str(product['unit_id'])
                    val['sendo_stock_quantity'] = int(product['stock_quantity']) or 0
                    val['sendo_promotion_from_date'] = datetime.fromtimestamp(
                        int(product['promotion_from_date_timestamp'])) or None
                    val['sendo_promotion_to_date'] = datetime.fromtimestamp(
                        int(product['promotion_to_date_timestamp'])) or None
                    # val['sendo_is_promotion'] = product['is_promotion']
                    val['sendo_special_price'] = float(product['special_price'])
                    val['sendo_url_avatar_image'] = product['image']
                    #

                    existed_seller_product = self.env['product.template'].search([('name', '=', product['name'])],
                                                                                 limit=1)
                    #   Check Product In Database
                    if len(existed_seller_product) < 1:
                        self.env['product.template'].create(val)
                    else:
                        existed_seller_product.write(val)

        except Exception as e:
            print(e)

        #       Call API For Each Product

    def get_each_product_sendo_to_product_template(self):
        try:
            current_seller = self.env['sendo.seller'].sudo().search([])[0]

            list_product_sendo = self.env['sendo.seller.product'].sudo().search([])

            for each_product_sendo in list_product_sendo:

                url = "https://open.sendo.vn/api/partner/product?id=" + each_product_sendo["seller_product_id"]

                payload = ""

                headers = {
                    'Authorization': 'Bearer ' + current_seller.token_connection
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                seller_products = response.json()

                product = seller_products["result"]

                val = {}
                # for product in list_products:
                if 'id' in product:
                    #   Link To Sendo Categories
                    existed_categories_product = self.env['product.category'].search(
                        [('sendo_cate_id', '=', int(product['cat_4_id']))], limit=1)
                    val['categ_id'] = int(existed_categories_product.id)
                    val['sendo_product_id'] = int(product['id'])
                    val['sendo_category_id'] = int(existed_categories_product.sendo_cate_id)
                    val['type'] = 'product'
                    val['name'] = product['name']
                    val['taxes_id'] = None
                    val['is_published'] = True
                    val['list_price'] = product['price']
                    val['default_code'] = product['sku']
                    val['sale_ok'] = True
                    val['purchase_ok'] = False
                    val['image_1920'] = base64.b64encode(urlopen(product["image"]).read())
                    val['weight'] = float(product['weight'] / 1000)
                    val['description'] = re.sub(r'<.*?>', '', product['description'])

                    #   Field Sendo Add To Core
                    val['sendo_height'] = float(product['height'])
                    val['sendo_length'] = float(product['length'])
                    val['sendo_width'] = float(product['width'])
                    val['sendo_unit_id'] = str(product['unit_id'])
                    val['sendo_url_avatar_image'] = product['image']

                    #   Check Sendo Product Stock Available
                    if product['stock_availability']:
                        val['sendo_stock_availability'] = True
                        val['sendo_stock_quantity'] = int(product['stock_quantity'])
                    else:
                        val['sendo_stock_availability'] = False

                    #   Check Sendo Product Is Promotion
                    if product['is_promotion']:
                        val['sendo_is_promotion'] = True
                        val['sendo_special_price'] = float(product['special_price'])
                        if product['promotion_from_date_timestamp']:
                            val['sendo_promotion_from_date'] = date.fromtimestamp(
                                int(product['promotion_from_date_timestamp']))
                        else:
                            val['sendo_promotion_from_date'] = date.today()
                        if product['promotion_to_date_timestamp']:
                            val['sendo_promotion_to_date'] = date.fromtimestamp(
                                int(product['promotion_to_date_timestamp']))
                        else:
                            val['sendo_promotion_to_date'] = date.today() + timedelta(days=9000)
                    else:
                        val['sendo_is_promotion'] = False

                    existed_seller_product = self.env['product.template'].search([('name', '=', product['name'])],
                                                                                 limit=1)
                    #   Check Product In Database
                    if len(existed_seller_product) < 1:
                        self.env['product.template'].create(val)
                    else:
                        existed_seller_product.write(val)

                    #   Check Sendo Product Have Variant
                    atrri_product = {}
                    if product['is_config_variant']:
                        for attribute_product in product['attributes']:
                            if attribute_product['attribute_is_checkout']:
                                atrri_product['name'] = attribute_product['attribute_name']
                                atrri_product['sendo_attribute_id'] = attribute_product['attribute_id']
                                atrri_product['sendo_attribute_code'] = attribute_product['attribute_code']
                                atrri_product['check_sendo_attribute'] = True
                                atrri_product['display_type'] = 'radio'

                                #   Check Attribute Product In Database
                                existed_attribute_product = self.env['product.attribute'].search(
                                    [('sendo_attribute_id', '=', attribute_product['attribute_id'])], limit=1)
                                if len(existed_attribute_product) < 1:
                                    self.env['product.attribute'].create(atrri_product)
                                else:
                                    pass
                                #   Add Attribute Value Sendo Product In Database
                                atrri_product_value = {}
                                for child_attribute in attribute_product['attribute_values']:
                                    if child_attribute['is_selected']:
                                        search_attribute_product_sendo = self.env['product.attribute'].search(
                                            [('sendo_attribute_id', '=', attribute_product['attribute_id'])], limit=1)
                                        atrri_product_value['sendo_attribute_value_id'] = child_attribute['id']
                                        atrri_product_value['name'] = child_attribute['value']
                                        atrri_product_value['attribute_id'] = search_attribute_product_sendo.id
                                        atrri_product_value['check_sendo_attribute_value'] = True

                                        #   Check Attribute Product In Database
                                        existed_attribute_value_product = self.env['product.attribute.value'].search(
                                            [('sendo_attribute_value_id', '=', child_attribute['id'])], limit=1)
                                        if len(existed_attribute_value_product) < 1:
                                            self.env['product.attribute.value'].create(atrri_product_value)
                                        else:
                                            pass
                                    else:
                                        pass
                            else:
                                pass
                        # val_child_product = {}
                        # val_child_product_attribute = {}
                        # for child_product in product['variants']:
                        #     #   Search Attribute ID & Attribute Value
                        #     search_sendo_attribute_value = self.env['product.attribute.value'].search(
                        #         [(
                        #          'sendo_attribute_value_id', '=', child_product['variant_attributes'][0]['option_id'])],
                        #         limit=1)
                        #     search_sendo_product_id = self.env['product.template'].search(
                        #         [('sendo_product_id', '=', product['id'])], limit=1)
                        #     val_child_product['attribute_id'] = search_sendo_attribute_value.attribute_id.id
                        #     # val_child_product['value_ids'] = search_sendo_attribute_value.id
                        #     val_child_product['product_tmpl_id'] = search_sendo_product_id.id
                        #     self.env['product.template.attribute.line'].create(val_child_product)
                            # val_child_product_attribute['product_attribute_value_id'] = search_sendo_attribute_value.id
                            # val_child_product_attribute['product_template_attribute_line_id'] = search_sendo_attribute_value.id

                            # search_sendo_product_attribute = self.env['product.template.attribute.line'].search(
                            #     [('product_attribute_value_id', '=',
                            #       child_product['variant_attributes'][0]['option_id'])],
                            #     limit=1)
                            # if len(search_sendo_product_attribute) < 1:
                            #     self.env['product.template.attribute.line'].create(val_child_product)
                            # else:
                            #     pass
                    else:
                        pass

        except Exception as e:
            print(e)
