function state = ShiftRows(state)
    % ---------------------------------------------------------
    % ShiftRows: 순열(Permutation)을 이용한 초고속 구현
    %
    % 입력: [16 x N x M ...] 임의 차원 지원
    % 원리: 4x4 행렬 변환 없이 인덱스 치환만으로 행 이동 효과를 냄
    % ---------------------------------------------------------

    % 1. 원본 차원 저장 (나중에 복구용)
    original_size = size(state);

    % 2. 차원 단순화 (Flattening)
    %    [16 x N x M] -> [16 x (N*M)]
    %    3차원 이상의 배열을 2차원 행렬(16행)로 폅니다.
    %    MATLAB의 reshape는 데이터 복사 없이 메타데이터만 변경하므로 매우 빠릅니다.
    flat_state = reshape(state, 16, []);

    % 3. 순열 인덱스 (Permutation Vector) 정의
    %    AES ShiftRows 규칙을 1차원 인덱스(1~16)로 변환한 결과입니다.
    %    (매번 계산하지 않고 하드코딩하는 것이 가장 빠릅니다)
    %
    %    변환 원리:
    %    Row 1 (0 shift):  1,  5,  9, 13 ->  1,  5,  9, 13
    %    Row 2 (1 shift):  2,  6, 10, 14 ->  6, 10, 14,  2
    %    Row 3 (2 shift):  3,  7, 11, 15 -> 11, 15,  3,  7
    %    Row 4 (3 shift):  4,  8, 12, 16 -> 16,  4,  8, 12
    %    -> 이를 세로(Column-major) 순서로 다시 읽으면 아래 배열이 됩니다.
    p = [1; 6; 11; 16; ...  % 1열
         5; 10; 15; 4; ...  % 2열
         9; 14; 3;  8; ...  % 3열
         13; 2;  7; 12];    % 4열

    % 4. 순열 적용 (All Columns at once)
    %    flat_state(p, :)를 수행하면 모든 컬럼(블록)에 대해
    %    동시에 행 섞기가 수행됩니다.
    flat_state = flat_state(p, :);

    % 5. 원래 차원으로 복구
    state = reshape(flat_state, original_size);
end