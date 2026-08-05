close; clear; clc;

% --- 사용 예시 ---
% 평문과 키 (16바이트)
%plaintext = '6bc1bee22e409f96e93d7e117393172a';
%key       = '2b7e151628aed2a6abf7158809cf4f3c';
%ciphertext_ref = '3ad77bb40d7a3660a89ecaf32466ef97';

plaintext      = '6bc1bee22e409f96e93d7e117393172a6bc1bee22e409f96e93d7e117393172a6bc1bee22e409f96e93d7e117393172a';
key            = '2b7e151628aed2a6abf7158809cf4f3c';
ciphertext_ref = '3ad77bb40d7a3660a89ecaf32466ef973ad77bb40d7a3660a89ecaf32466ef973ad77bb40d7a3660a89ecaf32466ef97';

%plaintext = '00000000000000000000000000000000';
%key       = '000102030405060708090A0B0C0D0E0F';


fprintf('plaintext: %s \n', plaintext);
fprintf('key: %s \n', key);


pbyte = uint8(sscanf(plaintext, '%2x')).';
pbyte = reshape(pbyte, 16, []);
kbyte = uint8(sscanf(key, '%2x')).';
kbyte = reshape(kbyte, 16, []);


% AES 키 스케줄 함수
RoundKey = aes.KeyExpansion(kbyte);
    aes.debug_state(RoundKey, 'KeyExpansion', '');

% AES 암호화 함수
Nr = 10;
state = pbyte;
aes.debug_state(state, 'state', 0);


% --- Round 0 ---
state = aes.AddRoundKey(state, RoundKey(:,1));
    aes.debug_state(state, 'AddRoundKey', 0);

% --- Rounds 1 to Nr-1 ---
for round = 1 : (Nr - 1)
    state = aes.SubBytes(state);
        aes.debug_state(state, 'SubBytes', round);
    
    state = aes.ShiftRows(state);
        aes.debug_state(state, 'ShiftRows', round);

    state = aes.MixColumns(state);
        aes.debug_state(state, 'MixColumns', round);

    state = aes.AddRoundKey(state, RoundKey(:,round + 1));
        aes.debug_state(state, 'AddRoundKey', round);
end

% --- Round Nr (Final Round) ---
state = aes.SubBytes(state);
    aes.debug_state(state, 'SubBytes', 10);

state = aes.ShiftRows(state);
    aes.debug_state(state, 'ShiftRows', 10);

state = aes.AddRoundKey(state, RoundKey(:,Nr+1));
    aes.debug_state(state, 'AddRoundKey', 10);


fprintf('\n\n');
ciphertext = lower(reshape(dec2hex(state(:).', 2).', 1, []));


fprintf('ciphertext    : %s \n', ciphertext);
fprintf('ciphertext_ref: %s \n', ciphertext_ref);
