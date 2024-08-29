import { Outlet, NavLink, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import github from "../../assets/github.svg";
import logo from "../../assets/Daiichi_Sankyo.png";
import styles from "./NavSection.module.css";
import { BiUserCircle } from "react-icons/bi";
import Navbar from "../Navbar/navbar";
import { useTheme } from '../../ThemeContext';
 
interface Props {
    pageTitle: string;
    pageSubTitle: string;
    setIsSidebarOpen: (isSidebarOpen: boolean) => void;
    isSidebarOpen: boolean;
    promptTemplate: string;
    setPromptTemplate: (promptTemplate: string) => void;
}
 
const NavSection = ({ pageTitle, pageSubTitle, isSidebarOpen, setIsSidebarOpen, promptTemplate, setPromptTemplate }: Props) => {
    const [userName, setUserName] = useState<string>("user.name");
    const { isDarkTheme } = useTheme();
    const [isConfigPanelOpen, setIsConfigPanelOpen] = useState(false);
 
    function getCookie(name: string) {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                return cookie.substring(name.length + 1);
            }
        }
        return "user.name";
    }
 
    useEffect(() => {
        const name = getCookie("username");
        const decodedName = decodeURIComponent(name.replace(/^"(.*)"$/, "$1").replace(/\\054/g, ","));
        console.log(decodedName);
 
        setUserName(decodedName);
    }, []);
 
    return (
        <div className={styles.layout}>
            <header className={`${styles.header} ${isDarkTheme ? styles.dark : styles.bright}`} role={"banner"}>
                <Navbar
                    isSidebarOpen={isSidebarOpen}
                    setIsSidebarOpen={setIsSidebarOpen}
                    onParameters={() => setIsConfigPanelOpen(!isConfigPanelOpen)}
                    toggleNavbar={function (): void {
                        throw new Error("Function not implemented.");
                    }}
                    promptTemplate={promptTemplate}
                    setPromptTemplate={setPromptTemplate}
                />
                <div className={styles.headerContainer}>
                <Link to="/" className={styles.logoContainer}>
                        <img src={logo} alt="Daiichi Sankyo logo"
                            style={{
                                filter: isDarkTheme ? 'brightness(2)' : 'brightness(1)'
                            }}
                        />
                    </Link>
                    <div className={styles.titleContainer}>
                        <h3 className={styles.headerTitle} style={{ color: isDarkTheme ? 'white' : 'black' }}>{pageTitle}</h3>
                        <h5 className={styles.headerSubtitle} style={{ color: isDarkTheme ? 'rgb(232, 228, 228)' : 'rgb(188, 182, 182)' }}>{pageSubTitle}</h5>
                    </div>
                    <div className={styles.userContainer}>
                        <h4 className={styles.headerRightText}
                        style={{ color: isDarkTheme ? 'white' : 'black' }}
                        >
                            {/* {userName} */}
                            {""}
                        </h4>
                        {""}
                        {/* <BiUserCircle fontSize="25px"
                        style={{ color: isDarkTheme ? 'white' : 'black' }} /> */}
                    </div>
                </div>
            </header>
        </div>
    );
};
 
export default NavSection;
