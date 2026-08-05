function state = AddRoundKey(state, RoundKey)
    % XOR 연산 (MATLAB Implicit Expansion 활용)
    %    - state가 [16 x 1]이면: 1:1 매칭 연산
    %    - state가 [16 x N]이면: rk_vector가 각 컬럼마다 자동으로 적용됨
    state = bitxor(state, RoundKey);
end