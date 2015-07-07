from prog.main import main as dm
from prog.content_search import main as cs
from prog.file_extractor import main as fe
from prog.sync_example import example_1 as e1
from prog.war_game_4 import game as ga
from prog.python import main as py
from io_custom.server import enable

database = {'Zero': 'nont',
            'Booster': 'hot topc',
            'NiGHTS': 'dream on',
            'no man': 'nic t nite',
            'James': 'corvette',
            'Josh': 'THE MAN',
            'Jay': 'The Music Man',
            'Nelson': '0006494942',
            'beeny baby': 'nonee',
            'asd': '',
            'a': 'z',
            'Stephen': 'open'}

programs = {'Disk Demo': (dm, (), {}),
            'Content Search': (cs, (), {}),
            'File Extractor': (fe, (), {}),
            'Sync Example': (e1, (), {}),
            'War Game V.4': (ga, (), {}),
            'Python Demo': (py, (), {})}

enable('127.0.0.1', 8080, database, programs)
