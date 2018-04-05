import os, csv, glob, datetime

mm_dd_yy = datetime.datetime.now().strftime("%m%d%y")


def file_cat(infile, outfile, header=''):
    infile_header = header

    with open(infile, 'r') as infilecsv, open(outfile, 'a') as outfilecsv:
        infile_reader = csv.DictReader(infilecsv, delimiter='\t')

        if not header:
            infile_header = infile_reader.fieldnames
        else:
            infile_header = header

        outfile_writer = csv.DictWriter(outfilecsv, fieldnames=infile_header, delimiter='\t',extrasaction='ignore')

        outfile_writer.writeheader()

        for line in infile_reader:
            outfile_writer.writerow(line)

    return


ccdg_qc_status_files = glob.glob('285*/285*.qcstatus.tsv')
ccdg_qc_status_outfile_header = ['QC Sample','WOID', 'PSE', 'Launch Status', 'Launch Date', 'Instrument Check',
                                 '# of Inputs','# of Instrument Data', 'QC Status', 'QC Date', 'QC Failed Metrics',
                                 'COD Collaborator', 'QC Directory', 'Top Up']

status_outfile = 'ccdg.qcstatus.summary' + mm_dd_yy + '.tsv'

if os.path.exists(status_outfile):
    os.remove(status_outfile)
for qc_status_file in ccdg_qc_status_files:
    file_cat(infile=qc_status_file, outfile=status_outfile, header=ccdg_qc_status_outfile_header)

ccdg_qc_all_files = glob.glob('285*/qc.*/attachments/*all*')
qc_all_outfile = 'ccdg.qcall.summary.' + mm_dd_yy + '.tsv'

if os.path.exists(qc_all_outfile):
    os.remove(qc_all_outfile)

for qc_all_file in ccdg_qc_all_files:
    file_cat(infile=qc_all_file, outfile=qc_all_outfile, header='')
