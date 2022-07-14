import re

#write
# span('2008-01-02 00:00', '2011-12-31 23:00')
#or even shorter
# span('2008-01-02', '2011-12-31')
#instead of
# pd.date_range('2008-01-02 00:00', '2011-12-31 23:00', freq='H')

def span(start, end=None, freq='H'):
    if not end:
        end = start
    pattern = re.compile("^....-..-..$") #matches patterns like YYYY-MM-DD
    if pattern.match(start):
        start += " 00:00"
    if pattern.match(end):
        end += " 23:00"
    return pd.date_range(start=start, end=end, freq=freq)