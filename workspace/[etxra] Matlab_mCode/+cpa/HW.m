function counts = HW(data)
    % 입력 데이터의 1의 개수(Hamming Weight)를 고속으로 계산
    % 입력: uint8, uint16, uint32, uint64 타입의 배열
    % 출력: 입력과 동일한 크기의 double 타입 배열

    % 1. 0~255까지의 비트 수 룩업 테이블 
    % [0, 1, 2, ..., 255] 순서에 해당하는 1의 개수
    bitCountsLUT = [ ...
        0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, ...
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, ...
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, ...
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, ...
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, ...
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, ...
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, ...
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, ...
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, ...
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, ...
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, ...
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, ...
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, ...
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, ...
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, ...
        4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8  ...
    ]'; % 열 벡터로 변환 (Transposed)

    % 2. 입력 데이터 정보 저장
    originalSize = size(data);
    originalClass = class(data);

    % 3. 데이터 타입 검증
    switch originalClass
        case 'uint8',  bytesPerElem = 1;
        case 'uint16', bytesPerElem = 2;
        case 'uint32', bytesPerElem = 4;
        case 'uint64', bytesPerElem = 8;
        otherwise
            if isempty(data) % 빈 배열 처리
                counts = zeros(originalSize);
                return;
            end
            error('지원하지 않는 데이터 타입입니다. (uint 계열만 가능)');
    end

    % 4. 데이터를 uint8 배열로 변환 (Typecast)
    % 빈 배열일 경우 바로 리턴
    if isempty(data)
        counts = zeros(originalSize);
        return;
    end
    dataAsBytes = typecast(data(:), 'uint8');

    % 5. 룩업 테이블 매핑
    % MATLAB 인덱싱(1-based) 보정: 값 0 -> 인덱스 1
    byteCounts = bitCountsLUT(int32(dataAsBytes) + 1);

    % 6. 원래 데이터 단위로 합산 및 차원 복원
    if bytesPerElem == 1
        counts = reshape(byteCounts, originalSize);
    else
        % 바이트 단위로 쪼개진 값을 요소별로 합산
        counts = sum(reshape(byteCounts, bytesPerElem, []), 1);
        counts = reshape(counts, originalSize);
    end
end