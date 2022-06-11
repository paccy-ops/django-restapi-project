

def get_period(month):
    period = ''
    if month == '01':
        period = 'Jan 1 - 31'
    elif month == '02':
        period = 'Feb 1 - 28'
    elif month == '03':
        period = 'Mar 1 - 31'
    elif month == '04':
        period = 'Apr 1 - 30'
    elif month == '05':
        period = 'May 1 - 31'
    elif month == '06':
        period = 'Jun 1 - 30'
    elif month == '07':
        period = 'Jul 1 - 31'
    elif month == '08':
        period = 'Aug 1 - 31'
    elif month == '09':
        period = 'Sep 1 - 30'
    elif month == '10':
        period = 'Oct 1 - 31'
    elif month == '11':
        period = 'Nov 1 - 30'
    elif month == '12':
        period = 'Dec 1 - 31'

    return period

def get_euro_format(_float):
    normal = "{:,.2f}".format(_float)
    tokens = normal.split('.')
    whole = tokens[0].replace(',','.')
    return f'{whole},{tokens[1]}'

    