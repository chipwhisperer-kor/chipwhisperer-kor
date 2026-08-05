function [ret_CAP, ret_CPA_TERM] = h5onMem(Fid, Path_t, PowerModel, TrTerm)    
    arguments
        Fid
        Path_t
        PowerModel
        TrTerm double = 0;
    end
    
    TR  = h5read(Fid, Path_t);  
    TraceNum = size(TR,2);
    HypoNum = size(PowerModel,2);
    if TraceNum ~= HypoNum
        error("# TR IV Error. \n(TraceNum: %d, HypoNum: %d)", TraceNum, HypoNum);
    end
    
    PowerModel = permute(PowerModel, [2 3 1]);
    
    H = sum(PowerModel,1);
    H2 = sum((PowerModel.^2),1);
    W = sum(TR(:,1:TraceNum),2);
    W2 = sum((TR(:,1:TraceNum).^2),2);
    
    clearvars -except W W2 H H2 TR PowerModel TraceNum TrTerm;
    
    W2 = (TraceNum * W2) - (W .^ 2);
    H2 = (TraceNum * H2) - (H .^ 2);
    ret_CAP = pagemtimes(TR(:,1:TraceNum), PowerModel);
    ret_CAP = TraceNum * ret_CAP;
    ret_CAP = ret_CAP - pagemtimes(W, H);
    ret_CAP = ret_CAP ./ sqrt(pagemtimes(W2, H2));
    
    if (TrTerm ~= 0)
        ret_CPA_TERM = zeros(fix(TraceNum/TrTerm), size(H,2), size(H,3));
        for  ii = 1:size(H,3)
            CTR = 1;
            for jj = TrTerm:TrTerm:TraceNum
                H = sum(PowerModel(1:jj,:,:),1);
                H2 = sum((PowerModel(1:jj,:,:).^2),1);
                W = sum(TR(:,1:jj),2);
                W2 = sum((TR(:,1:jj).^2),2);
                CORR_tmp = (TR(:,1:jj) * PowerModel(1:jj,:,ii));
                CORR_tmp = (jj * CORR_tmp) - (W * H(:,:,ii));
                CORR_tmp = CORR_tmp ./ sqrt(((jj * W2) - (W .^ 2)) * ((jj * H2(:,:,ii)) - (H(:,:,ii) .^ 2)));
                
                ret_CPA_TERM(CTR,:,ii) = max(abs(CORR_tmp));
                CTR = CTR + 1;
            end
        end
    end

end
