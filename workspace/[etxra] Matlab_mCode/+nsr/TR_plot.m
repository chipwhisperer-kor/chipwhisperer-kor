function TR_plot(TR, range, titleStr)

if nargin < 2
    range = NaN;
end
if nargin < 3
    titleStr = '';
end

if iscell(TR)
    for ii = 1:size(TR,1)
        figure;
        set(gcf,'Color','w');
        plot(TR{ii});
        xlim([0 size(TR{ii},1)]);    
        
        if ~isempty(titleStr)
            title(titleStr, 'Interpreter', 'none');
        end
        
        if ~isnan(range)
            ylim(range);        
        end
    end
else
    figure;
    set(gcf,'Color','w');
    plot(TR);
    xlim([0 size(TR,1)]);
    
    if ~isempty(titleStr)
        title(titleStr, 'Interpreter', 'none');
    end
    
    if ~isnan(range)
        ylim(range);        
    end
end

end