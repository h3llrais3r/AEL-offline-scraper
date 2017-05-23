#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# List metadata from a NoIntro DAT and several other sources.
#

# Copyright (c) 2017 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# --- Python standard library ---
from __future__ import unicode_literals
# import sys, os

# --- Import AEL modules ---
from AEL.resources.utils import *
from AEL.resources.rom_audit import *

# --- Data structures -----------------------------------------------------------------------------
systems = {
    # --- Amstrad ---
    'cpc' : {
        'nointro'   : '',
        'gamedb'    : 'data_gamedb_info_xml/Amstrad CPC.xml',
        'hyperlist' : 'data_hyperlist/Amstrad CPC.xml',
        'output'    : 'output_xml/Amstrad CPC.xml'
    },

    # --- Atari ---
    'a2600' : {
        'nointro'   : 'data_nointro/Atari - 2600 (20170123-074806).dat',
        'gamedb'    : 'data_gamedb_info_xml/Atari 2600.xml',
        'hyperlist' : '',
        'output'    : 'output_xml/Atari 2600.xml'
    },
    # 'a5200' : {},
    # 'a7800' : {},
    # 'jaguar' : {},
    # 'jaguarcd' : {},
    # 'lynx' : {},
    # 'atarist' : {},
    
    # --- Coleco ---
    # 'coleco' : {},

    # --- Commodore ---
    # 'c64' : {},
    # 'amiga' : {},
    # 'plus4' : {},
    # 'vic20' : {},

    # --- Magnavox ---
    # 'odyssey2' : {},

    # --- Microsoft ---
    # 'msx' : {},
    # 'msx2' : {},
    # 'msdos' : {},
    # 'windows' : {},
    # 'xbox' : {},

    # --- NEC ---
    # 'pce' : {},
    # 'pcecd' : {},
    # 'supergrafx' : {},
    # 'pcfx' : {},

    # --- Nintendo ---
    # 'gb' : {},
    # 'gbc' : {},
    # 'gba' : {},
    # 'ds' : {},
    # 'fds' : {},
    # 'nes' : {},
    'snes' : {
        'nointro'   : 'data_nointro/Nintendo - Super Nintendo Entertainment System Parent-Clone (20170507-052522).dat',
        'gamedb'    : 'data_gamedb_info_xml/Nintendo SNES.xml',
        'hyperlist' : '',
        'output'    : 'output_xml/Nintendo SNES.xml'
    },
    # 'virtualboy' : {},
    # 'n64' : {},
    # 'gamecube' : {},
    # 'wii' : {},

    # --- SEGA ---
    # 'sg1000' : {},
    # 'sms' : {},
    # 'gg' : {},
    'genesis' : {
        'nointro'   : 'data_nointro/Sega - Mega Drive - Genesis Parent-Clone (20170318-044444).dat',
        'gamedb'    : 'data_gamedb_info_xml/Sega MegaDrive.xml',
        'hyperlist' : 'data_hyperlist/Sega Genesis.xml',
        'output'    : 'output_xml/Sega MegaDrive.xml'
    },
    # 'megacd' : {},
    '32x' : {
        'nointro'   : 'data_nointro/Sega - 32X Parent-Clone (20161022-095033).dat',
        'gamedb'    : 'data_gamedb_info_xml/Sega 32X.xml',
        'hyperlist' : '',
        'output'    : 'output_xml/Sega 32X.xml'
    },
    # 'pico' : {},
    # 'saturn' : {},
    # 'dreamcast' : {},

    # --- SNK ---
    # 'neocd' : {},
    # 'ngp' : {},
    # 'ngpc' : {},

    # --- SONY ---
    'psx' : {
        'nointro'   : 'data_redump/Sony - PlayStation (20170306 02-03-12).dat',
        'gamedb'    : 'data_gamedb_info_xml/Sony PlayStation.xml',
        'hyperlist' : '',
        'output'    : 'output_xml/Sony PlayStation.xml'
    }
    # 'psx2' : {},
    # 'psp' : {},
}

