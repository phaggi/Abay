#Укажем что это за фича
Feature: Checking Danelia
#Укажем имя сценария (в одной фиче может быть несколько)
Scenario: Сheck making of keys
#И используем наши шаги.
  Given file "danelia/danelia_template.yml"
  When create instance of class "../danelia/keymaker.Keymaker" and call getkeys
  Then instance keychain return "owmkey" == "97867564" and "yandexkey" == "13243546"