from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class brokerage_config_settings(models.TransientModel):
	_name = "brokerage.config.settings"
	_inherit = "res.config.settings"

	# Intraday equity
	int_brokerage = fields.Float('Brokerage', digits=dp.get_precision('Brokerage'))
	int_gst = fields.Float('GST (%)')
	int_stt=fields.Float('STT Change')
	int_bse_transaction=fields.Float('Trasaction Change of BSE',digits=dp.get_precision('Brokerage'))
	int_sebi=fields.Float('SEBI Change')
	int_nse_transaction=fields.Float('Trasaction Change of NSE', digits=dp.get_precision('Brokerage'))
	# Intraday Deleivery
	del_brokerage = fields.Float('Brokerage', digits=dp.get_precision('Brokerage'))
	del_gst = fields.Float('GST (%)')
	del_stt=fields.Float('STT Change')
	del_bse_transaction=fields.Float('Trasaction Change of BSE')
	del_sebi=fields.Float('SEBI Change')
	del_nse_transaction=fields.Float('Trasaction Change of NSE')
	# Intraday equity
	fut_brokerage = fields.Float('Brokerage', digits=dp.get_precision('Brokerage'))
	fut_gst = fields.Float('GST (%)')
	fut_stt=fields.Float('STT Change')
	fut_bse_transaction=fields.Float('Trasaction Change of BSE')
	fut_sebi=fields.Float('SEBI Change')
	fut_nse_transaction=fields.Float('Trasaction Change of NSE')
	# Intraday Deleivery
	opt_brokerage = fields.Float('Brokerage', digits=dp.get_precision('Brokerage'))
	opt_gst = fields.Float('GST (%)')
	opt_stt=fields.Float('STT Change')
	opt_bse_transaction=fields.Float('Trasaction Change of BSE')
	opt_sebi=fields.Float('SEBI Change')
	opt_nse_transaction=fields.Float('Trasaction Change of NSE')


	@api.multi
	def set_equity_intraday(self):
		config_param_env = self.env['ir.config_parameter']

		equity_intraday = {
		'int_brokerage': self.int_brokerage or 0.00,
		'int_gst': self.int_gst or 0.00, 
		'int_stt': self.int_stt or 0.00,
		'int_bse_transaction': self.int_bse_transaction or 0.00,
		'int_nse_transaction': self.int_nse_transaction or 0.00,
		'int_sebi': self.int_sebi or 0.00,
		}
		config_param_env.set_param('equity_intraday', equity_intraday)


	@api.multi
	def get_default_equity_intraday(self):
		config_param_env = self.env['ir.config_parameter']

		equity_intraday = {}

		equity_intraday_str = config_param_env.get_param('equity_intraday')

		if equity_intraday_str:
			equity_intraday = eval(equity_intraday_str)

		return equity_intraday

	@api.multi
	def set_equity_delivery(self):
		config_param_env = self.env['ir.config_parameter']

		equity_delivery = {
		'del_brokerage': self.del_brokerage or 0.00,
		'del_gst': self.del_gst or 0.00, 
		'del_stt': self.del_stt or 0.00,
		'del_bse_transaction': self.del_bse_transaction or 0.00,
		'del_nse_transaction': self.del_nse_transaction or 0.00,
		'del_sebi': self.del_sebi or 0.00,
		}
		config_param_env.set_param('equity_delivery', equity_delivery)


	@api.multi
	def get_default_equity_delivery(self):
		config_param_env = self.env['ir.config_parameter']

		equity_delivery = {}

		equity_delivery_str = config_param_env.get_param('equity_delivery')

		if equity_delivery_str:
			equity_delivery = eval(equity_delivery_str)

		return equity_delivery

	@api.multi
	def set_equity_future(self):
		config_param_env = self.env['ir.config_parameter']

		equity_future = {
		'fut_brokerage': self.fut_brokerage or 0.00,
		'fut_gst': self.fut_gst or 0.00, 
		'fut_stt': self.fut_stt or 0.00,
		'fut_bse_transaction': self.fut_bse_transaction or 0.00,
		'fut_nse_transaction': self.fut_nse_transaction or 0.00,
		'fut_sebi': self.fut_sebi or 0.00,
		}
		config_param_env.set_param('equity_future', equity_future)


	@api.multi
	def get_default_equity_future(self):
		config_param_env = self.env['ir.config_parameter']

		equity_future = {}

		equity_future_str = config_param_env.get_param('equity_future')

		if equity_future_str:
			equity_future = eval(equity_future_str)

		return equity_future

	@api.multi
	def set_equity_option(self):
		config_param_env = self.env['ir.config_parameter']

		equity_option = {
		'opt_brokerage': self.opt_brokerage or 0.00,
		'opt_gst': self.opt_gst or 0.00, 
		'opt_stt': self.opt_stt or 0.00,
		'opt_bse_transaction': self.opt_bse_transaction or 0.00,
		'opt_nse_transaction': self.opt_nse_transaction or 0.00,
		'opt_sebi': self.opt_sebi or 0.00,
		}
		config_param_env.set_param('equity_option', equity_option)


	@api.multi
	def get_default_equity_option(self):
		config_param_env = self.env['ir.config_parameter']

		equity_option = {}

		equity_option_str = config_param_env.get_param('equity_option')

		if equity_option_str:
			equity_option = eval(equity_option_str)

		return equity_option