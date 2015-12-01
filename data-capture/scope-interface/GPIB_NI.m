%GPIB_NI Code for communicating with an instrument.
%
%   This is the machine generated representation of an instrument control
%   session. The instrument control session comprises all the steps you are
%   likely to take when communicating with your instrument. These steps are:
%   
%       1. Create an instrument object
%       2. Connect to the instrument
%       3. Configure properties
%       4. Write and read data
%       5. Disconnect from the instrument
% 
%   To run the instrument control session, type the name of the file,
%   GPIB_NI, at the MATLAB command prompt.
% 
%   The file, GPIB_NI.M must be on your MATLAB PATH. For additional information 
%   on setting your MATLAB PATH, type 'help addpath' at the MATLAB command 
%   prompt.
% 
%   Example:
%       gpib_ni;
% 
%   See also SERIAL, GPIB, TCPIP, UDP, VISA, BLUETOOTH.
% 
 
%   Creation time: 23-Nov-2015 17:58:13

% Find a GPIB object.
g = instrfind('Type', 'gpib', 'BoardIndex', 0, 'PrimaryAddress', 1, 'Tag', '');

% Create the GPIB object if it does not exist
% otherwise use the object that was found.
if isempty(g)
    g = gpib('NI', 0, 1);
else
    fclose(g);
    g = g(1);
end

% Connect to instrument object, g.
fopen(g);

%%
fprintf(g, 'ACQ:STATE RUN');
fprintf(g, 'ACQUIRE:NUMACQ?');
num_acqs = fscanf(g, '%d') 

prev_acqs = num_acqs;
orig_acqs = num_acqs;
curr_acqs = 1;

while(curr_acqs < orig_acqs + 500)
    fprintf(g, 'ACQUIRE:NUMACQ?');
    curr_acqs = fscanf(g,'%d');

    if(curr_acqs > prev_acqs)
        disp('Im here');
        %%
        fprintf(g,'DATA:SOURCE CH1');
        fprintf(g,'DATA:ENCdg ASCII');
        fprintf(g,'WFMO:BYT_N 4');
        fprintf(g,'DATA:START 1');
        fprintf(g,'DATA:STOP 10');

        %%

        fprintf(g, 'WFMOUTPRE?');
        source = fscanf(g)
        %%
        fprintf(g, 'CURVE?');
        source2 = fscanf(g)
        %%
        fprintf(g, 'DATA?');
        source3 = fscanf(g)
        %%
        filename = strcat('"C:\858\11-23-2015\W', int2str(curr_acqs), '.wfm"');
        fprintf(g, strcat('SAV:WAVE CH1,',filename));
        
        prev_acqs = curr_acqs
    end
    curr_acqs
end
%%

fclose(g);
delete(g);
clear g;