function CPA_plot(ret_CPA, Byte, key)
    arguments
        ret_CPA
        Byte double = 1;
        key double = [];
    end

    figure;
    set(gcf,'Color','w');
    if isempty(key)
        plot(ret_CPA(:,:,Byte));
    else
        plot(ret_CPA(:,:,Byte),'color', [0.7 0.7 0.7]);
        hold on;
        plot(ret_CPA(:,key,Byte),'r');
    end
    xlim([0 size(ret_CPA,1)]);

end