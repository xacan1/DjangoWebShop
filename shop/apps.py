from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Магазин UZM'

    def ready(self) -> None:
        from . import signals
        signals.post_delete.connect(signals.update_cart_product_signal, self.get_model('CartProduct'))
        signals.post_save.connect(signals.update_cart_product_signal, self.get_model('CartProduct'))
        signals.pre_save.connect(signals.calculate_product_cart_table_row, self.get_model('CartProduct'))
        return super().ready()
