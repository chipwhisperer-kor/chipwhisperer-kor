function state = MixColumns(state)
    % ---------------------------------------------------------
    % MixColumns: 열(Column) 단위 믹싱 연산
    %
    % 입력: [16 x N x M ...] 임의 차원 지원
    % 원리: 4xN 행렬로 변환하여 모든 컬럼을 동시에 연산 (Vectorized)
    % ---------------------------------------------------------

    % 1. 원본 차원 저장
    original_size = size(state);
    
    % 2. [4 x Total_Columns] 형태로 변환
    %    - AES에서 MixColumns는 4바이트(1개 컬럼) 단위로 독립적으로 수행됩니다.
    %    - 16바이트 블록 1개는 4개의 컬럼을 가집니다.
    %    - 따라서 데이터를 높이가 4인 행렬로 만들면, 옆으로 나열된 모든 컬럼에 대해
    %      동일한 연산을 한 번에 적용할 수 있습니다.
    s = reshape(state, 4, []);
    
    % 3. 각 행(Row) 추출 (가독성 및 연산 편의를 위해 분리)
    r1 = s(1, :);
    r2 = s(2, :);
    r3 = s(3, :);
    r4 = s(4, :);
    
    % 4. 공통항 Tmp 계산
    %    Tmp = r1 ^ r2 ^ r3 ^ r4
    Tmp = bitxor(r1, bitxor(r2, bitxor(r3, r4)));
    
    % 5. 원본 r1 저장 (마지막 r4 계산 시 필요)
    t = r1;
    
    % --- Row 1 업데이트 ---
    % Tm = r1 ^ r2
    Tm = bitxor(r1, r2);
    Tm = xtime(Tm);
    r1 = bitxor(r1, bitxor(Tm, Tmp));
    
    % --- Row 2 업데이트 ---
    % Tm = r2 ^ r3
    Tm = bitxor(r2, r3);
    Tm = xtime(Tm);
    r2 = bitxor(r2, bitxor(Tm, Tmp));
    
    % --- Row 3 업데이트 ---
    % Tm = r3 ^ r4
    Tm = bitxor(r3, r4);
    Tm = xtime(Tm);
    r3 = bitxor(r3, bitxor(Tm, Tmp));
    
    % --- Row 4 업데이트 ---
    % Tm = r4 ^ t (t는 원본 r1)
    Tm = bitxor(r4, t);
    Tm = xtime(Tm);
    r4 = bitxor(r4, bitxor(Tm, Tmp));
    
    % 6. 결과 병합
    s(1, :) = r1;
    s(2, :) = r2;
    s(3, :) = r3;
    s(4, :) = r4;
    
    % 7. 원래 차원으로 복구
    state = reshape(s, original_size);
end

function val = xtime(x)
    % ---------------------------------------------------------
    % xtime: 배열 입력(Vectorized)을 지원하도록 수정됨
    % ---------------------------------------------------------
    
    % 1. Shift 연산 (x << 1)
    t1 = bitshift(x, 1);
    
    % 2. MSB 체크 (x >> 7)
    %    배열 연산이므로 결과는 0 또는 1로 구성된 배열이 됩니다.
    t2 = bitand(bitshift(x, -7), 1);
    
    % 3. 조건부 XOR 연산 (if문 제거 -> 곱셈 마스킹)
    %    기존: if (t2==1) mask=0x1b else mask=0
    %    변경: mask = t2 * 0x1b
    %    t2가 1이면 0x1b가 되고, 0이면 0이 되어 if문과 동일하게 동작합니다.
    mask = t2 * 0x1b;
    
    % 4. 최종 결과
    val = bitxor(t1, mask);
end