from odoo import fields, models, api, _


class ApiSendoSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    date_to = fields.Date()

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    don_gia_thuong_theo_quy = fields.Float(string='Đơn giá thưởng quý')
    don_gia_ngay_nghi_phep = fields.Float(string='Đơn giá ngày nghỉ phép')
    muc_dong_gop_bao_hiem = fields.Float(string="Mức đóng góp bảo hiểm xã hội")
    muc_dong_doan_phi = fields.Float(string="Mức đóng góp đoàn phí")
    luong_toi_thieu = fields.Float(string="Lương tối thiểu vùng")
    giam_tru_phu_thuoc = fields.Float(string="Giảm trừ phù thuộc")
    giam_tru_ca_nhan = fields.Float(string="Giảm trừ cá nhân")

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            don_gia_thuong_theo_quy=float(params.get_param('gd_hr.don_gia_thuong_theo_quy')),
            don_gia_ngay_nghi_phep=float(params.get_param('gd_hr.don_gia_ngay_nghi_phep')),
            muc_dong_gop_bao_hiem=float(params.get_param('gd_hr.muc_dong_gop_bao_hiem')),
            muc_dong_doan_phi=float(params.get_param('gd_hr.muc_dong_doan_phi')),
            luong_toi_thieu=float(params.get_param('gd_hr.luong_toi_thieu')),
            giam_tru_phu_thuoc=float(params.get_param('gd_hr.giam_tru_phu_thuoc')),
            giam_tru_ca_nhan=float(params.get_param('gd_hr.giam_tru_ca_nhan')),
        )
        return res

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()

        field_luong_toi_thieu = self.luong_toi_thieu and self.luong_toi_thieu or False
        field_don_gia_thuong_theo_quy = self.don_gia_thuong_theo_quy and self.don_gia_thuong_theo_quy or False
        field_don_gia_ngay_nghi_phep = self.don_gia_ngay_nghi_phep and self.don_gia_ngay_nghi_phep or False
        field_muc_dong_gop_bao_hiem = self.muc_dong_gop_bao_hiem and self.muc_dong_gop_bao_hiem or False
        field_muc_dong_doan_phi = self.muc_dong_doan_phi and self.muc_dong_doan_phi or False
        field_giam_tru_ca_nhan = self.giam_tru_ca_nhan and self.giam_tru_ca_nhan or False
        field_giam_tru_phu_thuoc = self.giam_tru_phu_thuoc and self.giam_tru_phu_thuoc or False

        param.set_param('gd_hr.giam_tru_ca_nhan', field_giam_tru_ca_nhan)
        param.set_param('gd_hr.giam_tru_phu_thuoc', field_giam_tru_phu_thuoc)
        param.set_param('gd_hr.luong_toi_thieu', field_luong_toi_thieu)
        param.set_param('gd_hr.don_gia_thuong_theo_quy', field_don_gia_thuong_theo_quy)
        param.set_param('gd_hr.don_gia_ngay_nghi_phep', field_don_gia_ngay_nghi_phep)
        param.set_param('gd_hr.muc_dong_gop_bao_hiem', field_muc_dong_gop_bao_hiem)
        param.set_param('gd_hr.muc_dong_doan_phi', field_muc_dong_doan_phi)