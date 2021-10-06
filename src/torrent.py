import argparse
import libtorrent as lt
import time
import sys
from pathlib import Path
from os import system
from urllib.parse import quote

MOVE_TORRENT = 'mv -f "{0}" {1}'


def parse_arguments():
    parser = argparse.ArgumentParser(description='Torrent downloader')
    parser.add_argument(
        'magnet_link',
        type=str,
        help='Torrent magnet link'
    )
    parser.add_argument(
        '-s',
        '--save-path',
        default='',
        type=str,
        help='Save download path'
    )
    parser.add_argument(
        '-d',
        '--destination',
        type=str,
        help='Move downloaded torrent to destination'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='Show verbosity',
        action='store_true'
    )
    return parser.parse_args()


def download(magnet_link, save_path='', verbose=False):
    ses = lt.session()
    ses.listen_on(6881, 6891)
    params = {'save_path': save_path}
    x = lt.add_magnet_uri(ses, magnet_link, params)
    while not x.is_seed():
        if verbose:
            s = x.status()
            print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                s.num_peers, s.state), end=' ')
            sys.stdout.flush()
        time.sleep(1)
    if verbose:
        print(f'Downloaded {x.name()}')
    return x.name()


if __name__ == '__main__':
    args = parse_arguments()
    link = quote(args.magnet_link)
    if link:
        torrent_name = download(link, args.save_path, args.verbose)
        dest = args.destination
        if dest:
            src = Path(args.save_path, torrent_name)
            dst = Path(args.destination)
            system(MOVE_TORRENT.format(src, dst))
            if args.verbose:
                print(f'Downloaded torrent has been moved to: {dst}')
    else:
        print(f'No torrent link')
