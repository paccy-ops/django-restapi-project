def money_change_format(money):
    """Money change format function return """
    tokens = money.split(',')
    final_value = tokens[0].replace('.','')
    if len(tokens) > 1:
        final_value = '.'.join([final_value, tokens[1]])
    return final_value
