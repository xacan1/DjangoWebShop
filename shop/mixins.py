from shop import services


user_menu = {'Войти': 'login',
             'Регистрация': 'registration', 'Выйти': 'logout'}
main_menu = {'Главная': 'home', 'О нас': 'about-us',
             'Часто задаваемые вопросы': 'faq', 'Обратная связь': 'contact'}


class DataMixin:
    def get_user_context(self, **kwargs) -> dict:
        context = kwargs
        context_main_menu = main_menu.copy()
        context_user_menu = user_menu.copy()

        if self.request.user.is_anonymous:
            self.request.session['sessionid'] = self.request.session.session_key

        if not self.request.user.is_authenticated:
            context_main_menu.pop('Обратная связь')
            context_user_menu.pop('Выйти')
        elif not self.request.user.is_staff:
            context_user_menu[self.request.user.email] = 'profile'
            context_user_menu.pop('Войти')
            context_user_menu.pop('Регистрация')
        else:
            context_user_menu[self.request.user.email] = 'profile'
            context_user_menu.pop('Войти')
            context_user_menu.pop('Регистрация')

        context['user_menu'] = context_user_menu
        context['main_menu'] = context_main_menu
        context['categories'] = services.get_categories(None)
        context['currencies'] = services.get_currencies()
        return context
