import optparse
import codecs

import pycaption
import os

def main():
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("--sami",
            action='store_true',
            dest='sami',
            help="write captions in SAMI format",
            default=False,)
    parser.add_option("--dfxp",
            action='store_true',
            dest='dfxp',
            help="write captions in DFXP format",
            default=False,)
    parser.add_option("--srt",
            action='store_true',
            dest='srt',
            help="write captions in SRT format",
            default=False,)
    parser.add_option("--webvtt",
            action='store_true',
            dest='webvtt',
            help="write captions in webvtt format",
            default=False,)
    parser.add_option("--transcript",
            action='store_true',
            dest='transcript',
            help="write transcript for captions",
            default=False,)
    parser.add_option("--scc_lang",
            dest='lang',
            help="choose override language for input",
            default='',)
    parser.add_option("--scc_offset",
            dest='offset',
            help="choose offset for SCC file; measured in seconds",
            default=0)
    (options, args) = parser.parse_args()

    try:
        filename = args[0]
    except:
        raise Exception(
        ('Expected usage: python caption_converter.py <path to caption file> ',
        '[--sami --dfxp --srt --webvtt --transcript]'))

    try:
        captions = codecs.open(filename, encoding='utf-8', mode='r').read()
    except:
        captions = open(filename, 'r').read()
        captions = unicode(captions, errors='replace')

    content = read_captions(captions, options)
    
    # Check languages from captions file (dfxp only)
    languages = content.get_languages()
    output_filename = get_output_filename(filename) # Get input filename
    if not options.lang:
        for lang in languages:
            write_captions(content, options, lang, output_filename)
    elif options.lang in languages:
        write_captions(content, options, options.lang, output_filename)
    else:
        print 'Not found language: "' + options.lang + '"'
    #write_captions(content, options)


def read_captions(captions, options):
    scc_reader = pycaption.SCCReader()
    srt_reader = pycaption.SRTReader()
    sami_reader = pycaption.SAMIReader()
    dfxp_reader = pycaption.DFXPReader()
    webvtt_reader = pycaption.WebVTTReader()

    if scc_reader.detect(captions):
        if options.lang:
            return scc_reader.read(captions, lang=options.lang,
                                   offset=int(options.offset))
        else:
            return scc_reader.read(captions, offset=int(options.offset))
    elif srt_reader.detect(captions):
        return srt_reader.read(captions)
    elif sami_reader.detect(captions):
        return sami_reader.read(captions)
    elif dfxp_reader.detect(captions):
        return dfxp_reader.read(captions)
    elif webvtt_reader.detect(captions):
        return webvtt_reader.read(captions)
    else:
        raise Exception('No caption format detected :(')


def write_captions(content, options, lang='', filename=''):
    if options.sami:
        print pycaption.SAMIWriter().write(content).encode("utf-8")
    if options.dfxp:
        print pycaption.DFXPWriter().write(content).encode("utf-8")
    if options.webvtt:
        location = os.getcwd()
        f = open(location+'/captions/'+filename+'_'+lang+'.vtt', 'w') #Save vtt files into captions folder
        f.write(pycaption.WebVTTWriter().write(content, lang).encode("utf-8"))
        # print pycaption.WebVTTWriter().write(content, lang).encode("utf-8")
    if options.srt:
        print pycaption.SRTWriter().write(content).encode("utf-8")
    if options.transcript:
        print pycaption.TranscriptWriter().write(content).encode("utf-8")


def get_output_filename(filename):
    file_input_list = filename.split('/')
    file_input = ''.join(file_input_list[-1:])
    return file_input.split('.')[0]


if __name__ == '__main__':
    main()
