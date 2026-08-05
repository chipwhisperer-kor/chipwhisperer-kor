function data = binRead(fname, offset, len, opts)
% BINREAD 바이너리 파일을 지정된 오프셋, 타입, 엔디안으로 읽어옵니다.
%
%   DATA = BINREAD(FNAME)
%       파일 전체를 uint8 타입으로 읽어옵니다.
%
%   DATA = BINREAD(FNAME, LEN)
%       파일의 처음부터 LEN개의 요소를 읽어옵니다.
%
%   DATA = BINREAD(..., NAME, VALUE)
%       이름-값 쌍을 통해 정밀도(Type), 오프셋(Offset), 엔디안(Endian) 등을 지정합니다.
%
%   [입력 인수]
%       fname   : 읽을 파일의 경로 (문자열)
%       Offset  : 읽기 시작할 위치 (바이트 단위, 기본값: 0)
%       len     : 읽을 요소의 개수 (기본값: Inf - 끝까지 읽음)
%                 *주의: 바이트 수가 아니라 '데이터 타입의 개수'입니다.
%
%   [옵션 인수 (Name-Value)]
%       Type    : 데이터 타입 (기본값: "uint8")
%                 ("uint8" | "int16" | "double" 등 MATLAB 기본 타입 지원)
%       Origin  : 오프셋의 기준점 (기본값: "bof")
%                 ("bof": 파일 시작, "cof": 현재 위치, "eof": 파일 끝)
%       Endian  : 바이트 순서 (기본값: "little")
%                 ("little" | "big" | "native")
%
%   [사용 예시]
%       raw = binRead("data.bin");
%       vec = binRead("data.bin", 100, Type="uint16");
%       part = binRead("data.bin", Inf, Offset=128, Origin="bof", Endian="big");
%
%   See also FOPEN, FREAD, FSEEK.

    arguments
        fname (1,1) string {mustBeFile} % 파일이 실제로 존재하는지 미리 확인
        offset (1,1) double {mustBeInteger, mustBeNonnegative} = 0
        len   (1,1) double {mustBeNonnegative} = Inf

        
        % mustBeMember를 사용하여 허용된 값 이외의 입력이 들어오면 즉시 에러 발생
        opts.Type   (1,1) string {mustBeMember(opts.Type, ...
            ["uint8","int8","uint16","int16","uint32","int32", ...
             "uint64","int64","single","double","char","logical"])} = "uint8"             
        opts.Origin (1,1) string {mustBeMember(opts.Origin, ["bof", "cof", "eof"])} = "bof"
        opts.Endian (1,1) string {mustBeMember(opts.Endian, ["little", "big", "native"])} = "little"
    end

    %% 1. 설정 매핑 (사용자 입력 -> fopen/fseek 옵션)
    % 엔디안 설정: fopen에서 사용하는 기호로 변환 ('ieee-le', 'ieee-be' 등)
    machineFormat = getMachineFormat(opts.Endian);
    
    %% 2. 파일 열기
    % 'rb': 바이너리 읽기 모드 (Read Binary)
    fid = fopen(fname, "rb", machineFormat);
    
    % fopen이 -1을 반환하면 파일 열기 실패
    if fid < 0
        % ferror를 통해 구체적인 시스템 에러 메시지(예: 권한 없음 등)를 포함
        [msg, errNum] = ferror(fid); 
        error("binRead:FileOpenError", "파일을 열 수 없습니다: %s\n(시스템 메시지: %s, ID: %d)", fname, msg, errNum);
    end
    
    % onCleanup: 이 함수(binRead)가 종료되거나 에러로error("binRead:SeekError", "fseek 실패. 파일 범위를 벗어났을 수 있습니다.\n(Offset: %d, Origin: %s)", offset, opts.Origin); 중단될 때 
    % 자동으로 fclose(fid)를 실행하여 파일 핸들 누수를 방지함.
    cleanupObj = onCleanup(@() fclose(fid)); 

    %% 3. 오프셋 이동
    if offset > 0 || opts.Origin ~= "bof"
        status = fseek(fid, offset, opts.Origin);
        if status ~= 0
            error("binRead:SeekError", "fseek 실패. 파일 범위를 벗어났을 수 있습니다.\n(Offset: %d, Origin: %s)", offset, opts.Origin);
        end
    end

    %% 4. 데이터 읽기 (최적화)
    % 'source=>output' 형식을 생성합니다. (예: 'uint16=>uint16')
    % 이 방식은 읽어온 데이터를 double로 자동 변환하지 않고 원본 타입을 유지하므로
    % 메모리 사용량을 줄이고 속도를 높입니다.
    precisionStr = opts.Type + "=>" + opts.Type;
    
    % 데이터 읽기 실행
    data = fread(fid, len, precisionStr);
    
end

%% ----------------- 로컬 헬퍼 함수 -----------------

function format = getMachineFormat(endianStr)
% GETMACHINEFORMAT 엔디안 문자열을 fopen용 포맷으로 변환
    switch endianStr
        case "little"
            format = "ieee-le";
        case "big"
            format = "ieee-be";
        case "native"
            format = "native";
        otherwise
            % arguments 블록에서 이미 검증했지만 안전장치로 둠
            format = "native"; 
    end
end