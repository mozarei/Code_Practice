from collections import defaultdict

def keep_records(records):
    return [record for record in records if record.get('skip') is not True]


def integer_label(value):
    if type(value) is not int or value not in {0,1}:raise ValueError('Expected integer 0 or 1')
    return value


def field_state(record, key):
    if key not in record:return 'missing'
    value=record[key]
    if value is None:return 'null'
    if isinstance(value,str) and value=='':return 'empty'
    return 'value'
