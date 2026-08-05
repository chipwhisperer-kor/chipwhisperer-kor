close; clear;  clc;

FolderPath = '/home/user/docker-server/data/ing_AES_with_thpark/';
Fid_h5 = [FolderPath 'SCA_random.h5'];
h5disp(Fid_h5)

Fid_p = [FolderPath 'AES_PT_16B_1000.bin'];
Fid_k = [FolderPath 'AES_KEY_16B_1000.bin'];

pt = nsr.binRead(Fid_p, 16*1, 16*(1000-2));
pt = reshape(pt, 16, []);

GuessKey = uint8(nsr.binRead(Fid_k));
%GuessKey = reshape(uint8(0:255), 1, 1, []);

Hypo_IV = aes.AddRoundKey(pt, GuessKey);
Hypo_IV = aes.SubBytes(Hypo_IV);

PowerModel = cpa.HW(Hypo_IV); 
PowerModel = sum(PowerModel,1);


ret_CPA = cpa.h5onMem(Fid_h5, '/t_hw', PowerModel);

IsSave = false;
if IsSave
    ['CPA 결과 저장' '  ' char(datetime('now', 'Format', 'yy-MM-dd-HH-mm-ss'))]
    save_path = [FolderPath, 'CPA-result-', char(datetime('now', 'Format', 'yy-MM-dd-HH-mm-ss')), '.mat'];
    save(save_path,'ret_CPA');
else
    nsr.CPA_plot(ret_CPA,1);
end

