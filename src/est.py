import os
import sys
import gzip
import logging
import tempfile
import psutil

from estimators import lzss

def mem_usage_percent():
    process = psutil.Process(os.getpid())
    return process.memory_percent()

def get_tmpfilename():
    try:
        return tempfile.mktemp(prefix=tempfile.template)
    except TypeError:
        return tempfile.mktemp()

def file_append(f, s):
    with open(f, 'a') as fh:
        fh.write(s)

def lzss_calculate_compression_ratio(f):
    # Temporary filename for compressed version
    f_c = get_tmpfilename()

    # Get file handles of input and output files
    fh_i = open(f, 'rb')
    fh_o = open(f_c, 'wb')

    # Compress, get # bytes, clean up
    [bytes_i, bytes_o] = lzss.encode(fh_i, fh_o)
    os.remove(f_c)

    return bytes_i/bytes_o

def run_lzss_file(fn_i, fn_o):
    # Create temporary file name
    tfn = get_tmpfilename()

    # Process corpus line by line and produce output
    cnt_sen = 0
    cnt_crs = 0
    logging.info('loading [%s]', fn_i)
    logging.info('writing [%s]', fn_o)
    with open(fn_i, 'r') as fhi, open(fn_o, 'w') as fho:

        # Write output file header
        fho.write('nr\tlength\tratio\n')

        # Iterate over input sentences
        for sentence in fhi:
            cnt_sen += 1
            if cnt_sen % 50 == 0:
                logging.info('... %d lines', cnt_sen)

            # Strip POS tags
            tokens = [word.split('|')[0] for word in sentence.split()]

            # Append sentence w/o spaces
            tokenstring = ''.join(tokens)
            cnt_crs += len(tokenstring)
            file_append(tfn, tokenstring)

            # Get compression ratio and write output
            cr = lzss_calculate_compression_ratio(tfn)
            fho.write('%d\t%d\t%.8f\n' % (cnt_sen, cnt_crs, cr))

    # Cleanup
    os.remove(tfn)

    # Some reporting
    logging.info('%d lines processed', cnt_sen)

def run_lz77_mem(fn_i, fn_o):
    # Process corpus line by line and produce output
    cnt_sen = 0
    txt_plain = ''

    logging.info('loading [%s]', fn_i)
    logging.info('writing [%s]', fn_o)
    with open(fn_i, 'r') as fhi, open(fn_o, 'w') as fho:

        # Write output file header
        fho.write('nr\tlength\tratio\n')

        # Iterate over input sentences
        for sentence in fhi:
            cnt_sen += 1
            if cnt_sen % 50 == 0:
                mem_usage = mem_usage_percent()
                logging.info('... %d lines\tusing %.2f%% RAM', cnt_sen, mem_usage)
                if mem_usage > 90:
                    logging.error('Insufficient RAM. QUITTING!')
                    exit(1)

            # Strip POS tags
            tokens = [word.split('|')[0] for word in sentence.split()]

            # Append sentence w/o spaces, then add sentence with space sep
            tokenstring = ''.join(tokens)
            txt_plain += tokenstring + ' '
            txt_compr = gzip.compress(str.encode(txt_plain))

            # Get compression ratio and write output
            cr = len(txt_plain) / len(txt_compr)
            fho.write('%d\t%d\t%.8f\n' % (cnt_sen, len(txt_plain), cr))

    # Some reporting
    logging.info('%d lines processed', cnt_sen)


def main(argv):
    if len(argv) < 2:
        logging.error('Insufficient arguments')
        exit(1)

    # Run lz77 - in memory
    run_lz77_mem(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    logging.basicConfig(    stream=sys.stderr,
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%H:%M:%S')
    main(sys.argv[1:])
