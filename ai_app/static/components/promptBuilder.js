/**
 * 클라이언트 사이드 프롬프트 생성을 위한 모듈.
 * 사용자가 옵션을 변경할 때마다 서버에 전송될 프롬프트를 미리 보여주는 역할을 합니다.
 * 이 로직은 반드시 서버의 services/prompt_builder.py와 동일한 규칙을 가져야 합니다.
 */

const ROLE_MAP = {
    elementary: '초등학생을 위한 친근하고 이해하기 쉬운 언어를 사용하는 안전교육 전문가',
    middle: '중학생의 눈높이에 맞춰 현실적인 예시를 들어 설명하는 안전교육 교사',
    high: '고등학생에게 논리적이고 전문적인 정보를 제공하는 안전교육 강사'
};

const FORMAT_MAP = {
    notice: {
        format: '학부모님께 전달하는 공식적이고 신뢰감 있는 톤의 가정통신문',
        structure: ['정중한 인사말', '안전교육의 중요성 및 주제 소개', '핵심 내용(데이터 기반)', '가정에서의 연계 지도 방법', '학교의 노력 및 당부 말씀', '맺음말']
    },
    pdf: {
        format: '학생들이 직접 보고 학습할 수 있는 교육용 PDF 자료',
        structure: ['흥미를 끄는 제목', '학습 목표', '핵심 내용(데이터 기반, 소제목과 목록 활용)', '생각해보기 또는 간단한 활동지', '핵심 내용 요약 및 정리']
    }
};

/**
 * 서버의 prompt_builder.py와 동일한 로직으로 프롬프트를 생성합니다.
 * @param {string} schoolLevel - 'elementary', 'middle', 'high'
 * @param {string} outputType - 'notice', 'pdf'
 * @param {string} theme - 'fire_safety', 'general_safety'
 * @param {object} safetyData - 해당 테마의 JSON 데이터 객체
 * @returns {string} - 생성된 프롬프트 텍스트
 */
export function buildPromptPreview(schoolLevel, outputType, theme, safetyData) {
    const role = ROLE_MAP[schoolLevel] || '안전교육 전문가';
    const fmt = FORMAT_MAP[outputType] || FORMAT_MAP['pdf'];
    const themeKo = theme;
    
    // safetyData를 문자열로 변환하여 프롬프트에 포함
    const dataString = JSON.stringify(safetyData, null, 2);

    let prompt = `당신은 '${role}'입니다. 지금부터 다음 지시사항에 따라 '${fmt.format}' 형식의 글을 작성해 주세요. 최종 결과물은 반드시 한국어로 작성되어야 합니다.\n\n`;
    prompt += `## 주요 정보\n`;
    prompt += `- 교육 테마: ${themeKo}\n`;
    prompt += `- 교육 대상: ${schoolLevel}\n`;
    prompt += `- 활용할 데이터: ${dataString}\n\n`;
    prompt += `## 작성 구조\n`;
    prompt += `글의 전체 구조는 다음 순서를 반드시 따라야 합니다: ${fmt.structure.join(', ')}\n\n`;
    prompt += `## 추가 요구사항\n`;
    prompt += `- 학생(또는 학부모)의 눈높이에 맞춰 이해하기 쉽게 작성해 주세요.\n`;
    prompt += `- '활용할 데이터'에 있는 key_points와 scenarios를 반드시 본문에 자연스럽게 포함시켜 주세요.\n`;
    prompt += `- 딱딱한 정보 나열이 아닌, 실제적인 도움이 되는 내용으로 구성해 주세요.\n`;

    if (outputType === 'notice') {
        prompt += `- 가정통신문이므로 학부모님의 참여와 협조를 유도하는 문구를 포함해 주세요.\n- 결과물은 다른 설명 없이 바로 가정통신문 내용만 나올 수 있도록, HTML 마크업 형식으로 작성해주세요. (예: <h1>제목</h1><p>내용</p>)\n`;
} else { // pdf
        prompt += `- 글의 내용과 가장 잘 어울리는 지점에 이미지를 삽입해야 합니다.\n`;
        prompt += `- 이미지를 삽입할 때는 반드시 '[IMAGE: \"상세한 이미지 설명\"]' 형식을 사용해야 합니다.\n`;
        prompt += "- \"상세한 이미지 설명\"은 생성될 이미지의 장면 묘사(예 사람이 완강기를 사용하여 3층 건물 벽을 내려오는 모습),'단순하고 명확한 일러스트 스타일'이라는 단어로 끝나야 합니다.\n"
        prompt += `- 결과물은 다른 설명 없이 바로 PDF 내용만 나올 수 있도록, 마크다운 형식으로 작성해주세요.\n`;
    }
    
    prompt += `\n이제 작성을 시작해 주세요.`;

    return prompt;
}
