import os, csv, glob, datetime


# cat files together
def file_cat(infile, outfile, header=''):

    file_exits = os.path.isfile(outfile)

    with open(infile, 'r') as infilecsv, open(outfile, 'a') as outfilecsv:

        # read infile, either use header= or take header from file
        infile_reader = csv.DictReader(infilecsv, delimiter='\t')
        if not header:
            infile_header = infile_reader.fieldnames
        else:
            infile_header = header

        # set outfile writer object, write header if first pass through
        outfile_writer = csv.DictWriter(outfilecsv, fieldnames=infile_header, delimiter='\t',extrasaction='ignore')
        if not file_exits:
            outfile_writer.writeheader()

        # write to files if line populated in file with 'and condition', else write all lines.
        if 'QC Sample' in infile_header:
            for line in infile_reader:
                if line['QC Sample'] and line['Launch Status']:
                    outfile_writer.writerow(line)
        else:
            for line in infile_reader:
                outfile_writer.writerow(line)
    return


# create woid list, eliminate any glob matches with letters
def woid_list():
    woid_dirs = []

    def is_int(string):
        try:
            int(string)
        except ValueError:
            return False
        else:
            return True

    woid_dir_unfiltered = glob.glob('285*')

    for woid in filter(is_int, woid_dir_unfiltered):
        woid_dirs.append(woid)

    return woid_dirs


# set date
mm_dd_yy = datetime.datetime.now().strftime("%m%d%y")

# create status header field list
ccdg_qc_outfile_header = ['QC Sample', 'WOID', 'PSE', 'Launch Status', 'Launch Date', 'Instrument Check',
                          '# of Inputs','# of Instrument Data', 'QC Status', 'QC Date', 'QC Failed Metrics',
                          'COD Collaborator', 'QC Directory', 'Top Up']

# QC STATUS FILE
# glob qc status files
ccdg_qc_status_files = glob.glob('285*/285*.qcstatus.tsv')
# status outfile
status_outfile = 'ccdg.qcstatus.summary.' + mm_dd_yy + '.tsv'
# remove file if already exists so not appending duplicate sample info
if os.path.isfile(status_outfile):
    os.remove(status_outfile)
# cat status files with file_cat method
for qc_status_file in ccdg_qc_status_files:
    file_cat(infile=qc_status_file, outfile=status_outfile, header=ccdg_qc_outfile_header)

# QC ALL FILE
# glob qc all result files, all outfile
ccdg_qc_all_files = glob.glob('285*/qc.*/attachments/*all*')
qc_all_outfile = 'ccdg.qc.all.summary.' + mm_dd_yy + '.tsv'
# remove file if already exists so not appending duplicate sample info
if os.path.isfile(qc_all_outfile):
    os.remove(qc_all_outfile)
# cat qc all files with file_cat method
for qc_all_file in ccdg_qc_all_files:
    file_cat(infile=qc_all_file, outfile=qc_all_outfile)

# QC FAIL FILE
# glob qc fail files
qc_instrument_fail_files = glob.glob('285*/*launch.fail.tsv')
qc_fail_outfile = 'ccdg.launch.fail.' + mm_dd_yy + '.tsv'
# remove file if already exists so not appending duplicate sample info
if os.path.isfile(qc_fail_outfile):
    os.remove(qc_fail_outfile)
# cat all qc files with file cat method
for qc_fail_file in qc_instrument_fail_files:
    file_cat(qc_fail_file, qc_fail_outfile, header=ccdg_qc_outfile_header)

# QC instrument pass status active fails
# glob active fail files
qc_status_active_fail_files = glob.glob('285*/*instrument.pass.status.active.tsv')
qc_status_active_outfile = 'ccdg.instrument.pass.status.active.' + mm_dd_yy + '.tsv'
# remove file if already exists so not appending duplicate sample info
if os.path.isfile(qc_status_active_outfile):
    os.remove(qc_status_active_outfile)
# cat all qc files with file cat method
for qc_status_active_file in qc_status_active_fail_files:
    file_cat(qc_status_active_file, qc_status_active_outfile, header=ccdg_qc_outfile_header)

# populate woid list
woid_dirs = woid_list()

# QC analysis top up samples
# populate list of analysis only workorder all files
analysis_qc_all_files = []
for woid in woid_dirs:
    if not os.path.isfile(woid+'/'+woid+'.qcstatus.tsv'):
        analysis_qc_all_files.append(glob.glob(woid+'/qc.*/attachments/*all*'))
qc_analysis_all_outfile = 'ccdg.analysis.qc.all.' + mm_dd_yy + '.tsv'
if os.path.isfile(qc_analysis_all_outfile):
    os.remove(qc_analysis_all_outfile)
for file in analysis_qc_all_files:
    for qc_analysis_all_file in file:
        file_cat(qc_analysis_all_file, qc_analysis_all_outfile)


