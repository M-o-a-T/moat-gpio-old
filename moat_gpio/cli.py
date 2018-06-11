# -*- coding: utf-8 -*-

"""Main `moat-amqp` CLI."""

import os
import sys
import yaml

import trio_click as click

from . import __version__
from .main import run

import logging
logger = logging.getLogger(__name__)

def version_msg():
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = u'Moat-GPIO %(version)s from {} (Python {})'
    return message.format(location, python_version)


@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.version_option(__version__, u'-V', u'--version', message=version_msg())
@click.option('--config','-c', help="config file", default="/etc/moat.cfg")
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information', default=False
)
async def main(config, verbose):
    """Hook GPIO lines to AMQP.

    MoaT is free and open source software, developed and managed by
    volunteers. If you would like to help out or fund the project, please get
    in touch at https://github.com/M-o-a-T.
    """
    with open(config,"r") as f:
        config = yaml.safe_load(f)

    if 'gpio' not in config:
        try:
            config['config']['gpio']
        except KeyError:
            logger.error("he configuration doesn't cointain any GPIO")
            return
        else:
            config = config['config']

    # TODO configure logger via YAML
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    try:
        await run(config)
    except KeyboardInterrupt:
        logger.info("Program interrupted.")

if __name__ == "__main__":
    main()
