from django.apps import AppConfig



class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Интернет магазин'

    def ready(self) -> None:
        from shop import signals
        
        signals.post_delete.connect(signals.update_cart_product_signal, self.get_model('CartProduct'))
        signals.post_save.connect(signals.update_cart_product_signal, self.get_model('CartProduct'))
        signals.pre_save.connect(signals.calculate_product_cart_table_row, self.get_model('CartProduct'))
        signals.pre_save.connect(signals.set_default_currency, self.get_model('Currency'))
        signals.pre_save.connect(signals.set_default_price_type, self.get_model('PriceType'))
        signals.post_save.connect(signals.set_default_photo_product, self.get_model('ImageProduct'))
        return super().ready()
