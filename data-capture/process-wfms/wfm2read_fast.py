import os, struct
import numpy as np
import array

def rd_unpack(f, format_str, byteorder):
    return struct.unpack(byteorder+format_str, f.read(struct.calcsize(format_str)))[0]

def rd_unpack_a(f, num_bytes, format_str, byteorder):
    return [rd_unpack(f, format_str, byteorder) for n in xrange(num_bytes)]

def get_edim(fid, byteorder, wfm_version):
    dim = {}
    dim['dim_scale'] = rd_unpack(fid,'d',byteorder)
    dim['dim_offset'] = rd_unpack(fid,'d',byteorder)
    dim['dim_size'] = rd_unpack(fid,'I',byteorder)
    dim['units'] = rd_unpack(fid, '20s', byteorder)
    dim['dim_extent_min'] = rd_unpack(fid,'d',byteorder)
    dim['dim_extent_max'] = rd_unpack(fid,'d',byteorder)
    dim['dim_resolution'] = rd_unpack(fid,'d',byteorder)
    dim['dim_ref_point'] = rd_unpack(fid,'d',byteorder)
    dim['format'] = rd_unpack_a(fid,4,'b',byteorder)
    dim['storage_type'] = rd_unpack_a(fid,4,'b',byteorder)
    dim['n_value'] = rd_unpack(fid,'I',byteorder)
    dim['over_range'] = rd_unpack(fid,'i',byteorder)
    dim['under_range'] = rd_unpack(fid,'i',byteorder)
    dim['high_range'] = rd_unpack(fid,'i',byteorder)
    dim['low_range'] = rd_unpack(fid,'i',byteorder)
    dim['user_scale'] = rd_unpack(fid,'d',byteorder)
    dim['user_units'] = rd_unpack(fid,'20s',byteorder)
    dim['user_offset'] = rd_unpack(fid,'d',byteorder)

    # changes suggested by WFox
    if wfm_version >= 3:
        dim['point_density'] = rd_unpack(fid,'d',byteorder)
    else:
        dim['point_density'] = rd_unpack(fid,'I',byteorder)
    # end changes suggested by WFox

    dim['href'] = rd_unpack(fid,'d',byteorder)
    dim['trig_delay'] = rd_unpack(fid,'d',byteorder)
    return dim

def get_idim(fid, byteorder, wfm_version):
    dim = {}
    dim['dim_scale'] = rd_unpack(fid,'d',byteorder)
    dim['dim_offset'] = rd_unpack(fid,'d',byteorder)
    dim['dim_size'] = rd_unpack(fid,'I',byteorder)
    dim['units'] = rd_unpack(fid, '20s', byteorder)
    dim['dim_extent_min'] = rd_unpack(fid,'d',byteorder)
    dim['dim_extent_max'] = rd_unpack(fid,'d',byteorder)
    dim['dim_resolution'] = rd_unpack(fid,'d',byteorder)
    dim['dim_ref_point'] = rd_unpack(fid,'d',byteorder)
    dim['spacing'] = rd_unpack(fid,'I',byteorder)
    dim['user_scale'] = rd_unpack(fid,'d',byteorder)
    dim['user_units'] = rd_unpack(fid,'20s',byteorder)
    dim['user_offset'] = rd_unpack(fid,'d',byteorder)
    if wfm_version >= 3:
        dim['point_density'] = rd_unpack(fid,'d',byteorder)
    else:
        dim['point_density'] = rd_unpack(fid,'I',byteorder)
    dim['href'] = rd_unpack(fid,'d',byteorder)
    dim['trig_delay'] = rd_unpack(fid,'d',byteorder)
    return dim

