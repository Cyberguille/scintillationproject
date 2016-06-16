__author__ = 'root'

import re
p = re.compile(ur'(?P<id>\d{2}),(?P<ele>([0-8]\d|90)),(?P<azi>([0-3]\d{2})),(?P<snr>\d{2})')
test_str = u"$GPGSV,2,1,07,07,79,048,42,02,51,062,43,26,36,256,42,27,27,138,42*71"
print [m.groupdict() for m in p.finditer(test_str)]
for m in p.finditer(test_str):
    print m.group('id')
