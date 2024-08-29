import { AskRequest, AskResponse, ChatRequest, Access, FileUpload } from "./models";

export async function askApi(options: AskRequest): Promise<AskResponse> {
    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: options.question,
            approach: options.approach,
            overrides: {
                retrieval_mode: options.overrides?.retrievalMode,
                semantic_ranker: options.overrides?.semanticRanker,
                semantic_captions: options.overrides?.semanticCaptions,
                top: options.overrides?.top,
                temperature: options.overrides?.temperature,
                prompt_template: options.overrides?.promptTemplate,
                prompt_template_prefix: options.overrides?.promptTemplatePrefix,
                prompt_template_suffix: options.overrides?.promptTemplateSuffix,
                exclude_category: options.overrides?.excludeCategory
            }
        })
    });

    const parsedResponse: AskResponse = await response.json();
    if (response.status > 299 || !response.ok) {
        throw Error(parsedResponse.error || "Unknown error");
    }

    return parsedResponse;
}

export async function accessApi(): Promise<Access> {
    const response = await fetch("/api/auth", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const parsedResponse: Access = await response.json();
    if (response.status > 299 || !response.ok) {
        throw Error(parsedResponse.error || "Unknown error");
    }
    return parsedResponse;
}

// export async function logoutApi(data: string): Promise<Response> {
export async function logoutApi(): Promise<Response> {
    const url = "/api/logout";
    // const data = { message: "This is a log message from Flask!" };

    const outputResponse = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // body: JSON.stringify(data),
        credentials: "include" //include cookies in the request
    });
    // .then(response => response.json())
    // .then(result => {
    //     console.log("Server response:", result);
    // })

    return outputResponse;
}

export async function chatApi(options: ChatRequest): Promise<Response> {
    const url = options.shouldStream ? "/chat_stream" : "/chat";
    return await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            history: options.history,
            approach: options.approach,
            overrides: {
                retrieval_mode: options.overrides?.retrievalMode,
                semantic_ranker: options.overrides?.semanticRanker,
                semantic_captions: options.overrides?.semanticCaptions,
                top: options.overrides?.top,
                temperature: options.overrides?.temperature,
                prompt_template: options.overrides?.promptTemplate,
                prompt_template_prefix: options.overrides?.promptTemplatePrefix,
                prompt_template_suffix: options.overrides?.promptTemplateSuffix,
                exclude_category: options.overrides?.excludeCategory,
                suggest_followup_questions: options.overrides?.suggestFollowupQuestions,
                model_type: options.overrides?.modelType
            }
        })
    });
}

export function getCitationFilePath(citation: string): string {
    return `/content/${citation}`;
}

export async function uploadApi(options: FileUpload): Promise<AskResponse> {
    const formData = new FormData();

    // Append each file to the formData
    options.files.forEach((file, index) => {
        formData.append(`file${index + 1}`, file);
    });

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const parsedResponse: AskResponse = await response.json();
    if (response.status > 599) {
        throw Error("try_after_some_time");
    } else if (response.status > 499) {
        throw Error("file_size_error");
    } else if (response.status > 399) {
        throw Error("csv_excel_error");
    } else if (response.status > 299 || !response.ok) {
        throw Error(parsedResponse.error || "Unknown error");
    } else if (response.status > 250) {
        throw Error("unstructured_data_already_uploaded");
    } else if (response.status > 200) {
        throw Error("csv_excel_already_present_error");
    }
    return parsedResponse;
}
