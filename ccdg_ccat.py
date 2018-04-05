import os, csv, glob, datetime

# TODO: Add topup skip option

# cat files together
def file_cat(infile, outfile, header=''):
    infile_header = header
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

        #write to files
        for line in infile_reader:
            if 'QC Sample' in infile_header and line['QC Sample'] and line['Launch Status']:
                outfile_writer.writerow(line)

            if 'WorkOrder' in infile_header:
                outfile_writer.writerow(line)

    return

# set date
mm_dd_yy = datetime.datetime.now().strftime("%m%d%y")

# glob qc status files, create status header field list
ccdg_qc_status_files = glob.glob('285*/285*.qcstatus.tsv')
ccdg_qc_status_outfile_header = ['QC Sample','WOID', 'PSE', 'Launch Status', 'Launch Date', 'Instrument Check',
                                 '# of Inputs','# of Instrument Data', 'QC Status', 'QC Date', 'QC Failed Metrics',
                                 'COD Collaborator', 'QC Directory', 'Top Up']

# status outfile
status_outfile = 'ccdg.qcstatus.summary' + mm_dd_yy + '.tsv'

# remove file if already exists so not appending duplicate sample info
if os.path.exists(status_outfile):
    os.remove(status_outfile)

# cat status files with file_cat method
for qc_status_file in ccdg_qc_status_files:
    file_cat(infile=qc_status_file, outfile=status_outfile, header=ccdg_qc_status_outfile_header)

# glob qc all result files, all outfile
ccdg_qc_all_files = glob.glob('285*/qc.*/attachments/*all*')
qc_all_outfile = 'ccdg.qc.all.summary.' + mm_dd_yy + '.tsv'

# remove file if already exists so not appending duplicate sample info
if os.path.exists(qc_all_outfile):
    os.remove(qc_all_outfile)

# cat qc all files with file_cat method
for qc_all_file in ccdg_qc_all_files:
    file_cat(infile=qc_all_file, outfile=qc_all_outfile, header='')
