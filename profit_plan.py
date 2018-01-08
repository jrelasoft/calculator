from openerp import fields, models, api
import random

class profit_planner(models.Model):
	_name="profit.planner"

	capital=fields.Float()
	stock_name=fields.Char()
	stock_prices=fields.Char()
	profit_margins=fields.Char()
	days=fields.Integer()
	leverage=fields.Float()
	profit_lines=fields.One2many('profit.planner.line','profit_plan_id')

	@api.multi
	def execute(self):
		stock_prices = map(float, self.stock_prices.split(','))
		profit_margins = map(float, self.profit_margins.split(','))
		capital = self.capital
		lines = [(6, 0, [])]

		i = 1
		while i < self.days + 1:
			buy_price = random.choice(stock_prices)
			sell_price = buy_price + random.choice(profit_margins)
			quantity = int((capital*self.leverage) / buy_price)
			quantity = quantity if quantity < 2100 else 2100

			ttc, np = self.env['brokerage.calc'].get_charges(buy_price, sell_price, quantity)
			capital += np

			lines.append((0,0,{
				'sequence': i, 
				'buy_price': buy_price, 
				'sell_price': sell_price, 
				'quantity': quantity,
				'total_tax_and_charges': ttc,
				'net_profit': np,
				}))
			i += 1
		self.profit_lines = lines

class profit_planner_line(models.Model):
	_name="profit.planner.line"

	# @api.one
	# @api.depends('buy_price', 'sell_price', 'quantity')
	# def _get_charges(self):
	# 	if (self.buy_price or self.sell_price) and self.quantity:
	# 		ttc, np = self.env['brokerage.calc'].get_charges(self.buy_price or 0.00, self.sell_price or 0.00, self.quantity or 0.00)
			
	# 		self.total_tax_and_charges = ttc
	# 		self.net_profit = np

	sequence=fields.Integer()
	buy_price=fields.Float()
	sell_price=fields.Float()
	quantity=fields.Integer()
	total_tax_and_charges=fields.Float()
	net_profit=fields.Float()
	profit_plan_id=fields.Many2one('profit.planner')

