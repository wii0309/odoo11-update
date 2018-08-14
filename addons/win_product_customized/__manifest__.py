{
    'name': "win_product_customized",

    'author': "元植X先傑",
    'category': '',
    'version': '1.0',
    'description': """

        """,
    'depends': ['base','product','website_sale'],

    'data': [
        'views/product_template_views.xml',
        'views/category.xml',
        'views/color_table.xml',
        'views/size_table.xml',
        'views/product_product_inherit.xml',
        'views/product_class.xml',
        'views/region_code.xml',
        'views/gift_code.xml',
        'views/additional_code.xml',
        'views/add_res_ser_number.xml',
        'wizard/upload_excel.xml'
        # 'views/man_type.xml',
        # 'views/mid_type.xml',
        # 'views/sml_type.xml',
        # 'views/year_season.xml',
        # 'views/brand_info.xml',
        # 'views/big_type.xml',
        # 'views/brand_type.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}