def wfm2read(filename, datapoints=None, step=1, startind=0):
    # [y, t, info, ind_over, ind_under, frames]
    ''' function [y, t, info, ind_over, ind_under, frames] = wfm2read(filename, datapoints, step, startind)

    loads YT-waveform data from *.wfm file saved by Tektronix TDS5000/B, TDS6000/B/C,
    or TDS/CSA7000/B, MSO70000/C, DSA70000/B/C DPO70000/B/C DPO7000/ MSO/DPO5000
    instrument families into the variables y (y data) and t (time
    data). The structure "info" contains information about units and
    digitizing resolution of the y data. The matrices ind_over and ind_under
    contain the indices of overranged data points outside the upper / lower
    limit of the TDS AD converter.
    If the file contains fast frames data, the data of the first frame is
    stored as usual and of all frames it is stored in the optional
    output struct "frames":
    frames.frame#.y=(y-data of #-th frame, including the first frame again)
    frames.frame#.t
    frames.frame#.info (contains only frame-specific fields of the info structure for frame number #)
    frames.frame#.ind_over
    frames.frame#.ind_under
    
    optional input arguments:
    datapoints, step,startind: read data points startind:step:datapoints
    from the wvf file. if datapoints is omitted, all data are read, if step
    is omitted, step=1. If startind omitted, startind=1
    
    
    Reading of *.wfm files written by other than the above Oscilloscopes may
    result in errors, since the file format seems not to be downward compatible.
    Other projects exist for the older format, e.g. wfmread.m by Daniel Dolan.
    
    Author:
    Erik Benkler
    Physikalisch-Technische Bundesanstalt
    Section 4.53: Optical Femtosecond Metrology
    Bundesallee 100
    D-38116 Braunschweig
    Germany
    Erik.Benkler a t ptb.de
    
    The implementation is based on Tektronix Article 077-0220-01
    (December 07, 2010): "Performance Oscilloscope Reference Waveform File Format"
    which can be found at:
    http://www2.tek.com/cmswpt/madetails.lotr?ct=MA&cs=mpm&ci=17905&lc=EN
    or by searching for 077022001 on the TEKTRONIX website (the last two
    digits seem to define the revision of the document, so you may search for
    077922002, 077922003, ... to find newer revisions in future.
    
    current state of the project and change history:
    
    Version 2.0, 22.03.2011
    (a)    added warning IDs for all warnings to render them switchable
    (b)    changed behaviour of the "datapoints" input parameter, which now
           defines the number of data points to be returned by wfm2read.
           Added a warning when "datapoints" is too large such that one would
           need more data points in the file / frame.
    
    Version 1.9, December 26, 2010 (re-submitted to FileExchange)
    (a)   implemented Fast frames
    (b)   added wfm2readframe for reading single frame
          in a fast frames measurement
    (c)   Added optional input argument startind, for starting reading at
          this datapoint within each frame
    
    Version 1.8, April 30, 2009 (re-submitted to FileExchange)
    (a)   improved file name checking
    
    Version 1.7, January 26, 2009 (re-submitted to FileExchange):
    (a)   improved performance when using the step argument by preallocating
          the array
    (b)   moved all "unused" read variables to info structure (produces less
          m-lint messages)
    
    Version 1.6, July 23, 2008 (re-submitted to FileExchange):
    (a)   Fixed the bug related to default char set on some Linux systems
          pointed out by Markus Kuhn
    (b)   Added compatibility with WFM003 format as suggested by Will Fox.
          (the comment in footnote 6 of the SDK on pixmap size has not been
          regarded).
          For a description of the new file format, download and unzip
          http://www.tek.com/products/oscilloscopes/openchoice/SDK_CD_2.0_122
          72006.zip and look for the file 001137803.pdf in the subdirectory
          bin/Articles/
    
    Version 1.5, December 11, 2005:
    (a)   added "step" input argument for reduced data reading.
    
    Version 1.4, November 11, 2005:
    (a)   changed to read unit string until NULL string only.
    
    Version 1.3, October 31, 2005 (submitted to FileExchange):
    (a)   Added handling of overranged values. Added two output variables
          ind_over and ind_under for this purpose.
    
    Version 1.2, July 07, 2005:
    (a)   Added optional second input parameter to limit the number of data
          points to be read.
    
    Version 1.1, April 12, 2005:
    (a)   Removed the bug that the byte order verification (big-endian vs. little-endian)
          was disregarded.
    (b)   close file at the end.
    (c)   Checked functionality with YT-waveform measured with TDS6804B scope.
    
    Version 1.0, December 20, 2004
    
    Already done:
    1) All file fields listed in the SDK article are assigned to variables named like in the SDK article
    2) Only reading of YT waveform is implemented. It is assumed that the waveform is
    a simple YT waveform. This is not checked and may result in errors when waveform is other than YT.
    3) Optional WFM#002 format is implemented (footnote 6 in SDK article)
    4)Checked functionality with YT-waveform measured with TDS5104B scope
    
    Yet to be done:
    1) reading of XY-wavefroms etc.
    2) handle interpolated data
    3) error checking, e.g. after each file operation, or checking if data is YT waveform should be improved
    4) only some important header information is output at this stage
    5) file checksum not yet implemented
    6) how to handle old format wfm files? Downward compatibility...
    '''

    #checking of file name etc.
    file_ext = os.path.splitext(filename)[1]
    if (file_ext != '.wfm' or not os.path.exists(filename)):
        print 'Invalid file name: ', filename
        return None

    fid = open(filename, 'rb');

    if step < 1 or (int(step) != step):
        print 'step must be a positive integer. Setting step to 1'
        step=1

    if startind < 0 or (int(startind) != startind):
        print 'startind must be a positive integer. Setting startind to 0'
        startind = 0

    info = {}
    #read the waveform static file info
    info['byte_order_verification'] = '{0:04X}'.format(struct.unpack('H', fid.read(2))[0])
    byteorder = '>' # big-endian byte order
    if info['byte_order_verification'] == '0F0F':
        byteorder = '<'; # little-endian byte order
    info['versioning_number'] = struct.unpack(byteorder+'8s', fid.read(8))[0]

    #There's a misprinting in the SDK article, the ":" at the beginning of version number string is missing.
    wfm_version = int(info['versioning_number'].split('#')[1]);
    if (wfm_version > 3):
        print 'wfm2read has only been tested with WFM file versions <= 3'

    info['num_digits_in_byte_count'] = rd_unpack(fid,'B',byteorder)
    info['num_bytes_to_EOF'] = rd_unpack(fid,'i',byteorder)
    info['num_bytes_per_point'] = rd_unpack(fid,'B',byteorder) #do not convert to same type, since required as double later
    info['byte_offset_to_beginning_of_curve_buffer'] = rd_unpack(fid,'I',byteorder)
    info['horizontal_zoom_scale_factor'] = rd_unpack(fid,'i',byteorder)
    info['horizontal_zoom_position'] = rd_unpack(fid,'f',byteorder)
    info['vertical_zoom_scale_factor'] = rd_unpack(fid,'d',byteorder)
    info['vertical_zoom_position'] = rd_unpack(fid,'f',byteorder)
    info['waveform_label'] = rd_unpack(fid,'32s',byteorder)
    info['N'] = rd_unpack(fid,'I',byteorder)
    info['size_of_waveform_header'] = rd_unpack(fid,'H',byteorder)

    #read waveform header
    info['setType'] = rd_unpack_a(fid,4,'B',byteorder)
    info['wfmCnt'] = rd_unpack(fid,'I',byteorder)
    rd_unpack(fid,'24s',byteorder) #skip bytes 86 to 109 (not for use)
    info['wfm_update_spec_count'] = rd_unpack(fid,'I',byteorder)
    info['imp_dim_ref_count'] = rd_unpack(fid,'I',byteorder)
    info['exp_dim_ref_count'] = rd_unpack(fid,'I',byteorder)
    info['data_type'] = rd_unpack_a(fid,4,'B',byteorder)
    rd_unpack(fid,'16s',byteorder) #skip bytes 126 to 141 (not for use)
    info['curve_ref_count'] = rd_unpack(fid,'I',byteorder)
    info['num_req_fast_frames'] = rd_unpack(fid,'I',byteorder)
    info['num_acq_fast_frames'] = rd_unpack(fid,'I',byteorder)

    #read optional entry in WFM#002 (and higher) file format:

    if wfm_version >= 2: # for version number >=2  only
        info['summary_frame_type'] = rd_unpack(fid,'H',byteorder)

    info['pixmap_display_format'] = rd_unpack_a(fid,4,'b',byteorder)
    info['pixmap_max_value'] = rd_unpack(fid,'Q',byteorder) #storage in a uint64 variable does not work. Uses only double. Bug in Matlab?

    #explicit dimension 1
    info['ed1'] = get_edim(fid, byteorder, wfm_version)
    # explicit dimension 2
    info['ed2'] = get_edim(fid, byteorder, wfm_version)
    #implicit dimension 1
    info['id1'] = get_idim(fid, byteorder, wfm_version)
    #implicit dimension 2
    info['id2'] = get_idim(fid, byteorder, wfm_version)

    #time base 1
    info['tb1_real_point_spacing'] = rd_unpack(fid,'I',byteorder)
    info['tb1_sweep'] = rd_unpack_a(fid,4,'b',byteorder)
    info['tb1_type_of_base'] = rd_unpack_a(fid,4,'b',byteorder)
    
    #time base 2
    info['tb2_real_point_spacing'] = rd_unpack(fid,'I',byteorder)
    info['tb2_sweep'] = rd_unpack_a(fid,4,'b',byteorder)
    info['tb2_type_of_base'] = rd_unpack_a(fid,4,'b',byteorder)

    #wfm update specification (first frame only if fast frames)
    info['real_point_offset'] = rd_unpack(fid,'I',byteorder)
    info['tt_offset'] = rd_unpack(fid,'d',byteorder)
    info['frac_sec'] = rd_unpack(fid,'d',byteorder)
    info['GMT_sec'] = rd_unpack(fid,'i',byteorder)

    #wfm curve information (first frame only if fast frames)
    info['state_flags'] = rd_unpack(fid,'I',byteorder)
    info['type_of_checksum'] = rd_unpack_a(fid,4,'b',byteorder)
    info['checksum'] = rd_unpack(fid,'h',byteorder)
    info['precharge_start_offset'] = rd_unpack(fid,'I',byteorder)
    info['data_start_offset'] = rd_unpack(fid,'I',byteorder) #do not convert to same type, since required as double later
    info['postcharge_start_offset'] = rd_unpack(fid,'I',byteorder) #do not convert to same type, since required as double later
    info['postcharge_stop_offset'] = rd_unpack(fid,'I',byteorder)
    info['end_of_curve_buffer_offset'] = rd_unpack(fid,'I',byteorder)

    frames = None
    if info['N']>0: #if the file contains fast frame data
        '''copy data for first frame to the frame struct (I do this to have all
        frames in  uniform output structure, although it is clear that this
        uses more memory than minimally needed, i.e. if not copying the data
        of the first frame):'''

        #wfm update specification
        frames = [None]*N
        frames[0] = {}
        frames[0]['info'] = {}
        frames[0]['info']['real_point_offset'] = info['real_point_offset']
        frames[0]['info']['tt_offset'] = info['tt_offset']
        frames[0]['info']['frac_sec'] = info['frac_sec']
        frames[0]['info']['GMT_sec'] = info['GMT_sec']

        #wfm curve information
        frames[0]['info']['state_flags']=info['state_flags']
        frames[0]['info']['type_of_checksum']=info['type_of_checksum']
        frames[0]['info']['checksum']=info['checksum']
        frames[0]['info']['precharge_start_offset']=info['precharge_start_offset']
        frames[0]['info']['data_start_offset']=info['data_start_offset']
        frames[0]['info']['postcharge_start_offset']=info['postcharge_start_offset']
        frames[0]['info']['postcharge_stop_offset']=info['postcharge_stop_offset']
        frames[0]['info']['end_of_curve_buffer_offset']=info['end_of_curve_buffer_offset']

        # read data for the other frames from the file:
        # TODO: May want to change this so that we read multiple samples at a time for faster reads
        for n in xrange(1, N):
            frames[n] = {}
            frames[n]['info'] = {}

            #wfm update specification
            frames[n]['info']['real_point_offset'] = rd_unpack(fid,'I',byteorder)
            frames[n]['info']['tt_offset'] = rd_unpack(fid,'d',byteorder)
            frames[n]['info']['frac_sec'] = rd_unpack(fid,'d',byteorder)
            frames[n]['info']['GMT_sec'] = rd_unpack(fid,'i',byteorder)

        for n in xrange(1, N):
            #wfm curve information
            frames[n]['info']['state_flags'] = rd_unpack(fid,'I',byteorder)
            frames[n]['info']['type_of_checksum'] = rd_unpack_a(fid,4,'b',byteorder)
            frames[n]['info']['checksum'] = rd_unpack(fid,'h',byteorder)
            frames[n]['info']['precharge_start_offset'] = rd_unpack(fid,'I',byteorder)
            frames[n]['info']['data_start_offset'] = rd_unpack(fid,'I',byteorder) #do not convert to same type, since required as double later
            frames[n]['info']['postcharge_start_offset'] = rd_unpack(fid,'I',byteorder) #do not convert to same type, since required as double later
            frames[n]['info']['postcharge_stop_offset'] = rd_unpack(fid,'I',byteorder)
            frames[n]['info']['end_of_curve_buffer_offset'] = rd_unpack(fid,'I',byteorder)

    # choose correct data format for reading in curve buffer data
    data_format = 'h'
    if info['ed1']['format'][0] == 0: 
        data_format='h'
    elif info['ed1']['format'][0] == 1: 
        data_format='i'
    elif info['ed1']['format'][0] == 2: 
        data_format='I'
    elif info['ed1']['format'][0] == 3: 
        #may not work properly. Bug in Matlab or not available in 32-bit Windows? Does not convert to uint64, but to double instead.
        data_format='Q'  
    elif info['ed1']['format'][0] == 4: 
        data_format='f'
    elif info['ed1']['format'][0] == 5: 
        data_format='d'
    elif info['ed1']['format'][0] == 6: 
        if (wfm_version >= 3):
            data_format='B'
        else:
            print 'invalid data format or error in file ', filename
            return None
    elif info['ed1']['format'][0] == 7: 
        if (wfm_version >= 3):
            data_format='b'
        else:
            print 'invalid data format or error in file ', filename
            return None
    else:
            print 'invalid data format or error in file ', filename
            return None

    #read the curve data (first frame only if file contains fast frame data)
    
    #jump to the beginning of the curve buffer
    offset = info['byte_offset_to_beginning_of_curve_buffer'] \
             + info['data_start_offset'] \
             + startind*info['num_bytes_per_point']
    byte_offset_nextframe = info['byte_offset_to_beginning_of_curve_buffer'] \
            + info['end_of_curve_buffer_offset'] #byte offset for the next frame (if it exists)
    fid.seek(offset,0)
    
    #read the curve buffer portion which is displayed on the scope only
    #(i.e. drop precharge and postcharge points)
    nop_all = (info['postcharge_start_offset']-info['data_start_offset'])/\
            info['num_bytes_per_point'] #number of data points stored in the file
    
    nop=nop_all-startind
    if datapoints is not None:
        if datapoints<1 or (int(datapoints)!=datapoints):
            # set to maximum number of data points which can be securely read from the file, using startind and step parameters 
            datapoints=int(np.floor(nop/step))
            print 'datapoints must be a positive integer. Setting datapoints to ', datapoints
        #maximum number of data points which can be securely read from the frame in the file, using startind and step parameters
        nop = np.floor(nop/step) 
        if datapoints > nop: #if more datapoints are requested than provided in the file
            print 'The requested combination of input parameters datapoints, \
                step and startind would require at least %d data points in %s \
                The actual number of data points in the trace is only %d.\n \
                The number of data points returned by wfm2read is thus only %d \
                instead of %d.' % ((datapoints-1)*step+startind+1, filename, \
                    nop_all, nop, datapoints)
        else:
            nop=datapoints

    values = array.array(data_format)
    values.fromstring(fid.read(struct.calcsize(data_format)*nop))
    t = info['id1']['dim_offset'] + info['id1']['dim_scale'] * np.arange(startind, (nop*step), step)
    values = np.array(values)
    y = info['ed1']['dim_offset'] + info['ed1']['dim_scale']*values  #scale data values to obtain in correct units
    
    #handling over- and underranged values
    ind_over=np.where(values==info['ed1']['over_range'])[0] #find indices of values that are larger than the AD measurement range (upper limit)
    ind_under=np.where(values<=-info['ed1']['over_range'])[0] #find indices of values that are larger than the AD measurement range (lower limit)
    
    info['yunit'] = info['ed1']['units']
    info['tunit'] = info['id1']['units']
    info['yres'] = info['ed1']['dim_resolution']
    info['samplingrate'] = 1/info['id1']['dim_scale']
    info['nop'] = nop;
    
    #print warning if there are wrong values because they are lying outside
    #the AD converter digitization window:
    if ind_over.size > 0: #ok
        print ' %d over range value(s) in file %s' % (ind_over.size, filename)
    if ind_under.size > 0: #ok
        print ' %d under range value(s) in file %s' % (ind_under.size, filename)

    if info['N']>0: #if file contains fast frame data and it is requested as output
        #copy data for first frame to the frame struct
        frames[0]['y']=y;
        frames[0]['t']=t;
        frames[0]['ind_over']=ind_over;
        frames[0]['ind_under']=ind_under;
    
        #get data for all remaining frames:
        for n in xrange(1, N):
            #jump to the beginning of the curve buffer
            offset = byte_offset_nextframe + frames[n]['info']['data_start_offset'] \
                     + startind*info['num_bytes_per_point']
            byte_offset_nextframe = byte_offset_nextframe + frames[n]['info']['end_of_curve_buffer_offset'] #byte offset for the next frame (if it exists)

            #read the curve buffer portion which is displayed on the scope only
            #(i.e. drop precharge and postcharge points)
            nop_all=(frames[n]['info']['postcharge_start_offset']-frames[n]['info']['data_start_offset'])/info.num_bytes_per_point #number of data points stored in the frame
            fid.seek(offset,0)
            nop=nop_all-startind;
            if datapoints is not None:
                nop = int(np.floor(nop/step)) #maximum number of data points which can be securely read from the frame in the file, using startind and step parameters
                if datapoints > nop: #if more datapoints are requested than provided in the file
                    # don't display warning again for the other frames, it has already been
                    # displayed for the first frame.
                    # print 'The requested combination of input parameters datapoints, 
                    #     step and startind would require at least %d data points in %s \n
                    #     The actual number of data points in the trace is only %d.\n 
                    #     The number of data points returned by wfm2read is thus only %d 
                    #     instead of %d.' % ((datapoints-1)*step+startind+1, filename,
                    #     nop_all, nop, datapoints)
                    pass
                else:
                    nop=datapoints
    
            values = [0] * nop
            for n in xrange(nop):
                values[n] = rd_unpack(fid,data_format,byteorder) 
                if step > 1:
                    rd_unpack(fid,'%ds' % info['num_bytes_per_point']*(step-1),byteorder) 
            tfix = info['GMT_sec']-info['frac_sec']+frames[n]['info']['GMT_sec']+frames[n]['info']['frac_sec']+(-info['tt_offset']+frames[n]['info']['tt_offset'])*info['id1']['dim_scale']
            frames[n]['t'] = info['id1']['dim_offset'] + info['id1']['dim_scale'] * np.arange(startind, (nop*step), step)-tfix
            values = np.array(values)
            frames[n]['y'] = info['ed1']['dim_offset'] + info['ed1']['dim_scale']*values  #scale data values to obtain in correct units
    
    
            #handling over- and underranged values
            frame[n]['ind_over']=np.where(values==info['ed1']['over_range'])[0] #find indices of values that are larger than the AD measurement range (upper limit)
            frame[n]['ind_under']=np.where(values<=-info['ed1']['over_range'])[0] #find indices of values that are larger than the AD measurement range (lower limit)
    
            #print warning if there are wrong values because they are lying outside
            #the AD converter digitization window:
            if frame[n]['ind_over'].size > 0: #ok
                print ' %d over range value(s) in file %s' % (frame[n]['ind_over'].size, filename)
            if frame[n]['ind_under'].size > 0: #ok
                print ' %d under range value(s) in file %s' % (frame[n]['ind_under'].size, filename)
    fid.close()
    return (y, t, info, ind_over, ind_under, frames)

if __name__ == "__main__":
    y, t, info, ind_over, ind_under, frames = wfm2read('../auth_tag_chiraag/150807_180742_Ch1.wfm')
    import matplotlib.pyplot as plt
    plt.plot(t, y)
    plt.show()


