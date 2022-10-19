user_menu = {'Войти': 'login',
             'Регистрация': 'registration', 'Выйти': 'logout'}
main_menu = {'Главная': 'home', 'О нас': 'about-us',
             'Обратная связь': 'contact'}


class DataMixin:
    def get_user_context(self, **kwargs) -> dict:
        context = kwargs
        context_main_menu = main_menu.copy()
        context_user_menu = user_menu.copy()

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
        return context
