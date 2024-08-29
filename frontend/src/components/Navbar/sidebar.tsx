import { TbHexagonLetterP } from "react-icons/tb";
import { MdSettingsSuggest } from "react-icons/md";
import { IoMdHelpCircleOutline } from "react-icons/io";
import { MdOutlineFeedback, MdLogout } from "react-icons/md";
import { BiUserCircle } from "react-icons/bi";
// import { Switch } from '@fluentui/react';

interface SidebarItem {
    title: string;
    path?: string;
    icon?: JSX.Element;
    cName: string;
    isSwitch?: boolean;
}

export const SidebarData = (isDarkTheme: boolean): SidebarItem[] => [
    {
        title: "username",
        icon: <BiUserCircle color="#333333" />,
        cName: "nav-text"
    },
    {
        title: isDarkTheme ? "Light Mode" : "Dark Mode",
        path: "",
        cName: "nav-text",
        isSwitch: true
    },
    {
        title: "Customize",
        icon: <MdSettingsSuggest color="#333333" />,
        cName: "nav-text"
    },
    {
        title: "Help",
        icon: <IoMdHelpCircleOutline color="#333333" />,
        cName: "nav-text"
    },
    {
        title: "Feedback",
        icon: <MdOutlineFeedback color="#333333" />,
        cName: "nav-text"
    },
    {
        title: "Logout",
        icon: <MdLogout color="#333333" />,
        cName: "nav-text"
    }
];
