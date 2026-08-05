clc; clear; close all;

FolderPath = '/home/user/docker-server/data/ing_AES_with_thpark/';
Fid_A = [FolderPath 'SCA_fixed_0.h5'];
Fid_B = [FolderPath 'SCA_random.h5'];

idx = h5info(Fid_A);

for i = 1:size(idx.Datasets,1)
    ret_TVLA{i} = tvla.h5onMem(Fid_A, ['/' idx.Datasets(i).Name], Fid_B, ['/' idx.Datasets(i).Name]);

end


IsSave = false;
if IsSave
    ['TVLA 결과 저장' '  ' char(datetime('now', 'Format', 'yy-MM-dd-HH-mm-ss'))]
    save_path = [FolderPath, 'TVLA-result-', char(datetime('now', 'Format', 'yy-MM-dd-HH-mm-ss')), '.mat'];
    save(save_path,ret_TVLA);
else
    for i = 1:size(idx.Datasets,1)
        nsr.TR_plot(ret_TVLA{i}, NaN, idx.Datasets(i).Name);
    end
end