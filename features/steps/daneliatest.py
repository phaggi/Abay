# -*- coding: utf-8 -*-
from behave import *
from danelia.keymaker import Keymaker


# Откроем главную страницу. Передадим в качестве аргумента адрес страницы.
@given('file "{filename}"')
def step(context, filename):
    #
    context.file = filename


# Теперь нажмем на кнопку "Найти"
@when(u'create instance of class "{classname}" and call getkeys')
def step(context, classname):
    keyobject = Keymaker(context.file)
    context.keychain = keyobject.getkeys()

# Проверим, что мы на странице с результатами поиска, есть некоторый искомый текст
@then(u'instance keychain return "{owmkeyname}" == "{owmkeytarget}" and "{yandexkeyname}" == "{yandexkeytarget}"')
def step(context, owmkeyname, owmkeytarget, yandexkeyname, yandexkeytarget):
    owmkey, yandexkey = context.keychain
    assert owmkeytarget == owmkey
    assert yandexkeytarget == yandexkey
