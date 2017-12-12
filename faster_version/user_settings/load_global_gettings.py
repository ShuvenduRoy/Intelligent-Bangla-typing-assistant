with open('user_settings/global_settings.txt', 'r') as f:
    language_settings = f.readline()
    global enabled_language
    enabled_language = 'bangla' if language_settings.split(' ')[1].startswith('bangla') else 'english'
    print("enabled languge: ",enabled_language)

    dictionary_settings = f.readline()
    global translate_to_bangla
    translate_to_bangla = True if dictionary_settings.split(' ')[1].startswith('yes') else False
