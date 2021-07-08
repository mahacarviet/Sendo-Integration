from odoo import fields, models, api


#       Class Inherit Sale Order
class ApiSendoSaleOrderInherit(models.Model):
    _inherit = "sale.order"

    sendo_order_number = fields.Char()
    sendo_order_status = fields.Selection([
        ('2', 'Mới'),
        ('3', 'Đang xử lý'),
        ('6', 'Đang vận chuyển'),
        ('7', 'Đã giao hàng'),
        ('8', 'Đã hoàn tất'),
        ('10', 'Đóng'),
        ('11', 'Yêu cầu hoãn'),
        ('12', 'Đang hoãn'),
        ('13', 'Hủy'),
        ('14', 'Yêu cầu tách'),
        ('15', 'Chờ tách'),
        ('19', 'Chờ gộp'),
        ('21', 'Đang đổi trả'),
        ('22', 'Đổi trả thành công'),
        ('23', 'Chờ Sendo xử lý')], string='Order Status')
    sendo_payment_status = fields.Selection([
        ('1', 'Chưa thanh toán'),
        ('2', 'Đã thanh toán COD'),
        ('3', 'Đã thanh toán'),
        ('4', 'Hoàn tất'),
        ('5', 'Đã hoàn tiền'),
        ('6', 'Đợi xác nhận'),
        ('7', 'Từ chối'),
        ('14', 'Đã thanh toán một phần'),
        ('15', 'Đã hoàn tiền một phần')], string='Payment Status')
    sendo_payment_method = fields.Selection([
        ('1', 'Thanh toán khi nhận hàng'),
        ('2', 'Thanh toán trực tuyến'),
        ('4', 'Thanh toán kết hợp'),
        ('5', 'Thanh toán trả sau')], string='Payment Method')

    # product_in_order_sale_order = fields.One2many('sale.order.line', 'product_in_list_order_sale_order')
