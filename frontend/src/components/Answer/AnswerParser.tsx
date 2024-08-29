import { renderToStaticMarkup } from "react-dom/server";
import { getCitationFilePath } from "../../api";

type HtmlParsedAnswer = {
    answerHtml: string;
    followupQuestions: string[];
    codeContent: string;
};

export function parseAnswerToHtml(answer: string): HtmlParsedAnswer {
    const citations: string[] = [];
    const followupQuestions: string[] = [];

    // Extract any follow-up questions that might be in the answer
    let parsedAnswer = answer.replace(/<<([^>>]+)>>/g, (match, content) => {
        followupQuestions.push(content);
        return "";
    });

    // trim any whitespace from the end of the answer after removing follow-up questions
    parsedAnswer = parsedAnswer.trim();

    const regex = /```([^`]+)```/g;
    const matches = [];
    let match;

    while ((match = regex.exec(parsedAnswer)) !== null) {
        const codeSnippet = match[1].trim();
        matches.push(codeSnippet);
    }

    // parsedAnswer = parsedAnswer.replace(
    //     regex,
    //     "<div style='background-color: black; padding: 20px;border-radius: 10px;'><code style='color: white; font-size: 16px;'>$1</code></div>"
    // );

    return {
        answerHtml: parsedAnswer,
        followupQuestions,
        codeContent: matches.join("")
    };
}
