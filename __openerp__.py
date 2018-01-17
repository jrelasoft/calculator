# -*- coding: utf-8 -*-
{
    'name': "Stock Market Profit Planner",

    'summary': """Brokerage Calculator and Forecasting Profit/Loss""",

    'description': """This aspp will help to calculate Total Tax and Charges for Indian Stock Market's Equity Intraday, Delivery, Futures, Options.
    forecasting profit/loss dynamically based on user input withing certain sessions.""",

    'author': "JRELA Soft / Praba",
    'website': "http://www.jrelasoft.com",
    'category': 'Stock Market',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'decimal_precision'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data.xml',
        'views/templates.xml',
        'views/brokerage_config_view.xml',
        'views/profit_plan_view.xml',
        'views/trade_view.xml',
    ],
   
}