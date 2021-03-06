#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Test AEL metadata scraper
#

# --- Python standard library ---
from __future__ import unicode_literals

# --- AEL modules ---
from AEL.resources.scrap import *
from AEL.resources.utils import *

# --- Print list of all scrapers currently in AEL ---
set_log_level(LOG_DEBUG) # >> LOG_INFO, LOG_VERB, LOG_DEBUG
print_scraper_list(scrapers_metadata)

# --- main ----------------------------------------------------------------------------------------
print('*** Arcade Database ************************************************************************')
ArcadeDB = metadata_ArcadeDB()

# results = ArcadeDB.get_search('dino', 'dino', 'MAME')
# results = ArcadeDB.get_search('aliens', 'aliens', 'MAME')
# results = ArcadeDB.get_search('spang', 'spang', 'MAME')
results = ArcadeDB.get_search('toki', 'toki', 'MAME')

# --- Fake game to produce a not found error ---
# results = ArcadeDB.get_search('asdfg', 'asdfg', 'MAME')

# --- Print list of fames found ---
print_games_search(results)
print_game_metadata(ArcadeDB, results)
