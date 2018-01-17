from openerp import fields, models, api
import random

class profit_planner(models.Model):
	_name="profit.planner"

	capital=fields.Float()
	days=fields.Integer()
	stock_lines=fields.One2many('stock.stock','profit_plan_id')
	profit_lines=fields.One2many('profit.planner.line','profit_plan_id')
	VALUES = [('intraday', 'Equity Intraday'), ('delivery', 'Equity Delivery'), ('futures', 'F&O Futures'),
              ('options', 'F&O Options')]
	select_mode = fields.Selection(VALUES, default="intraday")



	@api.multi
	def execute(self):
		stocks = []
		for stock in self.stock_lines:
			tmp_dict = {
				'name': stock.stock_name,
				'prices': map(float, stock.stock_prices.split(',')),
				'margins': map(float, stock.profit_margins.split(',')),
				'leverage': stock.leverage,
			}

			stocks.append(tmp_dict)
			lines = [(6, 0, [])]
		i = 1
		capital = self.capital
		select_mode = self.select_mode
		
		while i < self.days + 1:
			stock_select=random.choice(stocks)
			name=stock_select['name']
			leverage=stock_select['leverage']
			
			buy_price=random.choice(stock_select['prices'])
			margin=random.choice(stock_select['margins'])
			sell_price=buy_price + margin
			quantity= int((capital*leverage)/buy_price)
			quantity = quantity if quantity < 2100 else 2100


			print'---\n',buy_price,'--buy_price--\n'
			print'---\n',sell_price,'--sell_price---\n'
			print'---\n',leverage,'--leverage--\n'
			print'---\n',quantity,'--quantity--\n'

			ttc, np = self.env['brokerage.calc'].get_charges(buy_price, sell_price, quantity,select_mode)
			capital += np

			lines.append((0,0,{
				'sequence': i, 
				'name':name,
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

	@api.one
	@api.depends('buy_price', 'sell_price', 'quantity','select_mode')
	def _get_charges(self):
		if (self.buy_price or self.sell_price) and self.quantity:
			ttc, np, slct_md = self.env['brokerage.calc'].get_charges(self.buy_price or 0.00, self.sell_price or 0.00, self.quantity or 0.00, self.select_mode)
			
			self.total_tax_and_charges = ttc
			self.net_profit = np
			self.select_mode = slct_md
	name=fields.Char()
	sequence=fields.Integer()
	buy_price=fields.Float()
	sell_price=fields.Float()
	quantity=fields.Integer()
	total_tax_and_charges=fields.Float()
	net_profit=fields.Float()
	profit_plan_id=fields.Many2one('profit.planner')

class stock_stock(models.Model):
	_name="stock.stock"


	stock_name=fields.Char()
	stock_prices=fields.Char()
	profit_margins=fields.Char()
	leverage=fields.Float()
	profit_plan_id=fields.Many2one('profit.planner')