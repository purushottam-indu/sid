import React from "react";
import styles from "./GeneralHelp.module.css";
import { Separator } from "@fluentui/react";
import { BiItalic } from "react-icons/bi";
const GeneralHelp = () => {
    const manualLink = "https://sankyopharma.sharepoint.com/:b:/s/DSTeam_CoE_AIML/EVGrL14Oos1HmZBzF8kSbzwByLTmSe7KeCMGAzBdbYUJaQ?e=S2Gkn3";
    const chatdsi_user_manual = "https://sankyopharma.sharepoint.com/:b:/s/DSTeam_CoE_AIML/EXXqQH0G_VlGmAj5TwwbeEQBn3KHvmo0iw8wQG_EsBXePg?e=GjPPIg";
    const chatdsi_usage_guidelines = "https://sankyopharma.sharepoint.com/:b:/s/DSTeam_CoE_AIML/ETF4r68T6mtFvor7wgAhrLQBHh-g4dzaSzVvZNef3J4Uug?e=BPv32A";
    const app_support = " mailto:appsupport_genai@dsi.com";
    const chatdsi_landing_page = "https://my.dsi.com/web/parsippany-information-systems/chatdsi";
    const manualLink2 = "";
    return (
        <div>
            <div>
                <p className={styles.listItem}>
                    Whether you have general questions or need help generating applicable content via ChatDSI we are here to assist you! On this page, we’ve
                    provided a few tips for entering prompts to help get you started. To view the complete user manual and learn more about all of ChatDSI’s
                    features, as well as access helpful FAQs and Use-Cases, please visit the{" "}
                    <a href={chatdsi_landing_page} target="_blank">
                        ChatDSI Landing Page
                    </a>{" "}
                    on my.dsi.com. In addition, we highly recommend that you familiarize yourself with the -{" "}
                    <a href={chatdsi_usage_guidelines} target="_blank">
                        ChatDSI Usage Guidelines.
                    </a>{" "}
                    To contact someone from our team for additional help, please send a message to -{" "}
                    <a href={app_support} target="_blank">
                        mailto:appsupport_genai@dsi.com.
                    </a>
                    {/* <strong>mailto:appsupport_genai@dsi.com</strong>. */}
                </p>
                <h3>Prompt Tips</h3>
                <p className={styles.listItem}>To make the most out of your interactions, we recommend following these prompt techniques and examples:</p>
                <ol className={styles.listStyle}>
                    <li className={styles.listItem}>
                        <strong>Start with Question Keywords :</strong> Begin your prompt with question words like "What," "How," "Why," "When," or "Where" to
                        induce a more informative answer. Example - Enter{" "}
                        <span className={styles.exampleGood}>"What are the common side effects of drug X?"</span> instead of just{" "}
                        <span className={styles.exampleBad}> "Side effects of Drug X"</span>
                    </li>
                    <li className={styles.listItem}>
                        <strong>Use Complete Sentences :</strong> Frame your questions using complete sentences. This helps the model better understand the
                        context and provide a more coherent response.
                    </li>
                    <li className={styles.listItem}>
                        <strong>Ask for Pros and Cons :</strong> If relevant, ask for the pros and cons of a situation to get a more balanced response. Example:
                        Ask -{" "}
                        <span className={styles.exampleGood}>
                            "What are the benefits and drawbacks of using open-source software in an enterprise setting?"
                        </span>{" "}
                        instead of <span className={styles.exampleBad}>"Is open-source software better than proprietary software?"</span>
                    </li>
                    <li className={styles.listItem}>
                        <strong>Ask for an Explanation :</strong> If you want a detailed explanation, consider using phrases like "Can you explain…" or "Tell me
                        more about." Example -
                        <span className={styles.exampleGood}> "Can you explain the concept of DevOps and its significance in software development?"</span>{" "}
                        instead of <span className={styles.exampleBad}>"What is DevOps?"</span>
                    </li>
                    <li className={styles.listItem}>
                        <strong>Experiment and Reframe : </strong>
                        If you're not getting the desired answer, try reframing your question or experimenting with different phrasings.
                    </li>
                </ol>
                {/* <h2>Configuring ChatDSI for a Specific Purpose</h2> */}
                <p className={styles.listItem}>
                    {" "}
                    To further refine how ChatDSI responds, use the <i>Customize feature found under <strong>left pane</strong>.</i>
                    The benefit of this feature is that it enables you to configure or customize the tool so that it responds in a certain way. In other words,
                    you can tailor the chat experience so that the tool acts in a way that serves a more precise but temporary need, e.g., turning it into a
                    personal translator for a specific language or a coding assistant. See the user manual for instructions on this feature.
                </p>
                <p className={styles.listItem}>
                    {" "}
                    Remember, content generated by ChatDSI may be incorrect and should not be relied upon for critical or sensitive matters without thorough
                    vetting as described in the{" "}
                    <a href={chatdsi_usage_guidelines} target="_blank">
                        Usage Guidelines.
                    </a>{" "}
                    For any feedback or questions, don't hesitate to reach out to our support team at the email address above.
                </p>
                <p className={styles.listItem}> Happy exploring and learning! </p>

                {/*  */}
                <Separator />
                {/* <p className={styles.listItem}>
                    For the full user manual visit -{" "}
                    <a href={manualLink} target="_blank">
                        User manual
                    </a>
                </p> */}
            </div>
        </div>
    );
};

export default GeneralHelp;
