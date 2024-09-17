#!/usr/bin/env python3
""" A template of a logging application
"""

import argparse
import configparser
import logging
import sys


class LogApp():
    """ A logging application """
    #log_format = '[%(filename)-21s:%(lineno)4s - %(funcName)20s()] \
    #        %(levelname)-7s | %(asctime)-15s | %(message)s'

    def __init__(self, args, description='Logging application'):
    #def __init__(self, args):
        self.args = args
        self.description = description
        self.config = None
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        numeric_level = getattr(logging, self.args.log_level, None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {numeric_level}')

        self.set_log_format()
        if self.args.log_file == 'stdout':
            logging.basicConfig(stream=sys.stdout, format=self.log_format, level=numeric_level)
        else:
            logging.basicConfig(filename=self.args.log_file, format=self.log_format, \
                    level=numeric_level)

    def set_log_format(self, log_format='[%(filename)-21s:%(lineno)4s - %(funcName)20s()] \
            %(levelname)-7s | %(asctime)-15s | %(message)s'):
        """ Set logging format """
        self.log_format = log_format

    # def read_conf(self, **kwargs

    def get_config(self, conf_name='', **kwargs):
        """ initialize and read config """
        if self.args.conf:
            logging.info('Config %s reading', self.args.conf)
            conf_name = self.args.conf

        # self.read_conf(

        self.config = configparser.ConfigParser(**kwargs)
        try:
            self.config.read(conf_name, encoding='utf-8')
        except configparser.Error:
            logging.exception('configparser.Error')


CONF_FILE_NAME = ""
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--conf', type=str, default=CONF_FILE_NAME, help='conf file')
PARSER.add_argument('--log_file', type=str, default='stdout', help='log destination')
PARSER.add_argument('--log_level', type=str, default="DEBUG", help='log level')

if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    LOGAPP = LogApp(args=ARGS)
    LOGAPP.get_config(inline_comment_prefixes=(';','#'), allow_no_value=True)
    # logging.debug('config=%s', LOGAPP.config.sections())
    for SEC in LOGAPP.config.sections():
        for OPT in LOGAPP.config.options(SEC):
            logging.debug('section=%s, option=%s, val=%s', SEC, OPT, LOGAPP.config[SEC][OPT])
