function [TimeVec,VoltageArray,AcqData] = ReadRigolOscBinData(bin_file,stp_file)
% This function reads the data from the rigol Oscilloscope DHO4204. If the
% waveform data was sourced from the 'screen', the bianry file contains all
% the required meta data. However, if the data was sourced from the
% internal memory, only the measured values are saved (as 2-byte unsigned
% intergers). To get useful and realistic units and at time vector, the stp
% file must be included. This can be saved with the binary files in the
% oscilloscope.
%
% If there is only one output Argument, this will only read out the ACQdata
% array

% Check if binary file exists
if ~exist(bin_file,"file")
    error(['File cannot be found: ', bin_file])
else
    idx = find(bin_file=='\',1,'last');
    disp(['reading file: ', bin_file(idx+1:end)])
end


% Open file
fid = fopen(bin_file,'r');


% HEADER
fileCookie = char(fread(fid, 2, '*uint8',0,'n')');

% Check if binary file has meta data included
if strcmpi(fileCookie,'RG')
    % Extract meta data
    fileVersion = (fread(fid, 2, '*uint8'));
    fileSize = (fread(fid, 1, '*uint64'));
    nWaveforms = (fread(fid,1, '*uint32'));

    VoltVec = cell(nWaveforms,1);
    TimeVec = cell(nWaveforms,1);
    MetaData = cell(nWaveforms,1);
    
    
    for ii = 1:nWaveforms
    
        % Waveform Header
        HeaderSize= fread(fid,1,'uint32'); 
        WaveformType = fread(fid,1,'uint32');
        NumWaveBuffer = fread(fid,1,'uint32');
        NumPoints = fread(fid,1,"uint32");
        Count = fread(fid,1,"uint32");
        XDisplayRange = fread(fid,1,"float32");
        XDisplayOrigin = fread(fid,1,"float64");
        XIncrement= fread(fid,1,"float64");
        XOrigin= fread(fid,1,"float64");
        XUnits= fread(fid,1,"uint32");
        YUnits= fread(fid,1,"uint32");
        Date= char(fread(fid,16,"uint8")');
        Time= char(fread(fid,16,"uint8")');
        Model= char(fread(fid,24,"uint8")');
        ChannelName= char(fread(fid,16,"uint8")');
    

        fseek(fid,12,'cof');    
            

        % Waveform Data Header
        HeaderSizeData = fread(fid,1,'uint32');
        BufferType = fread(fid,1,'uint16');
        BytesPerPoint = fread(fid,1,'uint16'); % uint16 
        BufferSize = fread(fid,1,'uint64');
        
        
        % parse info further
        switch WaveformType
            case 0
                WaveformType = 'Unknown';
            case 1
                WaveformType = 'Normal';
            case 2
                WaveformType = 'Peak Detection';
            case 3
                WaveformType = 'Average';
            case 6
                WaveformType = 'Logic';
        end
        
        switch XUnits
            case 0
                XUnits = 'Unknown';
            case 1
                XUnits = 'Volts (V)';
            case 2
                XUnits = 'Seconds (s)';
            case 3
                XUnits = 'Constant';
            case 4
                XUnits = 'Amps (A)';
            case 5
                XUnits = 'Decibel (dB)';
            case 6
                XUnits = 'Hetz (Hz)';
        end

        switch YUnits
            case 0
                YUnits = 'Unknown';
            case 1
                YUnits = 'Volts (V)';
            case 2
                YUnits = 'Seconds (s)';
            case 3
                YUnits = 'Constant';
            case 4
                YUnits = 'Amps (A)';
            case 5
                YUnits = 'Decibel (dB)';
            case 6
                YUnits = 'Hetz (Hz)';
        end
        
        switch BufferType
            case 0
                BufferType = 'Unknown';
            case 1
                BufferType = 'Normal 32-bit float data';
                
                data = fread(fid,NumPoints,'float32');
    
            case 2
                BufferType = 'maximum float data';
                data = fread(fid,NumPoints,'float32');
            case 3
                BufferType = 'Minimum float data';
                 data = fread(fid,NumPoints,'float64');
    
            case 5
                BufferType = 'Digital unsigned 8-bit character data';
    
                data = fread(fid,NumPoints,'uint8');
        end
        
    
        % ensure column data
        if size(data,2) ~= 1
            data = data';
        end
    
        % Read Data
        
        VoltVec{ii} = data;
        TimeVec{ii} = (0:XIncrement:XIncrement*(NumPoints-1));

        MetaData{ii} = struct(....
            'ChannelName',ChannelName,...
            'NumPoints',NumPoints,...
            'XUnits',XUnits,'YUnits',YUnits,...
            'Date',Date,'time',Time);

        figure()
        plot(TimeVec{ii},VoltVec{ii});
    end
    fclose(fid);

    TimeVec = TimeVec{1};
    if size(TimeVec,2) ~= 1
        TimeVec = TimeVec';
    end

    VoltageArray = [];
    for ii = 1:length(VoltVec)
        VoltageArray = cat(2,VoltageArray,VoltVec{ii});
    end

    AcqData = MetaData;

    return

else
    fclose(fid);
    % meta data not included in the header. Will need to extract that data
    % from the structure file.
    
    % if no structure file provided, assume same name structure file
    if nargin == 1
        stp_file = [bin_file(1:end-3),'stp'];
    end
    
    if exist(stp_file,"file")
        % Read structure file
        ACQ = ReadSTPfile(stp_file);

        if nargout==1
            % VoltageArray =ACQ;
            % AcqData =ACQ;
            TimeVec=ACQ;
            return
        end


        % Read binary file as 2-byte intgers into floats
        fid = fopen(bin_file,'r');
        data0 = fread(fid,'uint16=>double');
        fclose(fid);
        
        % Reshape based on the number of channels
        data = reshape(data0,ACQ.nChannels,[])';
        
        % Scale based on voltage scale and voltage offset
        for ii = 1:ACQ.nChannels
            data(:,ii) = (data(:,ii)/65535 - 1/2)*9*ACQ.Vscale(ACQ.ChannelsON(ii)); 
            data(:,ii) = data(:,ii) - ACQ.Voffset(ii);
        end  
        
        % Extract data
        TimeVec = ACQ.time_vec;
        VoltageArray = data;
        AcqData = ACQ;
        return
        
    else
        warning(['File cannot be found: ', stp_file])
        disp('recommend alternative analysis script')

        nChannels = 1;
    
        fid = fopen(bin_file,'r');
        data = fread(fid,'uint16=>float64');
        fclose(fid);
        data = data/65535 - 0.5;
        data = reshape(data,nChannels,[])';
    
        TimeVec = (1:length(data(:,1)))';
        VoltageArray = data;
        AcqData = 'nan';
        return
    end


    % % Check for structure file
    % if nargin == 2
    %     if ~exist(stp_file,"file")
    %         warning(['File cannot be found: ', stp_file])
    %     else
    % 
    %         % Read structure file
    %         ACQ = ReadSTPfile(stp_file);
    % 
    % 
    %         % Read binary file as 2-byte intgers into floats
    %         fid = fopen(bin_file,'r');
    %         data = fread(fid,'uint16=>double');
    %         fclose(fid);
    % 
    %         % Reshape based on the number of channels
    %         data = reshape(data,ACQ.nChannels,[])';
    % 
    %         % Scale based on voltage scale and voltage offset
    %         for ii = 1:ACQ.nChannels
    %             data(:,ii) = (data(:,ii)/65535 - 1/2)*9*ACQ.Vscale(ACQ.ChannelsON(ii)); 
    %             data(:,ii) = data(:,ii) - ACQ.Voffset(ii);
    %         end  
    % 
    %         % Extract data
    %         TimeVec = ACQ.time_vec;
    %         VoltageArray = data;
    %         AcqData = ACQ;
    %         return
    %     end
    % end
    % 
    % % If theres no structure file, output the integer values but shifted
    % % down to the origin
    % disp('No structure file: assuming 1 channel (recommend different analysis script)');
    % nChannels = 1;
    % 
    % fid = fopen(bin_file,'r');
    % data = fread(fid,'uint16=>float64');
    % fclose(fid);
    % data = data/65535 - 0.5;
    % data = reshape(data,nChannels,[])';
    % 
    % TimeVec = (1:length(data(:,1)))';
    % VoltageArray = data;
    % AcqData = 'nan';
    % return

end


end

function ACQ = ReadSTPfile(file)
    idx = find(file=='\',1,'last');
    disp(['reading file: ', file(idx+1:end)])

    acq_str = []; % acquistion relevant strings
    ch_str = cell(4,1); % Channel relevant strings.
    
    % Read file and save usefule strings
    fid = fopen(file,'r','n','UTF-8');
    while ~feof(fid)
        Line=fgetl(fid);  
    
        % Save useful Channel lines

        if strcmpi(Line,'<ServiceID1>') % Channel 1
            while ~strcmpi(Line,'</ServiceID1>')
                Line = fgetl(fid);
                ch_str{1}=[ch_str{1},Line];
            end
        end     
        if strcmpi(Line,'<ServiceID2>') % Channel 2
            while ~strcmpi(Line,'</ServiceID2>')
                Line = fgetl(fid);
                ch_str{2}=[ch_str{2},Line];
            end
        end           
        if strcmpi(Line,'<ServiceID3>') % Channel 3
            while ~strcmpi(Line,'</ServiceID3>')
                Line = fgetl(fid);
                ch_str{3}=[ch_str{3},Line];
            end
        end        
        if strcmpi(Line,'<ServiceID4>') % Channel 4
            while ~strcmpi(Line,'</ServiceID4>')
                Line = fgetl(fid);
                ch_str{4}=[ch_str{4},Line];
            end
        end 
    
    
        % Save Acquisiton setting lines
        if contains(Line,'nChannel') % number of recorded channels
            acq_str = [acq_str,Line];
        elseif contains(Line,'acq_mode') % acquisition mode (norm/hi-res)
            acq_str = [acq_str,Line];
        elseif contains(Line,'acq_dep') % Memory depth
            acq_str = [acq_str,Line];
        elseif contains(Line,'main_scale') % Hscale (time scaled: 1e15)
            acq_str = [acq_str,Line];
        elseif contains(Line,'nWaveFormat') % wave format: 1=internal memory
            acq_str = [acq_str,Line];
        elseif contains(Line,'acq_bit') % acq bits - not sure how
            acq_str = [acq_str,Line];
        elseif contains(Line,'imp') % impedence (1=omeg)
            acq_str = [acq_str,Line];
        elseif contains(Line,'main_offset') % main offset
            acq_str = [acq_str,Line];
        elseif contains(Line,'OffsetUnit') % main offset
            acq_str = [acq_str,Line];
        elseif contains(Line,'OffsetMax') % main offset
            acq_str = [acq_str,Line];
        elseif contains(Line,'OffsetMin') % main offset
            acq_str = [acq_str,Line];
        end
    end
    fclose(fid);

    % Read strings and Save data
    ACQ = struct();
    ACQ.filename = file;

    % Save channel data
    ACQ.Vscale = zeros(1,4);
    ACQ.Voffset = zeros(1,4);
    ACQ.label = cell(1,4);
    ACQ.ChannelsON = [];% save which channels indexes are on
    for ii = 1:4
        ACQ.Vscale(ii) = GetValueFromName(ch_str{ii},'<scale>','after','</scale>')*1e-9;
        ACQ.Voffset(ii) = GetValueFromName(ch_str{ii},'<null>','after','</null>')*1e-9;
        ACQ.label{ii} = GetValueFromName(ch_str{ii},'<label>','after','</label>');
        if GetValueFromName(ch_str{ii},'<on>','after','</on>')
            ACQ.ChannelsON = [ACQ.ChannelsON,ii];
        end   
    end
    
    
    
    % Save Acqusition settings
    ACQ.memdepth = GetValueFromName(acq_str,'acq_dep>','after','<');
    ACQ.Hscale = GetValueFromName(acq_str,'main_scale?','after','<')*1e-15;
    ACQ.mode = GetValueFromName(acq_str,'acq_mode>','after','<');
    ACQ.bits = GetValueFromName(acq_str,'acq_bit>','after','<');
    ACQ.nChannels = length(ACQ.ChannelsON);
    
    if ACQ.nChannels == 3
        ACQ.nChannels = 4;
        ACQ.ChannelsON  = [1,2,3,4];
    end
    

    % Number of points in memory based on setting value.
    switch ACQ.memdepth
        case 1
            ACQ.npoints = 1e3;
        case 2
            ACQ.npoints = 1e4;
        case 3
            ACQ.npoints = 1e5;
        case 4
            ACQ.npoints = 1e6;
        case 5
            ACQ.npoints = 1e7;
        case 6
            ACQ.npoints = 25e6;
        case 7
            ACQ.npoints = 50e6;
        case 8
            ACQ.npoints = 100e6;
        case 9
            ACQ.npoints = 125e6;
        case 10
            ACQ.npoints = 200e6;
        case 11
            ACQ.npoints = 250e6;
        case 12
            ACQ.npoints = 500e6;
        otherwise
            ACQ.npoints = nan;
    end
    
    switch ACQ.mode
        case 0
            ACQ.mode = 'Norm';
        case 1
            ACQ.mode = 'Peak';
        case 2
            ACQ.mode = 'Aver';
        case 3
            ACQ.mode = 'HRes';
        case 4
            ACQ.mode = 'Ultr';
    end
    
    switch ACQ.bits % Not sure if this is accurate.
        case 6
            ACQ.bits = 12;
        case 7
            ACQ.bits = 14;
        case 8
            ACQ.bits = 16;
    end
    
    % Determine time settings
    Horiz_offsets = [GetValueFromName(acq_str,'OffsetUnit>','after','<'),...
        GetValueFromName(acq_str,'OffsetMax>','after','<'),...
        GetValueFromName(acq_str,'OffsetMin>','after','<')];

    ratio = (Horiz_offsets(2)-Horiz_offsets(3))./Horiz_offsets(1)/4;
    ACQ.measurement_time = ACQ.Hscale*ratio;
    ACQ.time_vec = linspace(0,ACQ.measurement_time,ACQ.npoints)';
    ACQ.dt = ACQ.Hscale*ratio./ACQ.npoints;

end

function output = GetValueFromName(Name,ReferenceStr,Direction,Terminator)
    % This function takes a name (often a filenmae), locates the reference str
    % and outputs the neighbouring value. The ouput string/number is terminated
    % by the Terminator input. The funcation always attempts to output a number
    % and upon failing, outputs a string.
    %
    % Name [req]    - (string)
    % FlagStr[req]  - A string neighbouring the value of interst
    % Direction     - ['before','after' (default)] which side of the flag is 
    %                   the vlaue on
    % Terminator    - (string/int/cell of strings). Terminator is the end point
    %                   of the Value. a string or cell of strings match find
    %                   cap the Value string  w.r.t the shortest case. Using an
    %                   int, specifies the length of the value. If int = 0,
    %                   then it stops once a number is retruned.
    %
    % E.g. name="vat01_aom80_288angle.tdms"
    %   - GetValueFromName(name,'aom') = 80
    %   - GetValueFromName(name,'aom','after',0) = 80
    %   - GetValueFromName(name,'angle','before','_') = 288
    %   - GetValueFromName(name,'vat','after',{'angle','aom}) = '1_'
    
    if nargin == 2
        Direction = 'after';
        Terminator = 0;
    elseif nargin == 3
        Terminator = 0;
    end
    
    
    % Handle Direction part 1
    if strcmpi(Direction,'before')
       Name = reverse(Name);
       ReferenceStr = reverse(ReferenceStr);
       if isa(Terminator, 'char')|| isa(Terminator, 'cell')
           Terminator = reverse(Terminator);
       end
    elseif strcmpi(Direction,'after')
        Direction = 'after';
    end
    
    % Find starting index of value
    start_idx = regexp(Name,ReferenceStr);
    start_idx = start_idx + length(ReferenceStr);
    temp_name = Name(start_idx:end);
    
    if isempty(temp_name)
        if strcmpi(Direction,'before')        
            warning_str = ['No value from ',reverse(Name),' ',Direction,' ',reverse(ReferenceStr),' could be found'];
        else
            warning_str = ['No value from ',Name,' ',Direction,' ',ReferenceStr,' could be found'];
        end
        warning(warning_str)
        output = nan;
        return 
    end
       
    
    % Get end index from terminator
    switch class(Terminator)
        case 'char' % If terminator is just a string
            if isempty(Terminator)
                end_idx = length(temp_name);
            elseif Terminator == '.'
                end_idx = find(temp_name=='.')-1;            
            else
                end_idx = regexp(temp_name,Terminator) - 1;
            end
            
        case 'double' % Length of output string
            if Terminator > 0
                end_idx = Terminator;
            elseif Terminator == 0 && isstrprop(temp_name(1),'digit') % Assume digit and get number output
                end_idx = find(~isstrprop(temp_name,'digit'),1,'first') - 1;
            else
                end_idx = '';
            end
        case 'cell' % cell array of different terminal strings (use shortest)
            indexes = []; 
            for ii = 1:length(Terminator)
                index = find(temp_name==Terminator{ii});
                if ~isempty(index)
                    indexes(end+1) = index-1;
                end
            end
            end_idx = min(indexes);
    
        otherwise 
            end_idx = length(temp_name); 
    end
    
    if isempty(end_idx)
        end_idx = length(temp_name);
    end
    output_str = temp_name(1:end_idx);
    
    % handle Direction part 2
    if strcmpi(Direction,'before')
           output_str = reverse(output_str);
    end
    
    % Convert to number if possible
    output = str2num(output_str); %#ok<ST2NM>
    if isempty(output)
        output = output_str;
    end
            
end
