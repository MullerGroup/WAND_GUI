% plotting neural data recorded in hdf file format

classdef streamhdf < handle
    % streamplot is used to plot stream data recorded to hdf file
    % functions:
    %   plotch(channel, new)
    %       plots the raw channel data, cycle through channels with left and
    %       right arrow keys
    %       channel - which channel to start plotting from
    %       new - whether to open up a new figure or not
    %   get_errors()
    %       finds the errors in the data by searching for outliers
    %   plot_errors()
    %       plots error rate per channel and histogram of errors in each sample
    %   clean_data()
    %       removes errors from data using interpolation
    %   plotch_clean(channel, new)
    %       plots the cleaned channel data, cycle using arrow keys
    %   get_fft()
    %       calculate fft for each channel
    %   plot_fft
    %       plot ffts for each channel, cycle using arrow keys
    
    properties (SetAccess = private)
        file;               % hdf file containing raw data
        start_sample;       % which sample to start analysis from
        count;              % how many samples to analyze
        channels_raw;       % raw values indicating which channels are recorded
        numchannels;        % number of channels enabled
        channels;           % list of which actual channels are recorded
        datetime;           % date and time of start of recording
        data;               % raw data
        time;               % time stamps of samples
        error_loc;          % locations of errors in each channel
        error_tot;
        error_unique;       
        actual_errors;
        num_errors;         % number of errors in each channel
        polyorder;          % order for polynomial fit for data
        threshold;          % threshold for finding outliers
        fail_rates;         % error rates for each channel
        data_clean;         % cleaned data
        fftdata;            % ffts for each channel
        crc;
        ramp;
        crc_errors;
        
        % for plotting the raw data
        chidx;              % current ploted channel
        chidx_next;         % next channel
        chidx_prev;         % previous channel
        
        % for plotting the cleaned data
        chidx_clean;
        chidx_clean_next;
        chidx_clean_prev;
        
        % for plotting the fft's
        chidx_fft;
        chidx_fft_next;
        chidx_fft_prev;
        
    end
    
    properties
        % current opened figure
        fig;
    end

    methods
        
        function this = streamhdf(hdffile, start, count)
            
            if nargin < 3
                start = 1;
                temp_info = h5info(hdffile);
                count = temp_info.Groups(1).Datasets(1).Dataspace.Size;
            end
            
            this.error_unique = [];
            this.error_tot = [];
            
            % set these for finding errors:
            this.polyorder = 10; % order of polynomial for fitting the data
            this.threshold = 4; % number of standard deviations for finding outliers
            
            
            % constructor only needs the csv file name
            this.file = hdffile;    % filename that we will be working with
            
            % get which channels are enabled and recorded
            this.channels = [];
            hdf = h5read(hdffile,'/infoGroup/infoTable');
            this.channels_raw = hdf.channels;
%             this.channels_raw = [65535, 65535, 65532, 0, 0, 0, 0, 0];
            
            for i = 1:length(this.channels_raw)
                temp = dec2bin(this.channels_raw(i),16);
                for j = 1:length(temp)
                    if temp(j) == '1'
                        if length(this.channels) < 96
                            this.channels(end+1) = j + (i-1)*16 - 1;
                        end
                    end
                end
            end
            
            this.numchannels = length(this.channels);
            this.actual_errors = cell(1,this.numchannels);
            
 
            % get the raw data table
            this.start_sample = start;
            this.count = count;
            hdf = h5read(hdffile,'/dataGroup/dataTable',start, count);
            this.data = (hdf.out(2:this.numchannels+1, :))';
            this.crc = hdf.out(1,:);
            this.ramp = hdf.out(this.numchannels+2,:);
            this.time = hdf.time;
%             this.data = (hdf.data)';
%             this.time = hdf.time;
%             this.crc = hdf.crc;
%             this.ramp = hdf.ramp;

            % plotting parameters
            this.chidx = 1;
            this.chidx_next = 2;
            this.chidx_prev = this.numchannels;
            
            this.chidx_clean = 1;
            this.chidx_clean_next = 2;
            this.chidx_clean_prev = this.numchannels;
            
            this.chidx_fft = 1;
            this.chidx_fft_next = 2;
            this.chidx_fft_prev = this.numchannels;
            
            % error analysis
            this.error_loc = cell(1,this.numchannels);
            this.num_errors = zeros(1,this.numchannels);
            this.fail_rates = [];
            
            % cleaned data
            this.data_clean = this.data;
            
            % fft stuff
            this.fftdata = zeros(500,this.numchannels);
            
            
            
            % start the plot
            this.plotch(1,1);
            % plot error analysis
            this.get_errors();