def process_system(system):
    nointro_FN   = FileName('./' + system['nointro'])
    gamedb_FN    = FileName('./' + system['gamedb'])
    hyperlist_FN = FileName('./' + system['hyperlist'])
    output_FN    = FileName('./' + system['output'])

    # --- Load No-Intro PClone DAT file ---
    nointro_dic = audit_load_NoIntro_XML_file(nointro_FN)

    # --- Load GameDBInfo XML ---
    gamedb_dic = audit_load_GameDB_XML(gamedb_FN)

    # --- Load HyperList XML ---
    hyperlist_dic = audit_load_HyperList_XML(hyperlist_FN)

    # --- Load Overrides XML ---
    # override_dic = audit_load_HyperList_XML(hyperlist_FN)
    override_dic = {}

    # --- Make PClone dictionary ---
    # pclone_dic = { 'parent_name' : ['clone_1', 'clone_2', ...], ... }
    # parents_dic = { 'clone_name' : 'parent_name', ...}
    pclone_dic = audit_make_NoIntro_PClone_dic(nointro_dic)
    parents_dic = audit_make_NoIntro_Parents_dic(nointro_dic)

    # --- Make main ROM dictionary ---
    # >> Allows to know if ROM comes from No-Intro or GameDBInfo quickly.
    # >> main_rom_dic = { 'ROMname' : 'Parent | Clone | Extra', ... }
    # >> Status Parent -> ROM is in the NoIntro file and is a parent
    # >> Status Clone  -> ROM is in the NoIntro file and is a clone
    # >> Status Extra  -> ROM is not in the NoIntro file (is in GameDBInfo)

    # --- Make main ROM list ---
    # >> This list is sorted and is how ROMs will be listed and located in the out XML file.
    # >> main_rom_set = {'rom_name_1', 'rom_name_2', ... }
    main_rom_set = set()

    # >> Add ROMs from No-Intro DAT
    for rom_name in nointro_dic:   main_rom_set.add(rom_name)
    for rom_name in gamedb_dic:    main_rom_set.add(rom_name)
    for rom_name in hyperlist_dic: main_rom_set.add(rom_name)

    # --- Traverse main_rom_list and print all metadata ---
    metadata_dic = {}
    NAME_LENGTH = 64
    CLONE_LENGTH = 6
    DB_LENGTH = 31
    YEAR_LENGTH      = 4
    GENRE_LENGTH     = 20
    PUBLISHER_LENGTH = 29
    NPLAYERS_LENGTH  = 11
    ESRB_LENGTH      = 22
    PLOT_LENGTH      = 40
    line_1 = "{0} | {1} | {2} |"
    line_2 = "   {0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    line_3 = "   {0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    line_4 = "   {0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    for rom_key in sorted(main_rom_set):
        # if re.findall(r'^\[BIOS\]', rom_key): continue

        rom_name = text_limit_string(rom_key, NAME_LENGTH)
        dat_str = 'Yes' if rom_key in nointro_dic else 'No'
        if rom_name in nointro_dic:
            clone_str = 'Clone' if nointro_dic[rom_key]['cloneof'] else 'Parent'
        else:
            clone_str = '-----'
        gamedb_str = 'GameDBInfo' if rom_key in gamedb_dic else ''
        hl_str     = 'HyperList' if rom_key in hyperlist_dic else ''

        gamedb_year_srt     = gamedb_dic[rom_key]['year'] if rom_key in gamedb_dic else ''
        gamedb_genre_srt    = gamedb_dic[rom_key]['genre'] if rom_key in gamedb_dic else ''
        gamedb_studio_srt   = gamedb_dic[rom_key]['manufacturer'] if rom_key in gamedb_dic else ''
        gamedb_nplayers_srt = gamedb_dic[rom_key]['player'] if rom_key in gamedb_dic else ''
        gamedb_rating_srt   = gamedb_dic[rom_key]['rating'] if rom_key in gamedb_dic else ''
        gamedb_plot_srt     = gamedb_dic[rom_key]['story'] if rom_key in gamedb_dic else ''

        gamedb_genre_srt    = text_limit_string(gamedb_genre_srt, GENRE_LENGTH)
        gamedb_studio_srt   = text_limit_string(gamedb_studio_srt, PUBLISHER_LENGTH)
        gamedb_nplayers_srt = text_limit_string(gamedb_nplayers_srt, NPLAYERS_LENGTH)
        gamedb_rating_srt   = text_limit_string(gamedb_rating_srt, ESRB_LENGTH)
        gamedb_plot_srt     = text_limit_string(gamedb_plot_srt, PLOT_LENGTH)

        hl_year_srt     = hyperlist_dic[rom_key]['year'] if rom_key in hyperlist_dic else ''
        hl_genre_srt    = hyperlist_dic[rom_key]['genre'] if rom_key in hyperlist_dic else ''
        hl_studio_srt   = hyperlist_dic[rom_key]['manufacturer'] if rom_key in hyperlist_dic else ''
        hl_nplayers_srt = ''
        hl_rating_srt   = hyperlist_dic[rom_key]['rating'] if rom_key in hyperlist_dic else ''
        hl_plot_srt     = ''

        print(line_1.format(rom_name.ljust(NAME_LENGTH), dat_str.ljust(3), clone_str.ljust(CLONE_LENGTH)))
        print(line_2.format(gamedb_str.ljust(DB_LENGTH),
                            gamedb_year_srt.ljust(YEAR_LENGTH), gamedb_genre_srt.ljust(GENRE_LENGTH),
                            gamedb_studio_srt.ljust(PUBLISHER_LENGTH), gamedb_nplayers_srt.ljust(NPLAYERS_LENGTH),
                            gamedb_rating_srt.ljust(ESRB_LENGTH), gamedb_plot_srt.ljust(PLOT_LENGTH) ))

        print(line_3.format(hl_str.ljust(DB_LENGTH), 
                            hl_year_srt.ljust(YEAR_LENGTH), hl_genre_srt.ljust(GENRE_LENGTH),
                            hl_studio_srt.ljust(PUBLISHER_LENGTH), hl_nplayers_srt.ljust(NPLAYERS_LENGTH),
                            hl_rating_srt.ljust(ESRB_LENGTH), hl_plot_srt.ljust(PLOT_LENGTH) ))

        # --- Build metadata dictionary ---
        metadata = audit_new_rom_AEL_Offline()
        metadata_status = 'ERROR!'
        # >> Overrides always have priority
        if rom_key in override_dic:
            metadata_status = 'Own XML Override'
        elif rom_key in gamedb_dic:
            metadata_status = 'Own GameDBInfo'
            metadata['year']         = gamedb_dic[rom_key]['year']
            metadata['genre']        = gamedb_dic[rom_key]['genre']
            metadata['manufacturer'] = gamedb_dic[rom_key]['manufacturer']
            metadata['nplayers']     = gamedb_dic[rom_key]['player']
            metadata['rating']       = gamedb_dic[rom_key]['rating']
            metadata['plot']         = gamedb_dic[rom_key]['story']
        elif rom_key in hyperlist_dic:
            metadata_status = 'Own HyperList'
        else:
            # >> If ROM is a parent search among the clones
            if rom_key in pclone_dic:
                # log_info('Parent ROM')
                metadata_found_in_clones = False
                for clone_key in pclone_dic[rom_key]:
                    if clone_key in override_dic:
                        metadata_status = 'Clone XML Override'
                        metadata_found_in_clones = True
                        break
                    elif clone_key in gamedb_dic:
                        metadata_status = 'Clone GameDBInfo'
                        metadata['year']         = gamedb_dic[clone_key]['year']
                        metadata['genre']        = gamedb_dic[clone_key]['genre']
                        metadata['manufacturer'] = gamedb_dic[clone_key]['manufacturer']
                        metadata['nplayers']     = gamedb_dic[clone_key]['player']
                        metadata['rating']       = gamedb_dic[clone_key]['rating']
                        metadata['plot']         = gamedb_dic[clone_key]['story']
                        metadata_found_in_clones = True
                        break
                    elif clone_key in hyperlist_dic:
                        metadata_status = 'Clone HyperList'
                        metadata_found_in_clones = True
                        break
                # >> ROM is a parent and metadata not found in clones -> No metadata available
                if not metadata_found_in_clones:
                    metadata_status = 'Not available (No-Intro Parent)'

            # >> ROM is a clone
            elif rom_key in parents_dic:
                # log_info('Clone ROM')
                # >> First search parent
                parent_key = parents_dic[rom_key]
                if parent_key in override_dic:
                    metadata_status = 'Parent XML Override'
                    metadata_found_in_parent = True
                elif parent_key in gamedb_dic:
                    metadata_status = 'Parent GameDBInfo'
                    metadata['year']         = gamedb_dic[parent_key]['year']
                    metadata['genre']        = gamedb_dic[parent_key]['genre']
                    metadata['manufacturer'] = gamedb_dic[parent_key]['manufacturer']
                    metadata['nplayers']     = gamedb_dic[parent_key]['player']
                    metadata['rating']       = gamedb_dic[parent_key]['rating']
                    metadata['plot']         = gamedb_dic[parent_key]['story']
                elif parent_key in hyperlist_dic:
                    metadata_status = 'Parent HyperList'
                else:
                    # >> Metadata not found in parent
                    # >> Search list of clones
                    metadata_found_in_clones = False
                    for clone_key in pclone_dic[parent_key]:
                        if clone_key in override_dic:
                            metadata_status = 'Clone XML Override'
                            metadata_found_in_clones = True
                            break
                        elif clone_key in gamedb_dic:
                            metadata_status = 'Clone GameDBInfo'
                            metadata['year']  = gamedb_dic[clone_key]['year']
                            metadata['genre'] = gamedb_dic[clone_key]['genre']
                            metadata['manufacturer'] = gamedb_dic[clone_key]['manufacturer']
                            metadata['nplayers']     = gamedb_dic[clone_key]['player']
                            metadata['rating']       = gamedb_dic[clone_key]['rating']
                            metadata['plot']         = gamedb_dic[clone_key]['story']
                            metadata_found_in_clones = True
                            break
                        elif clone_key in hyperlist_dic:
                            metadata_status = 'Clone HyperList'
                            metadata_found_in_clones = True
                            break
                    # >> ROM is a parent and metadata not found in clones -> No metadata available
                    if not metadata_found_in_clones:
                        metadata_status = 'Not available (No-Intro Clone)'

        # >> Final metadata
        metadata['name'] = rom_key
        metadata['description'] = rom_key
        if rom_name in nointro_dic:
            metadata['cloneof'] = parents_dic[rom_key] if nointro_dic[rom_key]['cloneof'] else ''
        else:
            metadata['cloneof'] = ''
        metadata['source'] = 'ERROR'
        if   rom_key in nointro_dic: metadata['source'] = 'No-Intro/Redump DAT'
        elif rom_key in gamedb_dic:  metadata['source'] = 'GameDBInfo'
        metadata['status'] = metadata_status
        metadata_dic[rom_key] = metadata

        # >> Print
        m_year_srt         = text_limit_string(metadata['year'], YEAR_LENGTH)
        m_genre_srt        = text_limit_string(metadata['genre'], GENRE_LENGTH)
        m_manufacturer_srt = text_limit_string(metadata['manufacturer'], PUBLISHER_LENGTH)
        m_nplayers_srt     = text_limit_string(metadata['nplayers'], NPLAYERS_LENGTH)
        m_rating_srt       = text_limit_string(metadata['rating'], ESRB_LENGTH)
        m_plot_srt         = text_limit_string(metadata['plot'], PLOT_LENGTH)

        print(line_4.format(metadata_status.ljust(DB_LENGTH),
                            m_year_srt.ljust(YEAR_LENGTH), m_genre_srt.ljust(GENRE_LENGTH),
                            m_manufacturer_srt.ljust(PUBLISHER_LENGTH), m_nplayers_srt.ljust(NPLAYERS_LENGTH),
                            m_rating_srt.ljust(ESRB_LENGTH), m_plot_srt.ljust(PLOT_LENGTH) ))

    # --- Save Offline scraper XML ---
    # >> Create XML data
    str_list = []
    str_list.append('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    str_list.append('<menu>\n')
    str_list.append('  <header>\n')
    str_list.append(XML_text('listname', output_FN.getBase_noext(), 4))
    str_list.append(XML_text('DAT', nointro_FN.getBase(), 4))
    str_list.append('    <lastlistupdate></lastlistupdate>\n')
    str_list.append('    <listversion></listversion>\n')
    str_list.append('    <exporterversion></exporterversion>\n')
    str_list.append('  </header>\n')
    for rom_key in sorted(metadata_dic):
        # print(metadata_dic[rom_key])
        str_list.append('  <game name="{0}">\n'.format(text_escape_XML(rom_key)))
        str_list.append(XML_text('description',  text_str_2_Uni(metadata_dic[rom_key]['description']), 4))
        str_list.append(XML_text('cloneof',      text_str_2_Uni(metadata_dic[rom_key]['cloneof']), 4))
        str_list.append(XML_text('source',       text_str_2_Uni(metadata_dic[rom_key]['source']), 4))
        str_list.append(XML_text('status',       text_str_2_Uni(metadata_dic[rom_key]['status']), 4))
        str_list.append(XML_text('year',         text_str_2_Uni(metadata_dic[rom_key]['year']), 4))
        str_list.append(XML_text('genre',        text_str_2_Uni(metadata_dic[rom_key]['genre']), 4))
        str_list.append(XML_text('manufacturer', text_str_2_Uni(metadata_dic[rom_key]['manufacturer']), 4))
        str_list.append(XML_text('nplayers',     text_str_2_Uni(metadata_dic[rom_key]['nplayers']), 4))
        str_list.append(XML_text('rating',       text_str_2_Uni(metadata_dic[rom_key]['rating']), 4))
        str_list.append(XML_text('plot',         text_str_2_Uni(metadata_dic[rom_key]['plot']), 4))
        str_list.append('  </game>\n')
    str_list.append('</menu>\n')

    # >> Write XML file
    full_string = ''.join(str_list).encode('utf-8')
    file_obj = open(output_FN.getPath(), 'w')
    file_obj.write(full_string)
    file_obj.close()

    # --- Statistics ---
    print('***** Statistics *****')
    print('NoIntro roms          {0}'.format(len(nointro_dic)))
    print('GameDB roms           {0}'.format(len(gamedb_dic)))
    print('HyperList roms        {0}'.format(len(hyperlist_dic)))
    print('Offline scrapers roms {0}'.format(len(metadata_dic)))

# --- Main ----------------------------------------------------------------------------------------
set_log_level(LOG_DEBUG)
# process_system(systems['a2600'])
# process_system(systems['32x'])
for system_name in systems: process_system(systems[system_name])
