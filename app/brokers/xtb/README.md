http://developers.xstore.pro/documentation/#introduction

github search: xtb api filter python

https://github.com/Saitama298/Python-XTB-API
https://github.com/grimme-lab/xtb-python
https://github.com/federico123579/XTBApi



pip install websocket-client==1.4.1
pip install openpyxl==3.0.10

//////////////////////
from API import XTB

API = XTB("ID", "Password")
#your code
status, order_code = API.make_Trade("USDCAD", 0, 0, 0.1, comment="000001")
API.logout()

////////////////



