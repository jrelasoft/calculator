from openerp import fields, models, api
import datetime

VALUES = [('intraday', 'Intraday'), ('delivery', 'Delivery'), ('futures', 'F&O Futures'),
              ('options', 'F&O Options')]

class trade_trade(models.Model):
	_name="trade.trade"

	@api.one
	@api.depends('buy_p', 'sell_p', 'qty','type')
	def _get_charges(self):
		ttc, np = self.env['brokerage.calc'].get_charges(self.buy_p or 0.00, self.sell_p or 0.00, self.qty or 0.00, self.type)

		self.ttc = ttc
		self.net_profit = np

	@api.one
	@api.depends('datetime')
	def _date_change(self):
		date = self.datetime
		dt= datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
		self.filter_date = dt.date()


	name=fields.Char('Name')
	datetime=fields.Datetime(default=fields.Datetime.now())
	buy_p=fields.Float('Buy Price')
	sell_p=fields.Float('Sell Price')
	qty=fields.Integer('Quantity')
	filter_date = fields.Char(compute= _date_change, store=True)

	type = fields.Selection(VALUES, default="intraday")
	ttc=fields.Float('Total TAX & Charge', compute=_get_charges)
	net_profit= fields.Float('Net Profit', compute=_get_charges, store=True)

	

