def process_bangla(s):
    import re
    # s = "Example       aaaaaaaaa      \n \r String"
    replaced = re.sub(r'[\n|\r]', ' ', s)
    replaced = re.sub(r' +', ' ', replaced)

    return replaced