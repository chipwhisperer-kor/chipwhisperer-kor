function debug_state(state, label, r_num) 
    % -------------------------------------------------------------------------
    % debug_state: 상태 행렬을 16바이트 단위로 한 줄씩 출력
    %
    % 입력:
    %   state  : [16 x N x ...] 형태의 데이터 (첫 차원은 반드시 16)
    %   label  : 출력할 라벨 문자열 (예: 'Start', 'SubBytes' 등)
    %   r_num  : 현재 라운드 번호
    % -------------------------------------------------------------------------

    % 1. 차원 평탄화 (Flattening)
    %    입력이 [16, 1], [16, 10], [16, 5, 5] 등 어떤 형태이든
    %    [16 x (블록의 총 개수)] 형태의 2차원 행렬로 변환합니다.
    flat_state = reshape(state, 16, []);
    
    num_blocks = size(flat_state, 2);

    % 2. 블록 단위 반복 출력
    for i = 1:num_blocks
        % (선택사항) 여러 블록을 출력할 때 블록 인덱스를 함께 표시하여 구분
        if num_blocks > 1
            fprintf('%s(%02d) [Block %02d]: ', label, r_num, i);
        else
            fprintf('%s(%02d): ', label, r_num);
        end
        
        % 3. 해당 블록의 16바이트 데이터 출력
        %    flat_state(:, i)는 16x1 벡터이므로 차례대로 출력됩니다.
        fprintf('%02x ', flat_state(:, i));
        
        % 줄바꿈 (16바이트 출력 후)
        fprintf('\n');
    end
end