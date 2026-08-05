function ret_TVLA = h5onMem(Fid_A, PathA_t, Fid_B, PathB_t)    
    ['그룹 A 시작' '  ' char(datetime('now', 'Format', 'yy-MM-dd-HH-mm-ss'))]
    TR_GroupA  = h5read(Fid_A, PathA_t);
    Nref = size(TR_GroupA,2);
    Xref = sum(TR_GroupA,2);
    Xref2 = sum((TR_GroupA .^2),2);
    clear TR_GroupA
    
    ['그룹 B 시작' '  ' char(datetime('now', 'Format', 'yy-MM-dd-HH-mm-ss'))]
    TR_GroupB  = h5read(Fid_B, PathB_t);
    Nother = size(TR_GroupB,2);
    Xother = sum(TR_GroupB,2);
    Xother2 = sum((TR_GroupB .^2),2);
    clear TR_GroupB
        
    ['TVLA 시작' '  ' char(datetime('now', 'Format', 'yy-MM-dd-HH-mm-ss'))]
    Xref = Xref ./ Nref;
    Xother = Xother ./ Nother;
    Xref2 = Xref2 ./ Nref;
    Xother2 = Xother2 ./ Nother;
    ret_TVLA = (Xref - Xother) ./ sqrt(((Xref2-(Xref.^2)) ./Nref) + ((Xother2-(Xother.^2)) ./Nother)) ;
    ret_TVLA = abs(ret_TVLA);
end