%             % clean the data
%             this.clean_data();
%             % plot clean data
%             this.plotch_clean(1,1);
            % plot the ffts
            %this.get_fft();  
        end           
        
        function plotch(this, ch_index, new)
            if new == 1
                figure
            end
            
            plot(this.time, this.data(:,ch_index));
            title(strcat('Channel',{' '},num2str(this.channels(ch_index)),{' '},'Raw Data'));
            ylabel('Raw Data');
            xlabel('Time (s)');

            
            this.fig = gcf;
            set(this.fig,'KeyPressFcn',@(src,evt) keypress_callback(this,src,evt));
            
            this.chidx = ch_index;
            this.chidx_next = mod(ch_index, this.numchannels) + 1;
            if ch_index == 1
                this.chidx_prev = this.numchannels;
            else
                this.chidx_prev = ch_index - 1;
            end
            
        end
        
        function keypress_callback(this,obj,evt)
            if strcmp(evt.Key,'rightarrow') == 1
                this.plotch(this.chidx_next,0);
            elseif strcmp(evt.Key,'leftarrow') == 1
                this.plotch(this.chidx_prev,0);
            end
        end
        
        function get_errors(this)
            this.error_loc = []
            

            for i = 1:(length(this.ramp)-1)
                if this.ramp(i) + 1 ~= this.ramp(i+1)
                    if (this.ramp(i) == 65535) && (this.ramp(i+1) == 0)
                    else
                        this.error_loc(end+1) = i;
                    end
                end
            end

            this.actual_errors = [];

            for j = 1:length(this.error_loc)
                actual = 0;
                if j == length(this.error_loc)
                    actual = 1;
                elseif this.error_loc(j+1) ~= this.error_loc(j)+1
                    actual = 1;
                elseif this.error_loc(j) ~= 1
                    if this.ramp(this.error_loc(j)) ~= this.ramp(this.error_loc(j)-1)+1
                        if (this.ramp(this.error_loc(j))~=0) || (this.ramp(this.error_loc(j)-1)~=65535)
                            actual = 1;
                        end
                    end
                end
                if actual == 1
                    this.actual_errors(end+1) = this.error_loc(j);
                end
            end
                
            diffs = diff(this.ramp);
            for i = 1:length(this.actual_errors)
                this.actual_errors(2,i) = diffs(this.actual_errors(1,i));
            end
            
            for i = 1:length(this.num_errors)
                this.num_errors(i) = length(this.actual_errors);
            end
            
            this.error_tot = this.actual_errors;

            num_crcs = 0;
            for i = 1:length(this.crc)
                if this.crc(i) ~= 170
                    num_crcs = num_crcs + 1;
                end
            end
            this.crc_errors = num_crcs;
        end
        
            
        function clean_data(this)
            this.data_clean = this.data;
            for i = 1:this.numchannels
                end_of_runs = find(diff([this.error_loc{i},0])~=1);
                runs = {};
                start = 1;
                for j = 1:length(end_of_runs)
                    runs{end+1} = [start, end_of_runs(j)];
                    start = end_of_runs(j) + 1;
                end
                
                for j = 1:length(runs)
                    this.data_clean(this.error_loc{i}(runs{j}(1)):this.error_loc{i}(runs{j}(2)),i) = ...
                        round(mean([this.data_clean(max(1,this.error_loc{i}(runs{j}(1))-1),i),this.data_clean(min(length(this.data_clean(:,i)),this.error_loc{i}(runs{j}(2))+1),i)]));
                end 
            end
        end
        
        function plotch_clean(this, ch_index,new)
            if new == 1
                figure
            end
            
            plot(this.time, this.data_clean(:,ch_index));
            title(strcat('Channel',{' '},num2str(this.channels(ch_index)),{' '},'Cleaned Data'));
            ylabel('Raw Data');
            xlabel('Time (s)');

            
            this.fig = gcf;
            set(this.fig,'KeyPressFcn',@(src,evt) keypress_callback_clean(this,src,evt));
            
            this.chidx_clean = ch_index;
            this.chidx_clean_next = mod(ch_index, this.numchannels) + 1;
            if ch_index == 1
                this.chidx_clean_prev = this.numchannels;
            else
                this.chidx_clean_prev = ch_index - 1;
            end
            
        end
        
        function keypress_callback_clean(this,obj,evt)
            if strcmp(evt.Key,'rightarrow') == 1
                this.plotch_clean(this.chidx_clean_next,0);
            elseif strcmp(evt.Key,'leftarrow') == 1
                this.plotch_clean(this.chidx_clean_prev,0);
            end
        end
        
        function get_fft(this)
            this.fftdata = zeros(500,this.numchannels);
            for i = 1:this.numchannels
                y = abs(fft(this.data_clean(1:1000,i),1000));
                this.fftdata(:,i) = y(2:501);
            end
             
            this.plot_fft(1,1);
        end
        
        function plot_fft(this,ch_index,new)
            if new == 1
                figure
            end
            
            plot(this.fftdata(:,ch_index));
            title(strcat('Channel',{' '},num2str(this.channels(ch_index)),{' '},'FFT'));
            ylabel('Power');
            xlabel('Frequency (Hz)');
            
            this.fig = gcf;
            set(this.fig,'KeyPressFcn',@(src,evt) keypress_callback_fft(this,src,evt));
            
            this.chidx_fft = ch_index;
            this.chidx_fft_next = mod(ch_index, this.numchannels) + 1;
            if ch_index == 1
                this.chidx_fft_prev = this.numchannels;
            else
                this.chidx_fft_prev = ch_index - 1;
            end
        end
        
        function keypress_callback_fft(this,obj,evt)
            if strcmp(evt.Key,'rightarrow') == 1
                this.plot_fft(this.chidx_fft_next,0);
            elseif strcmp(evt.Key,'leftarrow') == 1
                this.plot_fft(this.chidx_fft_prev,0);
            end
        end
        
    end
    
end

    
    


    