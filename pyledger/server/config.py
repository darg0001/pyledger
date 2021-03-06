#    Pyledger. A simple ledger for smart contracts implemented in Python
#    Copyright (C) 2017  Guillem Borrell Nogueras
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import argparse
from collections import namedtuple
from cryptography.hazmat.backends import default_backend

# USER CONFIGURATION AT THE END OF THE FILE #

if len(sys.argv) > 2 and 'test' in sys.argv[2]:
    argstype = namedtuple('Arguments', ['db', 'debug', 'sync', 'port', 'test'])
    args = argstype(db='sqlite://', debug=False, sync=True, port=8888,
                    test=True)

elif 'pytest' in sys.argv[0]:
    argstype = namedtuple('Arguments', ['db', 'debug', 'sync', 'port', 'test'])
    args = argstype(db='sqlite://', debug=False, sync=True, port=8888,
                    test=True)

elif 'sphinx' in sys.argv[0]:
    argstype = namedtuple('Arguments', ['db', 'debug', 'sync', 'port', 'test'])
    args = argstype(db='sqlite://', debug=False, sync=False, port=8888,
                    test=False)

elif 'pydevconsole' in sys.argv[0]:
    argstype = namedtuple('Arguments', ['db', 'debug', 'sync', 'port', 'test'])
    args = argstype(db='sqlite://', debug=False, sync=False, port=8888,
                    test=False)

elif 'pyledger-verify' in sys.argv[0]:
    pass

elif 'pyledger-shell' in sys.argv[0]:
    pass

else:
    parser = argparse.ArgumentParser(description='Run the PyLedger server')
    parser.add_argument('--db', help="SQLAlchemy database address",
                        type=str, default="sqlite://")
    parser.add_argument('--sync', action='store_true')
    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('--port', type=int, default=8888)
    parser.add_argument('--test', action='store_true', default=False)
    args = parser.parse_args()


password_backend = default_backend()

# User configurable section

# - Put a very secret word here
SECRET = b'test'

# - Lifetime of the sessions in hours
LIFETIME = 1
