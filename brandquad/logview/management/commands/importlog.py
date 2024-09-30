"""
importlog - command imports Nginx log file into NgnixLog table.

Usage:
    python manage.py importlog [options] <filename>

See add_arguments below for detailes.

Author: Igor Polev, igor.polev@gmail.com
"""

import asyncio, json

from datetime import datetime as dt
from pathlib import Path
from django.core.management.base import BaseCommand, CommandParser

from logview.models import NgnixLog

class Command(BaseCommand):

    help = "Import log file into DB."
    
    data_buffer  = []    # Buffer for portion of data to be saved into DB
    data_reading = False # Data processing flag

    def add_arguments(self, parser):

        parser.add_argument(
            'filename',
            type    = str,
            help    = "Name of log file to be added into DB."
        )
        parser.add_argument(
            '-ps',
            '--parse_size',
            type    = int,
            default = 64,
            help    = "Size of log file in megabytes to be parsed at once. Default 64."
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):

        try:
            # Get filename
            logfile = Path(options['filename'])
            # Check file availability
            if not logfile.is_file():
                self.stdout.write("--- File '{}' not found.".format(logfile))
                return
            
            # Parsing log data
            self.stdout.write("Parsing log data from file '{}':".format(logfile))
            with logfile.open() as file:
                asyncio.run(self.__process_data(file, options['parse_size'] * 1048576))

        # Exceptions processing
        except Exception as ex:
            self.stdout.write("\n--- Unhandled exception occured, operation terminated!\n{}".format(ex))

    async def __process_data(self, file, max_data_size):

        # Reading first portion of data
        self.data_buffer = await self.__read_data(file, max_data_size)
        if not self.data_buffer:
            self.stdout.write("Nothing to process.")
            return

        # Reading and saving data portion by portion in parallel
        read_task = asyncio.create_task(self.__read_data(file, max_data_size))
        save_task = asyncio.create_task(self.__save_data())
        rec_count = 0
        self.data_reading = True
        while self.data_reading: # this loop terminates inside __read_data
            rec_count += await save_task
            new_data   = await read_task
            self.stdout.write("\r{} records parsed... ".format(rec_count), ending='')
            # If __read_data returns empty list because of data conversion error,
            # need to read next data portion until success or EoF.
            while self.data_reading and not new_data:
                new_data = await self.__read_data(file, max_data_size)
            self.data_buffer = new_data
        self.stdout.write("done.")

    async def __read_data(self, file, max_data_size):

        # Expand log record dict with split request field
        def request_split_in_dict(record):
            new_record = record
            new_record['request_split'] = record['request'].split()
            return new_record

        # Convert log record dict into NgnixLog object
        def dict_to_NgnixLog(record):
            return NgnixLog(
                time        = dt.strptime(record['time'], '%d/%b/%Y:%H:%M:%S %z'),
                remote_ip   = record['remote_ip'],
                remote_user = record['remote_user'],
                method      = record['request_split'][0],
                request_uri = record['request_split'][1],
                response    = int(record['response']),
                bytes       = int(record['bytes'])
            )

        # Reading data from file
        data = file.readlines(max_data_size)
        if not data: # EoF - normal process termination
            self.data_reading = False
            return data

        # Parsing data
        try:
            data = json.loads(data)
            data = map(request_split_in_dict, data)
            data = map(dict_to_NgnixLog, data)
        except Exception as ex:
            self.stdout.write(
                "\n--- Some errors during data parsing. Skipping entire data block!\n{}".format(ex)
            )
            return []
            # TODO: Localize particular record with errors

        return list(data)

    async def __save_data(self):
        return

