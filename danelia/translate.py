from yandex import Yandex
tr = Yandex("API")
elif 'переведи' in exersize or 'перевод' in exersize or 'переводчик' in exersize:
    	talk('На какой язык вы хотите перевести слово?')
    	r = sr.Recognizer()
    	with sr.Microphone() as source3:
    		audio3 = r.listen(source3)
    		language= r.recognize_google(audio3, language="ru-Ru").lower()
    		if 'французкий' in language or 'французкий' in language:
    			nameOFlanguage = 'fr'
    		elif 'русский' in language or 'руский' in language:
    			nameOFlanguage = 'ru'
    		elif 'арабский' in language:
    			nameOFlanguage = 'ar'
    		elif 'испанский' in language:
    			nameOFlanguage = 'es'
    		elif 'индонезиский' in language or 'индонезийский' in language:
    			nameOFlanguage = 'id'
    		elif 'португальский' in language:
    			nameOFlanguage = 'pt'
    		elif 'бенгальский' in language:
    			nameOFlanguage = 'bn'
    		elif 'хинди' in language or 'синди' in language or 'бенди' in language:
    			nameOFlanguage = 'hi'
    		elif 'английский' in language:
    			nameOFlanguage = 'en'
    		elif 'китайский' in language:
    			nameOFlanguage = 'zh'
    		elif 'японский' in language:
    			nameOFlanguage = 'ja'
    		elif 'турецкий' in language:
    			nameOFlanguage = 'tr'
    		elif 'немецкий' in language:
    			nameOFlanguage = 'de'
    	try:
    		language = r.recognize_google(audio3, language="ru-Ru").lower()
    		print('Вы сказали : ' + language)
    	except sr.UnknownValueError:
    		talk('Я вас не поняла , повторите пожалуйста ')
    		language = commands()
    		return language
    	talk('Какое слово вы хотите перевести ?')
    	r = sr.Recognizer()
    	with sr.Microphone() as source4:
    		audio4 = r.listen(source4)
    		nameOFsearch = r.recognize_google(audio4, language="ru-Ru").lower()
    	try:
    		nameOFsearch = r.recognize_google(audio4, language="ru-Ru").lower()
    		print('Вы сказали : ' + nameOFsearch)
    	except sr.UnknownValueError:
    		talk('Я вас не поняла , повторите пожалуйста ')
    		nameOFsearch = commands()
    		return nameOFsearch
    	talk(tr.translate(nameOFsearch, nameOFlanguage))
