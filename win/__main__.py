import sys
from tendo import singleton
from main import main

try:
    me = singleton.SingleInstance()
except singleton.SingleInstanceException:
    sys.exit(1)
main()