import { Outlet, NavLink, Link } from "react-router-dom";
import github from "../../assets/github.svg";
import styles from "./Layout.module.css";
import NavSection from "../../components/NavSection/NavSection";
import { RecoilRoot } from "recoil";

interface LayoutProps {
    isSidebarOpen: boolean;
    setIsSidebarOpen: (isSidebarOpen: boolean) => void;
    promptTemplate: string;
    setPromptTemplate: (promptTemplate: string) => void;
}

const Layout = ({ setIsSidebarOpen, isSidebarOpen, setPromptTemplate, promptTemplate }: LayoutProps) => {
    return (
        <div className={styles.layout}>
            <RecoilRoot>
                <header className={styles.header} role={"banner"}>
                    <NavSection
                        isSidebarOpen={isSidebarOpen}
                        setIsSidebarOpen={setIsSidebarOpen}
                        pageTitle="ChatDSI"
                        pageSubTitle="Powered by GPT-4o"
                        promptTemplate={promptTemplate}
                        setPromptTemplate={setPromptTemplate}
                    />
                </header>

                <Outlet />
            </RecoilRoot>
        </div>
    );
};

export default Layout;
